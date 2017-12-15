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


from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_future_day,
                                       QA_fetch_future_min,
                                       QA_fetch_future_tick,
                                       QA_fetch_index_day, QA_fetch_index_min,
                                       QA_fetch_stock_day, QA_fetch_stock_min)
from QUANTAXIS.QAMarket.QAMarket_engine import (market_future_engine,
                                                market_stock_day_engine,
                                                market_stock_engine)
from QUANTAXIS.QAUtil import (QA_util_log_info,
                              QA_util_to_json_from_pandas)


class QA_Market():
    """
    QUANTAXIS MARKET 部分

    回测/模拟盘
    股票/指数/期货/债券/ETF
    @yutiansut

    """

    def __init__(self, commission_fee_coeff=0.0015):
        self.engine = {'stock_day': QA_fetch_stock_day, 'stock_min': QA_fetch_stock_min,
                       'future_day': QA_fetch_future_day, 'future_min': QA_fetch_future_min, 'future_tick': QA_fetch_future_tick}
        self.commission_fee_coeff = commission_fee_coeff

    def __repr__(self):
        return '< QA_MARKET >'

    def _choice_trading_market(self, __order, __data=None):
        assert isinstance(__order.type, str)
        if __order.type == '0x01':
            __data = self.__get_stock_day_data(
                __order) if __data is None else __data
            return market_stock_day_engine(__order, __data, self.commission_fee_coeff)
        elif __order.type == '0x02':
            # 获取股票引擎
            __data = self.__get_stock_min_data(
                __order) if __data is None else __data

            return market_stock_engine(__order, __data, self.commission_fee_coeff)

        elif __order.type == '0x03':

            __data = self.__get_index_day_data(
                __order) if __data is None else __data
            return market_stock_engine(__order, __data, self.commission_fee_coeff)
        elif __order.type == '0x04':

            __data = self.__get_index_min_data(
                __order) if __data is None else __data
            return market_stock_engine(__order, __data, self.commission_fee_coeff)
        elif __order.type == '1x01':
            return market_future_engine(__order, __data)
        elif __order.type == '1x02':
            return market_future_engine(__order, __data)
        elif __order.type == '1x03':
            return market_future_engine(__order, __data)

    def __get_stock_min_data(self, __order):
        __data = QA_util_to_json_from_pandas(QA_fetch_stock_min(str(
            __order.code)[0:6], str(__order.datetime)[0:19], str(__order.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def __get_stock_day_data(self, __order):
        __data = QA_util_to_json_from_pandas(QA_fetch_stock_day(str(
            __order.code)[0:6], str(__order.datetime)[0:10], str(__order.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def __get_index_day_data(self, __order):
        __data = QA_util_to_json_from_pandas(QA_fetch_index_day(str(
            __order.code)[0:6], str(__order.datetime)[0:10], str(__order.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def __get_index_min_data(self, __order):
        __data = QA_util_to_json_from_pandas(QA_fetch_index_min(str(
            __order.code)[0:6], str(__order.datetime)[0:10], str(__order.datetime)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data

    def receive_order(self, __order, __data=None):
        """
        get the order and choice which market to trade

        """
        def __confirm_order(__order):
            if isinstance(__order.price, str):
                if __order.price == 'market_price':
                    return __order
                elif __order.price == 'close_price':
                    return __order
                elif __order.price == 'strict' or 'strict_model' or 'strict_price':
                    __order.price = 'strict_price'
                    return __order
                else:
                    QA_util_log_info('unsupport type:' + __order.price)
                    return __order
            else:
                return __order
        return self._choice_trading_market(__confirm_order(__order), __data)

    def trading_engine(self):
        pass
