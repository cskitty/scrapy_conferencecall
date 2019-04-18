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
        client = pymongo.MongoClient('MelodyLinux', 27017)
        db = client['conference_call']
        #self.collection = db['test']
        self.collection = db['crawl']
        self.earnings_collection = db['earnings']

    def get_unique_page_set(self):
        rows = list(self.collection.find({}, {"_id": 0, "page": 1}))
        return set([v['page'] for v in rows])

    def get_unique_ticker_set_from_url_col(self):
        rows = list(self.collection.find({}, {"_id": 0, "ticker": 1}))
        return set([v['ticker'] for v in rows])

    def get_unique_ticker_set_from_earnings_col(self):
        rows = list(self.earnings_collection.find({}, {"_id": 0, "ticker": 1}))
        return set([v['ticker'] for v in rows])

    def get_revenue_ticker_set_from_earnings_col(self):
        rows = list(self.earnings_collection.find({"rev": {"$eq": "" }}, {"_id": 0, "ticker": 1}))
        return set([v['ticker'] for v in rows])

    def get_eps_ticker_set_from_earnings_col(self):
        rows = list(self.earnings_collection.find({"eps": {"$eq": "" }}, {"_id": 0, "ticker": 1}))
        return set([v['ticker'] for v in rows])

    def get_urls_from_page(self, page):
        url_list = []
        cursors = self.collection.find({"page": page})
        for cur in cursors:
            if "2018" in cur['title'] and cur['html'] == "":
                url_list.append((cur['_id'], cur["url"]))
        return url_list

    def update_with_text(self, id, text):
        return self.collection.update_one({'_id': ObjectId(id)}, {"$set":{"text": text}}, upsert=False)

    def update_earnings(self, row):
        return self.earnings_collection.update_one({'ticker': row['ticker']}, {"$set":row}, upsert=False)

    def get_earnings_collection(self):
        return self.earnings_collection

    def get_conference_call_collection(self):
        return self.collection

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