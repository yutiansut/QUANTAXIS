# -* coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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


class ORDER_DIRECTION():
    """订单的买卖方向

    BUY 股票 买入
    SELL 股票 卖出
    BUY_OPEN 期货 多开
    BUY_CLOSE 期货 空平(多头平旧仓)
    SELL_OPEN 期货 空开
    SELL_CLOSE 期货 多平(空头平旧仓)

    ASK  申购
    """

    BUY = 1
    SELL = -1
    BUY_OPEN = 2
    BUY_CLOSE = 3
    SELL_OPEN = -2
    SELL_CLOSE = -3
    SELL_CLOSETODAY = -4
    BUY_CLOSETODAY = 4
    ASK = 0
    XDXR = 5
    OTHER = 6


class TIME_CONDITION():
    IOC = 'IOC'  # 立即完成，否则撤销
    GFS = 'GFS'  # 本节有效
    GFD = 'GFD'  # 当日有效
    GTD = 'GTD'  # 指定日期前有效
    GTC = 'GTC'  # 撤销前有效
    GFA = 'GFA'  # 集合竞价有效


class VOLUME_CONDITION():
    ANY = 'ANY'  # 任意数量
    MIN = 'MIN'  # 最小数量
    ALL = 'ALL'  # 全部数量


class EXCHANGE_ID():
    SSE = 'sse'  # 上交所
    SZSE = 'szse'  # 深交所
    SHFE = 'SHFE'  # 上期所
    DCE = 'DCE'  # 大商所
    CZCE = 'CZCE'  # 郑商所
    CFFEX = 'CFFEX'  # 中金所
    INE = 'INE'  # 能源中心
    HUOBI = 'huobi' # 火币Pro
    BINANCE = 'binance' # 币安
    BITMEX = 'bitmex' # BITMEX
    BITFINEX = 'BITFINEX' # BITFINEX
    OKEX = 'OKEx' # OKEx


class OFFSET():
    """订单的开平仓属性
    OPEN 股票/期货 开仓
    CLOSE 股票 卖出
    CLOSE_HISTORY 期货 平昨
    CLOSE_TODAY 期货 平今
    REVERSE 期货 反手(默认先平昨再平今)
    """

    OPEN = 'OPEN'
    CLOSE = 'CLOSE'
    CLOSETODAY = 'CLOSETODAY'
    REVERSE = 'REVERSE'


class ORDER_MODEL():
    """订单的成交模式

    LIMIT 限价模式
    MARKET 市价单 # 目前市价单在回测中是bar的开盘价 /实盘里面是五档剩余最优成交价
    CLOSE 收盘单 # 及在bar的收盘时的价格
    NEXT_OPEN 下一个bar的开盘价成交
    STRICT 严格订单 不推荐/仅限回测/是在当前bar的最高价买入/当前bar的最低价卖出

    @yutiansut/2017-12-18
    """

    LIMIT = 'LIMIT'  # 限价
    ANY = 'ANY'  # 市价(otg兼容)
    MARKET = 'MARKET'  # 市价/在回测里是下个bar的开盘价买入/实盘就是五档剩余最优成交价
    CLOSE = 'CLOSE'  # 当前bar的收盘价买入
    NEXT_OPEN = 'NEXT_OPEN'  # 下个bar的开盘价买入
    STRICT = 'STRICT'  # 严格模式/不推荐(仅限回测测试用)
    BEST = 'BEST'  # 中金所  最优成交剩余转限
    FIVELEVEL = 'FIVELEVEL'


class ORDER_STATUS():
    """订单状态

    status1xx 订单待生成
    status3xx 初始化订单  临时扣除资产(可用现金/可卖股份)
    status3xx 订单存活(等待交易)
    status2xx 订单完全交易/未完全交易
    status4xx 主动撤单
    status500 订单死亡(每日结算) 恢复临时资产    


    订单生成(100) -- 进入待成交队列(300) -- 完全成交(200) -- 每日结算(500)-- 死亡
    订单生成(100) -- 进入待成交队列(300) -- 部分成交(203) -- 未成交(300) -- 每日结算(500) -- 死亡
    订单生成(100) -- 进入待成交队列(300) -- 主动撤单(400) -- 每日结算(500) -- 死亡
    """

    # NEW = 100
    # SUCCESS_ALL = 200
    # SUCCESS_PART = 203
    # QUEUED = 300  # queued 用于表示在order_queue中 实际表达的意思是订单存活 待成交
    # CANCEL_ALL = 400
    # CANCEL_PART = 402
    # SETTLED = 500
    # FAILED = 600

    NEW = 'new'
    SUCCESS_ALL = 'success_all'  # == FINISHED
    SUCCESS_PART = 'success_part'
    QUEUED = 'queued'  # queued 用于表示在order_queue中 实际表达的意思是订单存活 待成交 == ALIVED
    CANCEL_ALL = 'cancel_all'
    CANCEL_PART = 'cancel_part'
    SETTLED = 'settled'
    FAILED = 'failed'
    NEXT = 'next'  # 当前bar未成交,下一个bar继续等待


