import scrapy
import sys
sys.path.append('..') #TODO add example directory to sys.path without this command
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Diversity import DiversityCrawler
from Rent import RentCrawler
from Transport import TransportCrawler

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(RentCrawler)
    process.crawl(DiversityCrawler)
    process.crawl(TransportCrawler)
    process.start(stop_after_crawl=True)