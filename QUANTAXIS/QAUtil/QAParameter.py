# -* coding: utf-8 -*-
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


"""
这里定义的是一些常用常量
"""


class ORDER_DIRECTION:
    """订单的买卖方向

    BUY 股票 买入
    SELL 股票 卖出
    BUY_OPEN 期货 多开
    BUY_CLOSE 期货 空平(多头平旧仓)
    SELL_OPEN 期货 空开
    SELL_CLOSE 期货 多平(空头平旧仓)
    SELL

    双开：多头空头同时开新仓
    双平：多头空头同时平旧仓
    多换：多头开新仓，新仓对应的是多平
    空换：空头开新仓，新仓对应的是空平
    """

    BUY = 1
    SELL = -1
    BUY_OPEN = 2
    BUY_CLOSE = 3
    SELL_OPEN = -2
    SELL_CLOSE = -3


class ORDER_MODEL:
    """订单的成交模式

    LIMIT 限价模式
    MARKET 市价单 # 目前市价单在回测中是bar的开盘价 /实盘里面是五档剩余最优成交价
    CLOSE 收盘单 # 及在bar的收盘时的价格
    NEXT_OPEN 下一个bar的开盘价成交
    STRICT 严格订单 不推荐/仅限回测/是在当前bar的最高价买入/当前bar的最低价卖出

    @yutiansut/2017-12-18
    """

    LIMIT = 'limit'  # 限价
    MARKET = 'market'  # 市价/在回测里是下个bar的开盘价买入/实盘就是五档剩余最优成交价
    CLOSE = 'close'  # 当前bar的收盘价买入
    NEXT_OPEN = 'next_open'  # 下个bar的开盘价买入
    STRICT = 'strict'  # 严格模式/不推荐(仅限回测测试用)


class ORDER_STATUS:
    """订单状态

    status1xx 订单待生成
    status3xx 初始化订单  临时扣除资产(可用现金/可卖股份)
    status3xx 订单存活(等待交易)
    status2xx 订单完全交易/未完全交易
    status4xx 主动撤单
    status500 订单死亡(每日结算) 恢复临时资产    

    200 委托成功,完全交易
    203 委托成功,未完全成功
    300 刚创建订单的时候
    400 已撤单
    500 服务器撤单/每日结算

    订单生成(100) -- 进入待成交队列(300) -- 完全成交(200) -- 每日结算(500)-- 死亡
    订单生成(100) -- 进入待成交队列(300) -- 部分成交(203) -- 未成交(300) -- 每日结算(500) -- 死亡
    订单生成(100) -- 进入待成交队列(300) -- 主动撤单(400) -- 每日结算(500) -- 死亡
    """

    NEW = 100
    SUCCESS_ALL = 200
    SUCCESS_PART = 203
    QUEUED = 300  # queued 用于表示在order_queue中 实际表达的意思是订单存活 待成交
    CANCEL_ALL = 400
    SETTLED = 500


class AMOUNT_MODEL:
    """订单的成交量

    by_price是按固定成交总额下单,动态计算成交量
    by_amount 按固定成家量下单
    """

    BY_PRICE = 'by_price'
    BY_AMOUNT = 'by_amount'


class RUNNING_ENVIRONMENT:
    """执行环境

    回测
    模拟
    实盘
    随机(按算法/分布随机生成行情)/仅用于训练测试
    """

    BACKETEST = 'backtest'
    SIMULATION = 'simulation'
    REAL = 'real'
    RANODM = 'random'


class TRADE_STATUS:
    """交易状态返回值

    涨跌停限制: 202
    成功交易 : 200
    当天无交易数据: 500
    订单失败(比如买卖价格超过涨跌停价格范围,交易量过大等等):400
    """

    SUCCESS = 200
    PRICE_LIMIT = 202
    NO_MARKET_DATA = 500
    FAILED = 400


class MARKET_ERROR:
    ACCOUNT_EXIST = 'Account has already exist'


