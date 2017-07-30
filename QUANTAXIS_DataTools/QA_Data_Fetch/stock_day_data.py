# coding:utf-8

import csv
import datetime
import json
import os
import sys
import time

import QUANTAXIS as QA
import tushare as ts

import pytdx
from pytdx.hq import TdxHq_API

try:
    from WindPy import w
except:
    print('no windpy module')

try:
    import gmsdk
except:
    sys.exit()


def get_stock_day_k(func):
    '一个包装函数的装饰器'
    def __decor(*args, **kwargs):
        func(*args, **kwargs)

    return __decor


@get_stock_day_k
def tushare_methods(code, start, end, method='pre'):
    'tushare的数据获取方式'
    if method == 'pre' or 'qfq':
        return ts.get_k_data(code, start, end, 'D', 'qfq')
    elif method == 'hfq' or 'last':
        return ts.get_k_data(code, start, end, 'D', 'hfq')
    elif method == 'bfq' or 'normal':
        return ts.get_k_data(code, start, end, 'D', 'None')


@get_stock_day_k
def gmsdk_methods(code, start, end, method='pre'):
    '掘金的日线获取方式'
    try:
        import gmsdk
    except:
        print(Exception)
        print('no gmsdk modules find!')
