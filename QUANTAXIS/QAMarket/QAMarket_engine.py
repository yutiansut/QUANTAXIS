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

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day, QA_fetch_stock_min
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_to_json_from_pandas)


"""stock market trading engine

renew in 2017/6/28

一个自带查询句柄的交易引擎

可以被装饰器包装,实现二次封装

"""


def market_stock_day_engine(__bid, __data=None, __commission_fee_coeff=0.0005):
    # data mod
    # inside function
    def __get_data(__bid):
        '隔离掉引擎查询数据库的行为'
        __data = QA_util_to_json_from_pandas(QA_fetch_stock_day(str(
            __bid.code)[0:6], str(__bid.date)[0:10], str(__bid.date)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data
    # trade mod

    if __data is None:
        __data = __get_data(__bid)
    else:
        pass

    def __trading(__bid, __data):
        """
        trading system
        """
        try:
            if __bid.price == 'market_price':

                __bid_t = __bid
                __bid_t.price = (float(__data["high"]) +
                                 float(__data["low"])) * 0.5
                return __trading(__bid_t, __data)

            elif __bid.price == 'close_price':
                __bid_t = __bid
                __bid_t.price = float(__data["close"])
                return __trading(__bid_t, __data)
            elif __bid.price == 'strict_price':
                '加入严格模式'
                __bid_t = __bid
                if __bid_t.towards == 1:

                    __bid_t.price = float(__data["high"])
                else:
                    __bid_t.price = float(__data["low"])

                return __trading(__bid_t, __data)
            else:
                if __bid.amount_model == 'price':
                    __bid_s = __bid
                    __bid_s.amount = int(
                        __bid.amount / (__bid.price * 100)) * 100
                    __bid_s.amount_model = 'amount'
                    return __trading(__bid_s, __data)
                else:
                    if float(__data['open']) == float(__data['high']) == float(__data['close']) == float(__data['low']):
                        return {
                            'header': {
                                'source': 'market',
                                'status': 202,
                                'reason': '开盘涨跌停 封版',
                                'code': str(__bid.code),
                                'session': {
                                    'user': str(__bid.user),
                                    'strategy': str(__bid.strategy)
                                },
                                'order_id': str(__bid.order_id),
                                'trade_id': str(random.random())
                            },
                            'body': {
                                'bid': {
                                    'price': 0,
                                    'code': str(__bid.code),
                                    'amount': 0,
                                    'date': str(__bid.date),
                                    'towards': __bid.towards
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
                                    'commission': 0
                                }
                            }
                        }
                    elif ((float(__bid.price) < float(__data["high"]) and
                           float(__bid.price) > float(__data["low"])) or
                          float(__bid.price) == float(__data["low"]) or
                            float(__bid.price) == float(__data['high'])):
                        '能成功交易的情况'
                        if float(__bid.amount) < float(__data['volume']) * 100 / 16:
                            __deal_price = __bid.price
                        elif float(__bid.amount) >= float(__data['volume']) * 100 / 16 and \
                                float(__bid.amount) < float(__data['volume']) * 100 / 8:
                            """
                            add some slippers

                            buy_price=mean(max{open,close},high)
                            sell_price=mean(min{open,close},low)
                            """
                            if int(__bid.towards) > 0:
                                __deal_price = (max(float(__data['open']), float(
                                    __data['close'])) + float(__data['high'])) * 0.5
                            else:
                                __deal_price = (min(float(__data['open']), float(
                                    __data['close'])) + float(__data['low'])) * 0.5

                        else:
                            __bid.amount = float(__data['volume']) / 8
                            if int(__bid.towards) > 0:
                                __deal_price = float(__data['high'])
                            else:
                                __deal_price = float(__data['low'])

                        if int(__bid.towards) > 0:
                            __commission_fee = 0
                        else:
                            __commission_fee = __commission_fee_coeff * \
                                float(__deal_price) * float(__bid.amount)
                            if __commission_fee < 5:
                                __commission_fee = 5

                        return {
                            'header': {
                                'source': 'market',
                                'status': 200,
                                'code': str(__bid.code),
                                'session': {
                                    'user': str(__bid.user),
                                    'strategy': str(__bid.strategy)
                                },
                                'order_id': str(__bid.order_id),
                                'trade_id': str(random.random())
                            },
                            'body': {
                                'bid': {
                                    'price': float("%.2f" % float(str(__deal_price))),
                                    'code': str(__bid.code),
                                    'amount': int(__bid.amount),
                                    'datetime': str(__bid.datetime),
                                    'date': str(__bid.date),
                                    'towards': int(__bid.towards)
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
                    else:
                        return {
                            'header': {
                                'source': 'market',
                                'status': 400,
                                'code': str(__bid.code),
                                'session': {
                                    'user': str(__bid.user),
                                    'strategy': str(__bid.strategy)
                                },
                                'order_id': str(__bid.order_id),
                                'trade_id': str(random.random())
                            },
                            'body': {
                                'bid': {
                                    'price': 0,
                                    'code': str(__bid.code),
                                    'amount': 0,
                                    'date': str(__bid.date),
                                    'towards': __bid.towards
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
                                    'commission': 0
                                }
                            }
                        }

        except:
            return {
                'header': {
                    'source': 'market',
                    'status': 500,
                    'code': str(__bid.code),
                    'session': {
                        'user': str(__bid.user),
                        'strategy': str(__bid.strategy)
                    },
                    'order_id': str(__bid.order_id),
                    'trade_id': str(random.random())
                },
                'body': {
                    'bid': {
                        'price': 0,
                        'code': str(__bid.code),
                        'amount': 0,
                        'date': str(__bid.date),
                        'towards': __bid.towards
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


def market_stock_engine(__bid, __data=None, __commission_fee_coeff=0.0015):
    # 新增一个__commission_fee_coeff 手续费系数

    def __trading(__bid, __data):
        """
        trading system
        """
        try:
            if float(__data['open']) == float(__data['high']) == float(__data['close']) == float(__data['low']):
                return {
                    'header': {
                        'source': 'market',
                        'status': 202,
                        'reason': '开盘涨跌停 封版',
                        'code': str(__bid.code),
                        'session': {
                            'user': str(__bid.user),
                            'strategy': str(__bid.strategy)
                        },
                        'order_id': str(__bid.order_id),
                        'trade_id': str(random.random())
                    },
                    'body': {
                        'bid': {
                            'price': 0,
                            'code': str(__bid.code),
                            'amount': 0,
                            'date': str(__bid.date),
                            'towards': __bid.towards
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
                            'commission': 0
                        }
                    }
                }
            elif ((float(__bid.price) < float(__data["high"]) and
                    float(__bid.price) > float(__data["low"])) or
                    float(__bid.price) == float(__data["low"]) or
                    float(__bid.price) == float(__data['high'])):
                '能成功交易的情况'
                if float(__bid.amount) < float(__data['volume']) * 100 / 16:
                    __deal_price = __bid.price
                elif float(__bid.amount) >= float(__data['volume']) * 100 / 16 and \
                        float(__bid.amount) < float(__data['volume']) * 100 / 8:
                    """
                    add some slippers

                    buy_price=mean(max{open,close},high)
                    sell_price=mean(min{open,close},low)
                    """
                    if int(__bid.towards) > 0:
                        __deal_price = (max(float(__data['open']), float(
                            __data['close'])) + float(__data['high'])) * 0.5
                    else:
                        __deal_price = (min(float(__data['open']), float(
                            __data['close'])) + float(__data['low'])) * 0.5

                else:
                    __bid.amount = float(__data['volume']) / 8
                    if int(__bid.towards) > 0:
                        __deal_price = float(__data['high'])
                    else:
                        __deal_price = float(__data['low'])

                if int(__bid.towards) > 0:
                    __commission_fee = 0
                else:
                    __commission_fee = __commission_fee_coeff * \
                        float(__deal_price) * float(__bid.amount)
                    if __commission_fee < 5:
                        __commission_fee = 5

                return {
                    'header': {
                        'source': 'market',
                        'status': 200,
                        'code': str(__bid.code),
                        'session': {
                            'user': str(__bid.user),
                            'strategy': str(__bid.strategy)
                        },
                        'order_id': str(__bid.order_id),
                        'trade_id': str(random.random())
                    },
                    'body': {
                        'bid': {
                            'price': float("%.2f" % float(str(__deal_price))),
                            'code': str(__bid.code),
                            'amount': int(__bid.amount),
                            'datetime': str(__bid.datetime),
                            'date': str(__bid.date),
                            'towards': int(__bid.towards)
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
            else:
                return {
                    'header': {
                        'source': 'market',
                        'status': 400,
                        'code': str(__bid.code),
                        'session': {
                            'user': str(__bid.user),
                            'strategy': str(__bid.strategy)
                        },
                        'order_id': str(__bid.order_id),
                        'trade_id': str(random.random())
                    },
                    'body': {
                        'bid': {
                            'price': 0,
                            'code': str(__bid.code),
                            'amount': 0,
                            'date': str(__bid.date),
                            'towards': __bid.towards
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
                            'commission': 0
                        }
                    }
                }

        except:
            return {
                'header': {
                    'source': 'market',
                    'status': 500,
                    'code': str(__bid.code),
                    'session': {
                        'user': str(__bid.user),
                        'strategy': str(__bid.strategy)
                    },
                    'order_id': str(__bid.order_id),
                    'trade_id': str(random.random())
                },
                'body': {
                    'bid': {
                        'price': 0,
                        'code': str(__bid.code),
                        'amount': 0,
                        'date': str(__bid.date),
                        'towards': __bid.towards
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


def market_future_engine(__bid, __data=None):
    # data mod
    # inside function
    def __get_data(__bid):
        '隔离掉引擎查询数据库的行为'
        __data = QA_util_to_json_from_pandas(QA_fetch_stock_day(str(
            __bid.code)[0:6], str(__bid.date)[0:10], str(__bid.date)[0:10], 'pd'))
        if len(__data) == 0:
            pass
        else:
            __data = __data[0]
        return __data
    # trade mod

    if __data is None:
        __data = __get_data(__bid)
    else:
        pass

    def __trading(__bid, __data):
        """
        trading system
        """
        try:
            if __bid.price == 'market_price':

                __bid_t = __bid
                __bid_t.price = (float(__data["high"]) +
                                 float(__data["low"])) * 0.5
                return __trading(__bid_t, __data)

            elif __bid.price == 'close_price':
                __bid_t = __bid
                __bid_t.price = float(__data["close"])
                return __trading(__bid_t, __data)
            elif __bid.price == 'strict_price':
                '加入严格模式'
                __bid_t = __bid
                if __bid_t.towards == 1:

                    __bid_t.price = float(__data["high"])
                else:
                    __bid_t.price = float(__data["low"])

                return __trading(__bid_t, __data)
            else:
                if __bid.amount_model == 'price':
                    __bid_s = __bid
                    __bid_s.amount = int(
                        __bid.amount / (__bid.price * 100)) * 100
                    __bid_s.amount_model = 'amount'
                    return __trading(__bid_s, __data)
                else:
                    if float(__data['open']) == float(__data['high']) == float(__data['close']) == float(__data['low']):
                        return {
                            'header': {
                                'source': 'market',
                                'status': 202,
                                'reason': '开盘涨跌停 封版',
                                'code': str(__bid.code),
                                'session': {
                                    'user': str(__bid.user),
                                    'strategy': str(__bid.strategy)
                                },
                                'order_id': str(__bid.order_id),
                                'trade_id': str(random.random())
                            },
                            'body': {
                                'bid': {
                                    'price': 0,
                                    'code': str(__bid.code),
                                    'amount': 0,
                                    'date': str(__bid.date),
                                    'towards': __bid.towards
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
                                    'commission': 0
                                }
                            }
                        }
                    elif ((float(__bid.price) < float(__data["high"]) and
                           float(__bid.price) > float(__data["low"])) or
                          float(__bid.price) == float(__data["low"]) or
                            float(__bid.price) == float(__data['high'])):
                        '能成功交易的情况'
                        if float(__bid.amount) < float(__data['volume']) * 100 / 16:
                            __deal_price = __bid.price
                        elif float(__bid.amount) >= float(__data['volume']) * 100 / 16 and \
                                float(__bid.amount) < float(__data['volume']) * 100 / 8:
                            """
                            add some slippers

                            buy_price=mean(max{open,close},high)
                            sell_price=mean(min{open,close},low)
                            """
                            if int(__bid.towards) > 0:
                                __deal_price = (max(float(__data['open']), float(
                                    __data['close'])) + float(__data['high'])) * 0.5
                            else:
                                __deal_price = (min(float(__data['open']), float(
                                    __data['close'])) + float(__data['low'])) * 0.5

                        else:
                            __bid.amount = float(__data['volume']) / 8
                            if int(__bid.towards) > 0:
                                __deal_price = float(__data['high'])
                            else:
                                __deal_price = float(__data['low'])

                        if int(__bid.towards) > 0:
                            __commission_fee = 0
                        else:
                            __commission_fee = 0.0015 * \
                                float(__deal_price) * float(__bid.amount)
                            if __commission_fee < 5:
                                __commission_fee = 5

                        return {
                            'header': {
                                'source': 'market',
                                'status': 200,
                                'code': str(__bid.code),
                                'session': {
                                    'user': str(__bid.user),
                                    'strategy': str(__bid.strategy)
                                },
                                'order_id': str(__bid.order_id),
                                'trade_id': str(random.random())
                            },
                            'body': {
                                'bid': {
                                    'price': float("%.2f" % float(str(__deal_price))),
                                    'code': str(__bid.code),
                                    'amount': int(__bid.amount),
                                    'date': str(__bid.date),
                                    'towards': int(__bid.towards)
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
                    else:
                        return {
                            'header': {
                                'source': 'market',
                                'status': 400,
                                'code': str(__bid.code),
                                'session': {
                                    'user': str(__bid.user),
                                    'strategy': str(__bid.strategy)
                                },
                                'order_id': str(__bid.order_id),
                                'trade_id': str(random.random())
                            },
                            'body': {
                                'bid': {
                                    'price': 0,
                                    'code': str(__bid.code),
                                    'amount': 0,
                                    'date': str(__bid.date),
                                    'towards': __bid.towards
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
                                    'commission': 0
                                }
                            }
                        }

        except:
            return {
                'header': {
                    'source': 'market',
                    'status': 500,
                    'code': str(__bid.code),
                    'session': {
                        'user': str(__bid.user),
                        'strategy': str(__bid.strategy)
                    },
                    'order_id': str(__bid.order_id),
                    'trade_id': str(random.random())
                },
                'body': {
                    'bid': {
                        'price': 0,
                        'code': str(__bid.code),
                        'amount': 0,
                        'date': str(__bid.date),
                        'towards': __bid.towards
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


if __name__ == '__main__':
    pass
