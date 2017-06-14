# encoding: UTF-8


"""
The MIT License (MIT)

Copyright (c) 2016-2017 yutiansut/QUANTAXIS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


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