class MARKET_TYPE():
    """市场种类

    日线 尾数01
    分钟线 尾数02
    tick 尾数03

    市场:
    股票 0
    指数/基金 1
    期货 2
    港股 3
    美股 4
    比特币/加密货币市场 5
    """

    STOCK_DAY = '0x01'
    STOCK_MIN = '0x02'
    STOCK_TRANSACTION = '0x03'

    INDEX_DAY = '1x01'
    INDEX_MIN = '1x02'
    INDEX_TRANSACTION = '1x03'

    FUTUER_DAY = '2x01'
    FUTUER_MIN = '2x02'
    FUTUER_TRANSACTION = '2x03'


class BROKER_TYPE:
    """执行环境

    回测
    模拟
    实盘
    随机(按算法/分布随机生成行情)/仅用于训练测试
    """

    BACKETEST = 'backtest'
    SIMULATION = 'simulation'
    REAL = 'real'
    RANODM = 'random'


class EVENT_TYPE:
    BROKER_EVENT = 'broker_event'
    ACCOUNT_EVENT = 'account_event'
    MARKET_EVENT = 'market_event'
    TRADE_EVENT = 'trade_event'
    ENGINE_EVENT = 'engine_event'
    ORDER_EVENT = 'order_event'


class MARKET_EVENT:
    QUERY_ORDER = 'query_order'
    QUERY_ASSETS = 'query_assets'
    QUERY_ACCOUNT = 'query_account'
    QUERY_CASH = 'query_cash'
    QUERY_DATA = 'query_data'


class ENGINE_EVENT:
    """引擎事件"""
    MARKET_INIT = 'market_init'
    BAR_SETTLE = 'bar_settle'
    DAILY_SETTLE = 'daily_settle'
    UPDATE = 'update'


class ACCOUNT_EVENT:
    """账户事件"""
    UPDATE = 'account_update'
    SETTLE = 'account_settle'
    MAKE_ORDER = 'account_make_order'


class BROKER_EVENT:
    """BROKER事件"""
    LOAD_DATA = 'load_data'
    TRADE = 'broker_trade'
    SETTLE = 'broker_settle'


class ORDER_EVENT:
    """订单事件

    创建订单 create
    交易 trade
    撤单 cancel

    """
    CREATE = 'create'
    TRADE = 'trade'
    CANCEL = 'cancel'


class MARKETDATA_TYPE:
    """查询的级别

    [description]
    """

    YEAR = 'year'  # 年bar
    QUARTER = 'quarter'  # 季度bar
    MONTH = 'month'  # 月bar
    WEEK = 'week'  # 周bar
    DAY = 'day'  # 日bar
    ONE_MIN = '1min'  # 1min bar
    FIVE_MIN = '5min'  # 5min bar
    FIFTEEN_MIN = '15min'  # 15min bar
    THIRTY_MIN = '30min'  # 30min bar
    HOUR = '60min'  # 60min bar
    SIXTY_MIN = '60min'  # 60min bar
    CURRENT = 'current'  # 当前bar
    TICK = 'tick'  # transaction


class SECURITY_TYPE:
    '证券的种类'
    STOCK_CN = 'stock_cn'  # 中国A股
    STOCK_HK = 'stock_hk'  # 港股
    STOCK_US = 'stock_us'  # 美股
    FUTURE_CN = 'future_cn'  # 国内期货
    OPTION_CN = 'option_cn'  # 国内期权
    STOCKOPTION_CN = 'stockoption_cn'  # 个股期权
    # BITCOIN = 'bitcoin'  # 比特币
    CRYPTOCURRENCY = 'cryptocurrency'  # 加密货币(衍生货币)
    INDEX_CN = 'index_cn'  # 中国指数
    FUND_CN = 'fund_cn'   # 中国基金
    BOND_CN = 'bond_cn'  # 中国债券


class CURRENCY_TYPE:
    """货币种类"""
    RMB = 'rmb'  # 人民币
    USD = 'usd'  # 美元
    EUR = 'eur'  # 欧元
    HKD = 'hkd'  # 港币
    GBP = 'GBP'  # 英镑
    BTC = 'btc'  # 比特币
    JPY = 'jpy'  # 日元
    AUD = 'aud'  # 澳元
    CAD = 'cad'  # 加拿大元
