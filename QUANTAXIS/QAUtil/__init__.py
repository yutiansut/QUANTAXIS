# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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
""""
yutiansut
util tool
"""
# path

# bar
from QUANTAXIS.QAUtil.QABar import (QA_util_make_hour_index,
                                    QA_util_make_min_index, QA_util_time_gap)
from QUANTAXIS.QAUtil.QACache import QA_util_cache
# config
from QUANTAXIS.QAUtil.QACfg import QA_util_cfg_initial, QA_util_get_cfg
# code function
from QUANTAXIS.QAUtil.QACode import QA_util_code_tolist, QA_util_code_tostr, QA_util_code_adjust_ctp
# csv
from QUANTAXIS.QAUtil.QACsv import QA_util_save_csv
# date
from QUANTAXIS.QAUtil.QADate import (QA_util_calc_time, QA_util_date_int2str,
                                     QA_util_date_stamp, QA_util_date_str2int,
                                     QA_util_date_today, QA_util_date_valid,
                                     QA_util_datetime_to_strdate,
                                     QA_util_stamp2datetime,
                                     QA_util_get_date_index,
                                     QA_util_tdxtimestamp,
                                     QA_util_get_index_date, QA_util_id2date,
                                     QA_util_is_trade, QA_util_ms_stamp,
                                     QA_util_realtime, QA_util_select_hours,
                                     QA_util_select_min, QA_util_time_delay,
                                     QA_util_time_now, QA_util_time_stamp,
                                     QA_util_to_datetime, QA_util_today_str,
                                     QATZInfo_CN)
# trade date
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_date_gap,
                                           QA_util_format_date2str,
                                           QA_util_future_to_realdatetime,
                                           QA_util_future_to_tradedatetime,
                                           QA_util_get_last_datetime,
                                           QA_util_get_last_day,
                                           QA_util_get_next_datetime,
                                           QA_util_get_next_day,
                                           QA_util_get_next_trade_date,
                                           QA_util_get_order_datetime,
                                           QA_util_get_pre_trade_date,
                                           QA_util_get_real_date,
                                           QA_util_get_real_datelist,
                                           QA_util_get_trade_datetime,
                                           QA_util_get_trade_gap,
                                           QA_util_get_trade_range,
                                           QA_util_if_trade,
                                           QA_util_if_tradetime,
                                           QA_util_get_next_day,
                                           QA_util_get_last_day,
                                           QA_util_get_last_datetime,
                                           QA_util_get_next_datetime,
                                           QA_util_get_order_datetime,
                                           QA_util_get_trade_datetime,
                                           QA_util_future_to_realdatetime,
                                           QA_util_future_to_tradedatetime,
                                           trade_date_sse,
                                           QA_util_get_next_period)
# datetolls
from QUANTAXIS.QAUtil.QADateTools import (QA_util_add_months,
                                          QA_util_get_1st_of_next_month,
                                          QA_util_getBetweenMonth,
                                          QA_util_getBetweenQuarter)
# dict function
from QUANTAXIS.QAUtil.QADict import QA_util_dict_remove_key
from QUANTAXIS.QAUtil.QAFile import QA_util_file_md5
# list function
from QUANTAXIS.QAUtil.QAList import (QA_util_diff_list,
                                     QA_util_multi_demension_list)

# code function
from QUANTAXIS.QAUtil.QACode import QA_util_code_tostr, QA_util_code_tolist
# dict function
from QUANTAXIS.QAUtil.QADict import QA_util_dict_remove_key
# log
from QUANTAXIS.QAUtil.QALogs import (QA_util_log_debug, QA_util_log_expection,
                                     QA_util_log_info)
# MongoDB
from QUANTAXIS.QAUtil.QAMongo import (QA_util_mongo_infos,
                                      QA_util_mongo_initial,
                                      QA_util_mongo_status)
# Parameter
from QUANTAXIS.QAUtil.QAParameter import (
    ACCOUNT_EVENT, AMOUNT_MODEL, BROKER_EVENT, BROKER_TYPE, DATASOURCE,
    ENGINE_EVENT, EVENT_TYPE, EXCHANGE_ID, FREQUENCE, MARKET_ERROR,
    MARKET_EVENT, MARKET_TYPE, ORDER_DIRECTION, ORDER_EVENT, ORDER_MODEL,
    TIME_CONDITION, VOLUME_CONDITION,
    ORDER_STATUS, OUTPUT_FORMAT, RUNNING_ENVIRONMENT, TRADE_STATUS, RUNNING_STATUS)
# RANDOM class
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QASetting import (DATABASE, QASETTING, QA_Setting,
                                        exclude_from_stock_ip_list,
                                        future_ip_list, info_ip_list,
                                        stock_ip_list)
from QUANTAXIS.QAUtil.QASingleton import singleton
# sql
from QUANTAXIS.QAUtil.QASql import (QA_util_sql_async_mongo_setting,
                                    QA_util_sql_mongo_setting,
                                    QA_util_sql_mongo_sort_ASCENDING,
                                    QA_util_sql_mongo_sort_DESCENDING)
# format
from QUANTAXIS.QAUtil.QATransform import (QA_util_to_json_from_pandas,
                                          QA_util_to_list_from_numpy,
                                          QA_util_to_list_from_pandas,
                                          QA_util_to_pandas_from_json,
                                          QA_util_to_pandas_from_list)

# 网络相关
from QUANTAXIS.QAUtil.QAWebutil import QA_util_web_ping
from QUANTAXIS.QAUtil.QAMail import QA_util_send_mail

# 文件相关

from QUANTAXIS.QAUtil.QAFile import QA_util_file_md5

# datetolls
from QUANTAXIS.QAUtil.QADateTools import (
    QA_util_getBetweenQuarter, QA_util_get_1st_of_next_month,
    QA_util_add_months, QA_util_getBetweenMonth
)

from QUANTAXIS.QAUtil.Parallelism import Parallelism, Parallelism_Thread
from QUANTAXIS.QAUtil.QACache import QA_util_cache
from QUANTAXIS.QAUtil.QASingleton import singleton

import platform
from functools import wraps
platform_flag = platform.system() == 'Windows'

if not platform_flag:
    from resource import getrusage as resource_usage, RUSAGE_SELF
    from time import time as timestamp

    def print_used_time(func):
        ''' 打印运行时间

        :param func: 运行的函数名称
        :return:
        '''

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time, start_resources = timestamp(), resource_usage(RUSAGE_SELF)
            func(*args, **kwargs)
            end_resources, end_time = resource_usage(RUSAGE_SELF), timestamp()
            print({'消耗时间': {'real': end_time - start_time,
                            'sys': end_resources.ru_stime - start_resources.ru_stime,
                            'user': end_resources.ru_utime - start_resources.ru_utime}})
            return True
        return wrapper
else:
    def print_used_time(func):
        ''' 打印运行时间

        :param func: 运行的函数名称
        :return:
        '''

        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            return True

        return wrapper
