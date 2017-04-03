# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WallstreetcnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    poster = scrapy.Field()
    tag = scrapy.Field()
    time = scrapy.Field()
    viewNum = scrapy.Field()
    comments = scrapy.Field()

class articlePool(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    comment_num = scrapy.Field()
    pic = scrapy.Field()
    news_no = scrapy.Field()
    title = scrapy.Field()
    news_url = scrapy.Field()
    abstract = scrapy.Field()
    author = scrapy.Field()