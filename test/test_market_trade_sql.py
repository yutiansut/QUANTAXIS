#coding:utf-8

import pymongo
coll=pymongo.MongoClient().quantaxis.market_history
for item in coll.find({}):
    if float(item['bid']['price']) > float(item['market']['high']) or float(item['bid']['price']) < float(item['market']['low']):
        print('wrong')
    else: print('ok')