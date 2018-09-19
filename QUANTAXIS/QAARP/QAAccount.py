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


import copy
import datetime
import warnings

import numpy as np
import pandas as pd

from QUANTAXIS import __version__
from QUANTAXIS.QAEngine.QAEvent import QA_Worker
from QUANTAXIS.QAMarket.QAOrder import QA_Order, QA_OrderQueue
from QUANTAXIS.QASU.save_account import save_account, update_account
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_get_next_day,
                                           QA_util_get_trade_range)
from QUANTAXIS.QAUtil.QAParameter import (ACCOUNT_EVENT, AMOUNT_MODEL,
                                          BROKER_TYPE, ENGINE_EVENT, FREQUENCE,
                                          MARKET_TYPE, ORDER_DIRECTION,
                                          ORDER_MODEL, RUNNING_ENVIRONMENT,
                                          TRADE_STATUS)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic

# 2017/6/4修改: 去除总资产的动态权益计算


# pylint: disable=old-style-class, too-few-public-methods
class QA_Account(QA_Worker):
    """QA_Account
    User-->Portfolio-->Account/Strategy

    :::::::::::::::::::::::::::::::::::::::::::::::::
    ::        :: Portfolio 1 -- Account/Strategy 1 ::
    ::  USER  ::             -- Account/Strategy 2 ::
    ::        :: Portfolio 2 -- Account/Strategy 3 ::
    :::::::::::::::::::::::::::::::::::::::::::::::::

    2018/1/5 再次修改 改版本去掉了多余的计算 精简账户更新
    ======================

    - 不再计算总资产/不再计算当前持仓/不再计算交易对照明细表
    - 不再动态计算账户股票/期货市值
    - 只维护 cash/history两个字段 剩下的全部惰性计算


    QA_Account 是QUANTAXIS的最小不可分割单元之一

    QA_Account是账户类 需要兼容股票/期货/指数
    QA_Account继承自QA_Worker 可以被事件驱动
    QA_Account可以直接被QA_Strategy继承

    有三类输入:
    信息类: 账户绑定的策略名/账户的用户名/账户类别/账户识别码/账户的broker
    资产类: 现金/可用现金/交易历史/交易对照表
    规则类: 是否允许卖空/是否允许t0结算

    方法:
    惰性计算:最新持仓/最新总资产/最新现金/持仓面板
    生成订单/接受交易结果数据
    接收新的数据/on_bar/on_tick方法/缓存新数据的market_data

    @royburns  1.添加注释
    2018/05/18

    T0交易的sell_available和正常的sell_available不一样:

    T0交易中, 当买入一笔/卖出一笔, 当天操作额度都会下降

    T0的订单-账户对应系统


    @2018/06/11
    QA_Account不会基于行情计算市值,因此都只会对应记录证券数量和现金资产 
    """

    def __init__(self, strategy_name=None, user_cookie=None, portfolio_cookie=None, account_cookie=None,
                 market_type=MARKET_TYPE.STOCK_CN, frequence=FREQUENCE.DAY, broker=BROKER_TYPE.BACKETEST,
                 init_hold={}, init_cash=1000000, commission_coeff=0.00025, tax_coeff=0.001,
                 margin_level=False, allow_t0=False, allow_sellopen=False,
                 running_environment=RUNNING_ENVIRONMENT.BACKETEST):
        """

        :param [str] strategy_name:  策略名称
        :param [str] user_cookie:   用户cookie
        :param [str] portfolio_cookie: 组合cookie
        :param [str] account_cookie:   账户cookie

        :param [dict] init_hold         初始化时的股票资产
        :param [float] init_cash:         初始化资金
        :param [float] commission_coeff:  交易佣金 :默认 万2.5   float 类型
        :param [float] tax_coeff:         印花税   :默认 千1.5   float 类型

        :param [Bool] margin_level:      保证金比例 默认False
        :param [Bool] allow_t0:          是否允许t+0交易  默认False
        :param [Bool] allow_sellopen:    是否允许卖空开仓  默认False

        :param [QA.PARAM] market_type:   市场类别 默认QA.MARKET_TYPE.STOCK_CN A股股票
        :param [QA.PARAM] frequence:     账户级别 默认日线QA.FREQUENCE.DAY
        :param [QA.PARAM] broker:        BROEKR类 默认回测 QA.BROKER_TYPE.BACKTEST
        :param [QA.PARAM] running_environment 当前运行环境 默认Backtest

        # 2018/06/11 init_assets 从float变为dict,并且不作为输入,作为只读属性
        #  :param [float] init_assets:       初始资产  默认 1000000 元 （100万）
        init_assets:{
            cash: xxx,
            stock: {'000001':2000},
            init_date: '2018-02-05',
            init_datetime: '2018-02-05 15:00:00'
        }
        # 2018/06/11 取消在初始化的时候的cash和history输入
        # :param [list] cash:              可用现金  默认 是 初始资产  list 类型
        # :param [list] history:           交易历史
        """
        super().__init__()
        # warnings.warn('QUANTAXIS 1.0.46 has changed the init_assets ==> init_cash, please pay attention to this change if you using init_cash to initial an account class,\
        #         ', DeprecationWarning, stacklevel=2)
        self._history_headers = ['datetime', 'code', 'price',
                                 'amount', 'cash', 'order_id', 'realorder_id', 'trade_id',
                                 'account_cookie', 'commission', 'tax', 'message']
        ########################################################################
        # 信息类:
        self.strategy_name = strategy_name
        self.user_cookie = user_cookie
        self.portfolio_cookie = portfolio_cookie
        self.account_cookie = QA_util_random_with_topic(
            'Acc') if account_cookie is None else account_cookie

        self.market_type = market_type
        self.broker = broker
        self.frequence = frequence
        self.running_environment = running_environment
        ########################################################################
        self.market_data = None
        self._currenttime = None
        self.commission_coeff = commission_coeff
        self.tax_coeff = tax_coeff
        self.datetime = None
        self.running_time = datetime.datetime.now()
        self.quantaxis_version = __version__
        ########################################################################
        # 资产类
        self.orders = QA_OrderQueue()  # 历史委托单
        self.init_cash = init_cash
        self.init_hold = pd.Series(init_hold, name='amount') if isinstance(
            init_hold, dict) else init_hold
        self.init_hold.index.name = 'code'
        self.cash = [self.init_cash]
        self.cash_available = self.cash[-1]    # 可用资金
        self.sell_available = copy.deepcopy(self.init_hold)
        self.buy_available = copy.deepcopy(self.init_hold)
        self.history = []
        self.time_index = []
        ########################################################################
        # 规则类
        # 1.是否允许t+0 及买入及结算
        # 2.是否允许卖空开仓
        # 3.是否允许保证金交易/ 如果不是false 就需要制定保证金比例(dict形式)

        # 期货: allow_t0 True allow_sellopen True
        #
        self.allow_t0 = allow_t0
        self.allow_sellopen = allow_sellopen
        self.margin_level = margin_level

    def __repr__(self):
        return '< QA_Account {}>'.format(self.account_cookie)

    @property
    def message(self):
        'the standard message which can be transfer'
        return {
            'source': 'account',
            'account_cookie': self.account_cookie,
            'portfolio_cookie': self.portfolio_cookie,
            'user_cookie': self.user_cookie,
            'broker': self.broker,
            'market_type': self.market_type,
            'strategy_name': self.strategy_name,
            'current_time': str(self._currenttime),
            'allow_sellopen': self.allow_sellopen,
            'allow_t0': self.allow_t0,
            'margin_level': self.margin_level,
            'init_assets': self.init_assets,
            'commission_coeff': self.commission_coeff,
            'tax_coeff': self.tax_coeff,
            'cash': self.cash,
            'history': self.history,
            'trade_index': self.time_index,
            'running_time': str(datetime.datetime.now()) if self.running_time is None else str(self.running_time),
            'quantaxis_version': self.quantaxis_version,
            'running_environment': self.running_environment,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

    @property
    def init_hold_with_account(self):
        """带account_id的初始化持仓

        Returns:
            [type] -- [description]
        """

        return self.init_hold.reset_index().assign(account_cookie=self.account_cookie).set_index(['code', 'account_cookie'])

    @property
    def init_assets(self):
        """初始化账户资产

        Returns:
            dict -- 2keys-cash,hold
        """

        return {
            'cash': self.init_cash,
            'hold': self.init_hold.to_dict()
        }

    @property
    def code(self):
        """
        该账户曾交易代码 用set 去重
        """
        return list(set([item[1] for item in self.history]))

    @property
    def date(self):
        """账户运行的日期

        Arguments:
            self {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        if self.datetime is not None:
            return str(self.datetime)[0:10]
        else:
            return None

    @property
    def start_date(self):
        """账户的起始交易日期

        Raises:
            RuntimeWarning -- [description]

        Returns:
            [type] -- [description]
        """

        if len(self.time_index) > 0:
            return str(min(self.time_index))[0:10]
        else:
            raise RuntimeWarning(
                'QAACCOUNT: THIS ACCOUNT DOESNOT HAVE ANY TRADE')

    @property
    def end_date(self):
        """账户的交易结束日期

        Raises:
            RuntimeWarning -- [description]

        Returns:
            [type] -- [description]
        """

        if len(self.time_index) > 0:
            return str(max(self.time_index))[0:10]
        else:
            raise RuntimeWarning(
                'QAACCOUNT: THIS ACCOUNT DOESNOT HAVE ANY TRADE')

    @property
    def trade_range(self):
        return QA_util_get_trade_range(self.start_date, self.end_date)


    @property
    def trade_day(self):
        return list(pd.Series(self.time_index).apply(lambda x: str(x)[0:10]).unique())

    @property
    def history_table(self):
        '交易历史的table'
        if len(self.history)>0:
            lens=len(self.history[0])
        else:
            lens=len(self._history_headers)

        return pd.DataFrame(data=self.history, columns=self._history_headers[:lens]).sort_index()

    @property
    def cash_table(self):
        '现金的table'
        _cash = pd.DataFrame(data=[self.cash[1::], self.time_index], index=[
                             'cash', 'datetime']).T
        _cash = _cash.assign(date=_cash.datetime.apply(lambda x: pd.to_datetime(str(x)[0:10]))).assign(
            account_cookie=self.account_cookie)  # .sort_values('datetime')
        return _cash.set_index(['datetime', 'account_cookie'], drop=False)
        """
        实验性质
        @2018-06-09

        ## 对于账户持仓的分解

        1. 真实持仓hold:

        正常模式/TZero模式:
            hold = 历史持仓(init_hold)+ 初始化账户后发生的所有交易导致的持仓(hold_available)

        动态持仓(初始化账户后的持仓)hold_available:
            self.history 计算而得

        2. 账户的可卖额度(sell_available)

        正常模式:
            sell_available
                结算前: init_hold+ 买卖交易(卖-)
                结算后: init_hold+ 买卖交易(买+ 卖-)
        TZero模式:
            sell_available
                结算前: init_hold - 买卖交易占用的额度(abs(买+ 卖-))
                结算过程 是为了补平(等于让hold={})
                结算后: init_hold
        """
    @property
    def hold(self):
        """真实持仓
        """
        return pd.concat([self.init_hold, self.hold_available]).groupby('code').sum().replace(0, np.nan).dropna().sort_index()

    @property
    def hold_available(self):
        """可用持仓
        """
        return self.history_table.groupby('code').amount.sum().replace(0, np.nan).dropna().sort_index()

    # @property
    # def order_table(self):
    #     """return order trade list"""
    #     return self.orders.trade_list

    @property
    def trade(self):
        """每次交易的pivot表

        Returns:
            pd.DataFrame

            此处的pivot_table一定要用np.sum
        """

        return self.history_table.pivot_table(index=['datetime', 'account_cookie'], columns='code', values='amount', aggfunc=np.sum).fillna(0).sort_index()

    @property
    def daily_cash(self):
        '每日交易结算时的现金表'
        return self.cash_table.drop_duplicates(subset='date', keep='last').set_index(['date', 'account_cookie'], drop=False).sort_index()

    @property
    def daily_hold(self):
        '每日交易结算时的持仓表'
        data = self.trade.cumsum()
        if len(data) < 1:
            return None
        else:
            data = data.assign(account_cookie=self.account_cookie).assign(
                date=data.index.levels[0])
            data.date = data.date.apply(lambda x: str(x)[0:10])
            data = data.set_index(['date', 'account_cookie'])
            return data[~data.index.duplicated(keep='last')].sort_index()
    # 计算assets的时候 需要一个market_data=QA.QA_fetch_stock_day_adv(list(data.columns),data.index[0],data.index[-1])
    # (market_data.to_qfq().pivot('close')*data).sum(axis=1)+user_cookie.get_account(a_1).daily_cash.set_index('date').cash

    @property
    def latest_cash(self):
        'return the lastest cash 可用资金'
        return self.cash[-1]

    @property
    def current_time(self):
        'return current time (in backtest/real environment)'
        return self._currenttime

    def hold_table(self, datetime=None):
        "到某一个时刻的持仓 如果给的是日期,则返回当日开盘前的持仓"
        if datetime is None:
            hold_available = self.history_table.set_index(
                'datetime').sort_index().groupby('code').amount.sum().sort_index()
        else:
            hold_available = self.history_table.set_index('datetime').sort_index(
            ).loc[:datetime].groupby('code').amount.sum().sort_index()

        return pd.concat([self.init_hold, hold_available]).groupby('code').sum().sort_index().apply(lambda x: x if x > 0 else None).dropna()

    def hold_price(self, datetime=None):
        """计算持仓成本  如果给的是日期,则返回当日开盘前的持仓

        Keyword Arguments:
            datetime {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """

        def weights(x):
            if sum(x['amount']) != 0:
                return np.average(x['price'], weights=x['amount'], returned=True)
            else:
                return np.nan
        if datetime is None:
            return self.history_table.set_index('datetime', drop=False).sort_index().groupby('code').apply(weights).dropna()
        else:
            return self.history_table.set_index('datetime', drop=False).sort_index().loc[:datetime].groupby('code').apply(weights).dropna()

    # @property
    def hold_time(self, datetime=None):
        """持仓时间

        Keyword Arguments:
            datetime {[type]} -- [description] (default: {None})
        """

        def weights(x):
            if sum(x['amount']) != 0:
                return pd.Timestamp(self.datetime)-pd.to_datetime(x.datetime.max())
            else:
                return np.nan
        if datetime is None:
            return self.history_table.set_index('datetime', drop=False).sort_index().groupby('code').apply(weights).dropna()
        else:
            return self.history_table.set_index('datetime', drop=False).sort_index().loc[:datetime].groupby('code').apply(weights).dropna()

    def reset_assets(self, init_cash=None):
        'reset_history/cash/'
        self.sell_available = copy.deepcopy(self.init_hold)
        self.history = []
        self.init_cash = init_cash
        self.cash = [self.init_cash]
        self.cash_available = self.cash[-1]  # 在途资金

    def receive_simpledeal(self, code, trade_price, trade_amount, trade_towards, trade_time, message=None):
        """快速撮合成交接口
        
        Arguments:
            code {[type]} -- [description]
            trade_price {[type]} -- [description]
            trade_amount {[type]} -- [description]
            trade_towards {[type]} -- [description]
            trade_time {[type]} -- [description]
        
        Keyword Arguments:
            message {[type]} -- [description] (default: {None})
        """

        self.datetime = trade_time

        market_towards = 1 if trade_towards > 0 else -1
        trade_money = float(trade_price*trade_amount*market_towards)
        # trade_price
        if self.market_type == MARKET_TYPE.FUTURE_CN:
            # 期货不收税
            # 双边手续费 也没有最小手续费限制
            commission_fee = self.commission_coeff * \
                abs(trade_money)
            tax_fee = 0
        elif self.market_type == MARKET_TYPE.STOCK_CN:
            commission_fee = self.commission_coeff * \
                abs(trade_money)
            tax_fee = self.tax_coeff * \
                abs(trade_money)

        trade_money += (commission_fee+tax_fee)
        # print(self.cash[-1])
        if self.cash[-1] > trade_money:
            self.time_index.append(trade_time)
            # TODO: 目前还不支持期货的锁仓
            if self.allow_sellopen:
                if trade_towards in [ORDER_DIRECTION.BUY_OPEN, ORDER_DIRECTION.SELL_OPEN]:
                    # 开仓单占用现金
                    self.cash.append(self.cash[-1]-abs(trade_money))
                    self.cash_available = self.cash[-1]

                elif trade_towards in [ORDER_DIRECTION.BUY_CLOSE, ORDER_DIRECTION.SELL_CLOSE]:
                    # 平仓单释放现金
                    self.cash.append(self.cash[-1]+abs(trade_money))
                    self.cash_available = self.cash[-1]
            else:
                self.cash.append(self.cash[-1]-trade_money)
                self.cash_available = self.cash[-1]

            if self.allow_t0:

                self.sell_available[code] = self.sell_available.get(
                    code, 0)+trade_amount*market_towards
                self.buy_available = self.sell_available

            self.history.append([trade_time, code, trade_price, market_towards*trade_amount, self.cash[-1], None, None, None, self.account_cookie,
                                 commission_fee, tax_fee, message])

        else:
            # print(self.cash[-1])
            self.cash_available = self.cash[-1]
            #print('NOT ENOUGH MONEY FOR {}'.format(order_id))

    def receive_deal(self, code: str, trade_id: str, order_id: str, realorder_id: str, trade_price: float, trade_amount: int, trade_towards: int, trade_time: str, message=None):
        """更新deal

        Arguments:
            code {str} -- [description]
            trade_id {str} -- [description]
            order_id {str} -- [description]
            realorder_id {str} -- [description]
            trade_price {float} -- [description]
            trade_amount {int} -- [description]
            trade_towards {int} -- [description]
            trade_time {str} -- [description]

        Returns:
            [type] -- [description]
        """

        print('receive deal')

        trade_time = str(trade_time)
        code = str(code)
        trade_price = float(trade_price)
        trade_towards = int(trade_towards)
        realorder_id = str(realorder_id)
        trade_id = str(trade_id)
        trade_amount = int(trade_amount)
        order_id = str(order_id)

        market_towards = 1 if trade_towards > 0 else -1
        trade_money = trade_price*trade_amount*market_towards
        commission_fee = trade_money*self.commission_coeff

        if self.market_type == MARKET_TYPE.STOCK_CN:
            if trade_towards > 0:
                commission_fee = self.commission_coeff * \
                    abs(trade_money)

                commission_fee = 5 if commission_fee < 5 else commission_fee

                tax_fee = 0  # 买入不收印花税
                if self.allow_t0:

                    self.sell_available = self.hold
                    self.buy_available = self.hold

            else:
                commission_fee = self.commission_coeff * \
                    abs(trade_money)

                commission_fee = 5 if commission_fee < 5 else commission_fee

                tax_fee = self.tax_coeff * \
                    abs(trade_money)

            # self.trade_money = self.deal_price * \
            #     self.deal_amount + self.commission_fee + self.tax
        elif self.market_type == MARKET_TYPE.FUTURE_CN:
            # 期货不收税
            # 双边手续费 也没有最小手续费限制
            commission_fee = self.commission_coeff * \
                abs(trade_money)

            # commission_fee = 5 if commission_fee < 5 else commission_fee

            #self.commission_fee = 5 if commission_fee < 5 else commission_fee

            tax_fee = 0  # 买入不收印花税

        trade_money += (commission_fee+tax_fee)

        if self.cash[-1] > trade_money:
            self.time_index.append(trade_time)
            # TODO: 目前还不支持期货的锁仓
            if self.allow_sellopen:
                if trade_towards in [ORDER_DIRECTION.BUY_OPEN, ORDER_DIRECTION.SELL_OPEN]:
                    # 开仓单占用现金
                    self.cash.append(self.cash[-1]-abs(trade_money))
                    self.cash_available = self.cash[-1]
                elif trade_towards in [ORDER_DIRECTION.BUY_CLOSE, ORDER_DIRECTION.SELL_CLOSE]:
                    # 平仓单释放现金
                    self.cash.append(self.cash[-1]+abs(trade_money))
                    self.cash_available = self.cash[-1]
            else:
                self.cash.append(self.cash[-1]-trade_money)
                self.cash_available = self.cash[-1]

            self.history.append(
                [trade_time, code, trade_price, market_towards*trade_amount, self.cash[-1], order_id, realorder_id, trade_id, self.account_cookie,
                    commission_fee, tax_fee, message])
            if self.allow_t0:

                self.sell_available = self.hold
                self.buy_available = self.hold
        else:
            print(self.cash[-1])
            self.cash_available = self.cash[-1]
            print('NOT ENOUGH MONEY FOR {}'.format(
                order_id))

        self.datetime = trade_time

        # return self.message

    def send_order(self, code=None, amount=None, time=None, towards=None, price=None, money=None, order_model=None, amount_model=None):
        """
        ATTENTION CHANGELOG 1.0.28
        修改了Account的send_order方法, 区分按数量下单和按金额下单两种方式

        - AMOUNT_MODEL.BY_PRICE ==> AMOUNT_MODEL.BY_MONEY # 按金额下单
        - AMOUNT_MODEL.BY_AMOUNT # 按数量下单

        在按金额下单的时候,应给予 money参数
        在按数量下单的时候,应给予 amount参数

        python code:
        Account=QA.QA_Account()

        Order_bymoney=Account.send_order(code='000001',
                                        price=11,
                                        money=0.3*Account.cash_available,
                                        time='2018-05-09',
                                        towards=QA.ORDER_DIRECTION.BUY,
                                        order_model=QA.ORDER_MODEL.MARKET,
                                        amount_model=QA.AMOUNT_MODEL.BY_MONEY
                                        )

        Order_byamount=Account.send_order(code='000001',
                                        price=11,
                                        amount=100,
                                        time='2018-05-09',
                                        towards=QA.ORDER_DIRECTION.BUY,
                                        order_model=QA.ORDER_MODEL.MARKET,
                                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                        )

        :param code: 证券代码
        :param amount: 买卖 数量多数股
        :param time:  Timestamp 对象 下单时间
        :param towards: int , towards>0 买入 towards<0 卖出
        :param price: 买入，卖出 标的证券的价格
        :param money: 买卖 价格
        :param order_model: 类型 QA.ORDER_MODE
        :param amount_model:类型 QA.AMOUNT_MODEL
        :return:
        """

        assert code is not None and time is not None and towards is not None and order_model is not None and amount_model is not None

        # 🛠todo 移到Utils类中，  时间转换
        # date 字符串 2011-10-11 长度10
        date = str(time)[0:10] if len(str(time)) == 19 else str(time)
        # time 字符串 20011-10-11 09:02:00  长度 19
        time = str(time) if len(
            str(time)) == 19 else '{} 09:31:00'.format(str(time)[0:10])

        # 🛠todo 移到Utils类中，  amount_to_money 成交量转金额
        # BY_MONEY :: amount --钱 如10000元  因此 by_money里面 需要指定价格,来计算实际的股票数
        # by_amount :: amount --股数 如10000股
        # amount = amount if amount_model is AMOUNT_MODEL.BY_AMOUNT else int(
        #     money / (price*(1+self.commission_coeff)))

        amount = amount if amount_model is AMOUNT_MODEL.BY_AMOUNT else int(

            money / (price*(1+self.commission_coeff))/100) * 100

        # 🛠todo 移到Utils类中，  money_to_amount 金额转成交量
        money = amount * price * \
            (1+self.commission_coeff) if amount_model is AMOUNT_MODEL.BY_AMOUNT else money

        # amount_model = AMOUNT_MODEL.BY_AMOUNT

        # flag 判断买卖 数量和价格以及买卖方向是否正确
        flag = False

        assert (int(towards) != 0)
        if int(towards) in [1, 2, 3]:
            # 是买入的情况(包括买入.买开.买平)
            if self.cash_available >= money:

                if self.market_type is MARKET_TYPE.STOCK_CN:  # 如果是股票 买入的时候有100股的最小限制
                    amount = int(amount / 100) * 100

                if self.running_environment == RUNNING_ENVIRONMENT.TZERO:

                    if self.buy_available.get(code, 0) >= amount:
                        flag = True
                        self.cash_available -= money
                        self.buy_available[code] -= amount
                    else:
                        flag = False
                        print('T0交易买入超出限额')
                else:
                    self.cash_available -= money
                    flag = True
            else:
                # 如果有负持仓-- 允许卖空的时候
                if self.allow_sellopen and towards == 3:  # 多平
                    _hold = self.sell_available.get(code, 0)
                    left_amount = amount+_hold if _hold < 0 else amount
                    _money = float(left_amount * price + amount *
                                   price*self.commission_coeff)
                    if self.cash_available >= _money:
                        self.cash_available -= _money
                        flag = True
                else:

                    print('QAACCOUNT: 可用资金不足 cash_available {}  code {} time {} amount {} towards {}'.format(
                        self.cash_available, code, time, amount, towards))

        elif int(towards) in [-1, -2, -3]:
            # 是卖出的情况(包括卖出，卖出开仓allow_sellopen如果允许. 卖出平仓)
            # print(self.sell_available[code])
            _hold = self.sell_available.get(code, 0)  # _hold 是你的持仓

            # 如果你的hold> amount>0
            # 持仓数量>卖出数量
            if _hold >= amount:
                self.sell_available[code] -= amount
                #towards = ORDER_DIRECTION.SELL
                flag = True
            # 如果持仓数量<卖出数量

            else:

                # 如果是允许卖空开仓 实际计算时  先减去持仓(正持仓) 再计算 负持仓 就按原先的占用金额计算
                if self.allow_sellopen:

                    # left_amount = amount-_hold if _hold > 0 else amount  # 如果仓位是反的
                    # _money = float(left_amount * price + amount *
                    #                price*self.commission_coeff)
                    if towards == -2:  # 卖开
                        if self.cash_available >= money:  # 卖空的市值小于现金（有担保的卖空）， 不允许裸卖空
                            #self.cash_available -= money
                            flag = True
                        else:
                            print('sellavailable', _hold)
                            print('amount', amount)
                            print('aqureMoney', money)
                            print('cash', self.cash_available)
                            print("卖空资金不足/不允许裸卖空")
            # else:
            #     print('资金股份不足/不允许卖空开仓')

        if flag and amount > 0:
            _order = QA_Order(user_cookie=self.user_cookie, strategy=self.strategy_name, frequence=self.frequence,
                              account_cookie=self.account_cookie, code=code, market_type=self.market_type,
                              date=date, datetime=time, sending_time=time, callback=self.receive_deal,
                              amount=amount, price=price, order_model=order_model, towards=towards, money=money,
                              amount_model=amount_model, commission_coeff=self.commission_coeff, tax_coeff=self.tax_coeff)  # init
            # 历史委托order状态存储， 保存到 QA_Order 对象中的队列中
            self.datetime = time
            self.orders.insert_order(_order)
            return _order
        else:
            print('ERROR : CODE {} TIME {}  AMOUNT {} TOWARDS {}'.format(
                code, time, amount, towards))
            return False

    def cancel_order(self, order):
        if order.towards in [ORDER_DIRECTION.BUY, ORDER_DIRECTION.BUY_OPEN, ORDER_DIRECTION.BUY_CLOSE]:
            if order.amount_model is AMOUNT_MODEL.BY_MONEY:
                self.cash_available += order.money
            elif order.amount_model is AMOUNT_MODEL.BY_AMOUNT:
                self.cash_available += order.price*order.amount
        elif order.towards in [ORDER_DIRECTION.SELL, ORDER_DIRECTION.SELL_CLOSE, ORDER_DIRECTION.SELL_OPEN]:
            self.sell_available[order.code] += order.amount

        # self.sell_available[]
    @property
    def close_positions_order(self):
        """平仓单

        Raises:
            RuntimeError -- if ACCOUNT.RUNNING_ENVIRONMENT is NOT TZERO

        Returns:
            list -- list with order
        """

        order_list = []
        time = '{} 15:00:00'.format(self.date)
        if self.running_environment == RUNNING_ENVIRONMENT.TZERO:
            for code, amount in self.hold_available.iteritems():
                order = False
                if amount < 0:
                    # 先卖出的单子 买平
                    order = self.send_order(code=code, price=0, amount=abs(
                        amount), time=time, towards=ORDER_DIRECTION.BUY_CLOSE,
                        order_model=ORDER_MODEL.CLOSE, amount_model=AMOUNT_MODEL.BY_AMOUNT)
                elif amount > 0:
                    # 先买入的单子, 卖平
                    order = self.send_order(code=code, price=0, amount=abs(
                        amount), time=time, towards=ORDER_DIRECTION.SELL_CLOSE,
                        order_model=ORDER_MODEL.CLOSE, amount_model=AMOUNT_MODEL.BY_AMOUNT)
                if order:
                    order_list.append(order)
            return order_list
        else:
            raise RuntimeError('QAACCOUNT with {} environments cannot use this methods'.format(
                self.running_environment))

    def settle(self):
        '同步可用资金/可卖股票'

        if self.running_environment == RUNNING_ENVIRONMENT.TZERO and self.hold_available.sum() != 0:
            raise RuntimeError('QAACCOUNT: 该T0账户未当日仓位,请平仓 {}'.format(
                self.hold_available.to_dict()))
        self.sell_available = self.hold
        self.buy_available = self.hold
        self.datetime = '{} 09:30:00'.format(QA_util_get_next_day(
            self.date)) if self.date is not None else None

    def on_bar(self, event):
        '''
        策略事件
        :param event:
        :return:
        '''
        'while updating the market data'

        print("on_bar account {} ".format(
            self.account_cookie), event.market_data)

    def on_tick(self, event):
        '''
        策略事件
        :param event:
        :return:
        '''
        'on tick event'
        print("on_tick ", event.market_data)
        pass

    def from_message(self, message):
        """resume the account from standard message
        这个是从数据库恢复账户时需要的"""
        self.account_cookie = message.get('account_cookie', None)
        self.portfolio_cookie = message.get('portfolio_cookie', None)
        self.user_cookie = message.get('user_cookie', None)
        self.broker = message.get('broker', None)
        self.market_type = message.get('market_type', None)
        self.strategy_name = message.get('strategy_name', None)
        self._currenttime = message.get('current_time', None)
        self.allow_sellopen = message.get('allow_sellopen', False)
        self.allow_t0 = message.get('allow_t0', False)
        self.margin_level = message.get('margin_level', False)
        self.init_cash = message.get(
            'init_cash', message.get('init_assets', 1000000))  # 兼容修改
        self.commission_coeff = message.get('commission_coeff', 0.00015)
        self.tax_coeff = message.get('tax_coeff', 0.0015)
        self.history = message['history']
        self.cash = message['cash']
        self.time_index = message['trade_index']
        self.running_time = message.get('running_time', None)
        self.quantaxis_version = message.get('quantaxis_version', None)
        self.running_environment = message.get(
            'running_environment', RUNNING_ENVIRONMENT.BACKETEST)
        self.settle()
        return self

    @property
    def table(self):
        """
        打印出account的内容
        """
        return pd.DataFrame([self.message, ]).set_index('account_cookie', drop=False).T

    def run(self, event):
        '''
        这个方法是被 QA_ThreadEngine 处理队列时候调用的， QA_Task 中 do 方法调用 run （在其它线程中）
       'QA_WORKER method 重载'
        :param event: 事件类型 QA_Event
        :return:
        '''
        'QA_WORKER method'
        if event.event_type is ACCOUNT_EVENT.SETTLE:
            self.settle()

        # elif event.event_type is ACCOUNT_EVENT.UPDATE:
        #     self.receive_deal(event.message)
        elif event.event_type is ACCOUNT_EVENT.MAKE_ORDER:
            """generate order
            if callback callback the order
            if not return back the order
            """
            data = self.send_order(code=event.code, amount=event.amount, time=event.time,
                                   amount_model=event.amount_model, towards=event.towards,
                                   price=event.price, order_model=event.order_model)
            if event.callback:
                event.callback(data)
            else:
                return data
        elif event.event_type is ENGINE_EVENT.UPCOMING_DATA:
            """update the market_data
            1. update the inside market_data struct
            2. tell the on_bar methods
            """

            self._currenttime = event.market_data.datetime[0]
            if self.market_data is None:
                self.market_data = event.market_data
            else:
                self.market_data = self.market_data + event.market_data
            self.on_bar(event)

            if event.callback:
                event.callback(event)

    def save(self):
        """
        存储账户信息
        """
        save_account(self.message)

    def sync_account(self, sync_message):
        """同步账户

        Arguments:
            sync_message {[type]} -- [description]
        """

        self.init_hold = sync_message['hold_available']
        self.init_cash = sync_message['cash_available']

        self.sell_available = copy.deepcopy(self.init_hold)
        self.history = []
        self.cash = [self.init_cash]
        self.cash_available = self.cash[-1]  # 在途资金

    def change_cash(self, money):
        """
        外部操作|高危|
        """
        res = self.cash[-1]+money
        if res >= 0:
            # 高危操作
            self.cash[-1] = res

    def get_orders(self, if_today=True):
        '''
        返回当日委托/历史委托
        :param if_today: true 只返回今天的订单
        :return: QA_OrderQueue
        '''
        # 🛠todo 筛选其它不是今天的订单返回
        return self.orders

    def get_history(self, start, end):
        """返回历史成交

        Arguments:
            start {str} -- [description]
            end {str]} -- [description]
        """
        return self.history_table.set_index('datetime', drop=False).loc[slice(pd.Timestamp(start), pd.Timestamp(end))]


class Account_handler():
    def __init__(self):
        pass

    def get_account(self, message):
        pass


if __name__ == '__main__':
    account = QA_Account()
    # 创建一个account账户
