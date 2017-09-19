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
""""
yutiansut
util tool
"""


# 日期相关
from .QADate import(QA_util_date_stamp, QA_util_time_stamp, QA_util_ms_stamp, QA_util_date_valid,
                    QA_util_realtime, QA_util_id2date, QA_util_is_trade, QA_util_get_date_index, 
                    QA_util_get_index_date, QA_util_select_hours, QA_util_date_int2str, QA_util_date_today,
                    QA_util_select_min, QA_util_time_delay, QA_util_time_now, QA_util_date_str2int)
# sql设置
from .QASql import (QA_util_sql_mongo_setting)
# log 文件相关
from .QALogs import (
    QA_util_log_debug, QA_util_log_expection, QA_util_log_info)
# config 文件相关
from .QACfg import (QA_util_cfg_initial, QA_util_get_cfg)
# QUANTAXIS设置相关
from .QASetting import QA_Setting
# 网络相关
from .QAWeb import QA_util_web_ping
# 交易日相关
from .QADate_trade import (trade_date_sse, QA_util_if_trade,QA_util_date_gap,
                           QA_util_get_real_datelist, QA_util_get_real_date,
                           QA_util_get_trade_range)
# csv 文件相关
from .QACsv import QA_util_save_csv
# list格式相关
from .QAList import QA_util_multi_demension_list, QA_util_diff_list
# 格式转换相关
from .QATransform import (QA_util_to_json_from_pandas,
                          QA_util_to_list_from_numpy, QA_util_to_list_from_pandas)
# MongoDB相关
from .QAMongo import (QA_util_mongo_initial, QA_util_mongo_make_index,
                      QA_util_mongo_status, QA_util_mongo_infos)
# bar 相关
from .QABar import (QA_util_make_min_index, QA_util_make_hour_index)
