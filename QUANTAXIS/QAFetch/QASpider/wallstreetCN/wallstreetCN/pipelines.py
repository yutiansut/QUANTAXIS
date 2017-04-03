# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymongo
from wallstreetCN.items import WallstreetcnItem,articlePool
from scrapy.conf import settings


class WallstreetcnPipeline(object):
    def __init__(self):
            # 链接数据库
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["wsc"]
        self.articles = db['articles']
        self.title= db['title']

    def process_item(self, item, spider):
        print ('get data')
        if isinstance(item, WallstreetcnItem):
            try:
                self.articles.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, articlePool):
            try:
                self.title.insert(dict(item))
            except Exception:
                pass
        return item