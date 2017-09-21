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
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info, trade_date_sse,
                              QA_util_to_json_from_pandas)

from concurrent.futures import ThreadPoolExecutor
import concurrent

# ip=select_best_ip()


def now_time():
    return datetime.datetime.now() - datetime.timedelta(days=1) if datetime.datetime.now().hour < 15 else datetime.datetime.now()


def QA_SU_save_stock_day(client=QA_Setting.client):
    __stock_list = QA_fetch_get_stock_time_to_market()
    coll_stock_day = client.quantaxis.stock_day
    coll_stock_day.ensure_index('code')
    __err = []

    def __saving_work(code, coll_stock_day):
        try:
            QA_util_log_info(
                '##JOB01 Now Saving STOCK_DAY==== %s' % (str(code)))

            ref = coll_stock_day.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]
            if ref.count() > 0:
                    # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

                start_date = ref[ref.count() - 1]['date']
            else:
                start_date = '1990-01-01'
            QA_util_log_info(' UPDATE_STOCK_DAY \n Trying updating %s from %s to %s' %
                             (code, start_date, end_date))
            if start_date != end_date:
                coll_stock_day.insert_many(
                    QA_util_to_json_from_pandas(
                        QA_fetch_get_stock_day(str(code), start_date, end_date, '00')[1::]))
        except:
            __err.append(str(code))
    for item in range(len(__stock_list)):
        QA_util_log_info('The %s of Total %s' %
                         (item, len(__stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(item / len(__stock_list) * 100))[0:4] + '%')

        __saving_work(__stock_list.index[item], coll_stock_day)


def QA_SU_save_stock_xdxr(client=QA_Setting.client):
    client.quantaxis.drop_collection('stock_xdxr')
    __stock_list = QA_fetch_get_stock_time_to_market()
    __coll = client.quantaxis.stock_xdxr
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code, __coll):
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
        __saving_work(__stock_list.index[i_], __coll)


def QA_SU_save_stock_min(client=QA_Setting.client):
    __stock_list = QA_fetch_get_stock_time_to_market()
    __coll = client.quantaxis.stock_min
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code, __coll):
        QA_util_log_info('##JOB03 Now Saving STOCK_MIN ==== %s' % (str(code)))
        try:
            for type in ['1min', '5min', '15min','30min','60min']:
                ref_ = __coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(datetime.datetime.now())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']
                else:
                    start_time = '2015-01-01'
                QA_util_log_info(
                    '##JOB03.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min','30min','60min'].index(type), str(code), start_time, end_time, type))
                if start_time != end_time:
                    __data=QA_fetch_get_stock_min(str(code), start_time, end_time, type)
                    if len(__data)>1:
                        __coll.insert_many(
                            QA_util_to_json_from_pandas(__data[1::]))

        except Exception as e:
            QA_util_log_info(e)

            __err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __stock_list.index[i_], __coll) for i_ in range(len(__stock_list))}
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        QA_util_log_info('The %s of Total %s' % (count, len(__stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__stock_list) * 100))[0:4] + '%')
        count = count + 1
    QA_util_log_info('ERROR CODE \n ')
    QA_util_log_info(__err)


def QA_SU_save_index_day(client=QA_Setting.client):
    __index_list = QA_fetch_get_stock_list('index')
    __coll = client.quantaxis.index_day
    __coll.ensure_index('code')
    __err = []
    def __saving_work(code, __coll):
        
        try:

            ref_ = __coll.find({'code': str(code)[0:6]})
            end_time = end_date = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']
            else:
                start_time = '1990-01-01'

            QA_util_log_info('##JOB04 Now Saving INDEX_DAY==== \n Trying updating %s from %s to %s' %
                             (code, start_time, end_time))

            if start_time != end_time:
                __coll.insert_many(
                    QA_util_to_json_from_pandas(
                        QA_fetch_get_index_day(str(code), start_time, end_time)[1::]))
        except:
            __err.append(str(code))
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list.index[i_][0], __coll)


def QA_SU_save_index_min(client=QA_Setting.client):
    __index_list = QA_fetch_get_stock_list('index')
    __coll = client.quantaxis.index_min
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code, __coll):
        
        QA_util_log_info('##JOB05 Now Saving Index_MIN ==== %s' % (str(code)))
        try:

            for type in ['1min', '5min', '15min','30min','60min']:
                ref_ = __coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(datetime.datetime.now())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']
                else:
                    start_time = '2015-01-01'
                QA_util_log_info(
                    '##JOB05.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min','30min','60min'].index(type), str(code), start_time, end_time, type))
                if start_time != end_time:
                    __data=QA_fetch_get_index_min(str(code), start_time, end_time, type)
                    if len(__data)>1:
                        __coll.insert_many(
                            QA_util_to_json_from_pandas(__data[1::]))

        except:
            __err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], __coll) for i_ in range(len(__index_list))}# multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        QA_util_log_info('The %s of Total %s' % (count, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__index_list) * 100))[0:4] + '%')
        count = count + 1
    QA_util_log_info('ERROR CODE \n ')
    QA_util_log_info(__err)


def QA_SU_save_etf_day(client=QA_Setting.client):
    __index_list = QA_fetch_get_stock_list('etf')
    __coll = client.quantaxis.index_day
    __coll.ensure_index('code')
    __err = []
    def __saving_work(code, __coll):
        
        try:

            ref_ = __coll.find({'code': str(code)[0:6]})
            end_time = end_date = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']
            else:
                start_time = '1990-01-01'

            QA_util_log_info('##JOB06 Now Saving ETF_DAY==== \n Trying updating %s from %s to %s' %
                             (code, start_time, end_time))

            if start_time != end_time:
                __coll.insert_many(
                    QA_util_to_json_from_pandas(
                        QA_fetch_get_index_day(str(code), start_time, end_time)[1::]))
        except:
            __err.append(str(code))
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list.index[i_][0], __coll)


def QA_SU_save_etf_min(client=QA_Setting.client):
    __index_list = QA_fetch_get_stock_list('etf')
    __coll = client.quantaxis.index_min
    __coll.ensure_index('code')
    __err = []

    def __saving_work(code, __coll):
        
        QA_util_log_info('##JOB07 Now Saving ETF_MIN ==== %s' % (str(code)))
        try:

            for type in ['1min', '5min', '15min','30min','60min']:
                ref_ = __coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(datetime.datetime.now())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']
                else:
                    start_time = '2015-01-01'
                QA_util_log_info(
                    '##JOB07.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min','30min','60min'].index(type), str(code), start_time, end_time, type))
                if start_time != end_time:
                    __data=QA_fetch_get_index_min(str(code), start_time, end_time, type)
                    if len(__data)>1:
                        __coll.insert_many(
                            QA_util_to_json_from_pandas(__data[1::]))

        except:
            __err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], __coll) for i_ in range(len(__index_list))}# multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        QA_util_log_info('The %s of Total %s' % (count, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__index_list) * 100))[0:4] + '%')
        count = count + 1
    QA_util_log_info('ERROR CODE \n ')
    QA_util_log_info(__err)


def QA_SU_save_stock_list(client=QA_Setting.client):
    client.quantaxis.drop_collection('stock_list')
    __coll = client.quantaxis.stock_list
    __coll.ensure_index('code')
    __err = []

    try:
        QA_util_log_info('##JOB08 Now Saving STOCK_LIST ====')
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
                    QA_fetch_get_stock_transaction(str(code), str(__stock_list[code]), str(now_time())[0:10])))
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
    # QA_SU_save_index_min()
    pass
