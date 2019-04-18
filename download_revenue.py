import json
from pymongo import MongoClient
import requests
from scrapy_spider.pipelines import ScrapySpiderPipeline
from stem import Signal
from stem.control import Controller
import time
from tqdm import tqdm

str = "machine_cookie=1692001658446; __utmc=150447540; _pxvid=f2897aca-5a1c-11e9-ae48-0242ac12000f; __gads=ID=0abb74ffef5a4ae0:T=1554741599:S=ALNI_Ma8HkYJYLl41gT4rpIALQMrcZ2WhQ; h_px=1; OX_plg=pm; __utma=150447540.257821618.1554741599.1554745034.1554754015.3; __utmz=150447540.1554754015.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=150447540.1.10.1554754015; _px=GYgc+UIBXvwVd2YgcAi1512G4UdTLy0PJh1oZ7G/TfImelOtrOkXlHySLNxrEnY6Yq+/soEXZRHtYHjCSchlBg==:1000:EKzDtzgUXSjETrzIqF23VM8mq+JHzDgYBxMdvSQRwS2pnH85H2RJQ/8f1skp1jF63LBm+LHjaDojLsjUigAKXX+ExrYIU25R4/+EtUoDAMfL5Uk9MBRP9HST1nOov5cjx/El74baOv+LoT25Z/niACLuz1EOecWPkdtulqAhAYemUYe0bLegFHJDUu585ABsGOlDA7Qy8ED/cXjvzm933ENP7SO13eew/s5ETtuk/zWPXjsK3PAIVKJgNbd7QBOxuN68nXpCOBGacOw8fLn38w==; _px2=eyJ1IjoiZGI3MzY3YzAtNWEzOS0xMWU5LTg4NzQtNjUxNWFkM2M2ZGY3IiwidiI6ImYyODk3YWNhLTVhMWMtMTFlOS1hZTQ4LTAyNDJhYzEyMDAwZiIsInQiOjE1NTQ3NTQ1MTYyNjIsImgiOiIxNzU4NmQ5NGJlOTlmNmM4ZDQyZDgwMzQwYjE5N2UwYWNlNzYxNTMyYWVmYmMyMjBlOTZhMGZlZWQ3YjIyZDcyIn0=; _pxde=9d9ed5371ef993927d29656b892db44ce42812c7f208b2bf0a43c18675cf0178:eyJ0aW1lc3RhbXAiOjE1NTQ3NTQwMjIxNzN"
cookie = dict(e[:-1].split('=',1) for e in str.split(' '))
pipeline = ScrapySpiderPipeline()


def retrieve_ip():
	# get info (IP...) from current connection
	session = requests.session()
	# Tor uses the 9050 port as the default socks port. You use it if you want to proxy something through Tor
	session.proxies = {'http':  'socks5://127.0.0.1:9050',
					'https': 'socks5://127.0.0.1:9050'}

	return session

def set_new_ip():
	with Controller.from_port(port=9051) as controller:
		controller.authenticate(password="1234")
		controller.signal(Signal.NEWNYM)


def download_revenue(ticker):
    url = 'https://seekingalpha.com/symbol/' + ticker + '/earnings/estimates_data?data_type=revenue'

    set_new_ip()
    session = retrieve_ip()

    session.headers.update({'referer': 'https://seekingalpha.com/symbol/' + ticker + '/earnings'})
    session.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})
    session.headers.update({'x-requested-with': 'XMLHttpRequest'})
    #session.cookies.update(cookie)


    downloadError = False
    try:
        rev = session.get(url).text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        downloadError = True

    print(" IP visible through Tor (stem)", session.get('http://httpbin.org/ip').text)
    #print(" get ", rev[:15])
    #eps = session.get(url).text

    retryCount = 0
    while (downloadError or (rev.startswith("<!DOCTYPE"))) and retryCount < 10:
        set_new_ip()
        session = retrieve_ip()
        print(" IP visible through Tor (stem)", session.get('http://httpbin.org/ip').text)

        retryCount += 1
        time.sleep(2)

        session.headers.update({'referer': 'https://seekingalpha.com/symbol/' + ticker + '/earnings'})
        session.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})
        session.headers.update({'x-requested-with': 'XMLHttpRequest'})
        #session.cookies.update(cookie)

        downloadError = False
        try:
            rev = session.get(url).text
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
            downloadError = True

    if(not rev.startswith("<!DOCTYPE")):
        doc = pipeline.get_earnings_collection().find_one({'ticker': ticker})
        if not doc:
            doc = {}
            doc['ticker'] = ticker
            doc['eps'] = ""

        doc['rev'] = rev
        print("downloaded for ticker ", ticker, " ... ", rev[:48])
        pipeline.get_earnings_collection().update_one({'ticker': ticker}, {"$set": doc}, upsert=True)



downloaded_tickers = pipeline.get_revenue_ticker_set_from_earnings_col()

for ticker in tqdm(downloaded_tickers):
    download_revenue(ticker)

"""
f = open('conf.json')
file_data = json.load(f)
f.close()

for row in file_data:
    #print(row)
    collection_crawl.update_one(row, {"$set":row}, upsert=True)
client.close()
"""

