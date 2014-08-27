# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class veillItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    villeDep = scrapy.Field()
    villeArr = scrapy.Field()
    dDep = scrapy.Field()
    hDep = scrapy.Field()
    prix = scrapy.Field()