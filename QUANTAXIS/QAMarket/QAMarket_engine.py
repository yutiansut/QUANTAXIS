# coding :utf-8
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

#from .market_config import stock_market,future_market,HK_stock_market,US_stock_market
import datetime
import random

from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info

"""stock market trading engine

renew in 2017/6/28

停止使用数据库的模式,隔离数据库和引擎,尽量使用函数句柄来替代

"""


def market_stock_day_engine(__bid, fp=None):
    # data mod
    # inside function
    def __get_data(__bid):

        __coll = QA_Setting.client.quantaxis.stock_day
        __data = __coll.find_one(
            {"code": str(__bid['code'])[0:6], "date": str(__bid['date'])[0:10]})
        return __data
    # trade mod

    if fp == None:
        __data = __get_data(__bid)
    else:
        __data = fp(__bid)

    def __trading(__bid, __data):
        """
        trading system
        """
        try:
            if __bid['price'] == 'market_price':
                __bid_t = __bid
                __bid_t['price'] = (float(__data["high"]) +
                                    float(__data["low"])) * 0.5
                return __trading(__bid_t, __data)

            elif __bid['price'] == 'close_price':
                __bid_t = __bid
                __bid_t['price'] = float(__data["close"])
                return __trading(__bid_t, __data)
            else:
                if __bid['amount_model'] == 'price':
                    __bid_s = __bid
                    __bid_s['amount'] = int(
                        __bid['amount'] / (__bid['price'] * 100)) * 100
                    __bid_s['amount_model'] = 'amount'
                    return __trading(__bid_s, __data)
                elif ((float(__bid['price']) < float(__data["high"]) and
                       float(__bid['price']) > float(__data["low"])) or
                      float(__bid['price']) == float(__data["low"]) or
                      float(__bid['price']) == float(__data['high'])):
                    if float(__bid['amount']) < float(__data['volume']) * 100 / 16:
                        __deal_price = __bid['price']
                    elif float(__bid['amount']) >= float(__data['volume']) * 100 / 16 and \
                            float(__bid['amount']) < float(__data['volume']) * 100 / 8:
                        """
                        add some slippers

                        buy_price=mean(max{open,close},high)
                        sell_price=mean(min{open,close},low)
                        """
                        if int(__bid['towards']) > 0:
                            __deal_price = (max(float(__data['open']), float(
                                __data['close'])) + float(__data['high'])) * 0.5
                        else:
                            __deal_price = (min(float(__data['open']), float(
                                __data['close'])) + float(__data['low'])) * 0.5

                    else:
                        __bid['amount'] = float(__data['volume']) / 8
                        if int(__bid['towards']) > 0:
                            __deal_price = float(__data['high'])
                        else:
                            __deal_price = float(__data['low'])

                    if int(__bid['towards']) > 0:
                        __commission_fee = 0
                    else:
                        __commission_fee = 0.0005 * \
                            float(__deal_price) * float(__bid['amount'])
                        if __commission_fee < 5:
                            __commission_fee = 5
                    return {
                        'header': {
                            'source': 'market',
                            'status': 200,
                            'code': str(__bid['code']),
                            'session': {
                                'user': str(__bid['user']),
                                'strategy': str(__bid['strategy'])
                            },
                            'order_id': str(__bid['order_id']),
                            'trade_id': str(random.random())
                        },
                        'body': {
                            'bid': {
                                'price': str(__deal_price),
                                'code': str(__bid['code']),
                                'amount': int(__bid['amount']),
                                'date': str(__bid['date']),
                                'towards': int(__bid['towards'])
                            },
                            'market': {
                                'open': __data['open'],
                                'high': __data['high'],
                                'low': __data['low'],
                                'close': __data['close'],
                                'volume': __data['volume'],
                                'code': __data['code']
                            },
                            'fee': {
                                'commission': float(__commission_fee)
                            }
                        }
                    }

        except:
            return {
                'header': {
                    'source': 'market',
                    'status': 500,
                    'code': str(__bid['code']),
                    'session': {
                        'user': str(__bid['user']),
                        'strategy': str(__bid['strategy'])
                    },
                    'order_id': str(__bid['order_id']),
                    'trade_id': str(random.random())
                },
                'body': {
                    'bid': {
                        'price': 0,
                        'code': str(__bid['code']),
                        'amount': 0,
                        'date': str(__bid['date']),
                        'towards': __bid['towards']
                    },
                    'market': {
                        'open': 0,
                        'high': 0,
                        'low': 0,
                        'close': 0,
                        'volume': 0,
                        'code': 0
                    },
                    'fee': {
                        'commission': 0
                    }
                }
            }
    return __trading(__bid, __data)


