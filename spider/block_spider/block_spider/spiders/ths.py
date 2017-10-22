# -*- coding: utf-8 -*-
import scrapy


class ThsSpider(scrapy.Spider):
    name = 'ths'
    allowed_domains = ['http://q.10jqka.com.cn/gn/']
    start_urls = ['http://http://q.10jqka.com.cn/gn//']

    def parse(self, response):
        pass
