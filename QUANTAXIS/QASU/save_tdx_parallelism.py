# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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
    QA_fetch_get_index_day,
    QA_fetch_get_stock_day,
    QA_fetch_get_stock_list
)
from QUANTAXIS.QAUtil import (
    DATABASE,
    QA_util_get_next_day,
    QA_util_log_info,
    QA_util_to_json_from_pandas
)
from QUANTAXIS.QAUtil import Parallelism, Parallelism_Thread
import pandas as pd
import pymongo
from multiprocessing import cpu_count
from QUANTAXIS.QASU.save_tdx import now_time
from QUANTAXIS.QAFetch.QATdx import (
    get_ip_list_by_multi_process_ping,
    stock_ip_list,
    QA_fetch_get_stock_xdxr
)
from QUANTAXIS.QAUtil.QACache import QA_util_cache


def run(cls_instance, code):
    return cls_instance.do_working_1(code)


def get_coll(client=None):
    cache = QA_util_cache()
    results = cache.get('tdx_coll')
    if results:
        return results
    else:
        _coll = client.index_day
        _coll.create_index(
            [('code',
              pymongo.ASCENDING),
             ('date_stamp',
              pymongo.ASCENDING)]
        )
        cache.set('tdx_coll', _coll, age=86400)
        return _coll


class QA_SU_save_day_parallelism(Parallelism):
    def __init__(self, processes=cpu_count(), client=DATABASE, ui_log=None,
                 ui_progress=None):
        super(QA_SU_save_day_parallelism, self).__init__(processes)
        self.client = client
        self.ui_log = ui_log
        self.ui_progress = ui_progress
        self.err = []
        self.__total_counts = 0
        self.__code_counts = 0

    @property
    def code_counts(self):
        return self.__code_counts

    @code_counts.setter
    def code_counts(self, value):
        self.__code_counts = value

    @property
    def total_counts(self):
        return self.__total_counts

    @total_counts.setter
    def total_counts(self, value):
        if value > 0:
            self.__total_counts = value
        else:
            raise Exception('value must be great than zero.')

    def loginfo(self, code, listCounts=10):
        if len(self._loginfolist) < listCounts:
            self._loginfolist.append(code)
        else:
            str = ''
            for i in range(len(self._loginfolist)):
                str += + self._loginfolist[i] + ' '
            str += code
            QA_util_log_info(
                '##JOB02 Now Saved STOCK_DAY==== {}'.format(
                    ),
                self.ui_log
            )
            self._loginfolist.clear()

class QA_SU_save_day_parallelism_thread(Parallelism_Thread):
    def __init__(self, processes=cpu_count(), client=DATABASE, ui_log=None,
                 ui_progress=None):
        super(QA_SU_save_day_parallelism_thread, self).__init__(processes)
        self.client = client
        self.ui_log = ui_log
        self.ui_progress = ui_progress
        self.err = []
        self.__total_counts = 0
        self.__code_counts = 0

    @property
    def code_counts(self):
        return self.__code_counts

    @code_counts.setter
    def code_counts(self, value):
        self.__code_counts = value

    @property
    def total_counts(self):
        return self.__total_counts

    @total_counts.setter
    def total_counts(self, value):
        if value > 0:
            self.__total_counts = value
        else:
            raise Exception('value must be great than zero.')

    def loginfo(self, code, listCounts=10):
        if len(self._loginfolist) < listCounts:
            self._loginfolist.append(code)
        else:
            str = ''
            for i in range(len(self._loginfolist)):
                str += + self._loginfolist[i] + ' '
            str += code
            QA_util_log_info(
                '##JOB02 Now Saved STOCK_DAY==== {}'.format(
                    ),
                self.ui_log
            )
            self._loginfolist.clear()

