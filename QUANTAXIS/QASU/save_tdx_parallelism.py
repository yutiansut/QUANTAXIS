# -*- coding: utf-8 -*-
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

from QUANTAXIS.QAFetch.QATdx import (
    QA_fetch_get_option_day,
    QA_fetch_get_option_min,
    QA_fetch_get_index_day,
    QA_fetch_get_index_min,
    QA_fetch_get_stock_day,
    QA_fetch_get_stock_info,
    QA_fetch_get_stock_list,
    QA_fetch_get_future_list,
    QA_fetch_get_index_list,
    QA_fetch_get_future_day,
    QA_fetch_get_future_min,
    QA_fetch_get_stock_min,
    QA_fetch_get_stock_transaction,
    QA_fetch_get_stock_xdxr,
    select_best_ip
)
from QUANTAXIS.QAUtil import (
    DATABASE,
    QA_util_get_next_day,
    QA_util_get_real_date,
    QA_util_log_info,
    QA_util_to_json_from_pandas,
    trade_date_sse
)
from QUANTAXIS.QAUtil import Parallelism
import json
import pandas as pd
import pymongo
from multiprocessing import cpu_count
from QUANTAXIS.QASU.save_tdx import now_time
from QUANTAXIS.QAFetch.QATdx import ping, get_ip_list_by_multi_process_ping, stock_ip_list


class QA_SU_save_stock_day_parallelism(Parallelism):

    def __init__(self, processes=cpu_count(), client=DATABASE, ui_log=None, ui_progress=None):
        super(QA_SU_save_stock_day_parallelism, self).__init__(processes)
        self.client = client
        self.ui_log = ui_log
        self.ui_progress = ui_progress

    def add(self, func, iter):
        if isinstance(iter, list) and self.cores > 1 and len(iter) > self.cores:
            j = self.cores + 1
            for i in range(j):
                pLen = int(len(iter) / j) + 1
                self.data = self.pool.starmap_async(func, iter[int(i * pLen):int((i + 1) * pLen)],
                                                    callback=self.complete,
                                                    error_callback=self.exception)
                self.total_processes += 1
        else:
            self.data = self.pool.starmap_async(func=func, iterable=iter, callback=self.complete,
                                                error_callback=self.exception)
            self.total_processes += 1

    def complete(self, result):

        QA_util_log_info(
            '##JOB02 Saving STOCK_DAY==== {} ，股票数量： {}'.format('QA_SU_save_stock_day_parallelism class', len(result))
        )

        for value in result:
            self.__saving_work(value)

        super(QA_SU_save_stock_day_parallelism, self).complete(result)

    def __saving_work(self, df=pd.DataFrame()):
        try:
            if not (df is None) and len(df) > 0:
                coll_stock_day = self.client.stock_day
                coll_stock_day.create_index(
                    [("code",
                      pymongo.ASCENDING),
                     ("date_stamp",
                      pymongo.ASCENDING)]
                )
                coll_stock_day.insert_many(QA_util_to_json_from_pandas(df))
                QA_util_log_info(
                    '##JOB02 Now Saved STOCK_DAY==== {}'.format(df.code.unique()[0]),
                    self.ui_log
                )
            else:
                QA_util_log_info(
                    '##JOB02 Saving STOCK_DAY==== {}'.format('skipped'),
                    self.ui_log
                )

        except Exception as error0:
            print(error0, flush=True)
            # err.append(df.code.unique()[0])


def QA_SU_save_stock_day(client=DATABASE, ui_log=None, ui_progress=None):
    '''
     save stock_day
    保存日线数据
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    '''
    stock_list = QA_fetch_get_stock_list().code.unique().tolist()
    coll_stock_day = client.stock_day
    coll_stock_day.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []

    # saveing result

    def __gen_param(stock_list, coll_stock_day, ip_list=[]):
        results = []
        count = len(ip_list)
        total = len(stock_list)
        for item in range(len(stock_list)):
            try:
                code = stock_list[item]
                QA_util_log_info(
                    '##JOB01 Now Saving STOCK_DAY==== {}'.format(str(code)),
                    ui_log
                )

                # 首选查找数据库 是否 有 这个代码的数据
                search_cond = {'code': str(code)[0:6]}
                ref = coll_stock_day.find(search_cond)
                end_date = str(now_time())[0:10]
                ref_count = coll_stock_day.count_documents(search_cond)

                # 当前数据库已经包含了这个代码的数据， 继续增量更新
                # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
                if ref_count > 0:
                    # 接着上次获取的日期继续更新
                    start_date = ref[ref_count - 1]['date']
                    # print("ref[ref.count() - 1]['date'] {} {}".format(ref.count(), coll_stock_day.count_documents({'code': str(code)[0:6]})))
                else:
                    # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
                    start_date = '1990-01-01'
                QA_util_log_info(
                    'UPDATE_STOCK_DAY \n Trying updating {} from {} to {}'
                        .format(code,
                                start_date,
                                end_date),
                    ui_log
                )
                if start_date != end_date:
                    # 更新过的，不更新
                    results.extend([(code, start_date, end_date, '00', 'day', ip_list[item % count]['ip'],
                                     ip_list[item % count]['port'], item, total, ui_log, ui_progress)])
            except Exception as error0:
                print('Exception:{}'.format(error0))
                err.append(code)
        return results

    ips = get_ip_list_by_multi_process_ping(stock_ip_list, _type='stock')[:cpu_count() * 2 + 1]
    param = __gen_param(stock_list, coll_stock_day, ips)
    ps = QA_SU_save_stock_day_parallelism(processes=cpu_count() if len(ips) >= cpu_count() else len(ips),
                                          client=client, ui_log=ui_log)
    ps.add(do_saving_work, param)
    ps.run()

    if len(err) < 1:
        QA_util_log_info('SUCCESS save stock day ^_^', ui_log)
    else:
        QA_util_log_info('ERROR CODE \n ', ui_log)
        QA_util_log_info(err, ui_log)


def do_saving_work(code, start_date, end_date, if_fq='00', frequence='day', ip=None, port=None, item=0, total=1,
                   ui_log=None, ui_progress=None):
    try:
        # print(code, item, flush=True)
        QA_util_log_info('The {} of Total {}'.format(item, total))

        strProgressToLog = 'DOWNLOAD PROGRESS {} {}'.format(
            str(float(item / total * 100))[0:4] + '%',
            ui_log
        )
        intProgressToLog = int(float(item / total * 100 / 2))
        QA_util_log_info(
            strProgressToLog,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intProgressToLog
        )

        return QA_fetch_get_stock_day(code, start_date, end_date, if_fq, frequence, ip, port)
    except Exception as error0:
        print(code, error0, flush=True)
