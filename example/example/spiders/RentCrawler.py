import scrapy
from example.items import City

#potential cities
#philadelphia
#seattle
#portland
#new orleans
#boston
#new york
#miami
#oakland
#washington DC
#chicago
#phoenix
#austin
#houston

class RentCrawler(scrapy.Spider):
    name='rentcrawler'
    allowed_domains = ['craigslist.org']
    pages_to_scrape = 5 #the maximum amount of pages of results the spider will crawl
    current_result_page = 1 #the current results page the spider is crawling
    room_prices = {}
    current_pages = {}
    base_url_rent = '.craigslist.org/search/roo?hasPic=1&min_price=100&max_price=5000&availabilityMode=0'
    cities_USA = ['atlanta', 'austin', 'boston', 'chicago', 'houston', 'miami', 'neworleans', 'newyork', 'sfbayarea',
              'philadelphia', 'phoenix', 'portland', 'seattle', 'washington']
 #   cities_USA = ['neworleans']
    
    #creates a Scrapy request for each city in list cities_USA
    #sfbayarea only checks east bay area, newyork only checks brooklyn area
    def start_requests(self):
        for city in self.cities_USA:
            if city is 'sfbayarea':
                url = 'https://' + city + '.craigslist.org/search/eby/roo?hasPic=1&min_price=2&max_price=5000&availabilityMode=0'
            elif city is 'newyork':
                url = 'https://' + city + '.craigslist.org/search/que/roo?hasPic=1&min_price=2&max_price=5000&availabilityMode=0'
            else:
                url = 'https://' + city + self.base_url_rent
            yield scrapy.Request(url=url, callback=self.parse)

    #crawls each page from 1 to get_page_amt() and gathers all prices of room listings in a list for each respective city
    def parse(self, response):
        city = response.xpath('//select[@id="areaAbb"]/option/text()').extract_first() #gets the city page this info parser is crawling
        last_page = self.get_page_amt(int(response.xpath('//span[@class="totalcount"]/text()').extract_first())/120.0) 
        if city not in self.room_prices:
            self.room_prices[city] = response.xpath('//span[@class="result-meta"]/span[@class="result-price"]/text()').extract()
            self.current_pages[city] = 1
        else:
            self.room_prices[city].extend(response.xpath('//span[@class="result-meta"]/span[@class="result-price"]/text()').extract())
        if self.current_pages[city] < last_page:
            rel_page_url = response.xpath('//a[@class="button next"]/@href').extract_first()
            next_page = response.urljoin(rel_page_url)
            self.current_pages[city] += 1
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            yield self.parse_indetail(response)

    #parses the price data gathered into Scrapy items
    def parse_indetail(self, response):
        item = City()
        city = response.xpath('//select[@id="areaAbb"]/option/text()').extract_first()
        sorted_list = self.sort_prices(city)
        item['name'] = city
        item['avg_cost'] = self.avg_cost(sorted_list)
        item['med_cost'] = sorted_list[int(len(sorted_list)/2)]
        item['size'] = len(self.room_prices[city])
        return item

    #adds up every listing price and divides it by the total amount of listings gathered
    def avg_cost(self, prices):
        sum = 0
        for price in prices:
            sum += price
        return round(sum/len(prices), 2)
    
    #converts gathered data from str to int and sorts it in ascending order
    def sort_prices(self, city):
        sorted_list = []
        for price in self.room_prices[city]:
            sorted_list.append(int(price.strip('$')))
        return sorted(sorted_list)

    #takes the total amount of pages of listings on a craigslist site to determine how many pages the program should crawl
    #if there are enough pages to crawl by the amount specified in pages_to_scrape, return that
    #if not, return the total amount of pages of craigslist ads
    def get_page_amt(self, actual_pages):
        if actual_pages < self.pages_to_scrape:
            return actual_pages
        return self.pages_to_scrape