class QA_SU_save_stock_day_parallelism(QA_SU_save_day_parallelism):
    def complete(self, result):

        QA_util_log_info(
            '##JOB02 Saving STOCK_DAY==== {} ，股票数量： {}'.format(
                'QA_SU_save_stock_day_parallelism class', len(result))
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
                    '##JOB02 Now Saved STOCK_DAY==== {}'.format(
                        df.code.unique()[0]),
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
                    '##JOB01 Now Saving STOCK_DAY=== {}'.format(str(code)),
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
                    results.extend([(code, start_date, end_date, '00', 'day',
                                     ip_list[item % count]['ip'],
                                     ip_list[item % count]['port'], item,
                                     total,
                                     ui_log, ui_progress)])
            except Exception as error0:
                print('Exception:{}'.format(error0))
                err.append(code)
        return results

    ips = get_ip_list_by_multi_process_ping(stock_ip_list, _type='stock')[
          :cpu_count() * 2 + 1]
    param = __gen_param(stock_list, coll_stock_day, ips)
    ps = QA_SU_save_stock_day_parallelism(
        processes=cpu_count() if len(ips) >= cpu_count() else len(ips),
        client=client, ui_log=ui_log)
    ps.run(do_saving_work, param)

    if len(err) < 1:
        QA_util_log_info('SUCCESS save stock day ^_^', ui_log)
    else:
        QA_util_log_info('ERROR CODE \n ', ui_log)
        QA_util_log_info(err, ui_log)


def do_saving_work(code, start_date, end_date, if_fq='00', frequence='day',
                   ip=None, port=None, item=0, total=1,
                   ui_log=None, ui_progress=None):
    try:
        # print(code, item, flush=True)
        QA_util_log_info('The {} of Total {}'.format(item, total))
        if item % 10 or total - item < 5:
            # 每隔10个或者接近完成打印进度
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

        return QA_fetch_get_stock_day(code, start_date, end_date, if_fq,
                                      frequence, ip, port)
    except Exception as error0:
        print(code, error0, flush=True)
        return None


class QA_SU_save_index_day_parallelism(QA_SU_save_day_parallelism_thread):

    def get_index_or_etf_from_code(self, code):
        # 判断指数或基金
        if code.startswith('15') or code.startswith('5'):
            index_or_etf = 'ETF'
        else:
            index_or_etf = 'INDEX'
        return index_or_etf

    def __saving_work(self, code):
        def __QA_log_info(code, end_time, start_time):
            def loginfo(prefix='', astr='', listCounts=5):
                if len(self._loginfolist) < listCounts:
                    self._loginfolist.append(astr)
                else:
                    str = ''
                    for i in range(len(self._loginfolist)):
                        str += self._loginfolist[i] + ' '
                    str += astr
                    QA_util_log_info(
                        prefix.format(str),
                        self.ui_log
                    )
                    self._loginfolist.clear()

            index_or_etf = self.get_index_or_etf_from_code(code)
            prefix = '##JOB04 Saving {}_DAY ==== Trying updating\n{}'.format(index_or_etf, '{}')
            loginfo(prefix, ' {} from {} to {}'.format(
                code,
                start_time,
                end_time
            ))
            # log_info = '##JOB04 Saving {}_DAY====\nTrying updating {} from {} to {}'.format(
            #     index_or_etf,
            #     code,
            #     start_time,
            #     end_time
            # )
            # QA_util_log_info(
            #     log_info,
            #     ui_log=self.ui_log
            # )


        try:
            search_cond = {'code': str(code)[0:6]}
            ref_ = get_coll().find(search_cond)
            ref_count = get_coll().count_documents(search_cond)

            end_time = str(now_time())[0:10]
            if ref_count > 0:
                start_time = ref_[ref_count - 1]['date']

                __QA_log_info(code, end_time, start_time)

                if start_time != end_time:
                    get_coll().insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                QA_util_get_next_day(start_time),
                                end_time
                            )
                        )
                    )
            else:
                try:
                    start_time = '1990-01-01'
                    __QA_log_info(code, end_time, start_time)
                    get_coll().insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                start_time,
                                end_time
                            )
                        )
                    )
                except Exception as e:
                    start_time = '2009-01-01'
                    __QA_log_info(code, end_time, start_time)
                    get_coll().insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                start_time,
                                end_time
                            )
                        )
                    )
        except Exception as e:
            QA_util_log_info(e, ui_log=self.ui_log)
            self.err.append(str(code))
            QA_util_log_info(self.err, ui_log=self.ui_log)

    # @classmethod
    def do_working(self, code):
        # __saving_work('000001')
        #
        if self.total_counts > 0:
            self.code_counts += 1
            QA_util_log_info(
                'The {} of Total {}'.format(self.code_counts,
                                            self.total_counts),
                ui_log=self.ui_log
            )
            strLogProgress = 'DOWNLOAD PROGRESS {0:.2f}% '.format(
                self.code_counts / self.total_counts * 100
            )
            intLogProgress = int(
                float(self.code_counts / self.total_counts * 10000.0))
            QA_util_log_info(
                strLogProgress,
                ui_log=self.ui_log,
                ui_progress=self.ui_progress,
                ui_progress_int_value=intLogProgress
            )
        self.__saving_work(code)
        return code

    def complete(self, result):
        if len(self.err) < 1:
            QA_util_log_info('SUCCESS', ui_log=self.ui_log)
        else:
            QA_util_log_info(' ERROR CODE \n ', ui_log=self.ui_log)
            QA_util_log_info(self.err, ui_log=self.ui_log)


