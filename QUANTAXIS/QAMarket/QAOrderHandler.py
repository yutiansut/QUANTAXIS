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

import random
import sched
import threading
import time
import asyncio
import pandas as pd

from QUANTAXIS.QAEngine.QAEvent import QA_Event, QA_Worker
from QUANTAXIS.QAEngine.QATask import QA_Task
from QUANTAXIS.QAMarket.QAOrder import QA_OrderQueue
from QUANTAXIS.QASU.save_orderhandler import QA_SU_save_deal, QA_SU_save_order
from QUANTAXIS.QAUtil.QADate_trade import QA_util_if_tradetime
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


    # 重新设置ORDERHADLER的运行模式:

    -- 常规检查 5秒一次

    -- 如果出现订单 则2-3秒 对账户轮询(直到出现订单成交/撤单为止)



    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.order_queue = QA_OrderQueue()
        self.type = EVENT_TYPE.MARKET_EVENT

        self.event = QA_Event()
        self.order_status = pd.DataFrame()
        self.deal_status = pd.DataFrame()
        self.if_start_orderquery = False

        self.monitor = {}  # 1.1新增 用于监控订单

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
            order = event.broker.receive_order(
                QA_Event(event_type=BROKER_EVENT.TRADE, order=event.order, market_data=event.market_data))
            # print(threading.current_thread().ident)
            order = self.order_queue.insert_order(order)
            if event.callback:
                event.callback(order)

        elif event.event_type is BROKER_EVENT.TRADE:
            # 实盘和本地 同步执行
            self._trade()
            # event.event_queue.task_done()

        elif event.event_type is BROKER_EVENT.SETTLE:

            """订单队列的结算:


            当队列中的订单都被处理过后:
            算可以结算了
            """

            print('SETTLE ORDERHANDLER')

            # if len(self.order_queue.untrade) > 0:
            #     self.if_start_orderquery = False
            #     event.event_type = BROKER_EVENT.TRADE
            #     event.event_queue.put(
            #         QA_Task(
            #             worker=self,
            #             engine='ORDER',
            #             event=event
            #         )
            #     )

            if len(self.order_queue.untrade)==0:
                self._trade()
            else:
                
                self._trade()
                # print(self.order_queue.untrade)

            self.order_queue.settle()

            self.order_status = pd.DataFrame()
            self.deal_status = pd.DataFrame()

            try:
                event.event_queue.task_done()
            except:
                pass

        elif event.event_type is MARKET_EVENT.QUERY_ORDER:
            """query_order和query_deal 需要联动使用 

            query_order 得到所有的订单列表

            query_deal 判断订单状态--> 运行callback函数


            实盘涉及到外部订单问题: 
            及 订单的来源 不完全从QUANTAXIS中发出, 则QA无法记录来源 (标记为外部订单)
            """

            if self.if_start_orderquery:
                try:
                    # 做一些容错处理
                    res = [self.monitor[account].query_orders(
                        account.account_cookie, '') for account in list(self.monitor.keys())]

                    res = pd.concat(res, axis=0) if len(
                        res) > 0 else None
                    #print(res)
                except:
                    time.sleep(1)

                self.order_status = res if res is not None else self.order_status
                if len(self.order_status) > 0:
                    #print(self.order_status)
                    QA_SU_save_order(self.order_status)
                # else:
                #     time.sleep(1)

            # 这里加入随机的睡眠时间 以免被发现固定的刷新请求
            event.event_type = MARKET_EVENT.QUERY_DEAL
            if event.event_queue.qsize() < 1:
                time.sleep(random.randint(1, 2))

            # 非阻塞
            if self.if_start_orderquery:
                event.event_queue.put(
                    QA_Task(
                        worker=self,
                        engine='ORDER',
                        event=event
                    )
                )


        elif event.event_type is MARKET_EVENT.QUERY_DEAL:

            """order_handler- query_deal

            将order_handler订单队列中的订单---和deal中匹配起来


            """

            if self.if_start_orderquery:
                res = [self.monitor[account].query_orders(
                    account.account_cookie, 'filled') for account in list(self.monitor.keys())]

                try:
                    #res=[pd.DataFrame() if not isinstance(item,pd.DataFrame) else item for item in res]
                    res = pd.concat(res, axis=0) if len(
                        res) > 0 else pd.DataFrame()
                except:
                    res = None

                self.deal_status = res if res is not None else self.deal_status
                if len(self.deal_status) > 0:
                    QA_SU_save_deal(self.deal_status)
                # print(self.order_status)

            # 检查pending订单, 更新订单状态
            try:
                for order in self.order_queue.pending:
                    if len(self.deal_status) > 0:
                        if order.realorder_id in self.deal_status.index.levels[1]:
                            # 此时有成交推送(但可能是多条)
                            #
                            res = self.deal_status.loc[order.account_cookie,
                                                       order.realorder_id]

                            if isinstance(res, pd.Series):
                                order.trade(str(res.trade_id), float(res.trade_price), int(
                                    res.trade_amount), str(res.trade_time))
                            elif isinstance(res, pd.DataFrame):
                                if len(res) == 0:
                                    pass

                                elif len(res) == 1:
                                    res = res.iloc[0]
                                    order.trade(str(res.trade_id), float(res.trade_price), int(
                                        res.trade_amount), str(res.trade_time))
                                else:
                                    # print(res)
                                    # print(len(res))
                                    for _, deal in res.iterrows:
                                        order.trade(str(deal.trade_id), float(deal.trade_price), int(
                                            deal.trade_amount), str(deal.trade_time))
            except Exception as e:
                print(e)
                print(self.order_queue.order_list)
                print(self.deal_status.index)
                print(self.order_status)
            # event.event_queue.task_done()
            # 这里加入随机的睡眠时间 以免被发现固定的刷新请求
            if event.event_queue.qsize() < 1:
                time.sleep(random.randint(2, 5))
            event.event_type = MARKET_EVENT.QUERY_ORDER
            if self.if_start_orderquery:
                event.event_queue.put(
                    QA_Task(
                        worker=self,
                        engine='ORDER',
                        event=event
                    )
                )
            # self.run(event)
            # self.run(event)

        elif event.event_type is MARKET_EVENT.QUERY_POSITION:
            pass

    def subscribe(self, account, broker):
        print('subscribe')
        self.monitor[account] = broker

    def unsubscribe(self, account, broker):
        try:
            self.monitor.pop(account)
        except:
            print('failled to unscribe {}'.format(account.account_cookie))


    def _trade(self):
        res = [self.monitor[account].query_orders(
            account.account_cookie, 'filled') for account in list(self.monitor.keys())]

        try:
            #res=[pd.DataFrame() if not isinstance(item,pd.DataFrame) else item for item in res]
            res = pd.concat(res, axis=0) if len(
                res) > 0 else pd.DataFrame()
        except:
            res = None

        self.deal_status = res if res is not None else self.deal_status
        for order in self.order_queue.pending:



            if len(self.deal_status) > 0:
                if order.realorder_id in self.deal_status.index.levels[1]:
                    # 此时有成交推送(但可能是多条)
                    #
                    res = self.deal_status.loc[order.account_cookie,
                                                order.realorder_id]

                    if isinstance(res, pd.Series):
                        order.trade(str(res.trade_id), float(res.trade_price), int(
                            res.trade_amount), str(res.trade_time))
                    elif isinstance(res, pd.DataFrame):
                        if len(res) == 0:
                            pass

                        elif len(res) == 1:
                            res = res.iloc[0]
                            order.trade(str(res.trade_id), float(res.trade_price), int(
                                res.trade_amount), str(res.trade_time))
                        else:
                            #print(res)
                            #print(len(res))
                            for _, deal in res.iterrows:
                                order.trade(str(deal.trade_id), float(deal.trade_price), int(
                                    deal.trade_amount), str(deal.trade_time))
        return True