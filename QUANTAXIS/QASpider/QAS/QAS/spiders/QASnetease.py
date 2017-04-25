# -*- coding: utf-8 -*-
import scrapy


class QasneteaseSpider(scrapy.Spider):
    name = "QASnetease"
    allowed_domains = ["163.com"]
    start_urls = ['http://163.com/']

    def parse(self, response):
        pass
