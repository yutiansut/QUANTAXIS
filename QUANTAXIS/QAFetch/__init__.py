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
from . import QAThs as QAThs
#import QAFetch.QAGmsdk as QAGmsdk
#import QAFetch.QACrawlData as QACD


class QA_Fetcher():
    """
    一个通用的数据获取方法类


    """

    def __init__(self, *args, **kwargs):
        pass

    @property
    def security_list(self):
        return self.security_list


def use(package):
    if package in ['wind']:
        from WindPy import w
        # w.start()
        return QAWind
    elif package in ['tushare', 'ts']:
        return QATushare
    elif package in ['tdx', 'pytdx']:
        return QATdx
    elif package in ['ths', 'THS']:
        return QAThs


def QA_fetch_get_stock_day(package, code, startDate, endDate, if_fq='00', level='day', type_='json'):
    Engine = use(package)
    if package in ['ths', 'THS', 'wind']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, if_fq)
    elif package in ['ts', 'tushare']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, if_fq, type_)
    elif package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, if_fq, level)
    else:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate)


def QA_fetch_get_stock_realtime(package, code):
    Engine = use(package)
    return Engine.QA_fetch_get_stock_realtime(code)


def QA_fetch_get_stock_indicator(package, code, startDate, endDate):
    Engine = use(package)
    return Engine.QA_fetch_get_stock_indicator(code, startDate, endDate)


def QA_fetch_get_trade_date(package, endDate, exchange):
    Engine = use(package)
    return Engine.QA_fetch_get_trade_date(endDate, exchange)


def QA_fetch_get_stock_min(package, code, start, end, level='1min'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_min(code, start, end, level)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_list(package, type_='stock'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_list(type_)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_transaction(package, code, start, end, retry=2):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_transaction(code, start, end, retry)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_xdxr(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_xdxr(code)
    else:
        return 'Unsupport packages'


def QA_fetch_get_index_day(package, code, start, end, level='day'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_index_day(code, start, end, level)
    else:
        return 'Unsupport packages'


def QA_fetch_get_index_min(package, code, start, end, level='1min'):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_index_min(code, start, end, level)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_block(package):
    Engine = use(package)
    if package in ['tdx', 'pytdx', 'ths']:
        return Engine.QA_fetch_get_stock_block()
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_info(package, code):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_info(code)
    else:
        return 'Unsupport packages'