def market_stock_min_engine(__bid, fp=None):
    """
    time-delay stock trading engine


    分钟线的成交和日线有几个不同:
    分钟线不存在滑点的问题

    如果当前报价>总成交量/4 按总成交量/4 计算

    """
    # data mod
    # inside function
    def __get_data(__bid):

        __coll = QA_Setting.client.quantaxis.stock_min_5
        __data = __coll.find_one(
            {"code": str(__bid['code'])[0:6], "datetime": {'$gte': float(__bid['time'])}})
        # 我们只需要找到这个时间点下一条数据就行
        return __data
    # trade mod

    if fp == None:
        __data = __get_data(__bid)
    else:
        __data = fp(__bid)

    def __trading(__bid, __data):
        """
        trading system
        """
        try:
            if __bid['price'] == 'market_price':
                __bid_t = __bid
                __bid_t['price'] = (float(__data["high"]) +
                                    float(__data["low"])) * 0.5
                return __trading(__bid_t, __data)

            elif __bid['price'] == 'close_price':
                __bid_t = __bid
                __bid_t['price'] = float(__data["close"])
                return __trading(__bid_t, __data)
            else:
                if __bid['amount_model'] == 'price':
                    __bid_s = __bid
                    __bid_s['amount'] = int(
                        __bid['amount'] / (__bid['price'] * 100)) * 100
                    __bid_s['amount_model'] = 'amount'
                    return __trading(__bid_s, __data)
                elif ((float(__bid['price']) < float(__data["high"]) and
                       float(__bid['price']) > float(__data["low"])) or
                      float(__bid['price']) == float(__data["low"]) or
                      float(__bid['price']) == float(__data['high'])):
                    if float(__bid['amount']) < float(__data['volume']) / 4:
                        __deal_price = __bid['price']

                    else:
                        __bid['amount'] = float(__data['volume']) / 4
                        if int(__bid['towards']) > 0:
                            __deal_price = float(__data['high'])
                        else:
                            __deal_price = float(__data['low'])

                    if int(__bid['towards']) > 0:
                        __commission_fee = 0
                    else:
                        __commission_fee = 0.0005 * \
                            float(__deal_price) * float(__bid['amount'])
                        if __commission_fee < 5:
                            __commission_fee = 5
                    return {
                        'header': {
                            'source': 'market',
                            'status': 200,
                            'code': str(__bid['code']),
                            'session': {
                                'user': str(__bid['user']),
                                'strategy': str(__bid['strategy'])
                            },
                            'order_id': str(__bid['order_id']),
                            'trade_id': str(random.random())
                        },
                        'body': {
                            'bid': {
                                'price': str(__deal_price),
                                'code': str(__bid['code']),
                                'amount': int(__bid['amount']),
                                'date': str(__bid['date']),
                                'towards': int(__bid['towards'])
                            },
                            'market': {
                                'open': __data['open'],
                                'high': __data['high'],
                                'low': __data['low'],
                                'close': __data['close'],
                                'volume': __data['volume'],
                                'code': __data['code']
                            },
                            'fee': {
                                'commission': float(__commission_fee)
                            }
                        }
                    }

        except:
            return {
                'header': {
                    'source': 'market',
                    'status': 500,
                    'code': str(__bid['code']),
                    'session': {
                        'user': str(__bid['user']),
                        'strategy': str(__bid['strategy'])
                    },
                    'order_id': str(__bid['order_id']),
                    'trade_id': str(random.random())
                },
                'body': {
                    'bid': {
                        'price': 0,
                        'code': str(__bid['code']),
                        'amount': 0,
                        'date': str(__bid['date']),
                        'towards': __bid['towards']
                    },
                    'market': {
                        'open': 0,
                        'high': 0,
                        'low': 0,
                        'close': 0,
                        'volume': 0,
                        'code': 0
                    },
                    'fee': {
                        'commission': 0
                    }
                }
            }
    return __trading(__bid, __data)


def market_future_day_engine(__bid, fp=None):
    """
    future market daily trading engine
    """
    pass


def market_future_min_engine(__bid, fp=None):
    pass


def market_future_tick_engine(__bid, fp=None):
    pass
