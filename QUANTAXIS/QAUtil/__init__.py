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


from .QADate import(QA_util_date_stamp, QA_util_time_stamp, QA_util_ms_stamp, QA_util_date_valid,
                    QA_util_realtime, QA_util_id2date, QA_util_is_trade, QA_util_get_date_index,
                    QA_util_get_index_date, QA_util_get_real_date, QA_util_select_hours,
                    QA_util_select_min,QA_util_time_delay,QA_util_time_now)
from .QASql import (QA_util_sql_mongo_setting)
from .QALogs import (
    QA_util_log_debug, QA_util_log_expection, QA_util_log_info)
from .QACfg import (QA_util_cfg_initial, QA_util_get_cfg)
from .QASetting import QA_Setting
from .QAWeb import QA_util_web_ping
from .QADate_trade import trade_date_sse
def QA_start_initial(files):
    pass
