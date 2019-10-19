# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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

import numpy as np
import pandas as pd

from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAFetch.QAQuery import (
    QA_fetch_future_day,
    QA_fetch_future_min,
    QA_fetch_index_day,
    QA_fetch_index_min,
    QA_fetch_stock_day,
    QA_fetch_stock_min
)
from QUANTAXIS.QAFetch.QATdx import (
    QA_fetch_get_future_day,
    QA_fetch_get_future_min,
    QA_fetch_get_index_day,
    QA_fetch_get_index_min,
    QA_fetch_get_stock_day,
    QA_fetch_get_stock_min
)
from QUANTAXIS.QAMarket.QABroker import QA_Broker
from QUANTAXIS.QAMarket.QADealer import QA_Dealer
from QUANTAXIS.QAMarket.QAOrderHandler import QA_OrderHandler
from QUANTAXIS.QAUtil.QADate import QA_util_to_datetime
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_next_day
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import (
    AMOUNT_MODEL,
    BROKER_EVENT,
    ORDER_STATUS,
    BROKER_TYPE,
    ENGINE_EVENT,
    FREQUENCE,
    MARKET_EVENT,
    MARKET_TYPE,
    ORDER_DIRECTION,
    ORDER_MODEL
)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas


class QA_BacktestBroker(QA_Broker):
    """
    QUANTAXIS Broker 部分

    回测
    股票/指数/期货/债券/ETF/基金
    @yutiansut


    对于不同的市场规则:
    股票市场 t+1
    期货/期权/加密货币市场 t+0

    股票/加密货币市场不允许卖空
    期货/期权市场允许卖空

    t+1的市场是
    当日的买入 更新持仓- 不更新可卖数量- 资金冻结
    当日的卖出 及时更新可用资金

    t+0市场是:
    当日买入 即时更新持仓和可卖
    当日卖出 即时更新

    卖空的规则是
    允许无仓位的时候卖出证券(按市值和保证金比例限制算)
    """

    def __init__(self, if_nondatabase=False):
        """[summary]


        Keyword Arguments:
            commission_fee_coeff {[type]} -- [description] (default: {0})
            environment {[type]} -- [description] (default: {RUNNING_ENVIRONMENT})
            if_nondatabase {[type]} -- [description] (default: {False})
        """
        super().__init__()
        self.dealer = QA_Dealer()
        self.order_handler = QA_OrderHandler()

        self.fetcher = {
            (MARKET_TYPE.STOCK_CN,
             FREQUENCE.DAY): QA_fetch_stock_day,
            (MARKET_TYPE.STOCK_CN,
             FREQUENCE.FIFTEEN_MIN): QA_fetch_stock_min,
            (MARKET_TYPE.STOCK_CN,
             FREQUENCE.ONE_MIN): QA_fetch_stock_min,
            (MARKET_TYPE.STOCK_CN,
             FREQUENCE.FIVE_MIN): QA_fetch_stock_min,
            (MARKET_TYPE.STOCK_CN,
             FREQUENCE.THIRTY_MIN): QA_fetch_stock_min,
            (MARKET_TYPE.STOCK_CN,
             FREQUENCE.SIXTY_MIN): QA_fetch_stock_min,
            (MARKET_TYPE.FUTURE_CN,
             FREQUENCE.DAY): QA_fetch_future_day,
            (MARKET_TYPE.FUTURE_CN,
             FREQUENCE.FIFTEEN_MIN): QA_fetch_future_min,
            (MARKET_TYPE.FUTURE_CN,
             FREQUENCE.ONE_MIN): QA_fetch_future_min,
            (MARKET_TYPE.FUTURE_CN,
             FREQUENCE.FIVE_MIN): QA_fetch_future_min,
            (MARKET_TYPE.FUTURE_CN,
             FREQUENCE.THIRTY_MIN): QA_fetch_future_min,
            (MARKET_TYPE.FUTURE_CN,
             FREQUENCE.SIXTY_MIN): QA_fetch_future_min,
            (MARKET_TYPE.INDEX_CN,
             FREQUENCE.DAY): QA_fetch_index_day,
            (MARKET_TYPE.INDEX_CN,
             FREQUENCE.FIFTEEN_MIN): QA_fetch_index_min,
            (MARKET_TYPE.INDEX_CN,
             FREQUENCE.ONE_MIN): QA_fetch_index_min,
            (MARKET_TYPE.INDEX_CN,
             FREQUENCE.FIVE_MIN): QA_fetch_index_min,
            (MARKET_TYPE.INDEX_CN,
             FREQUENCE.THIRTY_MIN): QA_fetch_index_min,
            (MARKET_TYPE.INDEX_CN,
             FREQUENCE.SIXTY_MIN): QA_fetch_index_min,
            (MARKET_TYPE.FUND_CN,
             FREQUENCE.DAY): QA_fetch_index_day,
            (MARKET_TYPE.FUND_CN,
             FREQUENCE.FIFTEEN_MIN): QA_fetch_index_min,
            (MARKET_TYPE.FUND_CN,
             FREQUENCE.ONE_MIN): QA_fetch_index_min,
            (MARKET_TYPE.FUND_CN,
             FREQUENCE.FIVE_MIN): QA_fetch_index_min,
            (MARKET_TYPE.FUND_CN,
             FREQUENCE.THIRTY_MIN): QA_fetch_index_min,
            (MARKET_TYPE.FUND_CN,
             FREQUENCE.SIXTY_MIN): QA_fetch_index_min
        }

        self.market_data = None
        self.if_nondatabase = if_nondatabase
        self.name = BROKER_TYPE.BACKETEST
        self._quotation = {} # 一个可以缓存数据的dict
        self.broker_data = None
        self.deal_message = {}

    def run(self, event):
        print(
            ">>>>-----------------------QABacktestBroker.run----------------------------->",
            event.event_type
        )

        if event.event_type is MARKET_EVENT.QUERY_DATA:
            # 查询数据部分
            code = event.code
            frequence = event.frequence
            start = event.start
            end = start if event.end is None else event.end
            market_type = event.market_type
            res = self.query_data(code, start, end, frequence, market_type)
            if event.callback:
                event.callback(res)
            else:
                return res
        elif event.event_type is MARKET_EVENT.QUERY_ORDER:
            self.order_handler.run(event)
        elif event.event_type is ENGINE_EVENT.UPCOMING_DATA:
            # QABacktest 回测发出的事件

            new_marketdata_dict = event.market_data.dicts
            for item in new_marketdata_dict.keys():
                if item not in self._quotation.keys():
                    self._quotation[item] = new_marketdata_dict[item]

        elif event.event_type is BROKER_EVENT.RECEIVE_ORDER:
            self.order_handler.run(event)
            #self.run(QA_Event(event_type=BROKER_EVENT.TRADE, broker=self))
        elif event.event_type is BROKER_EVENT.TRADE:
            event = self.order_handler.run(event)
            event.message = 'trade'
            if event.callback:
                event.callback(event)
        elif event.event_type is BROKER_EVENT.SETTLE:
            self.dealer.settle() ## 清空交易队列
            if event.callback:
                event.callback('settle')

    def query_data(self, code, start, end, frequence, market_type=None):
        """
        标准格式是numpy
        """
        try:
            return self.broker_data.select_time(start,
                                                end).select_code(code
                                                                ).to_json()[0]

        except:
            return self.fetcher[(market_type,
                                 frequence)](
                                     code,
                                     start,
                                     end,
                                     frequence=frequence,
                                     format='json'
                                 )

    def receive_order(self, event):
        """
        get the order and choice which market to trade

        """
        order = event.order
        if 'market_data' in event.__dict__.keys():

            self.market_data = self.get_market(
                order
            ) if event.market_data is None else event.market_data

            if isinstance(self.market_data, dict):
                pass
            elif isinstance(self.market_data, pd.DataFrame):
                self.market_data = QA_util_to_json_from_pandas(
                    self.market_data
                )[0]
            elif isinstance(self.market_data, pd.core.series.Series):
                self.market_data = self.market_data.to_dict()
            elif isinstance(self.market_data, np.ndarray):
                data = self.market_data[0]

            else:
                # print(type(self.market_data))
                self.market_data = self.market_data.to_json()[0]
        else:
            self.market_data = self.get_market(order)
        if self.market_data is not None:

            order = self.warp(order)

            self.dealer.deal(order, self.market_data)
            order.queued(order.order_id) # 模拟的order_id 和 realorder_id 一致

        else:

            order.failed('MARKET DATA IS NONE')
        return order

    def query_order(self, order_id):
        return self.dealer.deal_message[order_id]

    def query_orders(self, account, status=''):

        if status == '':
            return self.dealer.deal_df.query(
                'account_cookie=="{}"'.format(account)
            ).loc[:,
                  self.orderstatus_headers].set_index(
                      ['account_cookie',
                       'realorder_id']
                  )
        elif status == 'filled':
            return self.dealer.deal_df.query(
                'account_cookie=="{}"'.format(account)
            ).loc[:,
                  self.dealstatus_headers].set_index(
                      ['account_cookie',
                       'realorder_id']
                  )
        elif status == 'open':
            pass

    def query_deal(self, account):
        pass

    def warp(self, order):
        """对order/market的封装

        [description]

        Arguments:
            order {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        # 因为成交模式对时间的封装
        if order.order_model == ORDER_MODEL.MARKET:
            """
            市价单模式
            """
            if order.frequence is FREQUENCE.DAY:

                order.date = order.datetime[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN,
                                     FREQUENCE.FIVE_MIN,
                                     FREQUENCE.FIFTEEN_MIN,
                                     FREQUENCE.THIRTY_MIN,
                                     FREQUENCE.SIXTY_MIN]:

                order.date = str(order.datetime)[0:10]
            #_original_marketvalue = order.price*order.amount

            order.price = (
                float(self.market_data.get('high')) +
                float(self.market_data.get('low'))
            ) * 0.5

        elif order.order_model == ORDER_MODEL.NEXT_OPEN:
            raise NotImplementedError
        elif order.order_model == ORDER_MODEL.CLOSE:
            """
            收盘价模式
            """
                    
            if order.frequence is FREQUENCE.DAY:
                order.date = order.datetime[0:10]
                order.datetime = '{} 15:00:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN,
                                     FREQUENCE.FIVE_MIN,
                                     FREQUENCE.FIFTEEN_MIN,
                                     FREQUENCE.THIRTY_MIN,
                                     FREQUENCE.SIXTY_MIN]:

                order.date = str(order.datetime)[0:10]                    

            order.price = float(self.market_data.get('close'))

        elif order.order_model == ORDER_MODEL.LIMIT:
            """
            限价单模式
            """
            if order.frequence is FREQUENCE.DAY:
                # exact_time = str(datetime.datetime.strptime(
                #     str(order.datetime), '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))

                order.date = order.datetime[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN,
                                     FREQUENCE.FIVE_MIN,
                                     FREQUENCE.FIFTEEN_MIN,
                                     FREQUENCE.THIRTY_MIN,
                                     FREQUENCE.SIXTY_MIN]:

                order.date = str(order.datetime)[0:10]
        elif order.order_model == ORDER_MODEL.STRICT:
            """
            严格模式
            """
            if order.frequence is FREQUENCE.DAY:
                # exact_time = str(datetime.datetime.strptime(
                #     str(order.datetime), '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))

                order.date = order.datetime[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN,
                                     FREQUENCE.FIVE_MIN,
                                     FREQUENCE.FIFTEEN_MIN,
                                     FREQUENCE.THIRTY_MIN,
                                     FREQUENCE.SIXTY_MIN]:

                order.date = str(order.datetime)[0:10]

            if order.towards == 1:
                order.price = float(self.market_data.get('high'))
            else:
                order.price = float(self.market_data.get('low'))

        if order.market_type == MARKET_TYPE.STOCK_CN:
            if order.towards == ORDER_DIRECTION.BUY:
                if order.order_model == AMOUNT_MODEL.BY_MONEY:
                    amount = order.money / \
                        (order.price*(1+order.commission_coeff))
                    money = order.money
                else:

                    amount = order.amount
                    money = order.amount * order.price * \
                        (1+order.commission_coeff)

                order.amount = int(amount / 100) * 100
                order.money = money
            elif order.towards == ORDER_DIRECTION.SELL:
                if order.order_model == AMOUNT_MODEL.BY_MONEY:
                    amount = order.money / \
                        (order.price*(1+order.commission_coeff+order.tax_coeff))
                    money = order.money
                else:

                    amount = order.amount
                    money = order.amount * order.price * \
                        (1+order.commission_coeff+order.tax_coeff)

                order.amount = amount
                order.money = money
        return order

    def get_market(self, order):
        """get_market func

        [description]

        Arguments:
            order {orders} -- [description]

        Returns:
            [type] -- [description]
        """

        # 首先判断是否在_quotation里面
        if (pd.Timestamp(order.datetime), order.code) in self._quotation.keys():
            return self._quotation[(pd.Timestamp(order.datetime), order.code)]

        else:
            try:
                data = self.fetcher[(order.market_type,
                                     order.frequence)](
                                         code=order.code,
                                         start=order.datetime,
                                         end=order.datetime,
                                         format='json',
                                         frequence=order.frequence
                                     )[0]
                if 'vol' in data.keys() and 'volume' not in data.keys():
                    data['volume'] = data['vol']
                elif 'vol' not in data.keys() and 'volume' in data.keys():
                    data['vol'] = data['volume']
                return data
            except Exception as e:
                QA_util_log_info('MARKET_ENGING ERROR: {}'.format(e))
                return None
