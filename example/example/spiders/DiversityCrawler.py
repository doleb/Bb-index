import scrapy
from example.items import City


#gathers census data for individual cities and determines the "diversity" of a given city based on the distribution of a population across ethnic groups
class DiversityCrawler(scrapy.Spider):
    name = 'diversitycrawler'
