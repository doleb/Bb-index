import scrapy
import os
from scrapy.crawler import CrawlerProcess
from Diversity import DiversityCrawler
from Rent import RentCrawler
from Transport import TransportCrawler

process = CrawlerProcess()
process.crawl(TransportCrawler)
process.crawl(DiversityCrawler)
process.crawl(RentCrawler)
process.start()