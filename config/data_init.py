import QUANTAXIS as QA
import clickhouse_driver
import datetime
import pprint
import numpy as np

import pandas as pd

"""
from rqdatac import *
from jqdatac import *


可以从 jqdata/ rqdata import 标准的

get_price
all_instrument
index_weight
等函数

"""


class datamodelx:

    def __init__(self, market, frequence):
        """
        current support 

        ::::
        stock
        future
        index
        ::::

        ::::
        1min
        1day




        market:


        合约类型	说明
        CS	Common Stock, 即股票
        ETF	Exchange Traded Fund, 即交易所交易基金
        LOF	Listed Open-Ended Fund，即上市型开放式基金 （以下分级基金已并入）
        INDX	Index, 即指数
        Future	Futures，即期货，包含股指、国债和商品期货
        Spot	Spot，即现货，目前包括上海黄金交易所现货合约
        Option	期权，包括目前国内已上市的全部期权合约
        Convertible	沪深两市场内有交易的可转债合约
        Repo	沪深两市交易所交易的回购合约


        1m - 分钟线
        1d - 日线
        1w - 周线，只支持'1w'
        tick

        """

        self.market_dict = {QA.MARKET_TYPE.STOCK_CN: 'CS', QA.MARKET_TYPE.FUTURE_CN: 'Future', QA.MARKET_TYPE.INDEX_CN: 'INDX',

                            QA.MARKET_TYPE.OPTION_CN: 'Option', 'etf_cn': 'ETF', 'lof_cn': 'LOF'}
        self.freq_dict = {QA.FREQUENCE.DAY: '1d', QA.FREQUENCE.ONE_MIN: '1m',
                          QA.FREQUENCE.FIVE_MIN: '5m', QA.FREQUENCE.FIFTEEN_MIN: '15m',
                          QA.FREQUENCE.TICK: 'tick'}

        self.market = market
        self.frequence = frequence

        self.table_name = self.market + '_' + self.frequence

        # clickhouse://[user:password]@localhost:9000/default{}
        self.client = clickhouse_driver.Client(host='localhost', database='quantaxis',user='', password='#',
                                               settings={
                                                   'insert_block_size': 100000000},
                                               compression=True)

        self.codelist = self.get_list().sort_values('listed_date', ascending=False)
        self.temp_data = []

    @property
    def today(self):
        return str(datetime.date.today())

    def __repr__(self):
        return self.market


    def create_table(self):

        #self.client.execute('DROP TABLE IF EXISTS {}'.format(self.table_name))
        if 'day' in self.frequence:

            if 'stock' in self.market:
                print('s')
                """
                    ['order_book_id', 'date', 'num_trades', 'close', 'limit_up', 'low',
               'open', 'high', 'limit_down', 'volume', 'total_turnover']
                """

                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        num_trades Float32,\
                        limit_up  Float32,\
                        limit_down  Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`date`)) \
                    ORDER BY (date, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'index' in self.market:

                """
                'order_book_id', 'date', 'total_turnover', 'num_trades', 'open', 'low',
                'high', 'volume', 'close'
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        num_trades Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`date`)) \
                    ORDER BY (date, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'future' in self.market:

                """                
                ['order_book_id', 'date', 'limit_down', 'low', 'limit_up',
                'total_turnover', 'high', 'open_interest', 'prev_settlement', 'open',
                'volume', 'settlement', 'close']
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        limit_up  Float32,\
                        limit_down  Float32,\
                        open_interest Float32,\
                        prev_settlement Float32,\
                        settlement Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`date`)) \
                    ORDER BY (date, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)

            elif 'lof' in self.market:
                """
                ['order_book_id', 'date', 'limit_up', 'high', 'iopv', 'open', 'low', 'num_trades', 'close',
                'volume', 'total_turnover', 'limit_down'],
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        limit_up  Float32,\
                        limit_down  Float32,\
                        iopv Float32,\
                        num_trades Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`date`)) \
                    ORDER BY (date, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'etf' in self.market:
                """
                ['order_book_id', 'date', 'limit_up', 'high', 'iopv', 'open', 'low',
                'num_trades', 'close', 'volume', 'total_turnover', 'limit_down']
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        limit_up  Float32,\
                        limit_down  Float32,\
                        iopv Float32,\
                        num_trades Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`date`)) \
                    ORDER BY (date, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'option' in self.market:
                """
                ['order_book_id', 'date', 'limit_up', 'contract_multiplier',
                    'strike_price', 'open_interest', 'high', 'open', 'low', 'close',
                    'volume', 'settlement', 'prev_settlement', 'total_turnover',
                    'limit_down']
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        limit_up  Float32,\
                        limit_down  Float32,\
                        strike_price Float32,\
                        contract_multiplier Float32,\
                        open_interest Float32,\
                        settlement Float32,\
                        prev_settlement Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`date`)) \
                    ORDER BY (date, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)

        elif 'min' in self.frequence:

            if 'stock' in self.market:
                """
                   ['order_book_id', 'datetime', 'low', 'total_turnover', 'high', 'open',
                   'volume', 'close']
                """

                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    datetime Datetime DEFAULT '1970-01-01',\
                        order_book_id String,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`datetime`)) \
                    ORDER BY (datetime, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'index' in self.market:

                """
                'order_book_id', 'date', 'total_turnover', 'num_trades', 'open', 'low',
                'high', 'volume', 'close'
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    datetime Datetime DEFAULT '1970-01-01',\
                        order_book_id String,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`datetime`)) \
                    ORDER BY (datetime, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)

            elif 'future' in self.market:

                """                
                ['order_book_id', 'datetime', 'low', 'total_turnover', 'high',
                       'open_interest', 'trading_date', 'open', 'volume', 'close']
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    datetime Datetime DEFAULT '1970-01-01',\
                    trading_date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        open_interest Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`datetime`)) \
                    ORDER BY (datetime, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'option' in self.market:

                """                
                ['order_book_id', 'datetime', 'open_interest', 'high', 'open', 'low',
                'trading_date', 'close', 'volume', 'total_turnover'],
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    datetime Datetime DEFAULT '1970-01-01',\
                    trading_date Date DEFAULT '1970-01-01',\
                        order_book_id String,\
                        open_interest Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`datetime`)) \
                    ORDER BY (datetime, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'etf' in self.market:

                """                
                ['order_book_id', 'datetime', 'high', 'iopv', 'open', 'low', 'close',
                    'volume', 'total_turnover'],
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    datetime Datetime DEFAULT '1970-01-01',\
                        order_book_id String,\
                        iopv Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`datetime`)) \
                    ORDER BY (datetime, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
            elif 'lof' in self.market:

                """                
                ['order_book_id', 'datetime', 'high', 'iopv', 'open', 'low', 'close',
                    'volume', 'total_turnover'],
                """
                query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`{}` (\
                    datetime Datetime DEFAULT '1970-01-01',\
                        order_book_id String,\
                        iopv Float32,\
                        open Float32,\
                        high Float32,\
                        low Float32,\
                        close Float32,\
                        volume Float32,\
                        total_turnover Float32\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    PARTITION BY (toYYYYMMDD(`datetime`)) \
                    ORDER BY (datetime, order_book_id)\
                    SETTINGS index_granularity=8192".format(self.table_name)
        elif 'tick' in self.frequence:
            if 'stock' in self.market:
                query = "CREATE TABLE IF NOT EXISTS \
                    `quantaxis`.`{}` (\
                        datetime Datetime DEFAULT '1970-01-01',\
                        trading_date Date, \
                        order_book_id String,\
                        open Float32,\
                        last Float32,\
                        high Float32,\
                        low  Float32,\
                        prev_close Float32,\
                        volume   Float32,\
                        total_turnover Float32,\
                        limit_up  Float32,\
                        limit_down Float32,\
                        a1  Float32,\
                        a2  Float32,\
                        a3  Float32,\
                        a4  Float32,\
                        a5  Float32,\
                        b1  Float32,\
                        b2  Float32,\
                        b3  Float32,\
                        b4  Float32,\
                        b5  Float32,\
                        a1_v Float32,\
                        a2_v Float32,\
                        a3_v Float32,\
                        a4_v Float32,\
                        a5_v Float32,\
                        b1_v Float32,\
                        b2_v Float32,\
                        b3_v Float32,\
                        b4_v Float32,\
                        b5_v Float32,\
                        change_rate Float32\
                        )\
                        ENGINE = ReplacingMergeTree() \
                        PARTITION BY (toYYYYMMDD(`datetime`)) \
                        ORDER BY (datetime, order_book_id)\
                        SETTINGS index_granularity=8192".format(self.table_name)
            elif 'future' in self.market:
                query = "CREATE TABLE IF NOT EXISTS \
                    `quantaxis`.`{}` (\
                        datetime Datetime DEFAULT '1970-01-01',\
                        trading_date Date, \
                        order_book_id String,\
                        open Float32,\
                        last Float32,\
                        high Float32,\
                        low  Float32,\
                        prev_settlement Float32,\
                        prev_close Float32,\
                        open_interest Float32,\
                        volume   Float32,\
                        total_turnover Float32,\
                        limit_up  Float32,\
                        limit_down Float32,\
                        a1  Float32,\
                        a2  Float32,\
                        a3  Float32,\
                        a4  Float32,\
                        a5  Float32,\
                        b1  Float32,\
                        b2  Float32,\
                        b3  Float32,\
                        b4  Float32,\
                        b5  Float32,\
                        a1_v Float32,\
                        a2_v Float32,\
                        a3_v Float32,\
                        a4_v Float32,\
                        a5_v Float32,\
                        b1_v Float32,\
                        b2_v Float32,\
                        b3_v Float32,\
                        b4_v Float32,\
                        b5_v Float32,\
                        change_rate Float32\
                        )\
                        ENGINE = ReplacingMergeTree() \
                        PARTITION BY (toYYYYMMDD(`datetime`)) \
                        ORDER BY (datetime, order_book_id)\
                        SETTINGS index_granularity=8192".format(self.table_name)
            elif 'option' in self.market:
                """
                ['order_book_id', 'datetime', 'trading_date', 'open', 'last', 'high',
                'low', 'prev_settlement', 'prev_close', 'volume', 'open_interest',
                'total_turnover', 'limit_up', 'limit_down', 'a1', 'a2', 'a3', 'a4',
                'a5', 'b1', 'b2', 'b3', 'b4', 'b5', 'a1_v', 'a2_v', 'a3_v', 'a4_v',
                'a5_v', 'b1_v', 'b2_v', 'b3_v', 'b4_v', 'b5_v', 'change_rate'],
                """
                query = "CREATE TABLE IF NOT EXISTS \
                    `quantaxis`.`{}` (\
                        datetime Datetime DEFAULT '1970-01-01',\
                        trading_date Date, \
                        order_book_id String,\
                        open Float32,\
                        last Float32,\
                        high Float32,\
                        low  Float32,\
                        prev_settlement Float32,\
                        prev_close Float32,\
                        open_interest Float32,\
                        volume   Float32,\
                        total_turnover Float32,\
                        limit_up  Float32,\
                        limit_down Float32,\
                        a1  Float32,\
                        a2  Float32,\
                        a3  Float32,\
                        a4  Float32,\
                        a5  Float32,\
                        b1  Float32,\
                        b2  Float32,\
                        b3  Float32,\
                        b4  Float32,\
                        b5  Float32,\
                        a1_v Float32,\
                        a2_v Float32,\
                        a3_v Float32,\
                        a4_v Float32,\
                        a5_v Float32,\
                        b1_v Float32,\
                        b2_v Float32,\
                        b3_v Float32,\
                        b4_v Float32,\
                        b5_v Float32,\
                        change_rate Float32\
                        )\
                        ENGINE = ReplacingMergeTree() \
                        PARTITION BY (toYYYYMMDD(`datetime`)) \
                        ORDER BY (datetime, order_book_id)\
                        SETTINGS index_granularity=8192".format(self.table_name)

            elif 'index' in self.market:
                query = "CREATE TABLE IF NOT EXISTS \
                    `quantaxis`.`{}` (\
                        datetime Datetime DEFAULT '1970-01-01',\
                        trading_date Date, \
                        order_book_id String,\
                        open Float32,\
                        last Float32,\
                        high Float32,\
                        low  Float32,\
                        prev_close Float32,\
                        volume   Float32,\
                        total_turnover Float32,\
                        limit_up  Float32,\
                        limit_down Float32,\
                        a1  Float32,\
                        a2  Float32,\
                        a3  Float32,\
                        a4  Float32,\
                        a5  Float32,\
                        b1  Float32,\
                        b2  Float32,\
                        b3  Float32,\
                        b4  Float32,\
                        b5  Float32,\
                        a1_v Float32,\
                        a2_v Float32,\
                        a3_v Float32,\
                        a4_v Float32,\
                        a5_v Float32,\
                        b1_v Float32,\
                        b2_v Float32,\
                        b3_v Float32,\
                        b4_v Float32,\
                        b5_v Float32,\
                        change_rate Float32\
                        )\
                        ENGINE = ReplacingMergeTree() \
                        PARTITION BY (toYYYYMMDD(`datetime`)) \
                        ORDER BY (datetime, order_book_id)\
                        SETTINGS index_granularity=8192".format(self.table_name)
            elif 'lof' in self.market:
                """
                ['order_book_id', 'datetime', 'trading_date', 'open', 'last', 'high',
                'low', 'prev_close', 'volume', 'total_turnover', 'limit_up',
                'limit_down', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4',
                'b5', 'a1_v', 'a2_v', 'a3_v', 'a4_v', 'a5_v', 'b1_v', 'b2_v', 'b3_v',
                'b4_v', 'b5_v', 'change_rate', 'iopv', 'prev_iopv']
                """
                query = "CREATE TABLE IF NOT EXISTS \
                    `quantaxis`.`{}` (\
                        datetime Datetime DEFAULT '1970-01-01',\
                        trading_date Date, \
                        order_book_id String,\
                        open Float32,\
                        last Float32,\
                        high Float32,\
                        low  Float32,\
                        prev_close Float32,\
                        volume   Float32,\
                        total_turnover Float32,\
                        limit_up  Float32,\
                        limit_down Float32,\
                        a1  Float32,\
                        a2  Float32,\
                        a3  Float32,\
                        a4  Float32,\
                        a5  Float32,\
                        b1  Float32,\
                        b2  Float32,\
                        b3  Float32,\
                        b4  Float32,\
                        b5  Float32,\
                        a1_v Float32,\
                        a2_v Float32,\
                        a3_v Float32,\
                        a4_v Float32,\
                        a5_v Float32,\
                        b1_v Float32,\
                        b2_v Float32,\
                        b3_v Float32,\
                        b4_v Float32,\
                        b5_v Float32,\
                        change_rate Float32,\
                        iopv Float32,\
                        prev_iopv\
                        )\
                        ENGINE = ReplacingMergeTree() \
                        PARTITION BY (toYYYYMMDD(`datetime`)) \
                        ORDER BY (datetime, order_book_id)\
                        SETTINGS index_granularity=8192".format(self.table_name)
        pprint.pprint(query)
        self.client.execute(query)

    def get_list(self, date=None):
        """
        order_book_id	str	证券代码，证券的独特的标识符。应以'.XSHG'或'.XSHE'或'.XHKG'结尾。 '.XSHG' - 上证，'.XSHE' - 深证， '.XHKG' - 港股
        symbol	str	证券的简称，例如'平安银行'
        abbrev_symbol	str	证券的名称缩写，在中国 A 股就是股票的拼音缩写。例如：'PAYH'就是平安银行股票的证券名缩写
        round_lot	int	一手对应多少股，中国 A 股一手是 100 股
        sector_code	str	板块缩写代码，全球通用标准定义
        sector_code_name	str	以当地语言为标准的板块代码名
        industry_code	str	国民经济行业分类代码，具体可参考下方“Industry 列表”
        industry_name	str	国民经济行业分类名称
        listed_date	str	该证券上市日期
        issue_price	float	该证券发行价 （元）
        de_listed_date	str	退市日期
        type	str	合约类型，目前支持的类型有: 'CS', 'INDX', 'LOF', 'ETF', 'Future'
        underlying_order_book_id已废弃	str	追踪基准的合约代码。目前仅限'ETF','LOF'
        underlying_name 已废弃	str	追踪基准的合约名称。目前仅限'ETF','LOF'
        concept_names 已废弃	str	概念股分类，例如：'铁路基建'，'基金重仓'等
        exchange	str	交易所，'XSHE' - 深交所, 'XSHG' - 上交所
        board_type	str	板块类别，'MainBoard' - 主板,'GEM' - 创业板,'SME' - 中小企业板,'KSH' - 科创板
        status	str	合约状态。'Active' - 正常上市, 'Delisted' - 终止上市, 'TemporarySuspended' - 暂停上市, 'PreIPO' - 发行配售期间, 'FailIPO' - 发行失败
        special_type	str	特别处理状态。'Normal' - 正常上市, 'ST' - ST 处理, 'StarST' - *ST 代表该股票正在接受退市警告, 'PT' - 代表该股票连续 3 年收入为负，将被暂停交易, 'Other' - 其他
        trading_hours	str	合约交易时间
        least_redeem	str	最低申赎份额，仅对 ETF 基金展示
        cross_market	str	沪深港通标识。True-支持，False-不支持。仅对港股生效
        eng_symbol	str	英文简称。仅对港股生效

        order_book_id	str	期货代码，期货的独特的标识符（郑商所期货合约数字部分进行了补齐。例如原有代码'ZC609'补齐之后变为'ZC1609'）。主力连续合约 UnderlyingSymbol+88，例如'IF88' ；指数连续合约命名规则为 UnderlyingSymbol+99
        symbol	str	期货的简称，例如'沪深 1005'
        margin_rate	float	期货合约的最低保证金率
        round_lot	float	期货全部为 1.0
        listed_date	str	期货的上市日期。主力连续合约与指数连续合约都为'0000-00-00'
        de_listed_date	str	期货的退市日期。
        industry_name	str	行业分类名称
        trading_code	str	交易代码
        market_tplus	str	交易制度。'0'表示 T+0，'1'表示 T+1，往后顺推
        type	str	合约类型，'Future'
        contract_multiplier	float	合约乘数，例如沪深 300 股指期货的乘数为 300.0
        underlying_order_book_id	str	合约标的代码，目前除股指期货(IH, IF, IC)之外的期货合约，这一字段全部为'null'
        underlying_symbol	str	合约标的名称，例如 IF1005 的合约标的名称为'IF'
        maturity_date	str	期货到期日。主力连续合约与指数连续合约都为'0000-00-00'
        exchange	str	交易所，'DCE' - 大连商品交易所, 'SHFE' - 上海期货交易所，'CFFEX' - 中国金融期货交易所, 'CZCE'- 郑州商品交易所
        trading_hours	str	合约交易时间
        product	str	合约种类，'Commodity'-商品期货，'Index'-股指期货，'Government'-国债期货
        """

        return all_instruments(type=self.market_dict[self.market], market='cn', date=date)

    def get_all_history(self):
        codelist = self.codelist.order_book_id.tolist()
        print(codelist)
        return get_price(codelist, start_date='2000-01-04', end_date=self.endtime,
                         frequency=self.freq_dict[self.frequence], adjust_type='none', expect_df=True)

    def get_code(self, code):
        return get_price(code, start_date='2000-01-04', end_date=self.endtime,
                         frequency=self.freq_dict[self.frequence], adjust_type='none', expect_df=True)

    @property
    def endtime(self):
        return self.get_end_time()

    def get_end_time(self):

        now = datetime.datetime.today()
        if now.hour < 15:
            """
            日内
            """
            end = QA.QA_util_get_last_day(datetime.date.today()) + ' 17:00:00'
        else:
            end = str(self.today) + ' 17:00:00'
        # print(end)
        return end

    def get_data(self, start, end=None):

        codelist = self.codelist.order_book_id.tolist()

        if end is None:
            end = self.endtime
        print('get data', start, end)
        return get_price(codelist, start_date=start, end_date=end,
                         frequency=self.freq_dict[self.frequence], adjust_type='none', expect_df=True)

    def get_raw(self, code, start, end):
        return get_price(code, start_date=start, end_date=end,
                         frequency=self.freq_dict[self.frequence], adjust_type='none', expect_df=True)

    def save_history(self, data=None):
        """ 
        """

        self.create_table()
        print(self.market)
        if 'day' in self.frequence:
            if data is None:
                self.temp_data = self.get_all_history()

            self.save_data(self.temp_data)
        elif 'min' in self.frequence:
            if data is None:
                codelist = self.codelist.order_book_id.tolist()
                for code in codelist:
                    print(code, codelist.index(code), len(codelist))
                    self.temp_data = self.get_code(code)
                    if self.temp_data is None:
                        pass
                    else:
                        self.save_data(self.temp_data)
        elif 'tick' in self.frequence:

            if data is None:

                datelist = QA.QA_util_get_trade_range(
                    '2000-01-01',  self.endtime[0:10])[::-1]
                codelist = self.codelist.order_book_id.tolist()
                for date in datelist:
                    print(date, datelist.index(date), len(datelist))

                    if 'stock' in self.market:

                        for ic in range(0, len(codelist), 120):

                            codes = codelist[ic:ic+120]
                            #print(codes, date)
                            self.temp_data = self.get_raw(
                                codes, date+' 00:00:00', date+' 23:59:59')

                            if self.temp_data is None:
                                pass
                            else:
                                self.save_data(self.temp_data)
                    elif 'future' in self.market:

                        codelist = self.get_list(date).order_book_id.tolist()

                        for ic in range(0, len(codelist), 20):

                            codes = codelist[ic:ic+20]
                            print(ic, codes)
                            self.temp_data = self.get_raw(
                                codes, date+' 00:00:00', date+' 23:59:59.999')
                            if self.temp_data is None:
                                pass
                            else:
                                self.save_data(self.temp_data)

    def resave_history(self, start_id=0):
        """
        集中下载时候的
        """

        if 'day' in self.frequence:
            pass
        elif 'min' in self.frequence:

            codelist = self.codelist.order_book_id.tolist()
            for code in codelist[start_id:]:
                print(code, codelist.index(code), len(codelist))
                data = self.get_code(code)
                if data is None:
                    pass
                else:
                    self.save_data(data)
        elif 'tick' in self.frequence:

            codelist = self.codelist.order_book_id.tolist()
            datelist = QA.QA_util_get_trade_range(
                '2000-01-01', self.endtime[0:10])[::-1]

            for date in datelist[start_id:]:
                print(date, datelist.index(date), len(datelist))
                codelist = self.codelist.order_book_id.tolist()
                self.temp_data = self.get_raw(
                    codelist, date+' 00:00:00', date+' 23:59:59')

                if self.temp_data is None:
                    pass
                else:
                    self.save_data(self.temp_data)

    def save_data(self, data):
        """
        save data
        """
        print(data)
        if 'day' in self.frequence:
            data = data.reset_index().sort_values('date').to_dict('records')
            rangex = 100
        elif 'min' in self.frequence:
            data = data.reset_index().sort_values('datetime').to_dict('records')
            rangex = 10000

        elif 'tick' in self.frequence:
            data = data.reset_index().sort_values('datetime').to_dict('records')
            rangex = 800000


        print('finish process data')

        for i in range(0, len(data), rangex):
            self.client.execute('INSERT INTO {} VALUES'.format(
                self.table_name), data[i:i+rangex])
        self.client.execute('optimize table {}'.format(self.table_name))

    def drop_table(self):

        self.client.execute('DROP TABLE IF EXISTS {}'.format(self.table_name))

    def query_dblastdate(self,):
        if 'min' in self.frequence:
            return self.client.execute('SELECT datetime from quantaxis.{} order by datetime desc limit 1'.format(self.table_name))[0][0]
        elif 'day' in self.frequence:
            return self.client.execute('SELECT date from quantaxis.{} order by date desc limit 1'.format(self.table_name))[0][0]

    def update_all(self):
        lastdate = self.query_dblastdate()
        print('last datetime in database', lastdate)
        data = self.get_data(lastdate)
        self.save_data(data)

    def update_today(self):
        now = datetime.datetime.now()
        if now.hour > 15 and now.hour < 21:
            date = str(datetime.date.today())
            yes_night = QA.QA_util_get_last_day(date) + ' 20:50:00'
            end = date + ' 17:00:00'
            print(yes_night, end)
            self.temp_data = self.get_data(start=yes_night, end=end)
            self.save_data(self.temp_data)

    def update_from(self, start):
        data = self.get_data(start)
        self.save_data(data)

    def save_codelist(self):
        if 'stock' in self.market:
            self.client.execute('DROP TABLE IF EXISTS stock_cn_codelist')
            self.client.execute("CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`stock_cn_codelist` (\
                    order_book_id String,\
                    industry_code String,\
                    market_tplus  Int32,\
                    symbol   String,\
                    special_type  String,\
                    exchange    String,\
                    status      String,\
                    type       String,\
                    de_listed_date   String,\
                    listed_date   String,\
                    sector_code_name String,\
                    abbrev_symbol String,\
                    sector_code  String,\
                    round_lot Float32,\
                    trading_hours String,\
                    board_type  String,\
                    industry_name  String,\
                    issue_price  Float32,\
                    trading_code String,\
                    purchasedate   String\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    ORDER BY (listed_date, order_book_id)\
                    SETTINGS index_granularity=8192")

            rangex = 1000
            data = self.codelist.assign(issue_price=self.codelist.issue_price.fillna(
                0.0)).fillna('nan').to_dict('records')
            #data  = data.assign(listed_date=pd.to_datetime(data.listed_date))

            for i in range(0, len(data), rangex):
                print(i)
                # print(data[i:i+rangex])
                self.client.execute(
                    'INSERT INTO stock_cn_codelist VALUES', data[i:i+rangex])

            self.client.execute('optimize table stock_cn_codelist')
    def save_fundlist(self):

        self.client.execute('DROP TABLE IF EXISTS fund_cn_codelist')
        self.client.execute("CREATE TABLE IF NOT EXISTS \
            `quantaxis`.`fund_cn_codelist` (\
                order_book_id String,\
                establishment_date String,\
                listed_date  String,\
                transition_time   Int64,\
                amc  String,\
                symbol    String,\
                fund_type      String,\
                fund_manager       String,\
                latest_size   Float32,\
                benchmark   String,\
                accrued_daily Boolean,\
                de_listed_date String,\
                stop_date  String,\
                exchange String,\
                round_lot Float32\
                )\
                ENGINE = ReplacingMergeTree() \
                ORDER BY (order_book_id)\
                SETTINGS index_granularity=8192")


        rangex = 1000
        data  = fund.all_instruments()
        data =data.assign(benchmark=data.benchmark.map(str)).to_dict('records')
        for i in range(0, len(data), rangex):
            print(i)
            # print(data[i:i+rangex])
            self.client.execute(
                'INSERT INTO fund_cn_codelist VALUES', data[i:i+rangex])

        self.client.execute('optimize table fund_cn_codelist')




    def save_adj_factor(self):
        if 'stock' in self.market:
            codelist = self.codelist.order_book_id.tolist()
            fac = get_ex_factor(codelist, start_date='1990-01-01',
                                end_date=self.endtime, market='cn')
            print('finish get factor')

            def apply_adjust(fac):
                u1 = fac.reset_index()  # .query('order_book_id=="000001.XSHE"')
                u1 = u1.assign(
                    adj=(1/u1.ex_factor.values[::-1].cumprod())[::-1])
                eu = pd.concat([u1.loc[:, ['ex_date', 'adj']], pd.DataFrame(pd.to_datetime(QA.trade_date_sse), columns=[
                               'ex_date'])]).sort_values('ex_date').bfill().set_index('ex_date').loc[:datetime.date.today()].fillna(1)  # .dropna()
                return eu.shift(-1).fillna(1)

            fu = fac.groupby('order_book_id').apply(apply_adjust).reset_index()
            fu.columns = ['order_book_id', 'date', 'adj']
            print('finish execute factor')
            data = fu.sort_values('date').to_dict('records')
            print('prepare clear database')
            self.client.execute('DROP TABLE IF EXISTS stock_adj')
            query = "CREATE TABLE IF NOT EXISTS \
                `quantaxis`.`stock_adj` (\
                    date Date DEFAULT '1970-01-01',\
                    adj Float32,\
                    order_book_id String\
                    )\
                    ENGINE = ReplacingMergeTree() \
                    ORDER BY (date, order_book_id)\
                    SETTINGS index_granularity=8192"
            self.client.execute(query)

            print('prepare insert database')


            self.client.execute(
                    'INSERT INTO stock_adj VALUES', data)

            self.client.execute('optimize table stock_adj')

    def save_list(self):
        pass

    def quit(self):
        self.client.disconnect()
