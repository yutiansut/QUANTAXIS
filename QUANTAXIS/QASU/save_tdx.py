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

import concurrent
import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pandas as pd
import pymongo

from QUANTAXIS.QAFetch import QA_fetch_get_stock_block
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_index_day,
                                     QA_fetch_get_index_min,
                                     QA_fetch_get_stock_day,
                                     QA_fetch_get_stock_info,
                                     QA_fetch_get_stock_list,
                                     QA_fetch_get_stock_min,
                                     QA_fetch_get_stock_transaction,
                                     QA_fetch_get_stock_xdxr, select_best_ip)
from QUANTAXIS.QAFetch.QATushare import QA_fetch_get_stock_time_to_market
from QUANTAXIS.QAUtil import (DATABASE, QA_util_get_real_date,
                              QA_util_log_info, QA_util_to_json_from_pandas,
                              trade_date_sse)

# ip=select_best_ip()


def now_time():
    return str(QA_util_get_real_date(str(datetime.date.today() - datetime.timedelta(days=1)), trade_date_sse, -1)) + \
        ' 17:00:00' if datetime.datetime.now().hour < 15 else str(QA_util_get_real_date(
            str(datetime.date.today()), trade_date_sse, -1)) + ' 15:00:00'


def QA_SU_save_stock_day(client=DATABASE):
    """save stock_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = QA_fetch_get_stock_time_to_market()
    coll_stock_day = client.stock_day
    coll_stock_day.create_index(
        [("code", pymongo.ASCENDING), ("date_stamp", pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll_stock_day):
        try:
            QA_util_log_info(
                '##JOB01 Now Saving STOCK_DAY==== %s' % (str(code)))

            ref = coll_stock_day.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]
            if ref.count() > 0:
                    # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

                start_date = ref[ref.count() - 1]['date']

                QA_util_log_info(' UPDATE_STOCK_DAY \n Trying updating %s from %s to %s' %
                                 (code, start_date, end_date))
                if start_date != end_date:
                    coll_stock_day.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_stock_day(str(code), start_date, end_date, '00')[1::]))
            else:
                start_date = '1990-01-01'
                QA_util_log_info(' UPDATE_STOCK_DAY \n Trying updating %s from %s to %s' %
                                 (code, start_date, end_date))
                if start_date != end_date:
                    coll_stock_day.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_stock_day(str(code), start_date, end_date, '00')))
        except:
            err.append(str(code))
    for item in range(len(stock_list)):
        QA_util_log_info('The %s of Total %s' %
                         (item, len(stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(item / len(stock_list) * 100))[0:4] + '%')

        __saving_work(stock_list.index[item], coll_stock_day)
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


def QA_SU_save_stock_xdxr(client=DATABASE):
    """[summary]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    client.drop_collection('stock_xdxr')
    stock_list = QA_fetch_get_stock_time_to_market()
    coll = client.stock_xdxr
    coll.create_index([('code', pymongo.ASCENDING),
                       ('date', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):
        QA_util_log_info('##JOB02 Now Saving XDXR INFO ==== %s' % (str(code)))
        try:
            coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_xdxr(str(code))))

        except:

            err.append(str(code))
    for i_ in range(len(stock_list)):
        QA_util_log_info('The %s of Total %s' % (i_, len(stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(stock_list) * 100))[0:4] + '%')
        __saving_work(stock_list.index[i_], coll)
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:

        try_code = err
        err = []
        QA_util_log_info('Try to get stock xdxr info in erro list! \n')
        for i__ in range(len(try_code)):
            QA_util_log_info('The %s of Total %s' % (i__, len(try_code)))
            QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
                float(i__ / len(try_code) * 100))[0:4] + '%')
            __saving_work(try_code[i__], coll)
        if len(err) < 1:
            QA_util_log_info('SUCCESS')
        else:
            QA_util_log_info('ERROR CODE \n ')
            QA_util_log_info(err)


