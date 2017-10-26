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
    调用网络数据接口获取数据
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


def QA_fetch_get_stock_day(package, code, startDate, endDate, **kwargs):
    Engine = use(package)
    if package in ['ths', 'THS', 'wind']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, **kwargs)
    elif package in ['ts', 'tushare']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, **kwargs)
    elif package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, **kwargs)
    else:
        return Engine.QA_fetch_get_stock_day(code, startDate, endDate, **kwargs)


def QA_fetch_get_stock_realtime(package, code, **kwargs):
    Engine = use(package)
    return Engine.QA_fetch_get_stock_realtime(code, **kwargs)


def QA_fetch_get_stock_indicator(package, code, startDate, endDate, **kwargs):
    Engine = use(package)
    return Engine.QA_fetch_get_stock_indicator(code, startDate, endDate, **kwargs)


def QA_fetch_get_trade_date(package, endDate, exchange, **kwargs):
    Engine = use(package)
    return Engine.QA_fetch_get_trade_date(endDate, exchange, **kwargs)


def QA_fetch_get_stock_min(package, code, start, end, **kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_min(code, start, end, **kwargs)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_list(package, **kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_list(**kwargs)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_transaction(package, code, start, end, **kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_transaction(code, start, end, **kwargs)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_xdxr(package, code, **kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_xdxr(code, **kwargs)
    else:
        return 'Unsupport packages'


def QA_fetch_get_index_day(package, code, start, end, **kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_index_day(code, start, end, **kwargs)
    else:
        return 'Unsupport packages'


def QA_fetch_get_index_min(package, code, start, end, **kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_index_min(code, start, end, **kwargs)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_block(package, **kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_block(**kwargs)
    else:
        return 'Unsupport packages'


def QA_fetch_get_stock_info(package,code,**kwargs):
    Engine = use(package)
    if package in ['tdx', 'pytdx']:
        return Engine.QA_fetch_get_stock_info(code,**kwargs)
    else:
        return 'Unsupport packages'