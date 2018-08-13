# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

#Definition of city and the desired attributes
#cost is overall Cost of Living obtained from indices on numbeo.com or data.bls.gov if i can figure it out
#transport is the per capita ridership of public transport within a city
#diversity is how spread out a population is across different 
#artActivity is the size 
class City(Item):
    # define the fields for your item here like:
    name = Field()
    avg_cost = Field()
    med_cost = Field()
    size = Field()
