import scrapy
from selenium import webdriver
from example.file_utils import CITY_LIST
import time
from example.items import City


class RentCrawler(scrapy.Spider):
    name='rentcrawler'
    allowed_domains = ['google.com', 'craigslist.org']
    pages_to_scrape = 5 #the maximum amount of pages of results the spider will crawl
    current_result_page = 1 #the current results page the spider is crawling
    room_prices = {}
    current_pages = {}
    craigslist_page_names = {}
    craigslist_url_extension = '?hasPic=1&min_price=100&max_price=5000&availabilityMode=0'
    start_urls = []

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        for line in CITY_LIST:
            self.start_urls.append('https://cse.google.com/cse?q=craigslist+rooms+%s&cx=007479151798586256926:vc_was3sgg4' % line.rstrip())

    def parse(self, response):
        self.driver.get(response.url)
        link = self.driver.find_element_by_xpath('//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div/a')
        url = link.get_attribute('href')
        time.sleep(1)
        self.craigslist_page_names[self.get_craigslist_page_city(url)] = str(response.url).split('=')[1].split('&')[0].split('+',2)[2].replace('%20', ' ')
        craigslist_url = url + self.craigslist_url_extension
        yield scrapy.Request(url=craigslist_url, callback=self.parse_craigslist)

    #crawls each page from 1 to get_page_amt() and gathers all prices of room listings in a list for each respective city
    def parse_craigslist(self, response):
        self.logger.info('You are now crawling: %s', response.url)
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
            yield scrapy.Request(url=next_page, callback=self.parse_craigslist)
        else:
            yield self.parse_indetail(response)

    #parses the price data gathered into Scrapy items
    def parse_indetail(self, response):
        item = City()
        city = self.get_craigslist_page_city(response.url)
        sorted_list = self.sort_prices(response.xpath('//select[@id="areaAbb"]/option/text()').extract_first())
        item['name'] = self.craigslist_page_names[city]
        item['avg_cost'] = self.avg_cost(sorted_list)
        item['med_cost'] = sorted_list[int(len(sorted_list)/2)]
        item['listing_count'] = len(self.room_prices[response.xpath('//select[@id="areaAbb"]/option/text()').extract_first()])
        return item

    def get_craigslist_page_city(self, url):
        return str(url).split('.')[0].split('/')[2]

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