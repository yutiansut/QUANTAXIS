# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
QA fetch module

@yutiansut

QAFetch is Under [QAStandard#0.0.2@10x] Protocol


"""
from . import QAWind as QAWind
from . import QATushare as QATushare
from . import QATdx as QATdx
from .QAQuery import QA_fetch_stock_day, QA_fetch_stocklist_day, QA_fetch_index_day
from . import QAThs as QAThs
#import QAFetch.QAGmsdk as QAGmsdk
#import QAFetch.QACrawlData as QACD


#from WindPy import w
# w.start()

"""
author yutiansut
"""


def use(package):
    if package in ['wind']:
        from WindPy import w
        w.start()
        return QAWind
    elif package in ['tushare', 'ts']:
        return QATushare
    elif package in ['tdx', 'pytdx']:
        return QATdx
    elif package in ['ths', 'THS']:
        return QAThs


def QA_fetch_get_stock_day(package, code, startDate, endDate, if_fq='01',type_='json'):
    Engine = use(package)
    if package in ['ths', 'THS']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, if_fq)
    elif package in ['ts','tushare']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, if_fq,type_)
    else:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate)


def QA_fetch_get_stock_realtime(package):
    Engine = use(package)
    return Engine.QA_fetch_get_stock_realtime()


def QA_fetch_get_stock_indicator(package, code, startDate, endDate):
    Engine = use(package)
    return Engine.QA_fetch_get_stock_indicator(code, startDate, endDate)


def QA_fetch_get_trade_date(package, endDate, exchange):
    Engine = use(package)
    return Engine.QA_fetch_get_trade_date(endDate, exchange)



def QA_fetch_get_stock_min(package,code,start,end,type_):
    Engine = use(package)
    if package in ['tdx','pytdx']:
        return Engine.QA_fetch_get_stock_min(code,start,end,type_)
    else:
        pass