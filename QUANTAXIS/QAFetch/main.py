# encoding: UTF-8
"""
QA_Fetch main entry
with QAWind/QATushare

@author yutiansut
"""
from . import QAWind as QAWind
from . import QATushare as QATushare
#import QAFetch.QAGmsdk as QAGmsdk
#import QAFetch.QACrawlData as QACD
import pymongo

#from WindPy import w
#w.start()
#w.start()

def use(package):
    if package in ['wind']:
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

