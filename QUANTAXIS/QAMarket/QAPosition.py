#
import re
import uuid
import datetime
from QUANTAXIS.QAMarket.market_preset import MARKET_PRESET
from QUANTAXIS.QAMarket.QAOrder import QA_Order
from QUANTAXIS.QAUtil.QAParameter import (
    EXCHANGE_ID,
    MARKET_TYPE,
    ORDER_DIRECTION,
    ORDER_STATUS
)
from QUANTAXIS.QASU.save_position import save_position
from QUANTAXIS.QAUtil.QASetting import DATABASE


class QA_Position():
    '''一个持仓模型:/兼容股票期货/兼容保证金持仓

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
    4/ 支持资金分配和PMS内部资金结算(moneypreset)

    PMS 内部可以预分配一个资金限额, 方便pms实时计算属于PMS的收益

    兼容QA_Account的创建/拆入Positions库

    QAPosition 不对订单信息做正确性保证, 需要自行在外部构建 OMS系统 {QACEPEngine/QAAccountPro}

    '''

    def __init__(self,
                 code='000001',
                 account_cookie='quantaxis',
                 portfolio_cookie='portfolio',
                 username='quantaxis',
                 moneypreset=100000,  # 初始分配资金
                 frozen=None,
                 moneypresetLeft=None,
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
                 position_id=None,

                 market_type=None,
                 exchange_id=None,
                 trades=None,
                 orders=None,
                 name=None,
                 commission=0.0015,
                 auto_reload=False,
                 allow_exceed=False,

                 spms_id=None,
                 oms_id=None,

                 *args,
                 **kwargs

                 ):
        if '.' in code:
            self.code = code.split('.')[1]
        else:
            self.code = code

        self.market_preset = MARKET_PRESET().get_code(self.code)

        self.account_cookie = account_cookie
        self.portfolio_cookie = portfolio_cookie
        self.username = username
        self.time = ''
        self.position_id = str(
            uuid.uuid4()) if position_id is None else position_id
        self.moneypreset = moneypreset
        self.moneypresetLeft = self.moneypreset if moneypresetLeft is None else moneypresetLeft
        '''{'name': '原油',
            'unit_table': 1000,
            'price_tick': 0.1,
            'buy_frozen_coeff': 0.1,
            'sell_frozen_coeff': 0.1,
            'exchange': 'INE',
            'commission_coeff_peramount': 0,
            'commission_coeff_pervol': 20.0,
            'commission_coeff_today_peramount': 0,
            'commission_coeff_today_pervol': 0.0}
        '''
        self.rule = 'FIFO'
        self.name = name

        if market_type is None:

            self.market_type = MARKET_TYPE.FUTURE_CN if re.search(
                r'[a-zA-z]+', self.code) else MARKET_TYPE.STOCK_CN
        self.exchange_id = self.market_preset['exchange'] if exchange_id == None else exchange_id

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

        self.position_price_long = open_price_long if position_price_long == 0 else position_price_long
        self.position_price_short = open_price_short if position_price_short == 0 else position_price_short

        self.open_cost_long = open_cost_long if open_cost_long != 0 else open_price_long * \
            self.volume_long*self.market_preset.get('unit_table', 1)
        self.open_cost_short = open_cost_short if open_cost_short != 0 else open_price_short * \
            self.volume_short*self.market_preset.get('unit_table', 1)
        self.position_cost_long = position_cost_long if position_cost_long != 0 else self.position_price_long * \
            self.volume_long*self.market_preset.get('unit_table', 1)
        self.position_cost_short = position_cost_short if position_cost_short != 0 else self.position_price_short * \
            self.volume_short*self.market_preset.get('unit_table', 1)

        self.last_price = 0
        self.commission = commission
        self.trades = [] if trades is None else trades
        self.orders = {} if orders is None else orders
        self.frozen = {} if frozen is None else frozen
        self.spms_id = spms_id
        self.oms_id = oms_id

        if auto_reload:
            self.reload()
        self.allow_exceed = allow_exceed

    def __repr__(self):
        return '< QAPOSITION {} amount {}/{} >'.format(
            self.code,
            self.volume_long,
            self.volume_short
        )

    def read_diff(self, diff_slice):
        '''[summary]

        Arguments:
            diff_slice {dict} -- [description]

            {'user_id': '100002',
            'exchange_id': 'SHFE',
            'instrument_id': 'rb1905',
            'volume_long_today': 0,
            'volume_long_his': 0,
            'volume_long': 0,
            'volume_long_frozen_today': 0,
            'volume_long_frozen_his': 0,
            'volume_long_frozen': 0,
            'volume_short_today': 0,
            'volume_short_his': 0,
            'volume_short': 0,
            'volume_short_frozen_today': 0,
            'volume_short_frozen_his': 0,
            'volume_short_frozen': 0,
            'open_price_long': 4193.0,
            'open_price_short': 4192.0,
            'open_cost_long': 0.0,
            'open_cost_short': 0.0,
            'position_price_long': 4193.0,
            'position_price_short': 4192.0,
            'position_cost_long': 0.0,
            'position_cost_short': 0.0,
            'last_price': 4137.0,
            'float_profit_long': 0.0,
            'float_profit_short': 0.0,
            'float_profit': 0.0,
            'position_profit_long': 0.0,
            'position_profit_short': 0.0,
            'position_profit': 0.0,
            'margin_long': 0.0,
            'margin_short': 0.0,
            'margin': 0.0}

        Returns:
            QA_Position -- [description]
        '''
        self.account_cookie = diff_slice['user_id']
        self.code = diff_slice['instrument_id']
        self.volume_long_today = diff_slice['volume_long_today']
        self.volume_long_his = diff_slice['volume_long_his']
        self.volume_long_frozen_today = diff_slice['volume_long_frozen_today']
        self.volume_long_frozen_his = diff_slice['volume_long_frozen_his']
        self.volume_short_today = diff_slice['volume_short_today']
        self.volume_short_his = diff_slice['volume_short_his']
        self.volume_short_frozen_today = diff_slice['volume_short_frozen_today']
        self.volume_short_frozen_his = diff_slice['volume_short_frozen_his']
        self.open_price_long = diff_slice['open_price_long']
        self.open_price_short = diff_slice['open_price_short']
        self.open_cost_long = diff_slice['open_cost_long']
        self.open_cost_short = diff_slice['open_cost_short']
        self.position_price_long = diff_slice['position_price_long']
        self.position_price_short = diff_slice['position_price_short']
        self.position_cost_long = diff_slice['position_cost_long']
        self.position_cost_short = diff_slice['position_cost_short']
        self.margin_long = diff_slice['margin_long']
        self.margin_short = diff_slice['margin_short']
        self.exchange_id = diff_slice['exchange_id']
        self.market_type = MARKET_TYPE.FUTURE_CN
        return self

    @property
    def volume_long(self):
        return self.volume_long_today + self.volume_long_his - self.volume_long_frozen

    @property
    def volume_short(self):
        return self.volume_short_his + self.volume_short_today - self.volume_short_frozen

    @property
    def volume_long_frozen(self):
        return self.volume_long_frozen_his + self.volume_long_frozen_today

    @property
    def volume_short_frozen(self):
        return self.volume_short_frozen_his + self.volume_short_frozen_today

    @property
    def margin(self):
        return self.margin_long + self.margin_short

    @property
    def float_profit_long(self):
        if self.market_preset is not None:
            return self.last_price * self.volume_long * self.market_preset.get(
                'unit_table',
                1
            ) - self.open_cost_long

    @property
    def float_profit_short(self):
        if self.market_preset is not None:
            return self.open_cost_short - self.last_price * self.volume_short * self.market_preset.get(
                'unit_table',
                1
            )

    @property
    def float_profit(self):
        return self.float_profit_long + self.float_profit_short

    @property
    def position_profit_long(self):
        if self.market_preset is not None:
            return self.last_price * self.volume_long * self.market_preset.get(
                'unit_table',
                1
            ) - self.position_cost_long

    @property
    def position_profit_short(self):
        if self.market_preset is not None:
            return self.position_cost_short - self.last_price * self.volume_short * self.market_preset.get(
                'unit_table',
                1
            )

    @property
    def position_profit(self):
        return self.position_profit_long + self.position_profit_short

    @property
    def static_message(self):
        return {
            # 基础字段
            'code': self.code,  # 品种名称
            'instrument_id': self.code,
            'user_id': self.account_cookie,
            'portfolio_cookie': self.portfolio_cookie,
            'username': self.username,
            'position_id': self.position_id,
            'account_cookie': self.account_cookie,
            'frozen': self.frozen,
            'name': self.name,
            'spms_id': self.spms_id,
            'oms_id': self.oms_id,
            'market_type': self.market_type,
            'exchange_id': self.exchange_id,  # 交易所ID
            'moneypreset': self.moneypreset,
            'moneypresetLeft': self.moneypresetLeft,
            'lastupdatetime': str(self.time),
            # 持仓量
            'volume_long_today': int(self.volume_long_today),
            'volume_long_his': int(self.volume_long_his),
            'volume_long': int(self.volume_long),
            'volume_long_yd': 0,
            'volume_short_yd': 0,
            'volume_short_today': int(self.volume_short_today),
            'volume_short_his': int(self.volume_short_his),
            'volume_short': int(self.volume_short),
            'pos_long_his': int(self.volume_long_his),
            'pos_long_today': int(self.volume_long_today),
            'pos_short_his': int(self.volume_short_his),
            'pos_short_today': int(self.volume_short_today),
            # 平仓委托冻结(未成交)
            'volume_long_frozen_today': int(self.volume_long_frozen_today),
            'volume_long_frozen_his': int(self.volume_long_frozen_his),
            'volume_long_frozen': int(self.volume_long_frozen),
            'volume_short_frozen_today': int(self.volume_short_frozen_today),
            'volume_short_frozen_his': int(self.volume_short_frozen_his),
            'volume_short_frozen': int(self.volume_short_frozen),
            # 保证金
            'margin_long': self.margin_long,       # 多头保证金
            'margin_short': self.margin_short,
            'margin': self.margin,
            # 持仓字段
            'position_price_long': self.position_price_long,  # 多头成本价
            'position_cost_long': self.position_cost_long,   # 多头总成本(  总市值)
            'position_price_short': self.position_price_short,
            'position_cost_short': self.position_cost_short,
            # 平仓字段
            'open_price_long': self.open_price_long,  # 多头开仓价
            'open_cost_long': self.open_cost_long,  # 多头开仓成本
            'open_price_short': self.open_price_short,  # 空头开仓价
            'open_cost_short': self.open_cost_short,  # 空头成本
            # 历史字段
            'trades': self.trades,
            'orders': self.orders
        }
    @property
    def qifimessage(self):
        return {
            # 基础字段
            'code': self.code,  # 品种名称
            'instrument_id': self.code,
            'user_id': self.account_cookie,
            'portfolio_cookie': self.portfolio_cookie,
            'username': self.username,
            'position_id': self.position_id,
            'account_cookie': self.account_cookie,
            'market_type': self.market_type,
            'exchange_id': self.exchange_id,  # 交易所ID
            # 持仓量
            'volume_long_today': int(self.volume_long_today),
            'volume_long_his': int(self.volume_long_his),
            'volume_long': int(self.volume_long),
            'volume_long_yd': 0,
            'volume_short_yd': 0,
            'volume_short_today': int(self.volume_short_today),
            'volume_short_his': int(self.volume_short_his),
            'volume_short': int(self.volume_short),
            'pos_long_his': int(self.volume_long_his),
            'pos_long_today': int(self.volume_long_today),
            'pos_short_his': int(self.volume_short_his),
            'pos_short_today': int(self.volume_short_today),
            # 平仓委托冻结(未成交)
            'volume_long_frozen_today': int(self.volume_long_frozen_today),
            'volume_long_frozen_his': int(self.volume_long_frozen_his),
            'volume_long_frozen': int(self.volume_long_frozen),
            'volume_short_frozen_today': int(self.volume_short_frozen_today),
            'volume_short_frozen_his': int(self.volume_short_frozen_his),
            'volume_short_frozen': int(self.volume_short_frozen),
            # 保证金
            'margin_long': self.margin_long,       # 多头保证金
            'margin_short': self.margin_short,
            'margin': self.margin,
            # 持仓字段
            'position_price_long': self.position_price_long,  # 多头成本价
            'position_cost_long': self.position_cost_long,   # 多头总成本(  总市值)
            'position_price_short': self.position_price_short,
            'position_cost_short': self.position_cost_short,
            # 平仓字段
            'open_price_long': self.open_price_long,  # 多头开仓价
            'open_cost_long': self.open_cost_long,  # 多头开仓成本
            'open_price_short': self.open_price_short,  # 空头开仓价
            'open_cost_short': self.open_cost_short,  # 空头成本

            # 扩展字段
            'last_price': self.last_price,
            # //多头浮动盈亏  ps.last_price * ps.volume_long * ps.ins->volume_multiple - ps.open_cost_long;
            'float_profit_long': self.float_profit_long,
            # //空头浮动盈亏  ps.open_cost_short - ps.last_price * ps.volume_short * ps.ins->volume_multiple;
            'float_profit_short': self.float_profit_short,
            # //浮动盈亏 = float_profit_long + float_profit_short
            'float_profit': self.float_profit,
            'position_profit_long': self.position_profit_long,  # //多头持仓盈亏
            'position_profit_short': self.position_profit_short,  # //空头持仓盈亏
            # //持仓盈亏 = position_profit_long + position_profit_short
            'position_profit': self.position_profit
        }

    @property
    def hold_detail(self):
        return {
            # 持仓量
            'volume_long_today': self.volume_long_today,
            'volume_long_his': self.volume_long_his,
            'volume_long': self.volume_long,
            'volume_short_today': self.volume_short_today,
            'volume_short_his': self.volume_short_his,
            'volume_short': self.volume_short
        }

    @property
    def realtime_message(self):
        return {
            # 扩展字段
            'last_price': self.last_price,
            # //多头浮动盈亏  ps.last_price * ps.volume_long * ps.ins->volume_multiple - ps.open_cost_long;
            'float_profit_long': self.float_profit_long,
            # //空头浮动盈亏  ps.open_cost_short - ps.last_price * ps.volume_short * ps.ins->volume_multiple;
            'float_profit_short': self.float_profit_short,
            # //浮动盈亏 = float_profit_long + float_profit_short
            'float_profit': self.float_profit,
            'position_profit_long': self.position_profit_long,  # //多头持仓盈亏
            'position_profit_short': self.position_profit_short,  # //空头持仓盈亏
            # //持仓盈亏 = position_profit_long + position_profit_short
            'position_profit': self.position_profit
        }

    @property
    def message(self):
        msg = self.static_message
        msg.update(self.realtime_message)
        return msg

    def order_check(self, amount: int, price: float, towards: int, order_id: str) -> bool:
        res = False
        if towards == ORDER_DIRECTION.BUY_CLOSE:
            # print('buyclose')
            #print(self.volume_short - self.volume_short_frozen)
            # print(amount)
            if (self.volume_short - self.volume_short_frozen) >= amount:
                # check
                self.volume_short_frozen_today += amount
                res = True
            else:
                print('BUYCLOSE 仓位不足')

        elif towards == ORDER_DIRECTION.BUY_CLOSETODAY:
            if (self.volume_short_today - self.volume_short_frozen_today) >= amount:
                self.volume_short_frozen_today += amount
                res = True
            else:
                print('BUYCLOSETODAY 今日仓位不足')
        elif towards == ORDER_DIRECTION.SELL_CLOSE:
            # print('sellclose')
            #print(self.volume_long - self.volume_long_frozen)
            # print(amount)
            if (self.volume_long - self.volume_long_frozen) >= amount:
                self.volume_long_frozen_today += amount
                res = True
            else:
                print('SELL CLOSE 仓位不足')

        elif towards == ORDER_DIRECTION.SELL_CLOSETODAY:
            if (self.volume_long_today - self.volume_long_frozen_today) >= amount:
                # print('sellclosetoday')
                #print(self.volume_long_today - self.volume_long_frozen)
                # print(amount)
                self.volume_long_frozen_today += amount
                return True
            else:
                print('SELLCLOSETODAY 今日仓位不足')
        elif towards in [ORDER_DIRECTION.BUY_OPEN,
                         ORDER_DIRECTION.SELL_OPEN,
                         ORDER_DIRECTION.BUY]:
            '''
            冻结的保证金
            '''
            moneyneed = int(amount) * float(price) * float(
                self.market_preset.get('unit_table',
                                       1)
            ) * float(self.market_preset.get('buy_frozen_coeff',
                                             1))

            if (self.moneypresetLeft > moneyneed) or self.allow_exceed:
                self.moneypresetLeft -= moneyneed
                self.frozen[order_id] = moneyneed
                res = True
            else:
                print('开仓保证金不足 TOWARDS{} Need{} HAVE{}'.format(
                    towards, moneyneed, self.moneypresetLeft))

        return res

    def send_order(self, amount: int, price: float, towards: int):
        order_id = str(uuid.uuid4())
        if self.order_check(amount, price, towards, order_id):
            #print('order check success')
            order = {
                'position_id': str(self.position_id),
                'account_cookie': self.account_cookie,
                'instrument_id': self.code,
                'towards': int(towards),
                'exchange_id': str(self.exchange_id),
                'order_time': str(self.time),
                'volume': int(amount),
                'price': float(price),
                'order_id': order_id,
                'status': ORDER_STATUS.NEW
            }
            self.orders[order_id] = order
            return order
        else:
            print(RuntimeError('ORDER CHECK FALSE: {}'.format(self.code)))
            return False

    def update_pos(self, price, amount, towards):
        '''支持股票/期货的更新仓位

        Arguments:
            price {[type]} -- [description]
            amount {[type]} -- [description]
            towards {[type]} -- [description]

            margin: 30080
            margin_long: 0
            margin_short: 30080
            open_cost_long: 0
            open_cost_short: 419100
            open_price_long: 4193
            open_price_short: 4191
            position_cost_long: 0
            position_cost_short: 419100
            position_price_long: 4193
            position_price_short: 4191
            position_profit: -200
            position_profit_long: 0
            position_profit_short: -200
        '''
        self.on_price_change(price)
        temp_cost = int(amount)*float(price) * \
            float(self.market_preset.get('unit_table', 1))
        profit = 0
        if towards == ORDER_DIRECTION.BUY:
            # 股票模式/ 期货买入开仓
            marginValue = temp_cost

            self.margin_long += marginValue
            # 重算开仓均价
            self.open_price_long = (
                self.open_price_long * self.volume_long + amount * price
            ) / (
                amount + self.volume_long
            )
            # 重算持仓均价
            self.position_price_long = (
                self.position_price_long * self.volume_long + amount * price
            ) / (
                amount + self.volume_long
            )
            # 增加今仓数量 ==> 会自动增加volume_long
            self.volume_long_today += amount
            #
            self.open_cost_long += temp_cost
            self.position_cost_long += temp_cost
            self.moneypresetLeft -= marginValue

        elif towards == ORDER_DIRECTION.SELL:
            # 股票卖出模式:
            # 今日买入仓位不能卖出
            if self.volume_long_his >= amount:
                # volime_long --> count in sendorder model
                # and self.volume_long>=amount:
                if self.volume_long > 0:
                    self.position_cost_long = self.position_cost_long * \
                        (self.volume_long)/self.volume_long+ amount
                    self.open_cost_long = self.open_cost_long * \
                        (self.volume_long-amount)/self.volume_long +amount

                    self.volume_long_his -= amount
                    self.volume_long_frozen_today -= amount

                    marginValue = -1*(self.position_price_long * amount)
                    
                    self.margin_long += marginValue
                    profit = (price - self.position_price_long) * amount
                    self.moneypresetLeft += (-marginValue + profit)
                elif self.volume_long == 0:
                    # all close out
                    self.open_cost_long = 0
                    self.position_cost_long = 0

                    self.volume_long_his -= amount
                    self.volume_long_frozen_today -= amount

                    marginValue = -1*(self.position_price_long * amount)
                    self.margin_long += marginValue
                    profit = (price - self.position_price_long) * amount
                    self.moneypresetLeft += (-marginValue + profit)

            else:
                return 0, 0,0

        elif towards == ORDER_DIRECTION.BUY_OPEN:

            # 增加保证金
            marginValue = temp_cost * \
                self.market_preset.get('buy_frozen_coeff', 1)
            self.margin_long += marginValue
            # 重算开仓均价
            self.open_price_long = (
                self.open_price_long * self.volume_long + amount * price
            ) / (
                amount + self.volume_long
            )
            # 重算持仓均价
            self.position_price_long = (
                self.position_price_long * self.volume_long + amount * price
            ) / (
                amount + self.volume_long
            )
            # 增加今仓数量 ==> 会自动增加volume_long
            self.volume_long_today += amount
            #
            self.open_cost_long += temp_cost
            self.position_cost_long += temp_cost
            self.moneypresetLeft -= marginValue

        elif towards == ORDER_DIRECTION.SELL_OPEN:
            # 增加保证金
            '''
            1. 增加卖空保证金
            2. 重新计算 开仓成本
            3. 重新计算 持仓成本
            4. 增加开仓cost
            5. 增加持仓cost
            6. 增加空单仓位
            '''
            marginValue = temp_cost * \
                self.market_preset.get('sell_frozen_coeff', 1)
            self.margin_short += marginValue
            # 重新计算开仓/持仓成本
            self.open_price_short = (
                self.open_price_short * self.volume_short + amount * price
            ) / (
                amount + self.volume_short
            )
            self.position_price_short = (
                self.position_price_short * self.volume_short + amount * price
            ) / (
                amount + self.volume_short
            )
            self.open_cost_short += temp_cost
            self.position_cost_short += temp_cost
            self.volume_short_today += amount
            self.moneypresetLeft -= marginValue

        elif towards == ORDER_DIRECTION.BUY_CLOSETODAY:
            if self.volume_short_today > amount:
                self.position_cost_short = self.position_cost_short * \
                    self.volume_short/(self.volume_short + amount)
                self.open_cost_short = self.open_cost_short * \
                    self.volume_short/(self.volume_short + amount)

                self.volume_short_today -= amount
                self.volume_short_frozen_today += amount

                # close_profit = (self.position_price_short - price) * volume * position->ins->volume_multiple;
                marginValue = -(self.position_price_short * amount*self.market_preset.get('unit_table', 1) *
                                self.market_preset.get('sell_frozen_coeff', 1))

                self.margin_short += marginValue
                profit = (self.position_price_short - price
                          ) * amount * self.market_preset.get('unit_table', 1)

                self.moneypresetLeft += (-marginValue + profit)

                # 释放保证金
                # TODO
                # self.margin_short
                #self.open_cost_short = price* amount

        elif towards == ORDER_DIRECTION.SELL_CLOSETODAY:
            if self.volume_long_today > amount:
                self.position_cost_long = self.position_cost_long * \
                    self.volume_long / (self.volume_long + amount)
                self.open_cost_long = self.open_cost_long * \
                    self.volume_long / (self.volume_long + amount)

                self.volume_long_today -= amount
                self.volume_long_frozen_today -= amount

                marginValue = -1*(self.position_price_long * amount*self.market_preset.get('unit_table', 1) *
                                  self.market_preset.get('buy_frozen_coeff', 1))
                self.margin_long += marginValue
                profit = (price - self.position_price_long) * \
                    amount * self.market_preset.get('unit_table', 1)
                self.moneypresetLeft += (-marginValue + profit)

        elif towards == ORDER_DIRECTION.BUY_CLOSE:
            # 有昨仓先平昨仓

            if self.volume_short > 0:
                self.position_cost_short = self.position_cost_short * \
                    self.volume_short/(self.volume_short + amount)
                self.open_cost_short = self.open_cost_short * \
                    self.volume_short/(self.volume_short + amount)
            else:
                self.position_cost_short = 0
                self.open_cost_short = 0
            # if self.volume_short_his >= amount:
            #     self.volume_short_his -= amount
            # else:
            #     self.volume_short_today -= (amount - self.volume_short_his)
            #     self.volume_short_his = 0
            self.volume_short_frozen_today -= amount
            self.volume_short_today -= amount

            marginValue = -1*(self.position_price_short * amount*self.market_preset.get('unit_table', 1) *
                              self.market_preset.get('sell_frozen_coeff', 1))
            profit = (self.position_price_short - price
                      ) * amount * self.market_preset.get('unit_table', 1)
            self.margin_short += marginValue

            self.moneypresetLeft += (-marginValue + profit)
        elif towards == ORDER_DIRECTION.SELL_CLOSE:
            # 有昨仓先平昨仓
            # print(self.curpos)
            if self.volume_long > 0:
                self.position_cost_long = self.position_cost_long * \
                    self.volume_long / (self.volume_long + amount)
                self.open_cost_long = self.open_cost_long * \
                    self.volume_long / (self.volume_long + amount)
            else:
                self.position_cost_long = 0
                self.open_cost_long = 0
            # if self.volume_long_his >= amount:
            #     self.volume_long_his -= amount
            # else:
            #     self.volume_long_today -= (amount - self.volume_long_his)
            #     self.volume_long_his = 0
            self.volume_long_today -= amount
            self.volume_long_frozen_today -= amount
            marginValue = -1*(self.position_price_long * amount*self.market_preset.get('unit_table', 1) *
                              self.market_preset.get('buy_frozen_coeff', 1))
            profit = (price - self.position_price_long) * \
                amount * self.market_preset.get('unit_table', 1)
            self.margin_long += marginValue
            self.moneypresetLeft += (-marginValue + profit)
        # 计算收益/成本
        commission= self.calc_commission( price, amount, towards)
        self.commission +=commission
        return marginValue, profit, commission

    def settle(self):
        '''收盘后的结算事件
        '''
        self.volume_long_his += self.volume_long_today
        self.volume_long_today = 0
        self.volume_long_frozen_today = 0
        self.volume_short_his += self.volume_short_today
        self.volume_short_today = 0
        self.volume_short_frozen_today = 0

    @property
    def curpos(self):
        return {
            'volume_long': self.volume_long,
            'volume_short': self.volume_short,
            'volume_long_frozen': self.volume_long_frozen,
            'volume_short_frozen': self.volume_short_frozen
        }

    @property
    def close_available(self):
        '''可平仓数量

        Returns:
            [type] -- [description]
        '''
        return {
            'volume_long': self.volume_long - self.volume_long_frozen,
            'volume_short': self.volume_short - self.volume_short_frozen
        }

    def change_moneypreset(self, money):
        self.moneypreset = money

    def save(self):
        '''save&update

        save data to mongodb | update
        '''
        print(self.static_message)
        save_position(self.static_message)

    def reload(self):
        res = DATABASE.positions.find_one({
            'account_cookie': self.account_cookie,
            'portfolio_cookie': self.portfolio_cookie,
            'username': self.username,
            'position_id': self.position_id
        })
        if res is None:
            self.save()
        else:
            self.loadfrommessage(res)

    def calc_commission(self, trade_price, trade_amount, trade_towards,):
        if self.market_type == MARKET_TYPE.FUTURE_CN:
            # 期货不收税
            # 双边手续费 也没有最小手续费限制
            value = trade_price * trade_amount * \
                MARKET_PRESET().get_unit(self.code)

            commission_fee_preset = MARKET_PRESET().get_code(self.code)
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
            
        elif self.market_type == MARKET_TYPE.STOCK_CN:
            value = trade_price * trade_amount
            if trade_towards == ORDER_DIRECTION.BUY_OPEN:
                """买入万 2 滑点"""
                commission_fee = value *  0.0002
            else:
                """卖出千 1.3 手续费+ 万 2 滑点"""
                commission_fee = value *  0.0015

        return commission_fee

    def loadfrommessage(self, message):
        try:

            self.__init__(
                code=message.get('code', 'instrument_id'),
                account_cookie=message['account_cookie'],
                frozen=message['frozen'],
                portfolio_cookie=message['portfolio_cookie'],
                username=message['username'],
                moneypreset=message['moneypreset'],  # 初始分配资金
                moneypresetLeft=message['moneypresetLeft'],
                volume_long_today=message['volume_long_today'],
                volume_long_his=message['volume_long_his'],
                volume_short_today=message['volume_short_today'],
                volume_short_his=message['volume_short_his'],

                volume_long_frozen_his=message['volume_long_frozen_his'],
                volume_long_frozen_today=message['volume_long_frozen_today'],
                volume_short_frozen_his=message['volume_short_frozen_his'],
                volume_short_frozen_today=message['volume_short_frozen_today'],

                margin_long=message['margin_long'],
                margin_short=message['margin_short'],

                open_price_long=message['open_price_long'],
                open_price_short=message['open_price_short'],
                # 逐日盯市的前一交易日的结算价
                position_price_long=message['position_price_long'],
                # 逐日盯市的前一交易日的结算价
                position_price_short=message['position_price_short'],

                open_cost_long=message['open_cost_long'],
                open_cost_short=message['open_cost_short'],
                position_cost_long=message['position_cost_long'],
                position_cost_short=message['position_cost_short'],
                position_id=message['position_id'],

                market_type=message['market_type'],
                exchange_id=message['exchange_id'],
                trades=message['trades'],
                orders=message['orders'],
                # commission=message['commission'],
                name=message['name'])
        except:
            self.read_diff(message)
        if self.volume_long + self.volume_short > 0:
            self.last_price = (self.open_price_long*self.volume_long + self.open_price_short *
                               self.volume_short)/(self.volume_long + self.volume_short)
        else:
            self.last_price = 0

        return self

    def on_order(self, order: QA_Order):
        '''这里是一些外部操作导致的POS变化

        - 交易过程的外部手动交易
        - 风控状态下的监控外部交易

        order_id 是外部的
        trade_id 不一定存在
        '''

        if order['order_id'] not in self.frozen.keys():
            print('OUTSIDE ORDER')
            # self.frozen[order['order_id']] = order[]
            # 回放订单/注册进订单系统
            order = self.send_order(
                order.get('amount', order.get('volume')),
                order['price'],
                eval('ORDER_DIRECTION.{}_{}'.format(
                    order.get('direction'),
                    order.get('offset')
                ))
            )
            self.orders[order]['status'] = ORDER_STATUS.QUEUED

    def on_transaction(self, transaction: dict):
        towards = transaction.get(
            'towards',
            eval(
                'ORDER_DIRECTION.{}_{}'.format(
                    transaction.get('direction'),
                    transaction.get('offset')
                )
            )
        )
        transaction['towards'] = towards
        # TODO:
        # 在这里可以加入更多关于PMS交易的代码
        try:
            self.update_pos(
                transaction['price'],
                transaction.get('amount',
                                transaction.get('volume')),
                towards
            )
            self.moneypresetLeft += self.frozen.get(transaction['order_id'], 0)
            # 当出现外部交易的时候, 直接在frozen中注册订单
            self.frozen[transaction['order_id']] = 0
            self.orders[transaction['order_id']] = ORDER_STATUS.SUCCESS_ALL
            self.trades.append(transaction)
        except Exception as e:
            raise e

    def on_price_change(self, price):
        self.last_price = price

    def on_bar(self, bar):
        '''只订阅这个code的数据

        Arguments:
            bar {[type]} -- [description]
        '''
        self.last_price = bar['close']
        # print(self.realtime_message)
        pass

    def on_tick(self, tick):
        '''只订阅当前code的tick

        Arguments:
            tick {[type]} -- [description]
        '''
        self.last_price = tick['LastPrice']
        # print(self.realtime_message)
        pass

    def on_signal(self, signal):
        raise NotImplementedError('此接口为内部接口 为CEP专用')

    def callback_sub(self):
        raise NotImplementedError('此接口为内部接口 为CEP专用')

    def callback_pub(self):
        raise NotImplementedError('此接口为内部接口 为CEP专用')