class AMOUNT_MODEL():
    """订单的成交量

    by_money是按固定成交总额下单,动态计算成交量
    by_amount 按固定数量下单
    """

    BY_MONEY = 'by_money'
    BY_AMOUNT = 'by_amount'


class RUNNING_ENVIRONMENT():
    """执行环境

    回测
    模拟
    t0
    实盘
    随机(按算法/分布随机生成行情)/仅用于训练测试
    """

    BACKETEST = 'backtest'
    SIMULATION = 'simulation'
    TZERO = 't0'
    REAL = 'real'
    RANDOM = 'random'
    TTS = 'tts'


class TRADE_STATUS():
    """交易状态返回值

    涨跌停限制: 202
    成功交易 : 200
    当天无交易数据: 500
    订单失败(比如买卖价格超过涨跌停价格范围,交易量过大等等):400
    """

    SUCCESS = 'trade_success'
    PRICE_LIMIT = 'trade_price_limit'  # 只是未成交
    NO_MARKET_DATA = 'trade_no_market_data'
    FAILED = 'trade_failed'


class MARKET_ERROR():
    """市场类的错误

    1. 账户以及存在(不能重复注册)
    2. 网络中断
    3. 数据库连接丢失
    4. 数值/索引不存在
    """

    ACCOUNT_EXIST = 'ACCOUNT EXIST {}'
    NETWORK_BROKERN = 'NETWORK BROKEN {}'
    DATABSECONNECT_LOST = 'DATABASECONNECTION LOST {}'
    VALUE_NOT_FOUND = 'VALUE_NOT_FOUND'


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
    STOCK_CN = 'stock_cn'  # 中国A股
    STOCK_CN_B = 'stock_cn_b'  # 中国B股
    STOCK_CN_D = 'stock_cn_d'  # 中国D股 沪伦通
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


class BROKER_TYPE():
    """执行环境

    回测
    模拟
    实盘
    随机(按算法/分布随机生成行情)/仅用于训练测试
    """

    BACKETEST = 'backtest'
    SIMULATION = 'simulation'
    REAL = 'real'
    RANDOM = 'random'
    SHIPANE = 'shipane'
    TTS = 'tts'


class EVENT_TYPE():
    """[summary]
    """

    BROKER_EVENT = 'broker_event'
    ACCOUNT_EVENT = 'account_event'
    MARKET_EVENT = 'market_event'
    TRADE_EVENT = 'trade_event'
    ENGINE_EVENT = 'engine_event'
    ORDER_EVENT = 'order_event'


class MARKET_EVENT():
    """交易前置事件
    query_order 查询订单
    query_assets 查询账户资产
    query_account 查询账户
    query_cash 查询账户现金
    query_data 请求数据
    query_deal 查询成交记录
    query_position 查询持仓
    """

    QUERY_ORDER = 'query_order'
    QUERY_ASSETS = 'query_assets'
    QUERY_ACCOUNT = 'query_account'
    QUERY_CASH = 'query_cash'
    QUERY_DATA = 'query_data'
    QUERY_DEAL = 'query_deal'
    QUERY_POSITION = 'query_position'


class ENGINE_EVENT():
    """引擎事件"""
    MARKET_INIT = 'market_init'
    UPCOMING_DATA = 'upcoming_data'
    UPCOMING_TICK = 'upcoming_tick'
    UPCOMING_BAR = 'upcoming_bar'
    BAR_SETTLE = 'bar_settle'
    DAILY_SETTLE = 'daily_settle'
    UPDATE = 'update'
    TRANSACTION = 'transaction'
    ORDER = 'order'


class ACCOUNT_EVENT():
    """账户事件"""
    UPDATE = 'account_update'
    SETTLE = 'account_settle'
    MAKE_ORDER = 'account_make_order'


class BROKER_EVENT():
    """BROKER事件
    BROKER 
    有加载数据的任务 load data
    撮合成交的任务 broker_trade

    轮询是否有成交记录 query_deal

    """
    LOAD_DATA = 'load_data'
    TRADE = 'broker_trade'
    SETTLE = 'broker_settle'
    DAILY_SETTLE = 'broker_dailysettle'
    RECEIVE_ORDER = 'receive_order'
    QUERY_DEAL = 'query_deal'
    NEXT_TRADEDAY = 'next_tradeday'


