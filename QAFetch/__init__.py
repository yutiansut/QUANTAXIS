#coding:utf-8

import QAFetch.QAWind as QAWind
"""
author yutiansut
"""

def get_stock_day(name,startDate,endDate):
    return QAWind.get_stock_day(name,startDate,endDate)
    
def get_trade_date(endDate,exchange):
    return QAWind.get_trade_date(endDate,exchange)


