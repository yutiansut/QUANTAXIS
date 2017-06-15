# coding :utf-8
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

#from .market_config import stock_market,future_market,HK_stock_market,US_stock_market
import datetime
import random

from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_sql_mongo_setting)

from .QAMarket_engine import market_future_day_engine,market_future_min_engine,market_future_tick_engine,market_stock_day_engine,market_stock_min_engine

class QA_Market():

    # client=QA_Setting.client
    # client=QA.QA_util_sql_mongo_setting()
    # db= client.market
    def __init__(self):
        self.message = {}

    def receive_bid(self):
        """
        get the bid and choice which market to trade

        """
        def __confirm_bid(self, __bid):
            assert type(__bid) == dict

            if type(__bid['price']) == str():
                pass
            elif type(__bid['price']) == float:
                pass

                
        @staticmethod
        def _choice_trading_market(__bid):
            pass
        


    def trading_engine(self):
        pass