class ORDER_EVENT():
    """订单事件

    创建订单 create
    交易 trade
    撤单 cancel

    """
    CREATE = 'create'
    TRADE = 'trade'
    CANCEL = 'cancel'
    FAIL = 'fail'


class FREQUENCE():
    """查询的级别

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
    TICK = 'tick'  # transaction
    ASKBID = 'askbid'  # 上下五档/一档
    REALTIME_MIN = 'realtime_min' # 实时分钟线
    LATEST = 'latest'  # 当前bar/latest

    2019/08/06 @yutiansut
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
    TICK = 'tick'  # transaction
    ASKBID = 'askbid'  # 上下五档/一档
    REALTIME_MIN = 'realtime_min'  # 实时分钟线
    LATEST = 'latest'  # 当前bar/latest


class CURRENCY_TYPE():
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


class DATASOURCE():
    """数据来源
    """

    WIND = 'wind'  # wind金融终端
    TDB = 'tdb'  # wind tdb
    THS = 'ths'  # 同花顺网页
    TUSHARE = 'tushare'  # tushare
    TDX = 'tdx'  # 通达信
    MONGO = 'mongo'  # 本地/远程Mongodb
    EASTMONEY = 'eastmoney'  # 东方财富网
    CHOICE = 'choice'  # choice金融终端
    CCXT = 'ccxt'  # github/ccxt 虚拟货币
    LOCALFILE = 'localfile'  # 本地文件
    AUTO = 'auto'  # 优先从Mongodb中读取数据，不足的数据从tdx下载


class OUTPUT_FORMAT():
    """输出格式
    """

    DATASTRUCT = 'datastruct'
    DATAFRAME = 'dataframe'
    SERIES = 'series'
    NDARRAY = 'ndarray'
    LIST = 'list'
    JSON = 'json'


class RUNNING_STATUS():
    """运行状态

    starting 是一个占用状态

    100 - 202 - 200 - 400 - 500
    """

    PENDING = 100
    SUCCESS = 200
    STARTING = 202
    RUNNING = 300
    WRONG = 400
    STOPED = 500
    DROPED = 600


DATABASE_TABLE = {
    (MARKET_TYPE.STOCK_CN, FREQUENCE.DAY): 'stock_day',
    (MARKET_TYPE.STOCK_CN, FREQUENCE.ONE_MIN): 'stock_min',
    (MARKET_TYPE.STOCK_CN, FREQUENCE.FIVE_MIN): 'stock_min',
    (MARKET_TYPE.STOCK_CN, FREQUENCE.FIFTEEN_MIN): 'stock_min',
    (MARKET_TYPE.STOCK_CN, FREQUENCE.THIRTY_MIN): 'stock_min',
    (MARKET_TYPE.STOCK_CN, FREQUENCE.SIXTY_MIN): 'stock_min',
    (MARKET_TYPE.STOCK_CN, FREQUENCE.HOUR): 'stock_min',
    (MARKET_TYPE.STOCK_CN, FREQUENCE.TICK): 'stock_transaction',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.DAY): 'index_day',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.ONE_MIN): 'index_min',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.FIVE_MIN): 'index_min',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.FIFTEEN_MIN): 'index_min',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.THIRTY_MIN): 'index_min',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.SIXTY_MIN): 'index_min',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.HOUR): 'index_min',
    (MARKET_TYPE.INDEX_CN, FREQUENCE.TICK): 'index_transaction',
    (MARKET_TYPE.FUND_CN, FREQUENCE.DAY): 'index_day',
    (MARKET_TYPE.FUND_CN, FREQUENCE.ONE_MIN): 'index_min',
    (MARKET_TYPE.FUND_CN, FREQUENCE.FIVE_MIN): 'index_min',
    (MARKET_TYPE.FUND_CN, FREQUENCE.FIFTEEN_MIN): 'index_min',
    (MARKET_TYPE.FUND_CN, FREQUENCE.THIRTY_MIN): 'index_min',
    (MARKET_TYPE.FUND_CN, FREQUENCE.SIXTY_MIN): 'index_min',
    (MARKET_TYPE.FUND_CN, FREQUENCE.HOUR): 'index_min',
    (MARKET_TYPE.FUND_CN, FREQUENCE.TICK): 'index_transaction',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.DAY): 'future_day',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.ONE_MIN): 'future_min',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.FIVE_MIN): 'future_min',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.FIFTEEN_MIN): 'future_min',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.THIRTY_MIN): 'future_min',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.SIXTY_MIN): 'future_min',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.HOUR): 'future_min',
    (MARKET_TYPE.FUTURE_CN, FREQUENCE.TICK): 'future_transaction'
}
