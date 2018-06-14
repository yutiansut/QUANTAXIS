# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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


"""
需要一个可以被修改和继承的基类

2017/8/12

"""
import datetime
from abc import abstractmethod

from QUANTAXIS.QAEngine.QAEvent import QA_Event, QA_Worker
from QUANTAXIS.QAUtil.QAParameter import EVENT_TYPE, FREQUENCE, ORDER_MODEL


class QA_Broker(QA_Worker):
    """MARKET ENGINGE ABSTRACT

    receive_order => warp => get_data => engine
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.type = EVENT_TYPE.BROKER_EVENT
        self.name = None

    def __repr__(self):
        return '< QA_Broker >'

    @abstractmethod
    def receive_order(self, event):
        '''
        QA_Broker 是一个抽象类，必须实现这个方法
        :param event:
        :return:
        '''
        raise NotImplementedError

    def get_market(self, order):
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

            if order.frequence is FREQUENCE.DAY:
                # exact_time = str(datetime.datetime.strptime(
                #     str(order.datetime), '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))

                order.date = order.datetime[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN, FREQUENCE.FIVE_MIN, FREQUENCE.FIFTEEN_MIN, FREQUENCE.THIRTY_MIN, FREQUENCE.SIXTY_MIN]:
                print(order.datetime)
                exact_time = str(datetime.datetime.strptime(
                    str(order.datetime), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=1))
                order.date = exact_time[0:10]
                order.datetime = exact_time
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            order.price = (float(self.market_data["high"]) +
                           float(self.market_data["low"])) * 0.5
        elif order.order_model == ORDER_MODEL.NEXT_OPEN:
            try:
                exact_time = str(datetime.datetime.strptime(
                    str(order.datetime), '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))
                order.date = exact_time[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            except:
                order.datetime = '{} 15:00:00'.format(order.date)
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            order.price = float(self.market_data["close"])
        elif order.order_model == ORDER_MODEL.CLOSE:

            try:
                order.datetime = self.market_data.datetime
            except:
                if len(str(order.datetime)) == 19:
                    pass
                else:
                    order.datetime = '{} 15:00:00'.format(order.date)
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            order.price = float(self.market_data["close"])

        elif order.order_model == ORDER_MODEL.STRICT:
            '加入严格模式'
            if order.frequence is FREQUENCE.DAY:
                exact_time = str(datetime.datetime.strptime(
                    order.datetime, '%Y-%m-%d %H-%M-%S') + datetime.timedelta(day=1))

                order.date = exact_time[0:10]
                order.datetime = '{} 09:30:00'.format(order.date)
            elif order.frequence in [FREQUENCE.ONE_MIN, FREQUENCE.FIVE_MIN, FREQUENCE.FIFTEEN_MIN, FREQUENCE.THIRTY_MIN, FREQUENCE.SIXTY_MIN]:
                exact_time = str(datetime.datetime.strptime(
                    order.datetime, '%Y-%m-%d %H-%M-%S') + datetime.timedelta(minute=1))
                order.date = exact_time[0:10]
                order.datetime = exact_time
            self.market_data = self.get_market(order)
            if self.market_data is None:
                return order
            if order.towards == 1:
                order.price = float(self.market_data["high"])
            else:
                order.price = float(self.market_data["low"])

        return order


class QA_BROKER_EVENT(QA_Event):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.event_type = None
