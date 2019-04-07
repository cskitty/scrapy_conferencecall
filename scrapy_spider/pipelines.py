# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from bson.objectid import ObjectId

class ScrapySpiderPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['conference_call']
        #self.collection = db['test']
        self.collection = db['crawl']

    def get_unique_page_set(self):
        rows = list(self.collection.find({}, {"_id": 0, "page": 1}))
        return set([v['page'] for v in rows])

    def get_urls_from_page(self, page):
        return self.collection.find({"page": page})

    def update_with_text(self, id, text):
        return self.collection.update_one({'_id': ObjectId(id)}, {"$set":{"text": text}}, upsert=False)

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