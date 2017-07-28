# coding:utf-8

import QUANTAXIS as QA
import tushare as ts

import pytdx
from pytdx.hq import TdxHq_API

try:
    from WindPy import w
except:
    print('no windpy module')

import json,time,datetime,csv