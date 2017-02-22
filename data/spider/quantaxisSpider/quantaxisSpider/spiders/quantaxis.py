# -*- coding: utf-8 -*-
import scrapy
import re
import json
from mongodbQuery import querylist
from quantaxisSpider.phantomjs import selenium_request
from scrapy.spiders import Spider  
from scrapy.selector import Selector  
import pymongo

class QuantaxisSpider(scrapy.Spider):
    name = "quantaxis"
    def start_requests(self):
         for i in range(1,5):
                api ='https://api.wallstreetcn.com/v2/pcarticles?page=%s&limit=100' %i
            yield scrapy.Request(api,self.parse_json_list)
    def parse(self, response):
        pass




