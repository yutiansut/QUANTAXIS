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

from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_future_day,
                                       QA_fetch_future_min,
                                       QA_fetch_future_tick,
                                       QA_fetch_index_day, QA_fetch_index_min,
                                       QA_fetch_stock_day, QA_fetch_stock_min)
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_sql_mongo_setting,
                              QA_util_to_json_from_pandas)

from .QAMarket_engine import (market_future_engine, market_stock_day_engine,
                              market_stock_engine)


class QA_Market():
    '在这里加载数据'
    # client=QA_Setting.client
    # client=QA.QA_util_sql_mongo_setting()
    # db= client.market

    def __init__(self, commission_fee_coeff=0.0015):
        self.engine = {'stock_day': QA_fetch_stock_day, 'stock_min': QA_fetch_stock_min,
                       'future_day': QA_fetch_future_day, 'future_min': QA_fetch_future_min, 'future_tick': QA_fetch_future_tick}
        self.commission_fee_coeff = commission_fee_coeff

    def _choice_trading_market(self, __bid, __data=None):
        assert isinstance(__bid.type, str)
        if __bid.type == '0x01':
            __data = self.__get_stock_day_data(
                __bid) if __data is None else __data
            return market_stock_day_engine(__bid, __data, self.commission_fee_coeff)
        elif __bid.type == '0x02':
            # 获取股票引擎
            __data = self.__get_stock_min_data(
                __bid) if __data is None else __data
            return market_stock_engine(__bid, __data, self.commission_fee_coeff)

        elif __bid.type == '0x03':
                # 获取股票引擎
            __data = self.__get_index_day_data(
                __bid) if __data is None else __data
            return market_stock_engine(__bid, __data, self.commission_fee_coeff)
        elif __bid.type == '0x04':
                # 获取股票引擎
            __data = self.__get_index_min_data(
                __bid) if __data is None else __data
            return market_stock_engine(__bid, __data, self.commission_fee_coeff)
        elif __bid.type == '1x01':
            return market_future_engine(__bid, __data)
        elif __bid.type == '1x02':
            return market_future_engine(__bid, __data)
        elif __bid.type == '1x03':
            return market_future_engine(__bid, __data)

    def __get_stock_min_data(self, __bid):
        __data = QA_util_to_json_from_pandas(QA_fetch_stock_min(str(
            __bid.code)[0:6], str(__bid.datetime)[0:19], str(__bid.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def __get_stock_day_data(self, __bid):
        __data = QA_util_to_json_from_pandas(QA_fetch_stock_day(str(
            __bid.code)[0:6], str(__bid.datetime)[0:10], str(__bid.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def __get_index_day_data(self, __bid):
        __data = QA_util_to_json_from_pandas(QA_fetch_index_day(str(
            __bid.code)[0:6], str(__bid.datetime)[0:10], str(__bid.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def __get_index_min_data(self, __bid):
        __data = QA_util_to_json_from_pandas(QA_fetch_index_min(str(
            __bid.code)[0:6], str(__bid.datetime)[0:10], str(__bid.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def receive_bid(self, __bid, __data=None):
        """
        get the bid and choice which market to trade

        """
        def __confirm_bid(__bid):
            if isinstance(__bid.price, str):
                if __bid.price == 'market_price':
                    return __bid
                elif __bid.price == 'close_price':
                    return __bid
                elif __bid.price == 'strict' or 'strict_model' or 'strict_price':
                    __bid.price = 'strict_price'
                    return __bid
                else:
                    QA_util_log_info('unsupport type:' + __bid.price)
                    return __bid
            else:
                return __bid
        return self._choice_trading_market(__confirm_bid(__bid), __data)

    def trading_engine(self):
        pass