def QA_SU_save_stock_min(client=DATABASE):
    """save stock_min

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = QA_fetch_get_stock_time_to_market()
    coll = client.stock_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):
        QA_util_log_info('##JOB03 Now Saving STOCK_MIN ==== %s' % (str(code)))
        try:
            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    QA_util_log_info(
                        '##JOB03.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                    if start_time != end_time:
                        __data = QA_fetch_get_stock_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'

                    QA_util_log_info(
                        '##JOB03.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                    if start_time != end_time:
                        __data = QA_fetch_get_stock_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data))
        except Exception as e:
            QA_util_log_info(e)

            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)
    #executor.map((__saving_work, stock_list.index[i_], coll),URLS)
    res = {executor.submit(
        __saving_work, stock_list.index[i_], coll) for i_ in range(len(stock_list))}
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        QA_util_log_info('The %s of Total %s' % (count, len(stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(stock_list) * 100))[0:4] + '%')
        count = count + 1
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


def QA_SU_save_index_day(client=DATABASE):
    """save index_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = QA_fetch_get_stock_list('index')
    coll = client.index_day
    coll.create_index([('code', pymongo.ASCENDING),
                       ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        try:

            ref_ = coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']

                QA_util_log_info('##JOB04 Now Saving INDEX_DAY==== \n Trying updating %s from %s to %s' %
                                 (code, start_time, end_time))

                if start_time != end_time:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(str(code), start_time, end_time)[1::]))
            else:
                start_time = '1990-01-01'
                QA_util_log_info('##JOB04 Now Saving INDEX_DAY==== \n Trying updating %s from %s to %s' %
                                 (code, start_time, end_time))
                coll.insert_many(
                    QA_util_to_json_from_pandas(
                        QA_fetch_get_index_day(str(code), start_time, end_time)))
        except:
            err.append(str(code))
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list.index[i_][0], coll)
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


def QA_SU_save_index_min(client=DATABASE):
    """save index_min

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = QA_fetch_get_stock_list('index')
    coll = client.index_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        QA_util_log_info('##JOB05 Now Saving Index_MIN ==== %s' % (str(code)))
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    QA_util_log_info(
                        '##JOB05.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                    if start_time != end_time:
                        __data = QA_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'
                    QA_util_log_info(
                        '##JOB05.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                    if start_time != end_time:
                        __data = QA_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], coll) for i_ in range(len(__index_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        QA_util_log_info('The %s of Total %s' % (count, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__index_list) * 100))[0:4] + '%')
        count = count + 1
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


def QA_SU_save_etf_day(client=DATABASE):
    """save etf_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = QA_fetch_get_stock_list('etf')
    coll = client.index_day
    coll.create_index([('code', pymongo.ASCENDING),
                       ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        try:

            ref_ = coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']

                QA_util_log_info('##JOB06 Now Saving ETF_DAY==== \n Trying updating %s from %s to %s' %
                                 (code, start_time, end_time))

                if start_time != end_time:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(str(code), start_time, end_time)[1::]))
            else:
                start_time = '1990-01-01'
                QA_util_log_info('##JOB06 Now Saving ETF_DAY==== \n Trying updating %s from %s to %s' %
                                 (code, start_time, end_time))

                if start_time != end_time:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(str(code), start_time, end_time)))
        except:
            err.append(str(code))
    for i_ in range(len(__index_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(__index_list) * 100))[0:4] + '%')
        __saving_work(__index_list.index[i_][0], coll)
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


