# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from pymongo import ReturnDocument
from example.file_utils import CITY_LIST
import pymongo

class MongoPipeline(object):


    #starts connection at 'localhost', creates mongo database and creates collection in created database 
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'],
        settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        updated_item = self.collection.find_one_and_update({'name' : item['name']}, {'$set' : dict(item)}, upsert=True)
        print('********************************************ADDED %s TO DATABASE********************************************' % str(item['name']).upper())
        print(dict(item))
        print('*********************************************************************************************************************')
        return updated_item
