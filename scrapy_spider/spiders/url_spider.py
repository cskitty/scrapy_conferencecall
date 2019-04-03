#!/usr/bin/env python3
import scrapy
from scrapy.crawler import CrawlerProcess   # Programmatically execute scrapy
from scrapy_spider.items import ScrapySpiderItem

from urllib.parse import urlparse
from slugify import slugify

# RANDOMIZE USER AGENTS ON EACH REQUEST:
debug_mode = False

class UrlSpider(scrapy.Spider):

    name = "url_spider"
    download_delay = 10.0
    custom_settings = {
            # 'LOG_LEVEL': 'CRITICAL', # 'DEBUG'
            'LOG_ENABLED': True,
            'DOWNLOAD_DELAY': 10 # 0.25 == 250 ms of delay, 1 == 1000ms of delay, etc.
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
        for x in range(0, last_page):
            # DEBUGGING: CHECK ONLY FIRST ELEMENT
            if debug_mode == True and x > 0:
                break
            url = "https://seekingalpha.com/earnings/earnings-call-transcripts/%d" % (x)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("Parsing results for: " + response.url)
        #links = response.css("a[sasource='earnings-center-transcripts_article']")
        links = response.css("li[class='list-group-item article']")

        links.extract()
        for index, link in enumerate(links):
            #url = link.xpath('@href').extract()
            url =  link.xpath("h3/a/@href").extract()[0]
            ticker = link.xpath("div/span")[0].xpath("a/text()").extract()[0]
            title = link.xpath("h3/a/text()").extract()[0]
            timestamp = link.xpath("div/text()").extract()[1].strip()
            page = response.url[response.url.rfind('/')+1:]
            # DEBUGGING MODE: Parse only first link
            #if debug_mode == True and index > 0:
            #    break
            #url = link.xpath('@href').extract()
            data = urlparse(response.url)
            urldata = data.scheme + "://" + data.netloc + url  # .scheme, .path, .params, .query
            print("======------======")
            print("Getting Page:")
            print("URL: " + urldata)
            print("======------======")
            #request = scrapy.Request(data,callback=self.save_contents)
            item = ScrapySpiderItem()
            item['ticker'] = ticker
            item['url'] =  urldata
            item['title'] = title
            item['time'] = timestamp
            item['page'] = page
            yield item