def QA_SU_save_etf_min(client=DATABASE):
    """save etf_min

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = QA_fetch_get_stock_list('etf')
    coll = client.index_min
    coll.create_index([('code', pymongo.ASCENDING), ('time_stamp',
                                                     pymongo.ASCENDING), ('date_stamp', pymongo.ASCENDING)])
    err = []

    def __saving_work(code, coll):

        QA_util_log_info('##JOB07 Now Saving ETF_MIN ==== %s' % (str(code)))
        try:

            for type in ['1min', '5min', '15min', '30min', '60min']:
                ref_ = coll.find(
                    {'code': str(code)[0:6], 'type': type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]['datetime']

                    QA_util_log_info(
                        '##JOB07.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                    if start_time != end_time:
                        __data = QA_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data[1::]))
                else:
                    start_time = '2015-01-01'
                    QA_util_log_info(
                        '##JOB07.%s Now Saving %s from %s to %s ==%s ' % (['1min', '5min', '15min', '30min', '60min'].index(type), str(code), start_time, end_time, type))
                    if start_time != end_time:
                        __data = QA_fetch_get_index_min(
                            str(code), start_time, end_time, type)
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data))
        except:
            err.append(code)

    executor = ThreadPoolExecutor(max_workers=4)

    res = {executor.submit(
        __saving_work, __index_list.index[i_][0], coll) for i_ in range(len(__index_list))}  # multi index ./.
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        QA_util_log_info('The %s of Total %s' % (count, len(__index_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(count / len(__index_list) * 100))[0:4] + '%')
        count = count + 1
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


def QA_SU_save_stock_list(client=DATABASE):
    """save stock_list

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    client.drop_collection('stock_list')
    coll = client.stock_list
    coll.create_index('code')
    err = []

    try:
        QA_util_log_info('##JOB08 Now Saving STOCK_LIST ====')
        coll.insert_many(QA_util_to_json_from_pandas(
            QA_fetch_get_stock_list()))
    except:
        pass


def QA_SU_save_stock_block(client=DATABASE):
    """save stock_block

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    client.drop_collection('stock_block')
    coll = client.stock_block
    coll.create_index('code')
    err = []
    try:
        QA_util_log_info('##JOB09 Now Saving STOCK_BlOCK ====')
        coll.insert_many(QA_util_to_json_from_pandas(
            QA_fetch_get_stock_block('tdx')))
        coll.insert_many(QA_util_to_json_from_pandas(
            QA_fetch_get_stock_block('ths')))
    except:
        pass


def QA_SU_save_stock_info(client=DATABASE):
    """save stock_info

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    client.drop_collection('stock_info')
    stock_list = QA_fetch_get_stock_time_to_market()
    coll = client.stock_info
    coll.create_index('code')
    err = []

    def __saving_work(code, coll):
        QA_util_log_info(
            '##JOB010 Now Saving STOCK INFO ==== %s' % (str(code)))
        try:
            coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_info(str(code))))

        except:
            err.append(str(code))
    for i_ in range(len(stock_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(stock_list) * 100))[0:4] + '%')
        __saving_work(stock_list.index[i_], coll)
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


def QA_SU_save_stock_transaction(client=DATABASE):
    """save stock_transaction

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    stock_list = QA_fetch_get_stock_time_to_market()
    coll = client.stock_transaction
    coll.create_index('code')
    err = []

    def __saving_work(code):
        QA_util_log_info(
            '##JOB10 Now Saving STOCK_TRANSACTION ==== %s' % (str(code)))
        try:
            coll.insert_many(
                QA_util_to_json_from_pandas(
                    QA_fetch_get_stock_transaction(str(code), str(stock_list[code]), str(now_time())[0:10])))
        except:
            err.append(str(code))
    for i_ in range(len(stock_list)):
        #__saving_work('000001')
        QA_util_log_info('The %s of Total %s' % (i_, len(stock_list)))
        QA_util_log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(stock_list) * 100))[0:4] + '%')
        __saving_work(stock_list.index[i_])
    if len(err) < 1:
        QA_util_log_info('SUCCESS')
    else:
        QA_util_log_info('ERROR CODE \n ')
        QA_util_log_info(err)


if __name__ == '__main__':
    # QA_SU_save_stock_day()
    # QA_SU_save_stock_xdxr()
    # QA_SU_save_stock_min()
    # QA_SU_save_stock_transaction()
    # QA_SU_save_index_day()
    # QA_SU_save_stock_list()
    # QA_SU_save_index_min()
    pass
