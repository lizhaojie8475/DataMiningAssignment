# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class TextspiderItem(Item):
    pass

class NewsItem(Item):
    title = Field()
    content = Field()
    type = Field()
    time = Field()
    url = Field()