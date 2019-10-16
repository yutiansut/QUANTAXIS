# coding:utf-8
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

import copy
import datetime
import warnings

import numpy as np
import pandas as pd
from pymongo import DESCENDING, ASCENDING

from QUANTAXIS import __version__
from QUANTAXIS.QAARP.market_preset import MARKET_PRESET
from QUANTAXIS.QAEngine.QAEvent import QA_Worker
from QUANTAXIS.QAMarket.QAOrder import QA_Order, QA_OrderQueue
from QUANTAXIS.QAMarket.QAPosition import QA_Position
from QUANTAXIS.QASU.save_account import save_account, update_account
from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QADate_trade import (
    QA_util_get_next_day,
    QA_util_get_trade_range
)
from QUANTAXIS.QAUtil.QAParameter import (
    ACCOUNT_EVENT,
    AMOUNT_MODEL,
    BROKER_TYPE,
    ENGINE_EVENT,
    FREQUENCE,
    MARKET_TYPE,
    ORDER_DIRECTION,
    ORDER_MODEL,
    RUNNING_ENVIRONMENT,
    TRADE_STATUS,
    EXCHANGE_ID
)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic

# 2017/6/4修改: 去除总资产的动态权益计算


# pylint: disable=old-style-class, too-few-public-methods
class QA_AccountPRO(QA_Worker):
    def __init__(
        self,
        user_cookie: str,
        portfolio_cookie: str,
        account_cookie=None,
        strategy_name=None,
        market_type=MARKET_TYPE.STOCK_CN,
        frequence=FREQUENCE.DAY,
        broker=BROKER_TYPE.BACKETEST,
        init_hold={},
        init_cash=1000000,
        commission_coeff=0.00025,
        tax_coeff=0.001,
        margin_level={},
        allow_t0=False,
        allow_sellopen=False,
        allow_margin=False,
        running_environment=RUNNING_ENVIRONMENT.BACKETEST,
        auto_reload=False,
        generated='direct',
        start=None,
        end=None
    ):
        super().__init__()

        self._history_headers = [
            'datetime',  # 日期/时间
            'code',  # 品种
            'price',  # 成交价
            'amount',  # 成交数量(股票 股数  期货 手数)
            'cash',  # 现金
            'order_id',  # 本地订单号
            'realorder_id',  # 实际委托单号
            'trade_id',  # 成交单号
            'account_cookie',  # 账号id
            'commission',  # 手续费
            'tax',  # 税
            'message',  # 备注
            'frozen',  # 冻结资金.
            'direction',  # 方向,
            'total_frozen'
        ]
        self.activity = {}
        ########################################################################
        # 信息类:

        if user_cookie is None or portfolio_cookie is None:
            raise RuntimeError('QUANTAXIS 1.3.0升级: 需要在创建Account的时候指定用户名/组合名')
        self.user_cookie = user_cookie
        self.strategy_name = strategy_name
        self.portfolio_cookie = portfolio_cookie
        self.account_cookie = QA_util_random_with_topic(
            'AccPro'
        ) if account_cookie is None else account_cookie
        self.market_type = market_type
        self.broker = broker
        self.frequence = frequence
        self.running_environment = running_environment
        ########################################################################
        self._market_data = None
        self._currenttime = None
        self.commission_coeff = commission_coeff
        self.tax_coeff = tax_coeff
        self.datetime = None
        self.running_time = datetime.datetime.now()
        self.quantaxis_version = __version__
        self.client = DATABASE.accountPro
        self.start_ = start
        self.end_ = end
        ### 下面是数据库创建index部分, 此部分可能导致部分代码和原先不兼容
        self.client.create_index(
            [
                ("account_cookie",
                 ASCENDING),
                ("user_cookie",
                 ASCENDING),
                ("portfolio_cookie",
                 ASCENDING)
            ],
            unique=True
        )
        ########################################################################
        # 资产类
        self.orders = QA_OrderQueue()  # 历史委托单
        self.init_cash = init_cash
        self.init_hold = pd.Series(
            init_hold,
            name='amount'
        ) if isinstance(init_hold,
                        dict) else init_hold
        self.init_hold.index.name = 'code'
        self.cash = [self.init_cash]
        self.cash_available = self.cash[-1]  # 可用资金
        self.sell_available = copy.deepcopy(self.init_hold)
        self.buy_available = copy.deepcopy(self.init_hold)
        self.history = []
        self.time_index_max = []

        # 在回测中, 每日结算后更新
        # 真实交易中, 为每日初始化/每次重新登录后的同步信息
        self.static_balance = {
            'static_assets': [],
            'cash': [],
            'frozen': [],
            'hold': [],
            'date': []
        }                        # 日结算
        self.today_trade = {'last': [], 'current': []}
        self.today_orders = {'last': [], 'current': []}
        self.positions = {}

        ########################################################################
        # 规则类
        # 1.是否允许t+0 及买入及结算
        # 2.是否允许卖空开仓
        # 3.是否允许保证金交易/ 如果不是false 就需要制定保证金比例(dict形式)

        # 期货: allow_t0 True allow_sellopen True
        #

        self.allow_t0 = allow_t0
        self.allow_sellopen = allow_sellopen
        self.allow_margin = allow_margin
        self.margin_level = margin_level  # 保证金比例

        if self.market_type is MARKET_TYPE.FUTURE_CN:
            self.allow_t0 = True
            self.allow_sellopen = True
            self.allow_margin = True

        self.market_preset = MARKET_PRESET()
        # if self.allow_t0 and self.allow_sellopen or self.market_type is MARKET_TYPE.FUTURE_CN:
        #     self.load_marketpreset()
        """期货的多开/空开 ==> 资金冻结进保证金  frozen

        对应平仓的时候, 释放保证金

        1. frozen  是一个dict :   {[code]:queue}
            key是标的 value是对应的交易queue

        """

        self.frozen = {}  # 冻结资金(保证金)
        self.finishedOrderid = []

        # if auto_reload:
        #     self.reload()

    def __repr__(self):
        return '< QA_AccountPRO {} market: {}>'.format(
            self.account_cookie,
            self.market_type
        )

    def get_position(self, code: str) -> QA_Position:
        """Get

        获取position
        same apis with QIFIAccount

        return  <QA_Position>

        """

        pos = self.positions.get(code, QA_Position(code=code, user_cookie=self.user_cookie,
                                                   portfolio_cookie=self.portfolio_cookie, account_cookie=self.account_cookie, auto_reload=False))
        if pos.market_type == self.market_type:
            self.positions[code] = pos
            return pos
        else:
            print('Current AccountPro {} is {} doesnot support {}'.format(
                self.account_cookie, self.market_type, pos.market_type))





    @property
    def hold_available(self):
        pass

    def send_order(
            self,
            code=None,
            amount=None,
            time=None,
            towards=None,
            price=None,
            money=None,
            order_model=ORDER_MODEL.LIMIT,
            amount_model=AMOUNT_MODEL.BY_AMOUNT,
            order_id=None,
            position_id=None,
            *args,
            **kwargs
    ):

        wrong_reason = None
        assert code is not None and time is not None and towards is not None and order_model is not None and amount_model is not None
        date = str(time)[0:10] if len(str(time)) == 19 else str(time)
        time = str(time) if len(str(time)) == 19 else '{} 09:31:00'.format(
            str(time)[0:10]
        )
        if self.allow_margin:
            amount = amount if amount_model is AMOUNT_MODEL.BY_AMOUNT else int(
                money / (
                    self.market_preset.get_unit(code) *
                    self.market_preset.get_frozen(code) * price *
                    (1 + self.commission_coeff)
                ) / 100
            ) * 100
        else:
            amount = amount if amount_model is AMOUNT_MODEL.BY_AMOUNT else int(
                money / (price * (1 + self.commission_coeff)) / 100
            ) * 100

        # 🛠todo 移到Utils类中，  money_to_amount 金额转成交量
        if self.allow_margin:
            money = amount * price * self.market_preset.get_unit(code)*self.market_preset.get_frozen(code) * \
                (1+self.commission_coeff) if amount_model is AMOUNT_MODEL.BY_AMOUNT else money
        else:
            money = amount * price * \
                (1+self.commission_coeff) if amount_model is AMOUNT_MODEL.BY_AMOUNT else money

        # flag 判断买卖 数量和价格以及买卖方向是否正确
        flag = False

        assert (int(towards) != 0)
        if int(towards) in [1, 2, 3]:
            # 是买入的情况(包括买入.买开.买平)
            if self.cash_available >= money:
                if self.market_type == MARKET_TYPE.STOCK_CN:  # 如果是股票 买入的时候有100股的最小限制
                    amount = int(amount / 100) * 100
                    self.cash_available -= money
                    flag = True

                if self.running_environment == RUNNING_ENVIRONMENT.TZERO:

                    if abs(self.buy_available.get(code, 0)) >= amount:
                        flag = True
                        self.cash_available -= money
                        self.buy_available[code] -= amount
                    else:
                        flag = False
                        wrong_reason = 'T0交易买入超出限额'

                if self.market_type == MARKET_TYPE.FUTURE_CN:
                    # 如果有负持仓-- 允许卖空的时候
                    if towards == 3:  # 多平
                        pos = self.get_position(code)
                        # 假设有负持仓:
                        # amount为下单数量 如  账户原先-3手 现在平1手

                        #left_amount = amount+_hold if _hold < 0 else amount
                        money_need = abs(
                            float(amount * price * (1 + self.commission_coeff))
                        )

                        if self.cash_available >= money_need:
                            if pos.volume_short > 0:
                                self.cash_available -= money_need

                                flag = True
                            else:
                                wrong_reason = '空单仓位不足'
                        else:
                            wrong_reason = '平多剩余资金不够'
                    if towards == 2:
                        self.cash_available -= money
                        flag = True
            else:
                wrong_reason = 'QAACCOUNT: 可用资金不足 cash_available {}  code {} time {} amount {} towards {}'.format(
                    self.cash_available,
                    code,
                    time,
                    amount,
                    towards
                )
        elif int(towards) in [-1, -2, -3]:
            # 是卖出的情况(包括卖出，卖出开仓allow_sellopen如果允许. 卖出平仓)
            # print(self.sell_available[code])
            pos = self.get_position(code)  # _hold 是你的持仓

            # 如果你的hold> amount>0
            # 持仓数量>卖出数量

            if towards == -1:
                if pos.volume_long_his >= amount:
                    self.sell_available[code] -= amount
                    # towards = ORDER_DIRECTION.SELL
                    flag = True
            elif towards == -2:
                if self.allow_sellopen:
                    if self.cash_available >= money:  # 卖空的市值小于现金（有担保的卖空）， 不允许裸卖空
                                                    # self.cash_available -= money
                        flag = True
                    else:
                        print('sellavailable', _hold)
                        print('amount', amount)
                        print('aqureMoney', money)
                        print('cash', self.cash_available)
                        wrong_reason = "卖空资金不足"
                else:
                    wrong_reason = "不允许卖空"

            else:
                if pos.volume_long >= amount:
                    self.sell_available[code] -= amount
                    # towards = ORDER_DIRECTION.SELL
                    flag = True
                # 如果持仓数量<卖出数量
                else:
                    wrong_reason = "卖出仓位不足"

        if flag and (amount > 0):
            _order = QA_Order(
                user_cookie=self.user_cookie,
                strategy=self.strategy_name,
                frequence=self.frequence,
                account_cookie=self.account_cookie,
                code=code,
                market_type=self.market_type,
                date=date,
                datetime=time,
                sending_time=time,
                #callback=self.receive_deal,
                amount=amount,
                price=price,
                order_model=order_model,
                towards=towards,
                money=money,
                broker=self.broker,
                amount_model=amount_model,
                commission_coeff=self.commission_coeff,
                tax_coeff=self.tax_coeff,
                position_id=position_id,
                order_id=order_id,
                *args,
                **kwargs
            )                                                           # init
            # 历史委托order状态存储， 保存到 QA_Order 对象中的队列中
            self.datetime = time
            self.orders.insert_order(_order)
            return _order
        else:
            print(
                'ERROR : CODE {} TIME {}  AMOUNT {} TOWARDS {}'.format(
                    code,
                    time,
                    amount,
                    towards
                )
            )
            print(wrong_reason)
            return False
