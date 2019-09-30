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
from QUANTAXIS.QAMarket.QAPosition import QA_Position, QA_PMS
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

# pylint: disable=old-style-class, too-few-public-methods


class QA_AccountPRO(QA_Worker):
    """QA_Account

    QAAccount

    在QAAccountPro/Position的模型中, Pos不负责OMS业务,因此, 需要使用AccPro的sendOrder来主导OMS模型


    一个简单的外部OMS

    POS 下单以后, 订单信息被AccPro接受, 并生成QA_Order
    基于QA_Order的成交 ==> receive_deal的回报模式, 记录history 更新POS的on_transaction
    """

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
        """

        :param [str] strategy_name:  策略名称
        :param [str] user_cookie:   用户cookie
        :param [str] portfolio_cookie: 组合cookie
        :param [str] account_cookie:   账户cookie

        :param [dict] init_hold         初始化时的股票资产
        :param [float] init_cash:         初始化资金
        :param [float] commission_coeff:  交易佣金 :默认 万2.5   float 类型
        :param [float] tax_coeff:         印花税   :默认 千1.5   float 类型

        :param [Bool] margin_level:      保证金比例 默认{}
        :param [Bool] allow_t0:          是否允许t+0交易  默认False
        :param [Bool] allow_sellopen:    是否允许卖空开仓  默认False
        :param [Bool] allow_margin:      是否允许保证金交易 默认False
        :param [Bool] auto_reload:       是否自动从数据库中同步数据
        :param [Bool] generated:         从哪里生成==> directed: 直接生成  portfolio: 组合生成


        ### 注意
        >>>>>>>>>>>>>
        在期货账户中:
        allow_t0/ allow_sellopen 是必须打开的

        allow_margin 是作为保证金账户的开关 默认关闭 可以打开 则按照market_preset中的保证金比例来计算
        具体可以参见: https://github.com/QUANTAXIS/QUANTAXIS/blob/master/EXAMPLE/test_backtest/FUTURE/TEST_%E4%BF%9D%E8%AF%81%E9%87%91%E8%B4%A6%E6%88%B7.ipynb

        >>>>>>>>>>>>>



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


        # 2018/11/9 修改保证金交易

        # 我们把冻结的保证金 看做是未来的已实现交易:
        # 如==> 当前的一手空单 认为是未来的卖出成交(已知价格 不知时间)
        # 因此我们如此对于保证金交易进行评估:
        # 账户买入:
        多单开仓:  cash 下降x 保证金增加x 增加一手未来的卖出合约(持仓)  ==> 平仓: cash上升 保证金恢复
        cash + frozen(平仓释放) + 未平仓位

        cash, available_cash

        frozen{
                RB1901: {
                        towards 2: {avg_money : xxx, amount: xxx, queue: collection.deque()},
                        towards -2: {avg_money, amount, queue: collection.deque()}
                        },
                IF1901: {
                        towards 2: {avg_money, amount,queue: collection.deque()},
                        towards -2: {avg_money, amount,queue: collection.deque()}
                }
            }
        }

        hold: {
            RB1901: {
                1, amount, # 多单待平仓
                -1, amount # 空单待平仓
            }
        }


        >>>>>>>>>>>>>>>>>>>>>>>>>

        init_hold面临的一个改进和问题:

        >> init_hold就是简化的position模型

        init_hold目前是一个类似这样的字段:

        {'000001':100}

        实际上我们需要对于他进行进一步的改进, 用以用于支持更多场景:


        {
        'code': 000001, #品种名称
        'instrument_id': 000001,
        'name': '中国平安', #
        'market_type': QA.MARKET_TYPE.STOCK_CN,
        'exchange_id': QA.EXCHANGE_ID.SZSE, #交易所ID
        'volume_short': 0, #空头持仓数量  
        'volume_long': 100,  #持仓数量

        'volume_long_today': 0,
        'volume_long_his': 1,
        'volume_long': 1,
        'volume_long_frozen_today': 0,
        'volume_long_frozen_his': 0,
        'volume_long_frozen': 0,
        'volume_short_today': 0,
        'volume_short_his: 0,
        'volume_short': 0,
        'volume_short_frozen_today': 0,
        'volume_short_frozen_his': 0,
        'volume_short_frozen': 0,

        'position_price_long': 9.5,   #多头成本价
        'position_cost_long': 9500,   # 多头成本
        'position_price_short': 0,
        'position_cost_short': 0,

        'open_price_long': 9.5,     #多头开仓价
        'open_cost_long': 9500,     #多头开仓成本
        'open_price_short': 0,      #空头开仓价
        'open_cost_short': 0,       #空头成本

        'margin_long': 0,       # 多头保证金
        'margin_short': 0,
        'margin': 0
         }

        AccPro 使用QA_Position来创建仓位管理

        - 当创建QA_Account的时候， 会从Positions库中查询并恢复新的Positions
        - 当申请创建一个新的分区的时候，Account会扣减一个额度(money_preset) 体现在cash/history中
        - 当删除一个poistion 释放额度
        - 策略会写入相应的position分区


        |           AccPro                         |

        |   MPMS  |     MPMS    | SPMS |  FREECASH |

        | POS POS | POS POS POS |  POS |           |


        """
        super().__init__()

        # warnings.warn('QUANTAXIS 1.0.46 has changed the init_assets ==> init_cash, please pay attention to this change if you using init_cash to initial an account class,\
        #         ', DeprecationWarning, stacklevel=2)
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
            'direction'  # 方向
        ]
        self._activity_headers = [
            'datetime',
            'activity',
            'event',
            ''
        ]
        self.activity = []
        ########################################################################
        # 信息类:

        if user_cookie is None or portfolio_cookie is None:
            raise RuntimeError('QUANTAXIS 1.3.0升级: 需要在创建Account的时候指定用户名/组合名')
        self.user_cookie = user_cookie
        self.strategy_name = strategy_name
        self.portfolio_cookie = portfolio_cookie
        self.account_cookie = QA_util_random_with_topic(
            'Acc'
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
        self.orders = QA_OrderQueue()       # 历史委托单
        self.PMS = QA_PMS()
        # self.risks = QA_RMS()
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
        self.pms = {}

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

        if auto_reload:
            self.reload()

    def __repr__(self):
        return '< QA_AccountPRO {} market: {}>'.format(
            self.account_cookie,
            self.market_type
        )

    @property
    def message(self):
        'the standard message which can be transfer'
        return {
            'source':
            'account',
            'frequence':
            self.frequence,
            'account_cookie':
            self.account_cookie,
            'portfolio_cookie':
            self.portfolio_cookie,
            'user_cookie':
            self.user_cookie,
            'broker':
            self.broker,
            'market_type':
            self.market_type,
            'strategy_name':
            self.strategy_name,
            'current_time':
            str(self._currenttime),
            'allow_sellopen':
            self.allow_sellopen,
            'allow_margin':
            self.allow_margin,
            'allow_t0':
            self.allow_t0,
            'margin_level':
            self.margin_level,
            'init_assets':
            self.init_assets,
            'init_cash':
            self.init_cash,
            'init_hold':
            self.init_hold.to_dict(),
            'commission_coeff':
            self.commission_coeff,
            'tax_coeff':
            self.tax_coeff,
            'cash':
            self.cash,
            'history':
            self.history,
            'trade_index':
            self.time_index_max,
            'running_time':
            str(datetime.datetime.now())
            if self.running_time is None else str(self.running_time),
            'quantaxis_version':
            self.quantaxis_version,
            'running_environment':
            self.running_environment,
            'start_date':
            self.start_date,
            'end_date':
            self.end_date,
            'frozen':
            self.frozen,
            'finished_id':
            self.finishedOrderid,
            'position_id':
            list(self.pms.keys())
        }

    @property
    def freecash_precent(self):
        """剩余资金比例

        Returns:
            float
        """

        return self.cash_available / self.init_cash

    def load_marketpreset(self):
        """加载市场表
        """

        self.market_preset = MARKET_PRESET()

    @property
    def init_hold_with_account(self):
        """带account_cookie的初始化持仓

        Returns:
            [type] -- [description]
        """

        return self.init_hold.reset_index().assign(
            account_cookie=self.account_cookie
        ).set_index(['code',
                     'account_cookie'])

    @property
    def init_assets(self):
        """初始化账户资产

        Returns:
            dict -- 2keys-cash,hold
        """

        return {'cash': self.init_cash, 'hold': self.init_hold.to_dict()}

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
    def positions(self):
        raise NotImplementedError

    @property
    def start_date(self):
        """账户的起始交易日期(只在回测中使用)

        Raises:
            RuntimeWarning -- [description]

        Returns:
            [type] -- [description]
        """
        if self.start_ == None:
            if len(self.time_index_max) > 0:
                return str(min(self.time_index_max))[0:10]
            else:
                print(
                    RuntimeWarning(
                        'QAACCOUNT: THIS ACCOUNT DOESNOT HAVE ANY TRADE'
                    )
                )
        else:
            return self.start_

    @property
    def end_date(self):
        """账户的交易结束日期(只在回测中使用)

        Raises:
            RuntimeWarning -- [description]

        Returns:
            [type] -- [description]
        """
        if self.start_ == None:
            if len(self.time_index_max) > 0:
                return str(max(self.time_index_max))[0:10]
            else:
                print(
                    RuntimeWarning(
                        'QAACCOUNT: THIS ACCOUNT DOESNOT HAVE ANY TRADE'
                    )
                )
        else:
            return self.end_

    @property
    def market_data(self):
        return self._market_data

    @property
    def trade_range(self):
        return QA_util_get_trade_range(self.start_date, self.end_date)

    @property
    def trade_range_max(self):
        if self.start_date < str(min(self.time_index_max))[0:10]:
            return QA_util_get_trade_range(self.start_date, self.end_date)
        else:
            return QA_util_get_trade_range(str(min(self.time_index_max))[0:10], str(max(self.time_index_max))[0:10])

    @property
    def time_index(self):
        if len(self.time_index_max):
            res_ = pd.DataFrame(self.time_index_max)
            res_.columns = (['datetime'])
            res_['date'] = [i[0:10] for i in res_['datetime']]
            res_ = res_[res_['date'].isin(self.trade_range)]
            return list(res_['datetime'])
        else:
            return self.time_index_max

    @property
    def history_min(self):
        if len(self.history):
            res_ = pd.DataFrame(self.history)
            res_['date'] = [i[0:10] for i in res_[0]]
            res_ = res_[res_['date'].isin(self.trade_range)]
            return np.array(res_.drop(['date'], axis=1)).tolist()
        else:
            return self.history

    @property
    def history_table_min(self):
        '区间交易历史的table'
        if len(self.history_min) > 0:
            lens = len(self.history_min[0])
        else:
            lens = len(self._history_headers)

        return pd.DataFrame(
            data=self.history_min,
            columns=self._history_headers[:lens]
        ).sort_index()

    @property
    def trade_day(self):
        return list(
            pd.Series(self.time_index_max).apply(
                lambda x: str(x)[0:10]).unique()
        )

    @property
    def history_table(self):
        '交易历史的table'
        if len(self.history) > 0:
            lens = len(self.history[0])
        else:
            lens = len(self._history_headers)

        return pd.DataFrame(
            data=self.history,
            columns=self._history_headers[:lens]
        ).sort_index()

    @property
    def today_trade_table(self):
        return pd.DataFrame(
            data=self.today_trade['current'],
            columns=self._history_headers
        ).sort_index()

    @property
    def cash_table(self):
        '现金的table'
        _cash = pd.DataFrame(
            data=[self.cash[1::],
                  self.time_index_max],
            index=['cash',
                   'datetime']
        ).T
        _cash = _cash.assign(
            date=_cash.datetime.apply(lambda x: pd.to_datetime(str(x)[0:10]))
        ).assign(account_cookie=self.account_cookie)                          # .sort_values('datetime')
        return _cash.set_index(['datetime', 'account_cookie'], drop=False)
        """
        实验性质
        @2018-06-09

        # 对于账户持仓的分解

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

    def create_position(self, code, money_preset):
        if self.cash_available > money_preset:
            pos = QA_Position(code=code, money_preset=money_preset, user_cookie=self.user_cookie,
                              portfolio_cookie=self.portfolio_cookie, account_cookie=self.account_cookie, auto_reload=True)
            self.pms[pos.position_id] = pos
            self.cash.append(self.cash[-1] - money_preset)
            self.cash_available = self.cash[-1]
            return pos
        else:
            return False

    def get_position(self, position_id):
        return self.pms.get(position_id, None)

    @property
    def hold(self):
        """真实持仓
        """
        return pd.concat(
            [self.init_hold,
             self.hold_available]
        ).groupby('code').sum().replace(0,
                                        np.nan).dropna().sort_index()

    @property
    def hold_available(self):
        """可用持仓
        """
        return self.history_table.groupby('code').amount.sum().replace(
            0,
            np.nan
        ).dropna().sort_index()

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

        return self.history_table.pivot_table(
            index=['datetime',
                   'account_cookie'],
            columns='code',
            values='amount',
            aggfunc=np.sum
        ).fillna(0).sort_index()

    @property
    def daily_cash(self):
        '每日交易结算时的现金表'
        res = self.cash_table.drop_duplicates(subset='date', keep='last')
        le = pd.DataFrame(pd.Series(data=None, index=pd.to_datetime(
            self.trade_range_max).set_names('date'), name='predrop'))
        ri = res.set_index('date')
        res_ = pd.merge(le, ri, how='left', left_index=True, right_index=True)
        res_ = res_.ffill().fillna(self.init_cash).drop(
            ['predrop', 'datetime', 'account_cookie'], axis=1).reset_index().set_index(['date'], drop=False).sort_index()
        res_ = res_[res_.index.isin(self.trade_range)]
        return res_

    @property
    def daily_hold(self):
        '每日交易结算时的持仓表'
        data = self.trade.cumsum()
        if len(data) < 1:
            return None
        else:
            # print(data.index.levels[0])
            data = data.assign(account_cookie=self.account_cookie).assign(
                date=pd.to_datetime(data.index.levels[0]).date
            )

            data.date = pd.to_datetime(data.date)
            data = data.set_index(['date', 'account_cookie'])
            res = data[~data.index.duplicated(keep='last')].sort_index()
            # 这里会导致股票停牌时的持仓也被计算 但是计算market_value的时候就没了
            le = pd.DataFrame(pd.Series(data=None, index=pd.to_datetime(
                self.trade_range_max).set_names('date'), name='predrop'))
            ri = res.reset_index().set_index('date')
            res_ = pd.merge(le, ri, how='left',
                            left_index=True, right_index=True)
            res_ = res_.ffill().fillna(0).drop(
                ['predrop', 'account_cookie'], axis=1).reset_index().set_index(['date']).sort_index()
            res_ = res_[res_.index.isin(self.trade_range)]
            return res_

    @property
    def daily_frozen(self):
        '每日交易结算时的持仓表'
        res_ = self.history_table.assign(date=pd.to_datetime(self.history_table.datetime)).set_index(
            'date').resample('D').frozen.last().fillna(method='pad')
        res_ = res_[res_.index.isin(self.trade_range)]
        return res_

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
                'datetime'
            ).sort_index().groupby('code').amount.sum().sort_index()
        else:
            hold_available = self.history_table.set_index(
                'datetime'
            ).sort_index().loc[:datetime].groupby('code'
                                                  ).amount.sum().sort_index()

        return pd.concat([self.init_hold,
                          hold_available]).groupby('code').sum().sort_index(
        ).apply(lambda x: x if x > 0 else None).dropna()

    def current_hold_price(self):
        """计算目前持仓的成本  用于模拟盘和实盘查询

        Returns:
            [type] -- [description]
        """

        def weights(x):
            n = len(x)
            res = 1
            while res > 0 or res < 0:
                res = sum(x[:n]['amount'])
                n = n-1

            x = x[n+1:]

            if sum(x['amount']) != 0:
                return np.average(
                    x['price'],
                    weights=x['amount'],
                    returned=True
                )
            else:
                return np.nan
        return self.history_table.set_index(
            'datetime',
            drop=False
        ).sort_index().groupby('code').apply(weights).dropna()

    def hold_price(self, datetime=None):
        """计算持仓成本  如果给的是日期,则返回当日开盘前的持仓

        Keyword Arguments:
            datetime {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """

        def weights(x):
            if sum(x['amount']) != 0:
                return np.average(
                    x['price'],
                    weights=x['amount'],
                    returned=True
                )
            else:
                return np.nan

        if datetime is None:
            return self.history_table.set_index(
                'datetime',
                drop=False
            ).sort_index().groupby('code').apply(weights).dropna()
        else:
            return self.history_table.set_index(
                'datetime',
                drop=False
            ).sort_index().loc[:datetime].groupby('code').apply(weights
                                                                ).dropna()

    # @property
    def hold_time(self, datetime=None):
        """持仓时间

        Keyword Arguments:
            datetime {[type]} -- [description] (default: {None})
        """

        def weights(x):
            if sum(x['amount']) != 0:
                return pd.Timestamp(self.datetime
                                    ) - pd.to_datetime(x.datetime.max())
            else:
                return np.nan

        if datetime is None:
            return self.history_table.set_index(
                'datetime',
                drop=False
            ).sort_index().groupby('code').apply(weights).dropna()
        else:
            return self.history_table.set_index(
                'datetime',
                drop=False
            ).sort_index().loc[:datetime].groupby('code').apply(weights
                                                                ).dropna()

    def reset_assets(self, init_cash=None):
        'reset_history/cash/'
        self.sell_available = copy.deepcopy(self.init_hold)
        self.history = []
        self.init_cash = init_cash
        self.cash = [self.init_cash]
        self.cash_available = self.cash[-1]  # 在途资金

    def receive_simpledeal(
            self,
            code,
            trade_price,
            trade_amount,
            trade_towards,
            trade_time,
            message=None,
            order_id=None,
            trade_id=None,
            realorder_id=None
    ):
        """快速撮合成交接口


        此接口是一个直接可以成交的接口, 所以务必确保给出的信息是可以成交的

        此接口涉及的是
        1. 股票/期货的成交
        2. 历史记录的增加
        3. 现金/持仓/冻结资金的处理

        Arguments:
            code {[type]} -- [description]
            trade_price {[type]} -- [description]
            trade_amount {[type]} -- [description]
            trade_towards {[type]} -- [description]
            trade_time {[type]} -- [description]

        Keyword Arguments:
            message {[type]} -- [description] (default: {None})


        2018/11/7 @yutiansut
        修复一个bug: 在直接使用该快速撮合接口的时候, 期货卖出会扣减保证金, 买回来的时候应该反算利润

        如 3800卖空 3700买回平仓  应为100利润
        @2018-12-31 保证金账户ok


        @2019/1/3 一些重要的意思
        frozen = self.market_preset.get_frozen(code) # 保证金率
        unit = self.market_preset.get_unit(code)  # 合约乘数
        raw_trade_money = trade_price*trade_amount*market_towards  # 总市值
        value = raw_trade_money * unit  # 合约总价值
        trade_money = value * frozen    # 交易保证金
        """

        self.datetime = trade_time
        if realorder_id in self.finishedOrderid:
            pass
        else:
            self.finishedOrderid.append(realorder_id)

        market_towards = 1 if trade_towards > 0 else -1
        # value 合约价值 unit 合约乘数
        if self.allow_margin:
            frozen = self.market_preset.get_frozen(
                code)                  # 保证金率
            unit = self.market_preset.get_unit(
                code)                      # 合约乘数
            raw_trade_money = trade_price * trade_amount * market_towards  # 总市值
            value = raw_trade_money * unit                                # 合约总价值
            trade_money = value * frozen                                  # 交易保证金
        else:
            trade_money = trade_price * trade_amount * market_towards
            raw_trade_money = trade_money
            value = trade_money
            unit = 1
            frozen = 1
            # 计算费用
            # trade_price

        if self.market_type == MARKET_TYPE.FUTURE_CN:
            # 期货不收税
            # 双边手续费 也没有最小手续费限制

            commission_fee_preset = self.market_preset.get_code(code)
            if trade_towards in [ORDER_DIRECTION.BUY_OPEN,
                                 ORDER_DIRECTION.BUY_CLOSE,
                                 ORDER_DIRECTION.SELL_CLOSE,
                                 ORDER_DIRECTION.SELL_OPEN]:
                commission_fee = commission_fee_preset['commission_coeff_pervol'] * trade_amount + \
                    commission_fee_preset['commission_coeff_peramount'] * \
                    abs(value)
            elif trade_towards in [ORDER_DIRECTION.BUY_CLOSETODAY,
                                   ORDER_DIRECTION.SELL_CLOSETODAY]:
                commission_fee = commission_fee_preset['commission_coeff_today_pervol'] * trade_amount + \
                    commission_fee_preset['commission_coeff_today_peramount'] * \
                    abs(value)

            tax_fee = 0  # 买入不收印花税
        elif self.market_type == MARKET_TYPE.STOCK_CN:

            commission_fee = self.commission_coeff * \
                abs(trade_money)

            commission_fee = 5 if commission_fee < 5 else commission_fee
            if int(trade_towards) > 0:
                tax_fee = 0  # 买入不收印花税
            else:
                tax_fee = self.tax_coeff * abs(trade_money)

        # 结算交易
        if self.cash[-1] > trade_money + commission_fee + tax_fee:
            self.time_index_max.append(trade_time)
            # TODO: 目前还不支持期货的锁仓
            if self.allow_sellopen:
                if trade_towards in [ORDER_DIRECTION.BUY_OPEN,
                                     ORDER_DIRECTION.SELL_OPEN]:
                    # 开仓单占用现金 计算avg
                    # 初始化
                    if code in self.frozen.keys():
                        if trade_towards in self.frozen[code].keys():
                            pass
                        else:
                            self.frozen[code][str(trade_towards)] = {
                                'money': 0,
                                'amount': 0,
                                'avg_price': 0
                            }
                    else:
                        self.frozen[code] = {
                            str(ORDER_DIRECTION.BUY_OPEN): {
                                'money': 0,
                                'amount': 0,
                                'avg_price': 0
                            },
                            str(ORDER_DIRECTION.SELL_OPEN): {
                                'money': 0,
                                'amount': 0,
                                'avg_price': 0
                            }
                        }
                    """[summary]
                    # frozen的计算
                    # money 冻结的资金
                    # amount  冻结的数量

                    2018-12-31                    

                    """

                    self.frozen[code][str(trade_towards)]['money'] = (
                        (
                            self.frozen[code][str(trade_towards)]['money'] *
                            self.frozen[code][str(trade_towards)]['amount']
                        ) + abs(trade_money)
                    ) / (
                        self.frozen[code][str(trade_towards)]['amount'] +
                        trade_amount
                    )
                    self.frozen[code][str(trade_towards)]['avg_price'] = (
                        (
                            self.frozen[code][str(trade_towards)]['avg_price'] *
                            self.frozen[code][str(trade_towards)]['amount']
                        ) + abs(raw_trade_money)
                    ) / (
                        self.frozen[code][str(trade_towards)]['amount'] +
                        trade_amount
                    )
                    self.frozen[code][str(trade_towards)
                                      ]['amount'] += trade_amount

                    self.cash.append(
                        self.cash[-1] - abs(trade_money) - commission_fee -
                        tax_fee
                    )
                elif trade_towards in [ORDER_DIRECTION.BUY_CLOSE, ORDER_DIRECTION.BUY_CLOSETODAY,
                                       ORDER_DIRECTION.SELL_CLOSE, ORDER_DIRECTION.SELL_CLOSETODAY]:
                    # 平仓单释放现金
                    # if trade_towards == ORDER_DIRECTION.BUY_CLOSE:
                    # 卖空开仓 平仓买入
                    # self.cash
                    # 买入平仓  之前是空开
                    if trade_towards in [ORDER_DIRECTION.BUY_CLOSE, ORDER_DIRECTION.BUY_CLOSETODAY]:
                                                                    # self.frozen[code][ORDER_DIRECTION.SELL_OPEN]['money'] -= trade_money
                        self.frozen[code][str(ORDER_DIRECTION.SELL_OPEN)
                                          ]['amount'] -= trade_amount

                        frozen_part = self.frozen[code][
                            str(ORDER_DIRECTION.SELL_OPEN)]['money'] * trade_amount
                        # 账户的现金+ 冻结的的释放 + 买卖价差* 杠杆
                        self.cash.append(
                            self.cash[-1] + frozen_part +
                            (frozen_part - trade_money) / frozen -
                            commission_fee - tax_fee
                        )
                        if self.frozen[code][str(ORDER_DIRECTION.SELL_OPEN)
                                             ]['amount'] == 0:
                            self.frozen[code][str(ORDER_DIRECTION.SELL_OPEN)
                                              ]['money'] = 0
                            self.frozen[code][str(ORDER_DIRECTION.SELL_OPEN)
                                              ]['avg_price'] = 0

                    # 卖出平仓  之前是多开
                    elif trade_towards in [ORDER_DIRECTION.SELL_CLOSE, ORDER_DIRECTION.SELL_CLOSETODAY]:
                                                                      # self.frozen[code][ORDER_DIRECTION.BUY_OPEN]['money'] -= trade_money
                        self.frozen[code][str(ORDER_DIRECTION.BUY_OPEN)
                                          ]['amount'] -= trade_amount

                        frozen_part = self.frozen[code][str(ORDER_DIRECTION.BUY_OPEN)
                                                        ]['money'] * trade_amount
                        self.cash.append(
                            self.cash[-1] + frozen_part +
                            (abs(trade_money) - frozen_part) / frozen -
                            commission_fee - tax_fee
                        )
                        if self.frozen[code][str(ORDER_DIRECTION.BUY_OPEN)
                                             ]['amount'] == 0:
                            self.frozen[code][str(ORDER_DIRECTION.BUY_OPEN)
                                              ]['money'] = 0
                            self.frozen[code][str(ORDER_DIRECTION.BUY_OPEN)
                                              ]['avg_price'] = 0
            else:  # 不允许卖空开仓的==> 股票

                self.cash.append(
                    self.cash[-1] - trade_money - tax_fee - commission_fee
                )
            if self.allow_t0 or trade_towards == ORDER_DIRECTION.SELL:
                self.sell_available[code] = self.sell_available.get(
                    code,
                    0
                ) + trade_amount * market_towards
                self.buy_available = self.sell_available

            self.cash_available = self.cash[-1]
            frozen_money = abs(trade_money) if trade_towards in [
                ORDER_DIRECTION.BUY_OPEN,
                ORDER_DIRECTION.SELL_OPEN
            ] else 0
            self.history.append(
                [
                    str(trade_time),
                    code,
                    trade_price,
                    market_towards * trade_amount,
                    self.cash[-1],
                    order_id,
                    realorder_id,
                    trade_id,
                    self.account_cookie,
                    commission_fee,
                    tax_fee,
                    message,
                    frozen_money,
                    trade_towards
                ]
            )

        else:
            print('ALERT MONEY NOT ENOUGH!!!')
            print(self.cash[-1])
            self.cash_available = self.cash[-1]
            #print('NOT ENOUGH MONEY FOR {}'.format(order_id))

    def receive_deal(
            self,
            code: str,
            trade_id: str,
            order_id: str,
            realorder_id: str,
            trade_price: float,
            trade_amount: int,
            trade_towards: int,
            trade_time: str,
            message=None
    ):
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

        print('QAACCOUNTPRO ==> receive deal')

        trade_time = str(trade_time)
        code = str(code)
        trade_price = float(trade_price)
        trade_towards = int(trade_towards)
        realorder_id = str(realorder_id)
        trade_id = str(trade_id)
        trade_amount = int(trade_amount)
        order_id = str(order_id)

        market_towards = 1 if trade_towards > 0 else -1
        """2019/01/03 直接使用快速撮合接口了
        2019/05/13 使用 PMS来更新成交记录
        """
        self.pms[self.oms[order_id]['positon_id']].on_transaction(
            {'towards': trade_towards,
             'code': code,
             'trade_id': trade_id,
             'amount': trade_amount,
             'time': trade_time,
             'price': trade_price}
        )

        self.receive_simpledeal(
            code,
            trade_price,
            trade_amount,
            trade_towards,
            trade_time,
            message=message,
            order_id=order_id,
            trade_id=trade_id,
            realorder_id=realorder_id
        )

    def send_order(
            self,
            code=None,
            amount=None,
            time=None,
            towards=None,
            price=None,
            money=None,
            order_model=None,
            amount_model=None,
            order_id=None,
            position_id=None,
            *args,
            **kwargs
    ):
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
        :return:  QA_Order | False

        @2018/12/23
        send_order 是QA的标准返回, 如需对接其他接口, 只需要对于QA_Order做适配即可


        @2018/12/27
        在判断账户为期货账户(及 允许双向交易)

        @2018/12/30 保证金账户的修改
        1. 保证金账户冻结的金额
        2. 保证金账户的结算
        3. 保证金账户的判断

        """
        wrong_reason = None
        assert code is not None and time is not None and towards is not None and order_model is not None and amount_model is not None

        # 🛠todo 移到Utils类中，  时间转换
        # date 字符串 2011-10-11 长度10
        date = str(time)[0:10] if len(str(time)) == 19 else str(time)
        # time 字符串 20011-10-11 09:02:00  长度 19
        time = str(time) if len(str(time)) == 19 else '{} 09:31:00'.format(
            str(time)[0:10]
        )

        # 🛠todo 移到Utils类中，  amount_to_money 成交量转金额
        # BY_MONEY :: amount --钱 如10000元  因此 by_money里面 需要指定价格,来计算实际的股票数
        # by_amount :: amount --股数 如10000股

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
                        _hold = self.sell_available.get(code, 0)
                        # 假设有负持仓:
                        # amount为下单数量 如  账户原先-3手 现在平1手

                        #left_amount = amount+_hold if _hold < 0 else amount
                        _money = abs(
                            float(amount * price * (1 + self.commission_coeff))
                        )

                        print(_hold)
                        if self.cash_available >= _money:
                            if _hold < 0:
                                self.cash_available -= _money

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
            _hold = self.sell_available.get(code, 0)  # _hold 是你的持仓

            # 如果你的hold> amount>0
            # 持仓数量>卖出数量
            if _hold >= amount:
                self.sell_available[code] -= amount
                # towards = ORDER_DIRECTION.SELL
                flag = True
            # 如果持仓数量<卖出数量
            else:

                # 如果是允许卖空开仓 实际计算时  先减去持仓(正持仓) 再计算 负持仓 就按原先的占用金额计算
                if self.allow_sellopen and towards == -2:

                    if self.cash_available >= money:  # 卖空的市值小于现金（有担保的卖空）， 不允许裸卖空
                                                     # self.cash_available -= money
                        flag = True
                    else:
                        print('sellavailable', _hold)
                        print('amount', amount)
                        print('aqureMoney', money)
                        print('cash', self.cash_available)
                        wrong_reason = "卖空资金不足/不允许裸卖空"
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
                callback=self.receive_deal,
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

    def cancel_order(self, order):
        if order.towards in [ORDER_DIRECTION.BUY,
                             ORDER_DIRECTION.BUY_OPEN,
                             ORDER_DIRECTION.BUY_CLOSE]:
            if order.amount_model is AMOUNT_MODEL.BY_MONEY:
                self.cash_available += order.money
            elif order.amount_model is AMOUNT_MODEL.BY_AMOUNT:
                self.cash_available += order.price * order.amount
        elif order.towards in [ORDER_DIRECTION.SELL,
                               ORDER_DIRECTION.SELL_CLOSE,
                               ORDER_DIRECTION.SELL_OPEN]:
            self.sell_available[order.code] += order.amount

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
                    order = self.send_order(
                        code=code,
                        price=0,
                        amount=abs(amount),
                        time=time,
                        towards=ORDER_DIRECTION.BUY,
                        order_model=ORDER_MODEL.CLOSE,
                        amount_model=AMOUNT_MODEL.BY_AMOUNT,
                    )
                elif amount > 0:
                    # 先买入的单子, 卖平
                    order = self.send_order(
                        code=code,
                        price=0,
                        amount=abs(amount),
                        time=time,
                        towards=ORDER_DIRECTION.SELL,
                        order_model=ORDER_MODEL.CLOSE,
                        amount_model=AMOUNT_MODEL.BY_AMOUNT
                    )
                if order:
                    order_list.append(order)
            return order_list
        else:
            raise RuntimeError(
                'QAACCOUNT with {} environments cannot use this methods'.format(
                    self.running_environment
                )
            )

    def settle(self, settle_data=None):
        """
        股票/期货的日结算

        股票的结算:  结转股票可卖额度
        T0的结算: 结转T0的额度

        期货的结算: 结转静态资金


        @2019-02-25 yutiansut
        hold 在下面要进行大变化:

        从 只计算数量 ==> 数量+成本+买入价 (携带更多信息)

        基于history去计算hold ==> last_settle+ today_pos_change

        """
        #print('FROM QUANTAXIS QA_ACCOUNT: account settle')
        if self.running_environment == RUNNING_ENVIRONMENT.TZERO and self.hold_available.sum(
        ) != 0:
            raise RuntimeError(
                'QAACCOUNT: 该T0账户未当日仓位,请平仓 {}'.format(
                    self.hold_available.to_dict()
                )
            )
        if self.market_type == MARKET_TYPE.FUTURE_CN:
            # 增加逐日盯市制度

            self.static_balance['frozen'].append(
                sum(
                    [
                        rx['money'] * rx['amount']
                        for var in self.frozen.values()
                        for rx in var.values()
                    ]
                )
            )

            self.static_balance['cash'].append(self.cash[-1])
            self.static_balance['hold'].append(self.hold.to_dict())
            self.static_balance['date'].append(self.date)
            """静态权益的结算

            只关心开仓价/ 不做盯市制度

            动态权益的结算需要关心

            """

            self.static_balance['static_assets'].append(
                self.static_balance['cash'][-1] +
                self.static_balance['frozen'][-1]
            )

        self.sell_available = self.hold
        self.buy_available = self.hold
        self.cash_available = self.cash[-1]
        self.datetime = '{} 09:30:00'.format(
            QA_util_get_next_day(self.date)
        ) if self.date is not None else None

    def on_bar(self, event):
        '''
        策略事件
        :param event:
        :return:
        '''
        'while updating the market data'

        print(
            "on_bar account {} ".format(self.account_cookie),
            event.market_data.data
        )
        print(event.send_order)
        try:
            for code in event.market_data.code:

                if self.sell_available.get(code, 0) > 0:
                    print('可以卖出 {}'.format(self._currenttime))
                    event.send_order(
                        account_cookie=self.account_cookie,
                        amount=self.sell_available[code],
                        amount_model=AMOUNT_MODEL.BY_AMOUNT,
                        time=self.current_time,
                        code=code,
                        price=0,
                        order_model=ORDER_MODEL.MARKET,
                        towards=ORDER_DIRECTION.SELL,
                        market_type=self.market_type,
                        frequence=self.frequence,
                        broker_name=self.broker
                    )
                else:
                    print('{} 无仓位, 买入{}'.format(self._currenttime, code))
                    event.send_order(
                        account_cookie=self.account_cookie,
                        amount=100,
                        amount_model=AMOUNT_MODEL.BY_AMOUNT,
                        time=self.current_time,
                        code=code,
                        price=0,
                        order_model=ORDER_MODEL.MARKET,
                        towards=ORDER_DIRECTION.BUY,
                        market_type=self.market_type,
                        frequence=self.frequence,
                        broker_name=self.broker
                    )
        except Exception as e:
            print(e)

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
        self.allow_margin = message.get('allow_margin', False)
        self.allow_t0 = message.get('allow_t0', False)
        self.margin_level = message.get('margin_level', False)
        self.frequence = message.get(
            'frequence', FREQUENCE.FIFTEEN_MIN)  # 默认15min
        self.init_cash = message.get(
            'init_cash',
            message.get('init_assets',
                        1000000)
        )                                       # 兼容修改
        self.init_hold = pd.Series(message.get('init_hold', {}), name='amount')
        self.init_hold.index.name = 'code'
        self.commission_coeff = message.get('commission_coeff', 0.00015)
        self.tax_coeff = message.get('tax_coeff', 0.0015)
        self.history = message['history']
        self.cash = message['cash']
        self.time_index_max = message['trade_index']
        self.running_time = message.get('running_time', None)
        self.quantaxis_version = message.get('quantaxis_version', None)
        self.running_environment = message.get(
            'running_environment',
            RUNNING_ENVIRONMENT.BACKETEST
        )
        self.frozen = message.get('frozen', {})
        self.finishedOrderid = message.get('finished_id', [])
        pos_id = message.get('position_id', [])
        print(pos_id)
        self.pms = dict(zip(pos_id, [QA_Position(position_id=item,
                                                 account_cookie=self.account_cookie, portfolio_cookie=self.portfolio_cookie,
                                                 user_cookie=self.user_cookie, auto_reload=True) for item in pos_id]))

        self.settle()
        return self

    def from_otgdict(self, message):
        """[summary]
        balance = static_balance + float_profit


            "currency": "",  # "CNY" (币种)
            "pre_balance": float("nan"),  # 9912934.78 (昨日账户权益)
            "static_balance": float("nan"),  # (静态权益)
            "balance": float("nan"),  # 9963216.55 (账户权益)
            "available": float("nan"),  # 9480176.15 (可用资金)
            "float_profit": float("nan"),  # 8910.0 (浮动盈亏)
            "position_profit": float("nan"),  # 1120.0(持仓盈亏)
            "close_profit": float("nan"),  # -11120.0 (本交易日内平仓盈亏)
            "frozen_margin": float("nan"),  # 0.0(冻结保证金)
            "margin": float("nan"),  # 11232.23 (保证金占用)
            "frozen_commission": float("nan"),  # 0.0 (冻结手续费)
            "commission": float("nan"),  # 123.0 (本交易日内交纳的手续费)
            "frozen_premium": float("nan"),  # 0.0 (冻结权利金)
            "premium": float("nan"),  # 0.0 (本交易日内交纳的权利金)
            "deposit": float("nan"),  # 1234.0 (本交易日内的入金金额)
            "withdraw": float("nan"),  # 890.0 (本交易日内的出金金额)
            "risk_ratio": float("nan"),  # 0.048482375 (风险度)
        """

        self.allow_margin = True
        self.allow_sellopen = True
        self.allow_t0 = True

        self.account_cookie = message['accounts']['user_id']
        # 可用资金
        self.cash_available = message['accounts']['available']
        self.balance = message['accounts']['balance']

        # 都是在结算的时候计算的
        # 昨日权益/静态权益 ==> 这两个是一样的
        self.static_balance = message['accounts']['static_balance']
        self.pre_balance = message['accounts']['pre_balance']

        # 平仓盈亏
        self.close_profit = message['accounts']['close_profit']
        # 持仓盈亏
        self.position_profit = message['accounts']['position_profit']

        # 动态权益
        self.float_profit = message['accounts']['float_profit']

        # 占用保证金
        self.margin = message['accounts']['margin']

        self.commission = message['accounts']['commission']

    @property
    def table(self):
        """
        打印出account的内容
        """
        return pd.DataFrame([
            self.message,
        ]).set_index(
            'account_cookie',
            drop=False
        ).T

    def run(self, event):
        '''
        这个方法是被 QA_ThreadEngine 处理队列时候调用的， QA_Task 中 do 方法调用 run （在其它线程中）
       'QA_WORKER method 重载'
        :param event: 事件类型 QA_Event
        :return:
        '''
        'QA_WORKER method'
        if event.event_type is ACCOUNT_EVENT.SETTLE:
            print('account_settle')
            self.settle()

        # elif event.event_type is ACCOUNT_EVENT.UPDATE:
        #     self.receive_deal(event.message)
        elif event.event_type is ACCOUNT_EVENT.MAKE_ORDER:
            """generate order
            if callback callback the order
            if not return back the order
            """
            data = self.send_order(
                code=event.code,
                amount=event.amount,
                time=event.time,
                amount_model=event.amount_model,
                towards=event.towards,
                price=event.price,
                order_model=event.order_model
            )
            if event.callback:
                event.callback(data)
            else:
                return data
        elif event.event_type is ENGINE_EVENT.UPCOMING_DATA:
            """update the market_data
            1. update the inside market_data struct
            2. tell the on_bar methods

            # 这样有点慢


            """

            self._currenttime = event.market_data.datetime[0]
            if self._market_data is None:
                self._market_data = event.market_data
            else:
                self._market_data = self._market_data + event.market_data
            self.on_bar(event)

            if event.callback:
                event.callback(event)

    @property
    def positions_with_pos(self):
        return pd.DataFrame([item.curpos for item in self.pms.values()],
                            index=pd.MultiIndex.from_tuples([(item.code, item.position_id) for item in self.pms.values()], names=['code', 'pos_id']))
    @property
    def positions(self):
        return self.positions_with_pos.groupby('code').sum()

    @property
    def hold_detail_with_pos(self):
        return pd.DataFrame([item.hold_detail for item in self.pms.values()],
                            index=pd.MultiIndex.from_tuples([(item.code, item.position_id) for item in self.pms.values()], names=['code', 'pos_id']))
    @property
    def hold_detail(self):
        return self.hold_detail_with_pos.groupby('code').sum()

    def get_position(self, code):
        """基于QAPosition的联合查询

        Arguments:
            code {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        try:
            return self.positions.loc[code].to_dict()
        except KeyError:
            return {'volume_long': 0, 'volume_short': 0, 'volume_long_frozen':0, 'volume_short_frozen': 0}

    def get_position_with_pos(self, code, pos_id):
        """基于QAPosition的联合查询

        Arguments:
            code {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        try:
            return self.positions_with_pos.loc[(code, pos_id)].to_dict()
        except KeyError:
            return {'volume_long': 0, 'volume_short': 0}

    def get_holddetail(self, code):
        try:
            return self.hold_detail.loc[code].to_dict()
        except KeyError:
            return {'volume_long': 0,
                    'volume_long_his': 0,
                    'volume_long_today': 0,
                    'volume_short': 0,
                    'volume_short_his': 0,
                    'volume_short_today': 0}


    def save(self):
        """
        存储账户信息
        """
        save_account(self.message, self.client)

    def reload(self):

        message = self.client.find_one(
            {
                'account_cookie': self.account_cookie,
                'portfolio_cookie': self.portfolio_cookie,
                'user_cookie': self.user_cookie
            }
        )

        if message is None:
            self.client.insert(self.message)
        else:
            self.from_message(message)

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
        res = self.cash[-1] + money
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
        return self.history_table.set_index(
            'datetime',
            drop=False
        ).loc[slice(pd.Timestamp(start),
                    pd.Timestamp(end))]


class Account_handler():

    def __init__(self):
        pass

    def get_account(self, message):
        pass


if __name__ == '__main__':
    account = QA_Account()
    # 创建一个account账户
