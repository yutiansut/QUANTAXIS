#coding:utf-8

import QAFetch.QAWind as QAWind
import QAFetch.QATushare as QATushare
#import QAFetch.QAGmsdk as QAGmsdk
#import QAFetch.QACrawlData as QACD

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

