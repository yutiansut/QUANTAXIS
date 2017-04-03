# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
from wallstreetCN.phantomjs import selenium_request


class WallstreetcnSpiderMiddleware(object):
    print("Using Spiders")
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def process_request(self, request, spider):
        print("Using process_request")
        true_page = selenium_request(request.url)
        return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request)