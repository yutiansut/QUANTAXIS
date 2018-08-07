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
import sched
import pandas as pd
import threading

from QUANTAXIS.QAEngine.QAEvent import QA_Event, QA_Worker
from QUANTAXIS.QAEngine.QATask import QA_Task
from QUANTAXIS.QAMarket.QAOrder import QA_OrderQueue
from QUANTAXIS.QAUtil.QAParameter import (BROKER_EVENT, BROKER_TYPE,
                                          EVENT_TYPE, MARKET_EVENT,
                                          ORDER_EVENT)
from QUANTAXIS.QAUtil.QADate_trade import QA_util_if_tradetime


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
        self.deal_status = pd.DataFrame()
        self.if_start_orderquery = False

    def run(self, event):
        if event.event_type is BROKER_EVENT.RECEIVE_ORDER:
            # 此时的message应该是订单类
            """
            OrderHandler 收到订单

            orderhandler 调控转发给broker

            broker返回发单结果(成功/失败)

            orderhandler.order_queue 插入一个订单

            执行回调

            """

            order = event.order
            print(event.broker)
            order = event.broker.receive_order(
                QA_Event(event_type=BROKER_EVENT.TRADE, order=event.order))
            print(threading.current_thread().ident)
            order = self.order_queue.insert_order(order)
            if event.callback:
                event.callback(order)

        elif event.event_type is BROKER_EVENT.TRADE:
            # 实盘和本地 同步执行
            res = []
            for order in self.order_queue.pending:
                result = event.broker.query_orders(
                    order.account_cookie, order.realorder_id)
                self.order_queue.set_status(
                    order.order_id, result['header']['status'])
                if order.callback:
                    order.callback(result)
                res.append(result)
            event.res = res

            return event

        elif event.event_type is BROKER_EVENT.SETTLE:
            self.order_queue.settle()

        elif event.event_type is MARKET_EVENT.QUERY_ORDER:
            """query_order和query_deal 需要联动使用 

            query_order 得到所有的订单列表

            query_deal 判断订单状态--> 运行callback函数


            实盘涉及到外部订单问题: 
            及 订单的来源 不完全从QUANTAXIS中发出, 则QA无法记录来源 (标记为外部订单)
            """

            if self.if_start_orderquery:
                if QA_util_if_tradetime:

                    # print(event.broker)
                    # print(event.account_cookie)
                    try:
                        # 做一些容错处理
                        res = [event.broker[i].query_orders(
                            event.account_cookie[i], '') for i in range(len(event.account_cookie))]
                        res = pd.concat(res, axis=0) if len(
                            res) > 0 else None

                    except:
                        time.sleep(1)

                    self.order_status = res if res is not None else self.order_status
                else:
                    time.sleep(1)

            # 这里加入随机的睡眠时间 以免被发现固定的刷新请求
            # event=event
            event.event_type = MARKET_EVENT.QUERY_DEAL
            if event.callback.qsize()<1:
                time.sleep(random.randint(1, 2))


            # 非阻塞    
            event.callback.put(
                QA_Task(
                    worker=self,
                    engine='ORDER',
                    event=event
                )
            )
            # time.sleep(random.randint(2,5))
            # print(event.event_type)
            # print(event2.event_type)
            # self.run(event)

            # print(self.order_status)
            #print('UPDATE ORDERS')

        elif event.event_type is MARKET_EVENT.QUERY_DEAL:

            """order_handler- query_deal

            将order_handler订单队列中的订单---和deal中匹配起来


            """

            # if len(self.order_queue.pending) > 0:
            #     for order in self.order_queue.pending:
            #         #self.query
            #         waiting_realorder_id = [
            #             order.realorder_id for order in self.order_queue.trade_list]
            #         result = event.broker.query_deal
            #         time.sleep(1)
            if self.if_start_orderquery:

                # print(event.broker)
                # print(event.account_cookie)
                self.deal_status = [event.broker[i].query_orders(
                    event.account_cookie[i], 'filled') for i in range(len(event.account_cookie))]
                # print(self.order_status)
                self.deal_status = pd.concat(self.deal_status, axis=0) if len(
                    self.deal_status) > 0 else pd.DataFrame()
                # print(self.order_status)

            

            # 这里加入随机的睡眠时间 以免被发现固定的刷新请求
            if event.callback.qsize()<1:
                time.sleep(random.randint(2, 5))
            event.event_type = MARKET_EVENT.QUERY_ORDER


            event.callback.put(
                QA_Task(
                    worker=self,
                    engine='ORDER',
                    event=event
                )
            )
            #self.run(event)
            # self.run(event)

        elif event.event_type is MARKET_EVENT.QUERY_POSITION:
            pass

    def query_order(self, order_id):
        pass
