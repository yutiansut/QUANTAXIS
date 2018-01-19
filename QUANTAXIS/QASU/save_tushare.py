# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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

from QUANTAXIS.QAFetch.QATushare import (QA_fetch_get_stock_day,
                                         QA_fetch_get_stock_info,
                                         QA_fetch_get_stock_list,
                                         QA_fetch_get_trade_date)
from QUANTAXIS.QAUtil import (QA_util_date_stamp, QA_util_log_info,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse)
from QUANTAXIS.QAUtil.QASetting import DATABASE


def QA_save_stock_day_all(client=DATABASE):
    df = ts.get_stock_basics()
    __coll = client.stock_day
    __coll.ensure_index('code')

    def saving_work(i):
        QA_util_log_info('Now Saving ==== %s' % (i))
        try:
            data_json = QA_fetch_get_stock_day(
                i, startDate='1990-01-01')

            __coll.insert_many(data_json)
        except:
            QA_util_log_info('error in saving ==== %s' % str(i))

    for i_ in range(len(df.index)):
        QA_util_log_info('The %s of Total %s' % (i_, len(df.index)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')


def QA_SU_save_stock_list(client=DATABASE):
    data = QA_fetch_get_stock_list()
    date = str(datetime.date.today())
    date_stamp = QA_util_date_stamp(date)
    coll = client.stock_list
    coll.insert({'date': date, 'date_stamp': date_stamp,
                 'stock': {'code': data}})


def QA_SU_save_trade_date_all(client=DATABASE):
    data = QA_fetch_get_trade_date('', '')
    coll = client.trade_date
    coll.insert_many(data)


def QA_SU_save_stock_info(client=DATABASE):
    data = QA_fetch_get_stock_info('all')
    coll = client.stock_info
    coll.insert_many(data)


def QA_save_stock_day_all_bfq(client=DATABASE):
    df = ts.get_stock_basics()

    __coll = client.stock_day_bfq
    __coll.ensure_index('code')

    def saving_work(i):
        QA_util_log_info('Now Saving ==== %s' % (i))
        try:
            data_json = QA_fetch_get_stock_day(
                i, startDate='1990-01-01', if_fq='00')

            __coll.insert_many(data_json)
        except:
            QA_util_log_info('error in saving ==== %s' % str(i))

    for i_ in range(len(df.index)):
        QA_util_log_info('The %s of Total %s' % (i_, len(df.index)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')


def QA_save_stock_day_with_fqfactor(client=DATABASE):
    df = ts.get_stock_basics()

    __coll = client.stock_day
    __coll.ensure_index('code')

    def saving_work(i):
        QA_util_log_info('Now Saving ==== %s' % (i))
        try:
            data_hfq = QA_fetch_get_stock_day(
                i, startDate='1990-01-01', if_fq='02', type_='pd')
            data_json = QA_util_to_json_from_pandas(data_hfq)
            __coll.insert_many(data_json)
        except:
            QA_util_log_info('error in saving ==== %s' % str(i))
    for i_ in range(len(df.index)):
        QA_util_log_info('The %s of Total %s' % (i_, len(df.index)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')

    QA_util_log_info('Saving Process has been done !')
    return 0


if __name__ == '__main__':
    QA_save_stock_day_with_fqfactor()
