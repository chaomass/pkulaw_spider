# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
import logging
import copy
from pkulaw.items import PkulawItem
from pkulaw.items import PkulawBrefItem

class PkulawPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.connection_string = "mongodb://%s:%d" % (settings['MONGODB_SERVER'],settings['MONGODB_PORT'])

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[settings['MONGODB_DB']]
        self.pkulaw = self.db[settings['MONGODB_COLLECTION']]
        self.pkulawbref = self.db['brefinfo']
        self.log = logging.getLogger(spider.name)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, PkulawItem):
            try:
                self.pkulaw.insert(dict(item))
                print "pkulaw:",pkulaw
            except Exception:
                pass
        elif isinstance(item, PkulawBrefItem):
            try:
                self.pkulawbref.insert(dict(item))
                print "pkulawbref:",pkulawbref
            except Exception:
                pass
        return item
