# -*- coding: utf-8 -*-
import scrapy


class QashexunSpider(scrapy.Spider):
    name = "QAShexun"
    allowed_domains = ["hexun.com"]
    start_urls = ['http://hexun.com/']

    def parse(self, response):
        pass
