# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HexunblogsItem(scrapy.Item):
    # define the fields for your item here like:
    articleName = scrapy.Field()
    articleUrl = scrapy.Field()
    articleClicks = scrapy.Field()
    articleComments = scrapy.Field()

