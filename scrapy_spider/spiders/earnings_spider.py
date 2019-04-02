#!/usr/bin/env python3
import scrapy
from scrapy.crawler import CrawlerProcess   # Programmatically execute scrapy

from urllib.parse import urlparse
from slugify import slugify

# RANDOMIZE USER AGENTS ON EACH REQUEST:
debug_mode = False

class EarningsSpider(scrapy.Spider):

    name = "earnings_spider"
    custom_settings = {
            # 'LOG_LEVEL': 'CRITICAL', # 'DEBUG'
            'LOG_ENABLED': False,
            'DOWNLOAD_DELAY': 3 # 0.25 == 250 ms of delay, 1 == 1000ms of delay, etc.
    }

    def start_requests(self):
        # GET LAST INDEX PAGE NUMBER
        urls = [ 'https://seekingalpha.com/earnings/earnings-call-transcripts/9999' ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_last_page)

    def parse_last_page(self, response):
        data = response.css("#paging > ul.list-inline > li:last-child a::text")
        last_page = data.extract()
        last_page = int(last_page[0])
        print("Last page = %d" % (last_page))
        for x in range(last_page, 0, -1):
            # DEBUGGING: CHECK ONLY FIRST ELEMENT
            if debug_mode == True and x > 0:
                break
            url = "https://seekingalpha.com/earnings/earnings-call-transcripts/%d" % (x)
            yield scrapy.Request(url=url, callback=self.parse)

    # SAVE CONTENTS TO AN HTML FILE 
    def save_contents(self, response):
        data = response.css("div#content-rail article #a-body")
        data = data.extract()
        url = urlparse(response.url)
        url = url.path
        filename = "../data/"+slugify(url) + ".html"
        with open(filename, 'w') as f:
            f.write(data[0])
            f.close()

    def parse(self, response):
        print("Parsing results for: " + response.url)
        links = response.css("a[sasource='earnings-center-transcripts_article']")
        links.extract()
        for index, link in enumerate(links):
            url = link.xpath('@href').extract()
            # DEBUGGING MODE: Parse only first link
            #if debug_mode == True and index > 0:
            #    break
            url = link.xpath('@href').extract()
            data = urlparse(response.url)
            data = data.scheme + "://" + data.netloc + url[0]  # .scheme, .path, .params, .query
            print("======------======")
            print("Getting Page:")
            print("URL: " + data + "?part=single")
            print("======------======")
            request = scrapy.Request(data,callback=self.save_contents)
            yield request
