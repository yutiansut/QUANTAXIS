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
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_depth_market_data,
                                     QA_fetch_get_future_day,
                                     QA_fetch_get_future_min,
                                     QA_fetch_get_future_transaction,
                                     QA_fetch_get_future_transaction_realtime,
                                     QA_fetch_get_index_day,
                                     QA_fetch_get_index_min,
                                     QA_fetch_get_stock_day,
                                     QA_fetch_get_stock_min)
from QUANTAXIS.QAMarket.QAMarket_engine import (market_future_engine,
                                                market_stock_engine)
from QUANTAXIS.QAUtil import QA_util_log_info, QA_util_to_json_from_pandas


class QA_Market():
    """
    QUANTAXIS MARKET 部分

    回测/模拟盘
    股票/指数/期货/债券/ETF
    @yutiansut

    """

    def __init__(self, commission_fee_coeff=0.0015):
        self.fetcher = {'0x01': QA_fetch_stock_day, '0x02': QA_fetch_stock_min,
                        '1x01': QA_fetch_index_day, '1x02': QA_fetch_index_min,
                        '2x01': QA_fetch_future_day, '2x02': QA_fetch_future_min, '2x03': QA_fetch_future_tick}
        self.engine = {'0x01': market_stock_engine, '0x02': market_stock_engine,
                       '1x01': market_stock_engine, '1x02': market_stock_engine,
                       '2x01': market_future_engine, '2x02': market_future_engine, '2x03': market_future_engine}
        self.commission_fee_coeff = commission_fee_coeff
        self.market_data = None

    def __repr__(self):
        return '< QA_MARKET >'

    def receive_order(self, order, market_data=None):
        """
        get the order and choice which market to trade

        """
        assert isinstance(order.type, str)

        self.market_data = self.warp_market(
            order) if market_data is None else market_data
        order = self.warp_order(order)

        return self.engine[order.type](order, self.market_data, self.commission_fee_coeff)

    def warp_market(self, order):
        try:
            return self.fetcher[order.type](code=order.code, start=order.datetime, end=order.datetime, format='json')[0]
        except:
            pass

    def warp_order(self, order):
        """对order的封装

        [description]

        Arguments:
            order {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        if order.order_model == 'market' and order.price is None:
            order.price = (float(self.market_data["high"]) +
                           float(self.market_data["low"])) * 0.5

        elif order.order_model == 'close' and order.price is None:

            order.price = float(self.market_data["close"])

        elif order.order_model == 'strict' and order.price is None:
            '加入严格模式'

            if order.towards == 1:

                order.price = float(self.market_data["high"])
            else:
                order.price = float(self.market_data["low"])

        # 对于股票 有最小交易100股限制
        order.amount = int(order.amount / (order.price * 100)) * \
            100 if order.type in ['0x01', '0x02', '0x03'] else order.amount

        return order
