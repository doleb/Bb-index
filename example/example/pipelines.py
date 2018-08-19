# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo

class MongoPipeline(object):

    #starts connection at 'localhost', creates mongo database and creates collection in created database 
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'],
        settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        print('ADDED %s TO DATABASE' % item['name'])
        self.collection.insert_one(dict(item))
        return item
