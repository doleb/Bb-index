# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

#Definition of city and the desired attributes
#avg_cost and med_cost are the average and median (respectively) monthly rate for rooms on craigslist for a given city
#transport_size is the per capita ridership of public transport within a city
#transport_cost is the monthly cost of riding public transport in a city
#diversity is how spread out a population is across different ethnic groups
class City(Item):
    # define the fields for your item here like:
    name = Field()
    avg_cost = Field()
    med_cost = Field()
    size = Field()
    diversity = Field()
