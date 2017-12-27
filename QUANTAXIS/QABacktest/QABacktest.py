# coding=utf-8
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


import configparser
import csv
import datetime
import json
import os
import queue
import random
import re
import sys
import threading
import time
from functools import lru_cache, reduce, update_wrapper, wraps
from statistics import mean
from threading import Thread, Timer

import apscheduler
import numpy as np
import pandas as pd
import pymongo
from tabulate import tabulate

from QUANTAXIS import (QA_Portfolio, QA_Risk, __version__)
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QABacktest.backtest_setting import backtest_setting
from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_backtest
from QUANTAXIS.QAData import QA_DataStruct_Stock_day, QA_DataStruct_Stock_min
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_index_day, QA_fetch_index_min,
                                       QA_fetch_stock_day, QA_fetch_stock_info,
                                       QA_fetch_stocklist_day,
                                       QA_fetch_trade_date)
from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_index_day_adv,
                                               QA_fetch_index_min_adv,
                                               QA_fetch_stock_block_adv,
                                               QA_fetch_stock_day_adv,
                                               QA_fetch_stock_min_adv,
                                               QA_fetch_stocklist_day_adv,
                                               QA_fetch_stocklist_min_adv)
from QUANTAXIS.QAMarket.QAOrder import QA_OrderQueue, QA_Order
from QUANTAXIS.QAMarket.QAMarket import QA_Market
from QUANTAXIS.QASU.save_backtest import (QA_SU_save_account_message,
                                          QA_SU_save_account_to_csv,
                                          QA_SU_save_backtest_message,
                                          QA_SU_save_pnl_to_csv)
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_date_gap,
                              QA_util_get_real_date, QA_util_log_expection,
                              QA_util_log_info, QA_util_make_min_index,
                              QA_util_random_with_topic, QA_util_time_gap,
                              QA_util_to_json_from_pandas, trade_date_sse)


"""


"""


class QA_Backtest():

    def __init__(self):
        pass
 