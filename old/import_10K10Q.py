import json
import os
import sys
import base64
import gridfs
from pymongo import MongoClient

LARGEST_FILE_SIZE = 8000000

def import_html_mongo(cik, collection):
    # Look for files scraped for that CIK
    try:
        os.chdir(cik)
    # ...if we didn't scrape any files for that CIK, exit
    except FileNotFoundError:
        print("Could not find directory for CIK", cik)
        return

    print("Parsing CIK %s..." % cik)

    row = {}
    row['cik'] = cik

    # Get list of scraped files
    # excluding hidden files and directories
    file_list = [fname for fname in os.listdir() if not (fname.startswith('.') | os.path.isdir(fname))]

    # Iterate over scraped files and clean
    for filename in file_list:
        row['name'] = filename
        row['gridfs'] = 0
        print(filename)
        with open(filename, 'r') as file:
            #base64 encoding requires 8 bit bytes as input
            row['file'] = base64.b64encode(bytes(file.read(), "utf-8"))
            print(filename, " size is ", sys.getsizeof(row['file']))
            if (sys.getsizeof(row['file']) >= LARGEST_FILE_SIZE):
                row['gridfs']  = fs.put(row['file'],filename=filename)
                row['file'] = ''
                print('file too large, put to grid FS with id ', row['gridfs'])
            collection.update_one(row, {"$set": row}, upsert=True)

    os.chdir('..')
    return


client = MongoClient('localhost', 27017)
db = client['sec_forms']
collection = db['10K']
fs = gridfs.GridFS(db)

pathname_10k = "/opt.hd/melody/research/10Q10K/10K"
os.chdir(pathname_10k)

file_list = [fname for fname in os.listdir() if not fname.startswith('.') and os.path.isdir(fname)]

# Iterate over CIKs and clean HTML filings
i = 0
for cik in file_list:
    i += 1
    import_html_mongo("0001088034", collection)
print("imported ",i," 10K CIKs")

#os.sys.exit(1)

collection = db['10Q']
pathname_10q = "/opt.hd/melody/research/10Q10K/10Q"
os.chdir(pathname_10q)

file_list = [fname for fname in os.listdir() if not fname.startswith('.') and os.path.isdir(fname)]

# Iterate over CIKs and clean HTML filings
i = 0
for cik in file_list:
    i += 1
    import_html_mongo("0001326003", collection)
print("imported ",i," 10Q CIKs")