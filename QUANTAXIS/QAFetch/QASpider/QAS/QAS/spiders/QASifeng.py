# -*- coding: utf-8 -*-
import scrapy


class QasifengSpider(scrapy.Spider):
    name = "QASifeng"
    allowed_domains = ["ifeng.com"]
    start_urls = ['http://ifeng.com/']

    def parse(self, response):
        pass