class QA_PMS():

    def __init__(self, init_position=None):
        self.pms = {}

    def add_pos(self, pos: QA_Position):
        if pos.code in self.pms.keys():
            self.pms[pos.code][pos.position_id] = pos
        else:
            self.pms[pos.code] = {pos.position_id: pos}

    def remove_pos(self, pos: QA_Position):
        del self.pms[pos.code][pos.position_id]

    def orderAction(self, order: QA_Order):
        '''
        委托回报
        '''
        return self.pms[order.code][order.order_id].receive_order(order)

    def dealAction(self):
        '''
        成交回报
        '''
        pass


if __name__ == '__main__':
    '''

    float_profit: 11636.923076923063
    float_profit_long: 50066.92307692306
    float_profit_short: -38430
    instrument_id: 'rb1905'
    last_price: 4193
    margin: 59727.99999999999
    margin_long: 32850.399999999994
    margin_short: 26877.6
    open_cost_long: 411163.07692307694
    open_cost_short: 338940
    open_price_long: 3737.846153846154
    open_price_short: 3766
    position_cost_long: 411163.07692307694
    position_cost_short: 338940
    position_price_long: 3737.846153846154
    position_price_short: 3766
    position_profit: 11636.923076923063
    position_profit_long: 50066.92307692306
    position_profit_short: -38430
    volume_long: 11
    volume_long_frozen: 1
    volume_long_frozen_his: 0
    volume_long_frozen_today: 0
    volume_long_his: 11
    volume_long_today: 0
    volume_short: 9
    volume_short_frozen: 1
    volume_short_frozen_his: 0
    volume_short_frozen_today: 0
    volume_short_his: 9
    volume_short_today: 0
    '''
    pos = QA_Position(
        code='rb1905',
        account_cookie='100002',
        market_type=MARKET_TYPE.FUTURE_CN,
        exchange_id=EXCHANGE_ID.SHFE,
        volume_long_his=11,
        volume_long_today=0,
        volume_short_his=9,
        open_price_long=3737.846153846154,
        open_price_short=3766,
        name='螺纹1905'
    )
    print(pos.static_message)

    pos.on_price_change(4193)
    print(pos.realtime_message)
    print(pos.static_message)
    pos.on_transaction(
        {
            'direction': 'SELL',
            'offset': 'OPEN',
            'price': 3678,
            'volume': 1
        }
    )

    print('STOCK TEST')

    pos = QA_Position(
        code='000001',
        account_cookie='100002',
        market_type=MARKET_TYPE.STOCK_CN,
        exchange_id=EXCHANGE_ID.SZSE,
        volume_long_his=1100,
        volume_long_today=0,
        open_price_long=8,
        name='中国平安'
    )
    print(pos.static_message)

    pos.on_price_change(10)
    print(pos.realtime_message)
    print(pos.static_message)
