import scrapy
from selenium import webdriver
from example.file_utils import CITY_LIST
import time
from example.items import City

#Finds the size of public transportation of cities and participation costs for rider
class TransportCrawler(scrapy.Spider):
    name = 'transportcrawler'
    allowed_domains = ['factfinder.census.gov']
    start_urls = []

    #start web driver
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.start_urls.append('https://factfinder.census.gov/faces/nav/jsf/pages/index.xhtml')

    #for each city in city_names.txt, navigate factfinder.census.gov to the city's transportation data table 
    def parse(self, response):
        print('******************************************************%s*****************************************' % CITY_LIST)
        for line in CITY_LIST:
            self.driver.get(response.url)
            search_box = self.driver.find_element_by_id('cfsearchtextboxmain')
            go_button = self.driver.find_element_by_xpath('//*[@id="cfmainsearchform"]/a')
            search_box.clear()
            search_box.send_keys(line.strip() + ' city')
            go_button.click()
            time.sleep(7.5)
            business_tab = self.driver.find_element_by_xpath('//*[@id="leftnav"]/a[3]')
            business_tab.click()
            time.sleep(5.5)
            table_link = self.driver.find_element_by_xpath('//*[@id="cf-content"]/div[1]/div[2]/div/div[2]/ul/li[3]/div/a')
            table_link.click()
            time.sleep(10)
            yield self.extract_data(line.strip())

    #find and extract data for public transport ridership and car ridership
    def extract_data(self, city_name):
        city = City()
        city['name'] = city_name
        transit_ridership = float(self.driver.find_element_by_xpath('//*[@id="data"]/tbody/tr[10]/td[1]').text.rstrip('%'))
        car_ridership = float(self.driver.find_element_by_xpath('//*[@id="data"]/tbody/tr[3]/td[1]').text.rstrip('%'))
        transport_index = transit_ridership
        if transit_ridership > car_ridership:
            transport_index *= 1.75
        city['transport'] = round(transport_index, 2)
        return city