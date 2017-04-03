#coding:utf-8

import QAWind as QAWind
import QATushare as QATushare
#import QAFetch.QAGmsdk as QAGmsdk
#import QAFetch.QACrawlData as QACD
import pymongo


"""
author yutiansut
"""
def use(package):
    if package in ['wind']:
        return QAWind
    elif package in ['tushare','ts']:
        return QATushare

def get_stock_day(package,name,startDate,endDate):
    Engine=use(package)
    return Engine.get_stock_day(name,startDate,endDate)

    
def get_trade_date(package,endDate,exchange):
    Engine=use(package)
    return Engine.get_trade_date(endDate,exchange)

def save_stock_day(package,startDate,endDate):
    Engine=use(package)
    client=pymongo.MongoClient()
    db=client.quantaxis
    collSelect=db.dates
    coll=db.stock_day
    for item in collSelect.find({"exchange":'SSE'}):
        name=item['varietyName']
        Engine.get_stock_day(name,'2000-01-01','2017-04-01')

def save_trade_date(package,endDate):
    Engine=use(package)
    client=pymongo.MongoClient()
    coll=client.quantaxis.dates
    #coll.insert()