# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class ScrapySpiderPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['conference_call']
        self.collection = db['crawl']

    def get_unique_page_set(self):
        rows = list(self.collection.find({}, {"_id": 0, "page": 1}))
        return set([v['page'] for v in rows])

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            #self.collection.insert(dict(item))
            print("insert to database ", dict(item))
            self.collection.update_one(dict(item), {"$set": dict(item)}, upsert=True)
        return item