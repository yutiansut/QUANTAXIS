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


import datetime

import numpy as np

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAEngine.QATask import QA_Task
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAMarket.QAOrderHandler import QA_OrderHandler
from QUANTAXIS.QAMarket.QARandomBroker import QA_RandomBroker
from QUANTAXIS.QAMarket.QARealBroker import QA_RealBroker
from QUANTAXIS.QAMarket.QAShipaneBroker import QA_SPEBroker
from QUANTAXIS.QAMarket.QASimulatedBroker import QA_SimulatedBroker
from QUANTAXIS.QAMarket.QATrade import QA_Trade
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import (ACCOUNT_EVENT, AMOUNT_MODEL,
                                          BROKER_EVENT, BROKER_TYPE,
                                          ENGINE_EVENT, FREQUENCE,
                                          MARKET_EVENT, ORDER_EVENT,
                                          ORDER_MODEL, RUNNING_ENVIRONMENT)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic


class QA_Market(QA_Trade):
    """
    QUANTAXIS MARKET 部分

    交易前置/可连接到多个broker中
    暂时还是采用多线程engine模式

    session 保存的是 QAAccout 对象
    """

    def __init__(self, if_start_orderthreading=False, *args, **kwargs):
        """[summary]

        Keyword Arguments:
            if_start_orderthreading {bool} -- 是否在初始化的时候开启查询子线程(实盘需要) (default: {False})
        """

        super().__init__()
        # 以下是待初始化的账户session
        self.session = {}
        # 以下都是官方支持的交易前置
        self._broker = {
            BROKER_TYPE.BACKETEST: QA_BacktestBroker,
            BROKER_TYPE.RANODM: QA_RandomBroker,
            BROKER_TYPE.REAL: QA_RealBroker,
            BROKER_TYPE.SIMULATION: QA_SimulatedBroker,
            BROKER_TYPE.SHIPANE: QA_SPEBroker
        }
        self.broker = {}
        self.running_time = None
        self.last_query_data = None
        self.if_start_orderthreading = if_start_orderthreading
        self.order_handler = False

    def __repr__(self):
        '''
                输出market市场对象的字符串
        '''
        return '<QA_Market with {} QA_Broker >'.format(list(self.broker.keys()))

    def upcoming_data(self, broker, data):
        '''
        更新市场数据
        broker 为名字，
        data 是市场数据
        被 QABacktest 中run 方法调用 upcoming_data
        '''
        # main thread'
        # if self.running_time is not None and self.running_time!= data.datetime[0]:
        #     for item in self.broker.keys():
        #         self._settle(item)
        self.running_time = data.datetime[0]
        for item in self.session.values():
            # session里面是已经注册的account
            self.event_queue.put(QA_Task(
                worker=item,  # item 是Account 类型， 是 QA_Work类型， 处理这个 事件
                event=QA_Event(
                    event_type=ENGINE_EVENT.UPCOMING_DATA,
                    # args 附加的参数
                    market_data=data,
                    broker_name=broker,
                    send_order=self.insert_order,  # 🛠todo insert_order = insert_order
                    query_data=self.query_data_no_wait,
                    query_order=self.query_order,
                    query_assets=self.query_assets,
                    query_trade=self.query_trade
                )
            ))

    def start(self):
        self.trade_engine.start()
        if self.if_start_orderthreading:
            """查询子线程开关
            """
            self.start_order_threading()

        # self.trade_engine.create_kernel('MARKET')
        # self.trade_engine.start_kernel('MARKET')

    def connect(self, broker):
        if broker in self._broker.keys():

            self.broker[broker] = self._broker[broker]()  # 在这里实例化
            self.trade_engine.create_kernel('{}'.format(broker))
            self.trade_engine.start_kernel('{}'.format(broker))
            # 开启trade事件子线程
            return True
        else:
            return False

    def register(self, broker_name, broker):
        if broker_name not in self._broker.keys():
            self.broker[broker_name] = broker
            self.trade_engine.create_kernel('{}'.format(broker_name))
            self.trade_engine.start_kernel('{}'.format(broker_name))
            return True
        else:
            return False

    def start_order_threading(self):
        """开启查询子线程(实盘中用)
        """

        self.if_start_orderthreading = True
        self.order_handler = QA_OrderHandler()
        self.trade_engine.create_kernel('ORDER')
        self.trade_engine.start_kernel('ORDER')

    def get_account(self, account_cookie):
        return self.session[account_cookie]

    def login(self, broker_name, account_cookie, account=None):
        """login 登录到交易前置

        2018-07-02 在实盘中,登录到交易前置后,需要同步资产状态

        Arguments:
            broker_name {[type]} -- [description]
            account_cookie {[type]} -- [description]

        Keyword Arguments:
            account {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        res = False
        if account is None:
            if account_cookie not in self.session.keys():
                self.session[account_cookie] = QA_Account(
                    account_cookie=account_cookie, broker=broker_name)
                if self.sync_account(broker_name, account_cookie):
                    res = True

        else:
            if account_cookie not in self.session.keys():
                account.broker = broker_name
                self.session[account_cookie] = account
                if self.sync_account(broker_name, account_cookie):
                    res = True

        if res:
            return res
        else:
            try:
                self.session.pop(account_cookie)
            except:
                pass
            return False

    def sync_account(self, broker_name, account_cookie):
        """同步账户信息

        Arguments:
            broker_id {[type]} -- [description]
            account_id {[type]} -- [description]
        """
        try:
            if isinstance(self.broker[broker_name], QA_BacktestBroker):
                pass
            else:
                self.session[account_cookie].sync_account(
                    self.broker[broker_name].query_positions(account_cookie))
            return True
        except Exception as e:
            print(e)
            return False

    def logout(self, account_cookie, broker_name):
        if account_cookie not in self.session.keys():
            return False
        else:
            self.session.pop(account_cookie)

    def get_trading_day(self):
        return self.running_time

    def get_account_id(self):
        return list(self.session.keys())

    def insert_order(self, account_id, amount, amount_model, time, code, price, order_model, towards, market_type, frequence, broker_name, money=None):
        #strDbg = QA_util_random_with_topic("QA_Market.insert_order")
        #print(">-----------------------insert_order----------------------------->", strDbg)

        flag = False
        if order_model in [ORDER_MODEL.CLOSE, ORDER_MODEL.NEXT_OPEN]:
            _price = self.query_data_no_wait(broker_name=broker_name, frequence=frequence,
                                             market_type=market_type, code=code, start=time)
            if isinstance(_price, np.ndarray):
                if (_price != np.array(None)).any():
                    price = float(_price[0][4])
                    flag = True
                else:
                    QA_util_log_info(
                        'MARKET WARING: SOMEING WRONG WITH ORDER \n ')
                    QA_util_log_info('code {} date {} price {} order_model {} amount_model {}'.format(
                        code, time, price, order_model, amount_model))
            else:
                if _price is not None and len(_price) > 0:
                    price = float(_price[0][4])
                    flag = True
                else:
                    QA_util_log_info(
                        'MARKET WARING: SOMEING WRONG WITH ORDER \n ')
                    QA_util_log_info('code {} date {} price {} order_model {} amount_model {}'.format(
                        code, time, price, order_model, amount_model))

        elif order_model is ORDER_MODEL.MARKET:
            _price = self.query_data_no_wait(broker_name=broker_name, frequence=frequence,
                                             market_type=market_type, code=code, start=time)
            if isinstance(_price, np.ndarray):
                if (_price != np.array(None)).any():
                    price = float(_price[0][1])
                    flag = True
                else:
                    QA_util_log_info(
                        'MARKET WARING: SOMEING WRONG WITH ORDER \n ')
                    QA_util_log_info('code {} date {} price {} order_model {} amount_model {}'.format(
                        code, time, price, order_model, amount_model))
            else:
                if _price is not None and len(_price) > 0:
                    price = float(_price[0][1])
                    flag = True
                else:
                    QA_util_log_info(
                        'MARKET WARING: SOMEING WRONG WITH ORDER \n ')
                    QA_util_log_info('code {} date {} price {} order_model {} amount_model {}'.format(
                        code, time, price, order_model, amount_model))
        elif order_model is ORDER_MODEL.LIMIT:
            # if price > self.last_query_data[0][2] or price < self.last_query_data[0][3]:
            flag = True
        if flag:
            order = self.get_account(account_id).send_order(
                amount=amount, amount_model=amount_model, time=time, code=code, price=price,
                order_model=order_model, towards=towards, money=money)

            # print("------------------------------------------------->")
            #print("order 排队")
            # print(order)
            #print("时间戳" )
            # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 日期格式化
            # print("<-------------------------------------------------")
            if order:
                self.event_queue.put_nowait(
                    QA_Task(
                        worker=self.broker[self.get_account(
                            account_id).broker],
                        engine=self.get_account(account_id).broker,
                        event=QA_Event(
                            event_type=BROKER_EVENT.RECEIVE_ORDER,
                            order=order,
                            callback=self.on_insert_order)))
        else:
            pass

        #print("<-----------------------insert_order-----------------------------<", strDbg)

    def on_insert_order(self, order):
        print(order)
        pass

    def _renew_account(self):
        for account in self.session.values():
            self.event_queue.put(
                QA_Task(
                    worker=account,
                    event=QA_Event(
                        event_type=ACCOUNT_EVENT.SETTLE)))

    def query_order(self, broker_name, order_id):

        res = self.event_queue.put(
            QA_Task(
                worker=self.broker[broker_name],
                engine=broker_name,
                event=QA_Event(
                    order_id=order_id
                )
            ))

        return res

    def query_assets(self, account_cookie):
        return self.get_account(account_cookie).assets

    def query_position(self, account_cookie):
        return self.get_account(account_cookie).hold

    def query_cash(self, account_cookie):
        return self.get_account(account_cookie).cash_available

    def query_data_no_wait(self, broker_name, frequence, market_type, code, start, end=None):
        return self.broker[broker_name].run(event=QA_Event(
            event_type=MARKET_EVENT.QUERY_DATA,
            frequence=frequence,
            market_type=market_type,
            code=code,
            start=start,
            end=end
        ))

    def query_data(self, broker_name, frequence, market_type, code, start, end=None):
        self.event_queue.put(
            QA_Task(
                worker=self.broker[broker_name],
                engine=broker_name,
                event=QA_Event(
                    event_type=MARKET_EVENT.QUERY_DATA,
                    frequence=frequence,
                    market_type=market_type,
                    code=code,
                    start=start,
                    end=end,
                    callback=self.on_query_data
                )
            ))

    def query_currentbar(self, broker_name, market_type, code):
        return self.broker[broker_name].run(event=QA_Event(
            event_type=MARKET_EVENT.QUERY_DATA,
            frequence=FREQUENCE.CURRENT,
            market_type=market_type,
            code=code,
            start=self.running_time,
            end=None
        ))

    def on_query_data(self, data):
        print('ON QUERY')
        print(data)
        self.last_query_data = data

    def on_trade_event(self, event):
        print('ON TRADE')
        print(event.res)

    def _trade(self, event):
        "内部函数"

        self.event_queue.put(QA_Task(
            worker=self.broker[event.broker_name],
            engine=event.broker_name,
            event=QA_Event(
                event_type=BROKER_EVENT.TRADE,
                broker=self.broker[event.broker_name],
                broker_name=event.broker_name,
                callback=self.on_trade_event
            )))

    def _settle(self, broker_name, callback=False):
        #strDbg = QA_util_random_with_topic("QA_Market._settle")
        #print(">-----------------------_settle----------------------------->", strDbg)

        # 向事件线程发送BROKER的SETTLE事件
        # 向事件线程发送ACCOUNT的SETTLE事件

        for account in self.session.values():

            if account.running_environment == RUNNING_ENVIRONMENT.TZERO:

                for order in account.close_positions_order:

                    self.event_queue.put(
                        QA_Task(
                            worker=self.broker[account.broker],
                            engine=account.broker,
                            event=QA_Event(
                                event_type=BROKER_EVENT.RECEIVE_ORDER,
                                order=order,
                                callback=self.on_insert_order)))

            if account.broker == broker_name:
                self.event_queue.put(
                    QA_Task(
                        worker=account,
                        engine=broker_name,
                        event=QA_Event(
                            event_type=ACCOUNT_EVENT.SETTLE)))
        self.event_queue.put(QA_Task(
            worker=self.broker[broker_name],
            engine=broker_name,
            event=QA_Event(
                event_type=BROKER_EVENT.SETTLE,
                broker=self.broker[broker_name],
                callback=callback)))

        print('===== SETTLED {} ====='.format(self.running_time))

        #strDbg = QA_util_random_with_topic("MAStrategy.on_bar call")
        #print("<-----------------------_settle-----------------------------<", strDbg)

    def _close(self):
        pass

    def clear(self):
        return self.trade_engine.clear()


if __name__ == '__main__':

    import QUANTAXIS as QA

    user = QA.QA_Portfolio()
    # 创建两个account

    a_1 = user.new_account()
    a_2 = user.new_account()
    market = QA_Market()

    market.connect(QA.RUNNING_ENVIRONMENT.BACKETEST)
    #