def QA_SU_save_index_day(client=DATABASE, ui_log=None, ui_progress=None):
    """save index_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    index__or_etf = 'index'
    _QA_SU_save_index_or_etf_day(index__or_etf, client, ui_log, ui_progress)


def _QA_SU_save_index_or_etf_day(index__or_etf, client, ui_log, ui_progress):
    index_list = QA_fetch_get_stock_list(index__or_etf).code.tolist()
    coll = get_coll(client)
    ips = get_ip_list_by_multi_process_ping(stock_ip_list, _type='stock')[
          :cpu_count() * 2 + 1]
    ps = QA_SU_save_index_day_parallelism(
        processes=cpu_count() if len(ips) >= cpu_count() else len(ips),
        client=client, ui_log=ui_log)
    # 单线程测试
    # ps = QA_SU_save_index_day_parallelism(
    #   processes=1 if len(ips) >= cpu_count() else len(ips),
    #   client=client, ui_log=ui_log)
    ps.total_counts = len(index_list)
    ps.run(index_list)


def QA_SU_save_etf_day(client=DATABASE, ui_log=None, ui_progress=None):
    """save etf_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    index__or_etf = 'etf'
    _QA_SU_save_index_or_etf_day(index__or_etf, client, ui_log, ui_progress)



def QA_SU_save_stock_xdxr(client=DATABASE, ui_log=None, ui_progress=None):
    """[summary]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    stock_list = QA_fetch_get_stock_list().code.unique().tolist()
    # client.drop_collection('stock_xdxr')
    try:

        coll = client.stock_xdxr
        coll.create_index(
            [('code',
              pymongo.ASCENDING),
             ('date',
              pymongo.ASCENDING)],
            unique=True
        )
    except:
        client.drop_collection('stock_xdxr')
        coll = client.stock_xdxr
        coll.create_index(
            [('code',
              pymongo.ASCENDING),
             ('date',
              pymongo.ASCENDING)],
            unique=True
        )
    err = []

    def __saving_work(code, coll):
        QA_util_log_info(
            '##JOB02 Now Saving XDXR INFO ==== {}'.format(str(code)),
            ui_log=ui_log
        )
        try:
            coll.insert_many(
                QA_util_to_json_from_pandas(QA_fetch_get_stock_xdxr(str(code))),
                ordered=False
            )

        except:

            err.append(str(code))

    for i_ in range(len(stock_list)):
        QA_util_log_info(
            'The {} of Total {}'.format(i_,
                                        len(stock_list)),
            ui_log=ui_log
        )
        strLogInfo = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(stock_list) * 100))[0:4] + '%'
        )
        intLogProgress = int(float(i_ / len(stock_list) * 100))
        QA_util_log_info(
            strLogInfo,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intLogProgress
        )
        __saving_work(stock_list[i_], coll)
