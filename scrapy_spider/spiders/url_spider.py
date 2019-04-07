#!/usr/bin/env python3
import scrapy
from scrapy.crawler import CrawlerProcess   # Programmatically execute scrapy
from scrapy_spider.items import ScrapySpiderItem
from scrapy_spider.pipelines import ScrapySpiderPipeline

from urllib.parse import urlparse
from slugify import slugify
from pymongo import MongoClient

# RANDOMIZE USER AGENTS ON EACH REQUEST:
debug_mode = False

class UrlSpider(scrapy.Spider):

    name = "url_spider"
    download_delay = 10.0
    custom_settings = {
            #'LOG_LEVEL': 'CRITICAL', # 'DEBUG'
            'LOG_ENABLED': True,
            'DOWNLOAD_DELAY': 10 # 0.25 == 250 ms of delay, 1 == 1000ms of delay, etc.
    }

    def start_requests(self):
        #get all the downloaded page set from mongodb
        unique_rows = ScrapySpiderPipeline().get_unique_page_set()

        url = "https://seekingalpha.com/earnings/earnings-call-transcripts/"
        for page in range(5413):
            # DEBUGGING: CHECK ONLY FIRST ELEMENT
            if debug_mode == True and page > 10:
                break
            if str(page) in unique_rows:
                print("already downloaded page ", page)
                continue
            yield scrapy.Request(url=url+str(page), callback=self.parse)

    def parse(self, response):
        print("Parsing results for: " + response.url)
        links = response.css("li[class='list-group-item article']")
        links.extract()
        for index, link in enumerate(links):
            url =  link.xpath("h3/a/@href").extract()[0]
            ticker = link.xpath("div/span")[0].xpath("a/text()").extract()[0]
            title = link.xpath("h3/a/text()").extract()[0]
            timestamp = link.xpath("div/text()").extract()[1].strip()
            page = response.url[response.url.rfind('/')+1:]

            data = urlparse(response.url)
            urldata = data.scheme + "://" + data.netloc + url  # .scheme, .path, .params, .query
            #print("======------======")
            #print("Getting Page:")
            #print("URL: " + urldata)
            #print("======------======")

            item = ScrapySpiderItem()
            item['ticker'] = ticker
            item['url'] =  urldata
            item['title'] = title
            item['time'] = timestamp
            item['page'] = page
            item['text'] = ""
            yield item
