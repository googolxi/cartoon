# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    area = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    type = scrapy.Field()
    desc = scrapy.Field()
    eps = scrapy.Field()
    hits = scrapy.Field()
    ep_list = scrapy.Field()
    pic = scrapy.Field()
    


class EpItem(scrapy.Item): 
    ccid = scrapy.Field()
    src_type = scrapy.Field()
    org_url = scrapy.Field()
    key = scrapy.Field()
    ep = scrapy.Field()
    ep_title = scrapy.Field()
