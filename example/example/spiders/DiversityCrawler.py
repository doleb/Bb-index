import scrapy
from selenium import webdriver 
import os
from example.items import City


#gathers census data for individual cities and determines the "diversity" of a given city based on the distribution of a population across ethnic groups
class DiversityCrawler(scrapy.Spider):
    name = 'diversitycrawler'
    allowed_urls = ['citydata.com']
    start_urls = []

    def __init__(self):
        for line in open(os.path.join(os.path.dirname(__file__), '..', 'city_names.txt')):
            dashed = line.replace(' ', '-')
            self.start_urls.append('http://www.city-data.com/races/races-%s.html' % dashed)

    def parse(self, response):
        print(response.url)