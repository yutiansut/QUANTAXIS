#coding:utf-8
"""
QA fetch module

@yutiansut

QAFetch is Under [QAStandard#0.0.2@10x] Protocol


"""
from . import QAWind as QAWind
from . import QATushare as QATushare
from .QAQuery import QA_fetch_data
#import QAFetch.QAGmsdk as QAGmsdk
#import QAFetch.QACrawlData as QACD
import pymongo

#from WindPy import w
#w.start()

"""
author yutiansut
"""
def use(package):
    if package in ['wind']:
        from WindPy import w
        w.start()
        return QAWind
    elif package in ['tushare','ts']:
        return QATushare

def QA_fetch_get_stock_day(package,name,startDate,endDate):
    Engine=use(package)
    return Engine.QA_fetch_get_stock_day(name,startDate,endDate)


def QA_fetch_get_stock_indicator(package,name,startDate,endDate):
    Engine=use(package)
    return Engine.QA_fetch_get_stock_indicator(name,startDate,endDate)
    
def QA_fetch_get_trade_date(package,endDate,exchange):
    Engine=use(package)
    return Engine.QA_fetch_get_trade_date(endDate,exchange)


def QA_fetch_save_stock_day(package,startDate,endDate):
    Engine=use(package)
    client=pymongo.MongoClient()
    db=client.quantaxis
    collSelect=db.dates
    coll=db.stock_day
    for item in collSelect.find({"exchange":'SSE'}):
        name=item['varietyName']
        Engine.QA_fetch_get_stock_day(name,'2000-01-01','2017-04-01')

