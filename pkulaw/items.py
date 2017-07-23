# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PkulawItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field()
    gid = scrapy.Field()
    court = scrapy.Field()
    html = scrapy.Field()
    urls = scrapy.Field()
    uid = scrapy.Field()
    text = scrapy.Field()

class PkulawBrefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field()
    gid = scrapy.Field()
    court = scrapy.Field()
    uid = scrapy.Field()
    closedate = scrapy.Field()
    casekind1 = scrapy.Field()
    casekind2 = scrapy.Field()
    casekind3 = scrapy.Field()
    casekindno = scrapy.Field()
    czjb = scrapy.Field()
    slcx = scrapy.Field()
    wslx = scrapy.Field()
    rksj = scrapy.Field()