#coding:utf-8

import QAFetch.QAWind as QAWind
import QAFetch.QATushare as QATushare
#import QAFetch.QAGmsdk as QAGmsdk
#import QAFetch.QACrawlData as QACD

"""
author yutiansut
"""

def get_stock_day(name,startDate,endDate):
    try:
        return QAWind.get_stock_day(name,startDate,endDate)
    except:
        return QATushare.get_stock_day(name,startDate,endDate)
    
def get_trade_date(endDate,exchange):
    return QAWind.get_trade_date(endDate,exchange)

