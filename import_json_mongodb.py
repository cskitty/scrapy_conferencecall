import json
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['conference_call']
collection_crawl = db['craw']

f = open('conf.json')
file_data = json.load(f)
f.close()

collection_crawl.insert(file_data)
client.close()