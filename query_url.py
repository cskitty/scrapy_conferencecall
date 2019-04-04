import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['conference_call']
collection_crawl = db['crawl']

rows = list(collection_crawl.find({},{"_id":0,"page":1}))

unique_rows = set([v['page'] for v in rows])
#print(unique_rows)
print(len(unique_rows))