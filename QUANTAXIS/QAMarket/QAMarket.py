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
import threading
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Event, Thread, Timer

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAEngine.QAEvent import QA_Event, QA_Job
from QUANTAXIS.QAEngine.QATask import QA_Task
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_future_day,
                                       QA_fetch_future_min,
                                       QA_fetch_future_tick,
                                       QA_fetch_index_day, QA_fetch_index_min,
                                       QA_fetch_stock_day, QA_fetch_stock_min)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_future_day,
                                     QA_fetch_get_future_min,
                                     QA_fetch_get_future_transaction,
                                     QA_fetch_get_future_transaction_realtime,
                                     QA_fetch_get_index_day,
                                     QA_fetch_get_index_min,
                                     QA_fetch_get_stock_day,
                                     QA_fetch_get_stock_min)
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAMarket.QABroker import QA_Broker
from QUANTAXIS.QAMarket.QADealer import QA_Dealer
from QUANTAXIS.QAMarket.QAOrderHandler import QA_OrderHandler
from QUANTAXIS.QAMarket.QARandomBroker import QA_RandomBroker
from QUANTAXIS.QAMarket.QARealBroker import QA_RealBroker
from QUANTAXIS.QAMarket.QASimulatedBroker import QA_SimulatedBroker
from QUANTAXIS.QAMarket.QATrade import QA_Trade
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import (ACCOUNT_EVENT, AMOUNT_MODEL,
                                          BROKER_EVENT, BROKER_TYPE,
                                          ORDER_EVENT, ORDER_MODEL)


class QA_Market(QA_Trade):
    """
    QUANTAXIS MARKET 部分

    交易前置

    暂时还是采用双线程spi模式

    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.session = {}
        self.order_handler = QA_OrderHandler()
        self._broker = {BROKER_TYPE.BACKETEST: QA_BacktestBroker, BROKER_TYPE.RANODM: QA_RandomBroker,
                        BROKER_TYPE.REAL: QA_RealBroker, BROKER_TYPE.SIMULATION: QA_SimulatedBroker}
        self.broker_name = None
        self.broker = None
        self.running_time = None
        self.spi_thread.setName('MARKET')
        # self.spi_thread.start()
        # print(self.spi_thread.is_alive())

    def __repr__(self):
        return '< QA_MARKET with {} Broker >'.format(self.broker_name)

    def connect(self, broker):
        if broker in self._broker.keys():
            self.broker_name = broker
            self.broker = self._broker[broker]()
            self.spi_thread.start()  # 开启trade事件子线程
            return True
        else:
            return False

    def login(self, account_cookie):
        if account_cookie not in self.session.keys():
            self.session[account_cookie] = QA_Account(
                account_cookie=account_cookie)
        else:
            return False

    def logout(self, account_cookie):
        if account_cookie not in self.session.keys():
            return False
        else:
            self.session.pop(account_cookie)

    def get_trading_day(self):
        return self.running_time

    def get_account_id(self):
        return [item.account_cookie for item in self.session.values()]

    # def spi_job(self):

    #     while True:
    #         print('running')
    #         try:
    #             event = self.event_queue.get()
    #             if event['type'] is ORDER_EVENT.CREATE:

    #                 self.order_handler.order_event(
    #                     event=event['type'], message=event['message'])
    #                 self.on_insert_order(
    #                     {'order_id': event['message'].order_id, 'order': event['message'].info()})
    #                 yield self.event_queue.put({
    #                     'type': ORDER_EVENT.TRADE})
    #             elif event['type'] is ORDER_EVENT.TRADE:
    #                 msg = self.order_handler.order_event(
    #                     event=event['type'], message={'broker': self.broker})
    #                 self.on_trade_event(msg)
    #         except:
    #             pass

    def insert_order(self, account_id, amount, amount_model, time, code, order_model, towards):
        order = self.session[account_id].send_order(
            amount=amount, amount_model=amount_model, time=time, code=code, order_model=order_model, towards=towards)

        self.event_queue.put(QA_Task(job=self.order_handler, event=QA_Event(
            event_type=ORDER_EVENT.CREATE, message=order)))

    def on_insert_order(self, data):
        print('callback')
        print(data)

    def query_order(self, order_id):
        return self.order_handler.order_queue.query_order(order_id)

    def query_asset(self, account_cookie):
        return self.session[account_cookie].cash

    def query_position(self, account_cookie):
        pass

    def on_trade_event(self, data):
        print('ON_TRADE')
        print(data)

    def _trade(self):
        "内部函数"
        self.event_queue.put(QA_Task(job=self.order_handler, event=QA_Event(
            event_type=BROKER_EVENT.TRADE, message={'broker': self.broker}, callback=self.on_trade_event)))


if __name__ == '__main__':

    import QUANTAXIS as QA

    user = QA.QA_Portfolio()
    # 创建两个account

    a_1 = user.new_account()
    a_2 = user.new_account()
    market = QA_Market()

    market.connect(QA.RUNNING_ENVIRONMENT.BACKETEST)
    print(market)
    market.login(a_1)
    market.login(a_2)
    print(market.get_account_id())
    market.insert_order(account_id=a_1, amount=10000, amount_model=QA.AMOUNT_MODEL.BY_PRICE,
                        time='2017-12-14', code='000001', order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY)
