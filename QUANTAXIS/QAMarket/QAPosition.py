#

from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, EXCHANGE_ID
from QUANTAXIS.QAARP.market_preset import MARKET_PRESET


class QA_Position():
    """一个持仓模型:/兼容股票期货/兼容保证金持仓

    兼容快期DIFF协议

    基础字段

    code [str]  品种名称 
    volume_long_today [float] 今仓 多单持仓
    volume_long_his   [float] 昨仓 多单持仓
    volume_short_today [float] 今仓 空单持仓
    volume_short_his  [float] 昨仓 空单持仓

    volume_long_frozen_his [float] 多单昨日冻结
    volume_long_frozen_today [float] 多单今日冻结
    volume_short_frozen_his [float] 空单昨日冻结
    volume_short_frozen_today [float] 空单今日冻结

    margin_long  [float] 多单保证金
    margin_short [float] 空单保证金

    open_price_long [float] 多单开仓价
    open_price_short [float] 空单开仓价
    position_price_long [float] 逐日盯市的前一交易日的结算价
    position_price_short [float] 逐日盯市的前一交易日的结算价

    open_cost_long [float] 多单开仓成本(指的是保证金冻结)
    open_cost_short [float] 空单开仓成本
    position_cost_long [float] 多单持仓成本(指的是基于逐日盯市制度下的成本价)
    position_cost_short [float] 空单持仓成本


    market_type=MARKET_TYPE.STOCK_CN [enum] 市场类别
    exchange_id=EXCHANGE_ID.SZSE [enum] 交易所id(支持股票/期货)
    name=None [str] 名称


    功能:

    1/ 支持当价格变化后的 持仓的自行计算更新
    2/ 支持调仓模型(未加入)
    3/ 支持仓位风控(未加入)

    """

    def __init__(self,
                 code='000001',
                 user_id='quantaxis',
                 account_cookie='quantaxis',
                 portfolio_cookie='quantaxis',
                 user_cookie='quantaxis',
                 volume_long_today=0,
                 volume_long_his=0,
                 volume_short_today=0,
                 volume_short_his=0,

                 volume_long_frozen_his=0,
                 volume_long_frozen_today=0,
                 volume_short_frozen_his=0,
                 volume_short_frozen_today=0,

                 margin_long=0,
                 margin_short=0,

                 open_price_long=0,
                 open_price_short=0,
                 position_price_long=0,  # 逐日盯市的前一交易日的结算价
                 position_price_short=0,  # 逐日盯市的前一交易日的结算价

                 open_cost_long=0,
                 open_cost_short=0,
                 position_cost_long=0,
                 position_cost_short=0,


                 market_type=MARKET_TYPE.STOCK_CN,
                 exchange_id=EXCHANGE_ID.SZSE,
                 name=None,

                 ):

        self.code = code
        self.user_id = user_id

        self.market_preset = MARKET_PRESET().get_code(self.code)

        """{'name': '原油',
            'unit_table': 1000,
            'price_tick': 0.1,
            'buy_frozen_coeff': 0.1,
            'sell_frozen_coeff': 0.1,
            'exchange': 'INE',
            'commission_coeff_peramount': 0,
            'commission_coeff_pervol': 20.0,
            'commission_coeff_today_peramount': 0,
            'commission_coeff_today_pervol': 0.0}
        """
        self.name = name
        self.market_type = market_type
        self.exchange_id = exchange_id

        self.volume_long_his = volume_long_his
        self.volume_long_today = volume_long_today
        self.volume_short_his = volume_short_his
        self.volume_short_today = volume_short_today

        self.volume_long_frozen_his = volume_long_frozen_his
        self.volume_long_frozen_today = volume_long_frozen_today
        self.volume_short_frozen_his = volume_short_frozen_his
        self.volume_short_frozen_today = volume_short_frozen_today

        self.margin_long = margin_long
        self.margin_short = margin_short

        self.open_price_long = open_price_long
        self.open_price_short = open_price_short
        self.position_price_long = position_price_long
        self.position_price_short = position_price_short

        self.open_cost_long = open_cost_long
        self.open_cost_short = open_cost_short
        self.position_cost_long = position_cost_long
        self.position_cost_short = position_cost_short

        self.last_price = 0

    def __repr__(self):
        return '< QAPOSITION {} amount {}/{} >'.format(self.code, self.volume_long, self.volume_short)

    @property
    def volume_long(self):
        return self.volume_long_today+self.volume_long_his

    @property
    def volume_short(self):
        return self.volume_short_his + self.volume_short_today

    @property
    def volume_long_frozen(self):
        return self.volume_long_frozen_his + self.volume_long_frozen_today

    @property
    def volume_short_frozen(self):
        return self.volume_short_frozen_his + self.volume_short_frozen_today

    @property
    def margin(self):
        return self.margin_long + self.margin_short

    def on_pirce_change(self, price):
        self.last_price = price

    @property
    def float_profit_long(self):
        if self.market_preset is not None:
            return self.last_price * self.volume_long * self.market_preset['unit_table'] - self.open_cost_long

    @property
    def float_profit_short(self):
        if self.market_preset is not None:
            return self.open_cost_short - self.last_price * self.volume_short * self.market_preset['unit_table']

    @property
    def float_profit(self):
        return self.float_profit_long + self.float_profit_short

    @property
    def position_profit_long(self):
        if self.market_preset is not None:
            return self.last_price * self.volume_long * self.market_preset['unit_table'] - self.position_cost_long

    @property
    def position_profit_short(self):
        if self.market_preset is not None:
            return self.position_cost_short - self.last_price * self.volume_short * self.market_preset['unit_table']

    @property
    def position_profit(self):
        return self.position_profit_long + self.position_profit_short

    @property
    def static_message(self):
        return {
            # 基础字段
            'code': self.code,  # 品种名称
            'instrument_id': self.code,
            'name': self.name,
            'market_type': self.market_type,
            'exchange_id': self.exchange_id,  # 交易所ID
            # 持仓量
            'volume_long_today': self.volume_long_today,
            'volume_long_his': self.volume_long_his,
            'volume_long': self.volume_long,
            'volume_short_today': self.volume_short_today,
            'volume_short_his': self.volume_short_his,
            'volume_short': self.volume_short,
            # 委托冻结(未成交)
            'volume_long_frozen_today': self.volume_long_frozen_today,
            'volume_long_frozen_his': self.volume_long_frozen_his,
            'volume_long_frozen': self.volume_long_frozen,
            'volume_short_frozen_today': self.volume_short_frozen_today,
            'volume_short_frozen_his': self.volume_short_frozen_his,
            'volume_short_frozen': self.volume_short_frozen,
            # 保证金
            'margin_long': self.margin_long,       # 多头保证金
            'margin_short': self.margin_short,
            'margin': self.margin,
            # 持仓字段
            'position_price_long': self.position_price_long,  # 多头成本价
            'position_cost_long': self.position_cost_long,   # 多头成本
            'position_price_short': self.position_price_short,
            'position_cost_short': self.position_cost_short,
            # 平仓字段
            'open_price_long': self.open_price_long,  # 多头开仓价
            'open_cost_long': self.open_cost_long,  # 多头开仓成本
            'open_price_short': self.open_price_short,  # 空头开仓价
            'open_cost_short': self.open_cost_short  # 空头成本
        }

    @property
    def realtime_message(self):
        return {
            # 扩展字段
            "last_price": self.last_price,
            # //多头浮动盈亏  ps.last_price * ps.volume_long * ps.ins->volume_multiple - ps.open_cost_long;
            "float_profit_long": self.float_profit_long,
            # //空头浮动盈亏  ps.open_cost_short - ps.last_price * ps.volume_short * ps.ins->volume_multiple;
            "float_profit_short": self.float_profit_short,
            # //浮动盈亏 = float_profit_long + float_profit_short
            "float_profit": self.float_profit,
            "position_profit_long": self.position_profit_long,  # //多头持仓盈亏
            "position_profit_short": self.position_profit_short,  # //空头持仓盈亏
            # //持仓盈亏 = position_profit_long + position_profit_short
            "position_profit": self.position_profit
        }
