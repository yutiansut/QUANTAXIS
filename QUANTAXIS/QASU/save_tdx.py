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

import pandas as pd
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_index_day,
                                     QA_fetch_get_index_min,
                                     QA_fetch_get_stock_day,
                                     QA_fetch_get_stock_list,
                                     QA_fetch_get_stock_min,
                                     QA_fetch_get_stock_transaction,
                                     QA_fetch_get_stock_xdxr, select_best_ip)
from QUANTAXIS.QAFetch.QATushare import QA_fetch_get_stock_time_to_market
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_to_json_from_pandas)

# ip=select_best_ip()


def save_stock_day(code, start, end, coll):
    QA_util_log_info('##JOB01 Now Saving STOCK_DAY==== %s' % (str(code)))
    coll.insert_many(
        QA_util_to_json_from_pandas(
            QA_fetch_get_stock_day(
                str(code), start, end, '00')))


def QA_SU_save_stock_day(start='1990-01-01', end=str(datetime.date.today()), client=QA_Setting.client):
    __stock_list = QA_fetch_get_stock_time_to_market()
    __coll = client.quantaxis.stock_day
    __coll.ensure_index('code')
    __err = []
    for i_ in range(len(__stock_list)):
        QA_util_log_info('The %s of Total %s' % (i_, len(__stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        try:
            save_stock_day(__stock_list.index[i_], start, end, __coll)
        except:
            __err.append(__stock_list.index[i_])
    if len(__err) > 0:
        QA_util_log_info('ERROR! Try Again with \n')
        QA_util_log_info(__err)


def QA_SU_save_stock_xdxr(client=QA_Setting.client):
    __stock_list = QA_fetch_get_stock_time_to_market()
    __coll = client.quantaxis.stock_xdxr
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code):
        QA_util_log_info('##JOB02 Now Saving XDXR INFO ==== %s' % (str(code)))
        try:
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_xdxr(str(code))))

        except:
            __err.append(str(code))
    for i_ in range(len(__stock_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        __saving_work(__stock_list.index[i_])


def save_stock_min(code, start, end, level, coll):
    QA_util_log_info('##JOB03 Now Saving STOCK_MIN ==== %s' % (str(code)))
    QA_util_log_info(
        '##JOB03.1 Now Saving STOCK_MIN %s==== %s' % (level, str(code)))
    coll.insert_many(
        QA_util_to_json_from_pandas(
            QA_fetch_get_stock_min(str(code), start, end, level)))


def QA_SU_save_stock_min(client=QA_Setting.client):
    __stock_list = QA_fetch_get_stock_time_to_market()
    __coll = client.quantaxis.stock_min
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code):
        QA_util_log_info('##JOB03 Now Saving STOCK_MIN ==== %s' % (str(code)))
        try:
            QA_util_log_info(
                '##JOB03.1 Now Saving STOCK_1_MIN ==== %s' % (str(code)))
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_min(str(code), '2015-01-01', str(datetime.date.today()), '1min')))
            QA_util_log_info(
                '##JOB03.2 Now Saving STOCK_5_MIN ==== %s' % (str(code)))
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_min(str(code), '2015-01-01', str(datetime.date.today()), '5min')))
            QA_util_log_info(
                '##JOB03.3 Now Saving STOCK_15_MIN ==== %s' % (str(code)))
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_min(str(code), '2015-01-01', str(datetime.date.today()), '15min')))
        except:
            __err.append(code)
    for i_ in range(len(__stock_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        __saving_work(__stock_list.index[i_])


def QA_SU_save_index_day(client=QA_Setting.client):
    __index_list = QA_fetch_get_stock_list('index')
    __coll = client.quantaxis.index_day
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code):
        try:
            QA_util_log_info(
                '##JOB04 Now Saving INDEX_DAY==== %s' % (str(code)))
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_index_day(str(code), '1990-01-01', str(datetime.date.today()))))
        except:
            __err.append(str(code))
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list['code'][i_])


def QA_SU_save_index_min(client=QA_Setting.client):
    __index_list = QA_fetch_get_stock_list('index')

    __coll = client.quantaxis.index_min
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code):
        QA_util_log_info('##JOB05 Now Saving INDEX_MIN  ==== %s' % (str(code)))
        try:
            QA_util_log_info(
                '##JOB05.1 Now Saving INDEX_1_MIN ==== %s' % (str(code)))
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_index_min(str(code), '2015-01-01', str(datetime.date.today()), '1min')))
            QA_util_log_info(
                '##JOB05.2 Now Saving INDEX_5_MIN ==== %s' % (str(code)))
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_index_min(str(code), '2015-01-01', str(datetime.date.today()), '5min')))
            QA_util_log_info(
                '##JOB05.3 Now Saving INDEX_15_MIN ==== %s' % (str(code)))
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_index_min(str(code), '2015-01-01', str(datetime.date.today()), '15min')))
        except:
            QA_util_log_info('error')
            __err.append(code)
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list['code'][i_])


def QA_SU_save_stock_list(client=QA_Setting.client):
    __coll = client.quantaxis.stock_list
    __coll.ensure_index('code')
    __err = []

    try:
        QA_util_log_info('##JOB06 Now Saving STOCK_LIST ====')
        __coll.insert_many(QA_util_to_json_from_pandas(
            QA_fetch_get_stock_list()))
    except:
        pass


def QA_SU_save_stock_transaction(client=QA_Setting.client):
    __stock_list = QA_fetch_get_stock_time_to_market()
    __coll = client.quantaxis.stock_transaction
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code):
        QA_util_log_info(
            '##JOB07 Now Saving STOCK_TRANSACTION ==== %s' % (str(code)))
        try:
            __coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_transaction(str(code), str(__stock_list[code]), str(datetime.date.today()))))
        except:
            __err.append(str(code))
    for i_ in range(len(__stock_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__stock_list) * 100))[0:4] + '%')
        __saving_work(__stock_list.index[i_])


if __name__ == '__main__':
    # QA_SU_save_stock_day()
    # QA_SU_save_stock_xdxr()
    # QA_SU_save_stock_min()
    # QA_SU_save_stock_transaction()
    # QA_SU_save_index_day()
    # QA_SU_save_stock_list()
    QA_SU_save_index_min()
