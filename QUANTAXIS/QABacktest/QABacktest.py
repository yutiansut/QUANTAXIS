#coding=utf-8
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
import random
import re
import time

import pymongo
from tabulate import tabulate

from QUANTAXIS import QA_Market, QA_Portfolio, QA_QAMarket_bid, QA_Risk
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day
from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info


class QA_Backtest():
    
    account=QA_Account()
    market=QA_Market()
    bid=QA_QAMarket_bid()
    setting=QA_Setting()
    clients=setting.client
    user=setting.QA_setting_user_name
    def QA_backtest_init(self):
        pass

    def QA_backtest_start(self):
        QA_util_log_info('backtest start')


    def QA_backtest_day_start(self):
        pass

    def QA_backtest_handle(self):
        pass

    def QA_backtest_day_end(self):
        pass

    def QA_get_data(self):
        self.QA_get_data_from_market()
    
    def QA_get_data_from_market(self):
        db=self.clients.quantaxis
        

    def QA_strategy_update(self):
        pass



class QA_Backtest_simple(QA_Backtest):
    pass