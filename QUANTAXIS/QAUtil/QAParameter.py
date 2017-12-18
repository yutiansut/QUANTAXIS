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


class Order_PRICE:
    """订单的价格模式

    [description]
    """


class ORDER_AMOUNT:
    """[summary]

    [description]
    """
    pass


class MARKET_TYPE():
    """市场种类

    [description]
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


class RUNNING_ENVIRONMENT:
    """执行环境
    
    回测
    模拟
    实盘
    """
    
    BACKETEST = 1
    SIMULATION = 2
    REAL = 3


class MARKET_STATUS:
    MARKET_CLOSE=500


class TRADE_STATUS:
    """交易状态返回值
    
    涨跌停限制: 202
    成功交易 : 200
    当天无交易数据: 500
    
    """
    
    SUCCESS = 200
    NO_MARKET_DATA = 500
    PRICE_LIMIT = 202
    