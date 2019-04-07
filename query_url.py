import json
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client['conference_call']
collection_crawl = db['crawl']
collection_test = db['test']
#rows = list(collection_crawl.find({},{"_id":0,"page":1}))
#unique_rows = set([v['page'] for v in rows])
#print(unique_rows)
#print(len(unique_rows))

#collection_crawl.update({}, {"$set" : {"text": ""}}, upsert = False, multi=True)

rows = list(collection_test.find({"page":"1"}))
for row in rows:
    row['text'] = "downloaded new"
    stringId = str(row["_id"])
    result = collection_test.update_one({'_id': ObjectId(stringId)}, {"$set": {"text":"aaa"}}, upsert=False)
    print(result.modified_count)
    break
