# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ticker = Field()
    title = Field()
    url = Field()
    time = Field()
    page = Field()
    pass
