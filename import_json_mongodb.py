import json
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['conference_call']
collection_crawl = db['crawl']

f = open('conf.json')
file_data = json.load(f)
f.close()

for row in file_data:
    #print(row)
    collection_crawl.update_one(row, {"$set":row}, upsert=True)
client.close()