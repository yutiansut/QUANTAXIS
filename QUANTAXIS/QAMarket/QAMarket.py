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


import datetime

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
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, RUNNING_ENVIRONMENT


class QA_Market():
    """
    QUANTAXIS MARKET 部分

    回测/模拟盘
    股票/指数/期货/债券/ETF
    @yutiansut

    """

    def __init__(self, commission_fee_coeff=0.0015, environment=RUNNING_ENVIRONMENT.BACKETEST, if_nondatabase=False):
        """[summary]

        [description]

        Keyword Arguments:
            commission_fee_coeff {[type]} -- [description] (default: {0})
            environment {[type]} -- [description] (default: {RUNNING_ENVIRONMENT})
            if_nondatabase {[type]} -- [description] (default: {False})
        """
        self.engine = {'0x01': market_stock_engine, '0x02': market_stock_engine,
                       '1x01': market_stock_engine, '1x02': market_stock_engine,
                       '2x01': market_future_engine, '2x02': market_future_engine, '2x03': market_future_engine}
        self.fetcher = {'0x01': QA_fetch_stock_day, '0x02': QA_fetch_stock_min,
                        '1x01': QA_fetch_index_day, '1x02': QA_fetch_index_min,
                        '2x01': QA_fetch_future_day, '2x02': QA_fetch_future_min, '2x03': QA_fetch_future_tick}
        self.nondatabase_fetcher = {'0x01': QA_fetch_get_stock_day, '0x02': QA_fetch_get_stock_min,
                                    '1x01': QA_fetch_get_index_day, '1x02': QA_fetch_get_index_min,
                                    '2x01': QA_fetch_get_future_day, '2x02': QA_fetch_get_future_min}
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
        order = self.warp(order)

        return self.engine[order.type](order, self.market_data, self.commission_fee_coeff)

    def warp(self, order):
        """对order/market的封装

        [description]

        Arguments:
            order {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        # 因为成交模式对时间的封装

        if order.order_model == 'market' and order.price is None:

            if order.type[-2:] == '01':
                exact_time = str(datetime.datetime.strptime(
                    order.datetime, '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))

                order.date = exact_time[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.type[-2:] == '02':
                exact_time = str(datetime.datetime.strptime(
                    order.datetime, '%Y-%m-%d %H-%M-%S') + datetime.timedelta(minute=1))
                order.date = exact_time[0:10]
                order.datetime = exact_time
            self.market_data = self.warp_market(order)
            if self.market_data is None:
                return order
            order.price = (float(self.market_data["high"]) +
                           float(self.market_data["low"])) * 0.5

        elif order.order_model == 'close' and order.price is None:
            try:
                order.datetime = self.market_data.datetime
            except:
                order.datetime = '{} 15:00:00'.format(order.date)
            self.market_data = self.warp_market(order)
            if self.market_data is None:
                return order
            order.price = float(self.market_data["close"])

        elif order.order_model == 'strict' and order.price is None:
            '加入严格模式'
            if order.type[-2:] == '01':
                exact_time = str(datetime.datetime.strptime(
                    order.datetime, '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))

                order.date = exact_time[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.type[-2:] == '02':
                exact_time = str(datetime.datetime.strptime(
                    order.datetime, '%Y-%m-%d %H-%M-%S') + datetime.timedelta(minute=1))
                order.date = exact_time[0:10]
                order.datetime = exact_time
            self.market_data = self.warp_market(order)
            if self.market_data is None:
                return order
            if order.towards == 1:
                order.price = float(self.market_data["high"])
            else:
                order.price = float(self.market_data["low"])

        # 对于股票 有最小交易100股限制
        order.amount = int(order.amount / (order.price * 100)) * \
            100 if order.type in ['0x01', '0x02', '0x03'] else order.amount

        return order

    def warp_market(self, order):
        try:
            data = self.fetcher[order.type](
                code=order.code, start=order.datetime, end=order.datetime, format='json')[0]
            if 'vol' in data.keys() and 'volume' not in data.keys():
                data['vol'] = data['volume']
            elif 'vol' in data.keys() and 'volume' not in data.keys():
                data['volume'] = data['vol']
            
            else:
                pass
            print(data)
            return data
        except Exception as e:
            QA_util_log_info('MARKET_ENGING ERROR: {}'.format(e))
            return None
