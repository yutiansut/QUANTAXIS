# coding:utf-8
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

import time
import random

import pandas as pd

from QUANTAXIS.QAEngine.QAEvent import QA_Event, QA_Worker
from QUANTAXIS.QAMarket.QAOrder import QA_OrderQueue
from QUANTAXIS.QAUtil.QAParameter import (BROKER_EVENT, BROKER_TYPE,
                                          EVENT_TYPE, MARKET_EVENT,
                                          ORDER_EVENT)


class QA_OrderHandler(QA_Worker):
    """ORDER执行器


    ORDEHANDLDER 归属于MARKET前置

    仅负责一个无状态的执行层

    ORDER执行器的作用是因为 
    在实盘中 当一个订单发送出去的时候,市场不会返回一个更新的订单类回来
    大部分时间都依赖子线程主动查询 或者是一个市场信息来进行判断

    ORDER_Handler的作用就是根据信息更新Order

    用于接受订单 发送给相应的marker_broker 再根据返回的信息 进行更新

    可用的market_broker:
    1.回测盘
    2.实时模拟盘
    3.实盘



    ORDERHANDLER 持久化问题:

    设定机制: 2秒查询1次
    持久化: 2秒一次

    2018-07-29



    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.order_queue = QA_OrderQueue()
        self.type = EVENT_TYPE.MARKET_EVENT

        self.event = QA_Event()
        self.order_status = pd.DataFrame()
        self.if_start_orderquery = False

    def run(self, event):
        if event.event_type is BROKER_EVENT.RECEIVE_ORDER:
            # 此时的message应该是订单类
            order = event.order
            order = event.broker.receive_order(
                QA_Event(event_type=BROKER_EVENT.TRADE, order=event.order))

            order = self.order_queue.insert_order(order)
            if event.callback:
                event.callback(order)

        elif event.event_type is BROKER_EVENT.TRADE:

            res = []
            for item in self.order_queue.trade_list:
                result = event.broker.query_orders(
                    item.account_cookie, item.realorder_id)
                self.order_queue.set_status(
                    item.order_id, result['header']['status'])
                if item.callback:
                    item.callback(result)
                res.append(result)
            event.res = res

            return event

        elif event.event_type is BROKER_EVENT.SETTLE:
            self.order_queue.settle()

        elif event.event_type is MARKET_EVENT.QUERY_ORDER:

            if self.if_start_orderquery:

                #print(event.broker)
                #print(event.account_cookie)
                self.order_status = [event.broker[i].query_orders(
                    event.account_cookie[i], '') for i in range(len(event.account_cookie))]
                #print(self.order_status)
                self.order_status = pd.concat(self.order_status, axis=0) if len(
                    self.order_status) > 0 else pd.DataFrame()
                #print(self.order_status)

            # 这里加入随机的睡眠时间 以免被发现固定的刷新请求
            time.sleep(random.randint(2,5))
            self.run(event)

            # print(self.order_status)
            #print('UPDATE ORDERS')

        elif event.event_type is BROKER_EVENT.QUERY_DEAL:
            while self.order_queue.len > 0:
                waiting_realorder_id = [
                    order.realorder_id for order in self.order_queue.trade_list]
                result = event.broker.query_deal
                time.sleep(1)

    def query_order(self, order_id):
        return self.order_queue.queue_df.query()
