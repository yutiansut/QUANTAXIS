# -*- coding: utf-8 -*-
import scrapy


class WscSpider(scrapy.Spider):
    name = "wsc"
    allowed_domains = ["http://wallstreetcn.com/"]
    start_urls = ['http://http://wallstreetcn.com//']

    def parse(self, response):
        pass
