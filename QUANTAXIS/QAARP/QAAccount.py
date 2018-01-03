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

import datetime

import pandas as pd

from QUANTAXIS.QAEngine.QAEvent import QA_Worker
from QUANTAXIS.QAMarket.QAOrder import QA_Order
from QUANTAXIS.QAUtil.QAParameter import (ACCOUNT_EVENT, AMOUNT_MODEL,
                                          BROKER_TYPE, ENGINE_EVENT,
                                          MARKET_TYPE, ORDER_DIRECTION)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic

# 2017/6/4修改: 去除总资产的动态权益计算


class QA_Account(QA_Worker):
    """[QA_Account]

    [description]
    QA_Account 是QUANTAXIS的最小不可分割单元之一

    QA_Account
    """

    # 一个hold改成list模式

    def __init__(self, strategy_name='', user='', account_type=MARKET_TYPE.STOCK_DAY,
                 hold=None, broker=BROKER_TYPE.BACKETEST,
                 sell_available=None,
                 init_assest=None, order_queue=None,
                 cash=None, history=None, detail=None, assets=None,
                 account_cookie=None):
        super().__init__()
        self._history_headers = ['datetime', 'code', 'price',
                                 'towards', 'amount', 'order_id', 'trade_id', 'commission_fee']
        self._detail_headers = ['datetime', 'code', 'price', 'towards', 'amount', 'order_id', 'trade_id',
                                'match_price', 'match_order_id', 'match_trade_id', 'commission_fee', 'match_commission']
        self._hold_headers = ['datetime', 'code',
                              'price', 'amount', 'order_id', 'trade_id']

        self.hold = [] if hold is None else hold

        self.init_assest = 1000000 if init_assest is None else init_assest
        self.strategy_name = strategy_name
        self.user = user
        self.account_type = account_type

        self.cash = [self.init_assest] if cash is None else cash
        self.assets = [self.init_assest] if assets is None else assets

        self.cash_available = self.cash[-1]  # 可用资金
        self.sell_available = [['datetime', 'code', 'price',
                                'amount', 'order_id', 'trade_id']] if sell_available is None else sell_available
        self.order_queue = pd.DataFrame() if order_queue is None else order_queue  # 已委托待成交队列

        self.history = [] if history is None else history
        self.detail = [] if detail is None else detail
        self.broker = broker
        self.account_cookie = QA_util_random_with_topic(
            'Acc') if account_cookie is None else account_cookie
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': self.user,
                    'strategy': self.strategy_name
                }
            },
            'body': {
                'account': {
                    'hold': self.hold,
                    'cash': self.cash,
                    'assets': self.cash,
                    'history': self.history,
                    'detail': self.detail
                },
                'running_time': str(datetime.datetime.now())
            }
        }
        self.market_data = None
        self._currenttime = None

    def __repr__(self):
        return '< QA_Account {} Assets:{} >'.format(self.account_cookie, self.assets[-1])

    @property
    def latest_assets(self):
        'return the lastest assets'
        return self.assets[-1]

    @property
    def latest_cash(self):
        'return the lastest cash'
        return self.cash[-1]

    @property
    def latest_hold(self):
        'return the lastest hold'
        return self.hold

    @property
    def current_time(self):
        return self._currenttime

    @property
    def hold_table(self):
        return pd.DataFrame(data=self.hold, columns=self._hold_headers)

    @property
    def assets_series(self):
        return pd.Series(self.assets)

    def init(self, init_assest=None):
        'init methods'
        self.hold = []
        self.sell_available = [['date', 'code', 'price',
                                'amount', 'order_id', 'trade_id']]
        self.history = []
        self.init_assest = init_assest
        self.account_cookie = QA_util_random_with_topic(topic='Acc')
        self.assets = [self.init_assest]
        self.cash = [self.init_assest]
        self.cash_available = self.cash[-1]  # 在途资金
        self.order_queue = pd.DataFrame()   # 已委托待成交队列
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': '',
                    'strategy': ''
                }
            },
            'body': {
                'account': {
                    'hold': self.hold,
                    'cash': self.cash,
                    'assets': self.cash,
                    'history': self.history,
                    'detail': self.detail
                },
                'running_time': str(datetime.datetime.now())
            }
        }

    def receive_deal(self, message):
        """[用于更新账户]

        [description]

        Arguments:
            message {json/dict} -- message_from_deal

        Returns:
            {json} -- message of account
        """

        if str(message['header']['status'])[0] == '2':

            # towards>1 买入成功
            # towards<1 卖出成功

            (__new_code, __new_amount, __new_trade_date, __new_towards,
                __new_price, __new_order_id,
                __new_trade_id, __new_trade_fee) = (str(message['body']['order']['code']),
                                                    float(message['body']['order']['amount']), str(
                                                        message['body']['order']['datetime']),
                                                    int(message['body']['order']['towards']), float(
                                                        message['body']['order']['price']),
                                                    str(message['header']['order_id']), str(
                                                        message['header']['trade_id']),
                                                    float(message['body']['fee']['commission']))
            if int(message['header']['status']) == 203:
                '委托成功 待交易'
                self.order_queue.append(
                    [__new_trade_date, __new_code, __new_price, __new_amount,
                     __new_order_id, __new_trade_id])

                # 如果是买入的waiting  那么要减少可用资金,增加在途资金
                # 如果是卖出的waiting 则减少hold_list
            elif int(message['header']['status']) == 200:
                '交易成功的处理'
                self.history.append(
                    [__new_trade_date, __new_code, __new_price, __new_towards,
                     __new_amount, __new_order_id, __new_trade_id, __new_trade_fee])
                # 先计算收益和利润

                # 修改持仓表
                if int(__new_towards) > 0:
                    # 买入
                    self.hold.append(
                        [__new_trade_date, __new_code, __new_price, __new_amount,
                         __new_order_id, __new_trade_id])
                    self.detail.append([__new_trade_date, __new_code, __new_price,
                                        __new_amount, __new_order_id, __new_trade_id,
                                        [], [], [], [], __new_amount, __new_trade_fee])
                # 将交易记录插入历史交易记录
                else:
                    # 卖出
                    __pop_list = []
                    while __new_amount > 0:

                        if len(self.hold) > 0:
                            for i in range(0, len(self.hold)):

                                if __new_code in self.hold[i]:
                                    if float(__new_amount) > (self.hold[i][3]):

                                        __new_amount = __new_amount - \
                                            self.hold[i][3]

                                        __pop_list.append(i)

                                    elif float(__new_amount) < float(self.hold[i][3]):
                                        self.hold[i][3] = self.hold[i][3] - \
                                            __new_amount

                                        for __item_detail in self.detail:
                                            if __item_detail[5] == self.hold[i][5] and \
                                                    __new_trade_id not in __item_detail[7]:
                                                __item_detail[6].append(
                                                    __new_price)
                                                __item_detail[7].append(
                                                    __new_order_id)
                                                __item_detail[8].append(
                                                    __new_trade_id)
                                                __item_detail[9].append(
                                                    __new_trade_date)
                                                __item_detail[10] = self.hold[i][3] - \
                                                    __new_amount
                                                __item_detail[11] += __new_trade_fee
                                        __new_amount = 0
                                    elif float(__new_amount) == float(self.hold[i][3]):

                                        __new_amount = 0
                                        __pop_list.append(i)

                    __pop_list.sort()
                    __pop_list.reverse()
                    for __id in __pop_list:

                        for __item_detail in self.detail:
                            if __item_detail[5] == self.hold[__id][5] and \
                                    __new_trade_id not in __item_detail[7]:
                                __item_detail[6].append(__new_price)
                                __item_detail[7].append(__new_order_id)
                                __item_detail[8].append(__new_trade_id)
                                __item_detail[9].append(__new_trade_date)
                                __item_detail[10] = 0
                                __item_detail[11] += __new_trade_fee

                        self.hold.pop(__id)
                    __del_id = []
                    for __hold_id in range(0, len(self.hold)):
                        if int(self.hold[__hold_id][3]) == 0:
                            __del_id.append(__hold_id)
                    __del_id.sort()
                    __del_id.reverse()

                    for __item in __del_id:
                        self.hold.pop(__item)

            # 将交易记录插入历史交易记录
        else:
            pass
        self.calc_profit(message)
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': message['header']['session']['user'],
                    'strategy': message['header']['session']['strategy'],
                    'code': message['body']['order']['code']
                }

            },
            'body': {
                'account': {
                    'hold': self.hold,
                    'history': self.history,
                    'cash': self.cash,
                    'assets': self.assets,
                    'detail': self.detail
                },
                'time': str(datetime.datetime.now()),
                'date_stamp': datetime.datetime.now().timestamp()
            }
        }

        return self.message

    def calc_profit(self, message):
        """用于计算profit

        [description]

        Arguments:
            message {[type]} -- [description]
        """

        if message['header']['status'] == 200 and message['body']['order']['towards'] == 1:
            # 买入/
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值

            # 买入的部分在update_message

            # 可用资金=上一期可用资金-买入的资金
            self.cash.append(float(self.cash[-1]) - float(
                message['body']['order']['price']) * float(
                    message['body']['order']['amount']) * message['body']['order']['towards'] - float(message['body']['fee']['commission']))

        elif message['header']['status'] == 200 and message['body']['order']['towards'] == -1:
            # success trade,sell
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值
            # 买入的部分在update_message

            # 卖出的时候,towards=-1,所以是加上卖出的资产
            # 可用资金=上一期可用资金+卖出的资金
            self.cash.append(float(self.cash[-1]) - float(
                message['body']['order']['price']) * float(
                    message['body']['order']['amount']) * message['body']['order']['towards'] - float(message['body']['fee']['commission']))

            # 更新可用资金历史

            # hold
        market_value = 0
        for i in range(0, len(self.hold)):
            market_value += (float(self.hold[i][2]) * float(self.hold[i][3]))
        self.assets.append(self.cash[-1] + market_value)

    def calc_assets(self):
        'get the real assets [from cash and market values]'

        return self.cash[-1] + sum([float(self.hold[i][2]) * float(self.hold[i][3]) for i in range(0, len(self.hold))])

    def send_order(self, code, amount, time, towards, price, order_model, amount_model, data_type, market_type):
        """[summary]

        [description]

        Arguments:
            code {[type]} -- [description]
            amount {[type]} -- [description]
            time {[type]} -- [description]
            towards {[type]} -- [description]
            order_model {[type]} -- [description]
            amount_model {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        flag = False
        date = str(time)[0:10] if len(str(time)) == 19 else str(time)
        time = str(time) if len(
            str(time)) == 19 else '{} 09:31:00'.format(str(time)[0:10])
        if towards in [ORDER_DIRECTION.BUY] and amount_model is AMOUNT_MODEL.BY_AMOUNT:
            if self.cash_available > amount * price:
                self.cash_available -= amount * price
                flag = True
        if towards in [ORDER_DIRECTION.BUY] and amount_model is AMOUNT_MODEL.BY_PRICE:
            if self.cash_available > amount:
                self.cash_available -= amount
                flag = True
        elif towards in [ORDER_DIRECTION.SELL] and amount_model is AMOUNT_MODEL.BY_AMOUNT:
            if self.sell_available[code] > amount:
                self.sell_available[code] -= amount
                flag = True
        elif towards in [ORDER_DIRECTION.SELL] and amount_model is AMOUNT_MODEL.BY_PRICE:
            if self.sell_available[code] > amount:
                self.sell_available[code] -= int(amount / price * 100) * 100
                flag = True
        if flag:
            return QA_Order(user=self.user, strategy=self.strategy_name, data_type=data_type,
                            account_cookie=self.account_cookie, code=code, market_type=market_type,
                            date=date, datetime=time, sending_time=time,
                            btype=self.account_type, amount=amount, price=price,
                            order_model=order_model, towards=towards, amount_model=amount_model)  # init
        else:
            return flag

    def settle(self):
        '初始化的时候 同步可用资金/可卖股票'
        self.cash_available = self.cash[-1]
        self.sell_available = pd.DataFrame(self.hold, columns=self._hold_headers).set_index(
            'code', drop=False)['amount'].groupby('code').sum()

    def on_bar(self, event):
        'while updating the market data'
        print(event.market_data)

    def on_tick(self, event):
        'on tick event'
        pass

    def from_message(self, message):
        'resume the account from standard message'
        self.account_cookie = message['header']['cookie']
        self.hold = message['body']['account']['hold']
        self.history = message['body']['account']['history']
        self.cash = message['body']['account']['cash']
        self.assets = message['body']['account']['assets']
        self.detail = message['body']['account']['detail']
        return self

    def run(self, event):
        'QA_WORKER method'
        if event.event_type is ACCOUNT_EVENT.SETTLE:
            self.settle()

        elif event.event_type is ACCOUNT_EVENT.UPDATE:
            self.receive_deal(event.message)
        elif event.event_type is ACCOUNT_EVENT.MAKE_ORDER:
            """generate order
            if callback callback the order
            if not return back the order
            """
            data = self.send_order(code=event.code, amount=event.amount, time=event.time,
                                   amount_model=event.amount_model, towards=event.towards,
                                   price=event.price, order_model=event.order_model,
                                   data_type=event.data_type,
                                   market_type=event.market_type)
            if event.callback:
                event.callback(data)
            else:
                return data
        elif event.event_type is ENGINE_EVENT.UPCOMING_DATA:
            """update the market_data
            1. update the inside market_data struct
            2. tell the on_bar methods
            """
            self._currenttime = event.market_data.datetime[-1]
            if self.market_data is None:
                self.market_data = event.market_data
            else:
                self.market_data.append(event.market_data)
            self.on_bar(event)

            if event.callback:
                event.callback(event)


if __name__ == '__main__':
    account = QA_Account()
    # 创建一个account账户
