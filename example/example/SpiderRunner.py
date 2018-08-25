import scrapy
import os
from scrapy.crawler import CrawlerProcess
from spiders.Diversity import DiversityCrawler
from spiders.Rent import RentCrawler
from spiders.Transport import TransportCrawler

process = CrawlerProcess()
process.crawl(TransportCrawler)
process.crawl(DiversityCrawler)
process.crawl(RentCrawler)
process.start()