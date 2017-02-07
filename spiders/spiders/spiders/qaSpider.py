# -*- coding: utf-8 -*-
import scrapy


class QaspiderSpider(scrapy.Spider):
    name = "qaSpider"
    allowed_domains = ["baidu.com"]
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
