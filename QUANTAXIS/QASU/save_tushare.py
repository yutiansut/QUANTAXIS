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

import datetime
import json
import re
import time

import tushare as ts

from QUANTAXIS.QAFetch import QATushare
from QUANTAXIS.QAUtil import QA_util_date_stamp, QA_util_time_stamp
from QUANTAXIS.QAUtil.QASetting import QA_Setting


def QA_save_stock_day_all():
    df = ts.get_stock_basics()
    __setting = QA_Setting()
    __coll = __setting.client.quantaxis.stock_day
    __coll.ensure_index('code')

    def saving_work(i):
        print('Now Saving ==== %s' % (i))
        try:
            data_json = QATushare.QA_fetch_get_stock_day(i)

            __coll.insert_many(data_json)
        except:
            print('error in saving ==== %s' % str(i))
    for item in df.index:
        saving_work(item)

    saving_work('hs300')
    saving_work('sz50')


def QA_SU_save_stock_list(client):
    data = QATushare.QA_fetch_get_stock_list()
    date = str(datetime.date.today())
    date_stamp = QA_util_date_stamp(date)
    coll = client.quantaxis.stock_list
    coll.insert({'date': date, 'date_stamp': date_stamp,
                 'stock': {'code': data}})


def QA_SU_save_trade_date_all():
    data = QATushare.QA_fetch_get_trade_date('', '')
    __setting = QA_Setting()
    coll = __setting.client.quantaxis.trade_date
    coll.insert_many(data)


def QA_SU_save_stock_info(client):
    data = QATushare.QA_fetch_get_stock_info('all')
    coll = client.quantaxis.stock_info
    coll.insert_many(data)
