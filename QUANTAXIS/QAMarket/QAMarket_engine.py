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

import copy

from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_random_with_topic,
                              QA_util_to_json_from_pandas)
from QUANTAXIS.QAUtil.QAParameter import MARKET_STATUS, TRADE_STATUS

"""stock market trading engine

renew in 2017/6/28

一个自带查询句柄的交易引擎

可以被装饰器包装,实现二次封装

"""


def market_stock_engine(order, market_data, commission_fee_coeff=0.0015):
    # 新增一个__commission_fee_coeff 手续费系数
    """MARKET ENGINE STOCK

    在拿到市场数据后对于订单的撮合判断 生成成交信息

    """

    def __trading(order, market_data):
        """
        trading system
        step1: check market_data
        step2: deal
        step3: return callback
        """

        try:
            if float(market_data['open']) == float(market_data['high']) == float(market_data['close']) == float(market_data['low']):
                return {
                    'header': {
                        'source': 'market',
                        'status': TRADE_STATUS.PRICE_LIMIT,
                        'reason': '开盘涨跌停 封版',
                        'code': str(order.code),
                        'session': {
                            'user': str(order.user),
                            'strategy': str(order.strategy)
                        },
                        'order_id': str(order.order_id),
                        'trade_id':  QA_util_random_with_topic('Trade')
                    },
                    'body': {
                        'bid': {
                            'price': 0,
                            'code': str(order.code),
                            'amount': 0,
                            'date': str(order.date),
                            'towards': order.towards
                        },
                        'market': {
                            'open': market_data['open'],
                            'high': market_data['high'],
                            'low': market_data['low'],
                            'close': market_data['close'],
                            'volume': market_data['volume'],
                            'code': market_data['code']
                        },
                        'fee': {
                            'commission': 0
                        }
                    }
                }
            elif ((float(order.price) < float(market_data["high"]) and
                    float(order.price) > float(market_data["low"])) or
                    float(order.price) == float(market_data["low"]) or
                    float(order.price) == float(market_data['high'])):
                '能成功交易的情况'
                if float(order.amount) < float(market_data['volume']) * 100 / 16:
                    deal_price = order.price
                elif float(order.amount) >= float(market_data['volume']) * 100 / 16 and \
                        float(order.amount) < float(market_data['volume']) * 100 / 8:
                    """
                    add some slippers

                    buy_price=mean(max{open,close},high)
                    sell_price=mean(min{open,close},low)
                    """
                    if int(order.towards) > 0:
                        deal_price = (max(float(market_data['open']), float(
                            market_data['close'])) + float(market_data['high'])) * 0.5
                    else:
                        deal_price = (min(float(market_data['open']), float(
                            market_data['close'])) + float(market_data['low'])) * 0.5

                else:
                    order.amount = float(market_data['volume']) / 8
                    if int(order.towards) > 0:
                        deal_price = float(market_data['high'])
                    else:
                        deal_price = float(market_data['low'])

                if int(order.towards) > 0:
                    __commission_fee = 0
                else:
                    __commission_fee = commission_fee_coeff * \
                        float(deal_price) * float(order.amount)
                    if __commission_fee < 5:
                        __commission_fee = 5

                return {
                    'header': {
                        'source': 'market',
                        'status': TRADE_STATUS.SUCCESS,
                        'code': str(order.code),
                        'session': {
                            'user': str(order.user),
                            'strategy': str(order.strategy)
                        },
                        'order_id': str(order.order_id),
                        'trade_id': QA_util_random_with_topic('Trade')
                    },
                    'body': {
                        'bid': {
                            'price': float("%.2f" % float(str(deal_price))),
                            'code': str(order.code),
                            'amount': int(order.amount),
                            'datetime': str(order.datetime),
                            'date': str(order.date),
                            'towards': int(order.towards)
                        },
                        'market': {
                            'open': market_data['open'],
                            'high': market_data['high'],
                            'low': market_data['low'],
                            'close': market_data['close'],
                            'volume': market_data['volume'],
                            'code': market_data['code']
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
                        'status': TRADE_STATUS.FAILED,
                        'code': str(order.code),
                        'session': {
                            'user': str(order.user),
                            'strategy': str(order.strategy)
                        },
                        'order_id': str(order.order_id),
                        'trade_id':  QA_util_random_with_topic('Trade')
                    },
                    'body': {
                        'bid': {
                            'price': 0,
                            'code': str(order.code),
                            'amount': 0,
                            'date': str(order.date),
                            'towards': order.towards
                        },
                        'market': {
                            'open': market_data['open'],
                            'high': market_data['high'],
                            'low': market_data['low'],
                            'close': market_data['close'],
                            'volume': market_data['volume'],
                            'code': market_data['code']
                        },
                        'fee': {
                            'commission': 0
                        }
                    }
                }

        except Exception as e:
            print(e)
            return {
                'header': {
                    'source': 'market',
                    'status': TRADE_STATUS.NO_MARKET_DATA,
                    'code': str(order.code),
                    'session': {
                        'user': str(order.user),
                        'strategy': str(order.strategy)
                    },
                    'order_id': str(order.order_id),
                    'trade_id':  QA_util_random_with_topic('Trade')
                },
                'body': {
                    'bid': {
                        'price': 0,
                        'code': str(order.code),
                        'amount': 0,
                        'date': str(order.date),
                        'towards': order.towards
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
    return __trading(order, market_data)


def market_future_engine(order, market_data=None, commission_fee_coeff=0.0015):
    # data mod
    # inside function

    def __trading(order, market_data):
        """
        trading system
        """
        try:
            if order.order_model == 'market_price':

                __order_t = order
                __order_t.price = (float(market_data["high"]) +
                                   float(market_data["low"])) * 0.5
                return __trading(__order_t, market_data)

            elif order.order_model == 'close_price':
                __order_t = order
                __order_t.price = float(market_data["close"])
                return __trading(__order_t, market_data)
            elif order.order_model == 'strict_price':
                '加入严格模式'
                __order_t = order
                if __order_t.towards == 1:

                    __order_t.price = float(market_data["high"])
                else:
                    __order_t.price = float(market_data["low"])

                return __trading(__order_t, market_data)
            else:
                if order.amount_model == 'price':
                    __order_s = order
                    __order_s.amount = int(
                        order.amount / (order.price * 100)) * 100
                    __order_s.amount_model = 'amount'
                    return __trading(__order_s, market_data)
                else:
                    if float(market_data['open']) == float(market_data['high']) == float(market_data['close']) == float(market_data['low']):
                        return {
                            'header': {
                                'source': 'market',
                                'status': 202,
                                'reason': '开盘涨跌停 封版',
                                'code': str(order.code),
                                'session': {
                                    'user': str(order.user),
                                    'strategy': str(order.strategy)
                                },
                                'order_id': str(order.order_id),
                                'trade_id':  QA_util_random_with_topic('Trade')
                            },
                            'body': {
                                'bid': {
                                    'price': 0,
                                    'code': str(order.code),
                                    'amount': 0,
                                    'date': str(order.date),
                                    'towards': order.towards
                                },
                                'market': {
                                    'open': market_data['open'],
                                    'high': market_data['high'],
                                    'low': market_data['low'],
                                    'close': market_data['close'],
                                    'volume': market_data['volume'],
                                    'code': market_data['code']
                                },
                                'fee': {
                                    'commission': 0
                                }
                            }
                        }
                    elif ((float(order.price) < float(market_data["high"]) and
                           float(order.price) > float(market_data["low"])) or
                          float(order.price) == float(market_data["low"]) or
                            float(order.price) == float(market_data['high'])):
                        '能成功交易的情况'
                        if float(order.amount) < float(market_data['volume']) * 100 / 16:
                            deal_price = order.price
                        elif float(order.amount) >= float(market_data['volume']) * 100 / 16 and \
                                float(order.amount) < float(market_data['volume']) * 100 / 8:
                            """
                            add some slippers

                            buy_price=mean(max{open,close},high)
                            sell_price=mean(min{open,close},low)
                            """
                            if int(order.towards) > 0:
                                deal_price = (max(float(market_data['open']), float(
                                    market_data['close'])) + float(market_data['high'])) * 0.5
                            else:
                                deal_price = (min(float(market_data['open']), float(
                                    market_data['close'])) + float(market_data['low'])) * 0.5

                        else:
                            order.amount = float(market_data['volume']) / 8
                            if int(order.towards) > 0:
                                deal_price = float(market_data['high'])
                            else:
                                deal_price = float(market_data['low'])

                        if int(order.towards) > 0:
                            __commission_fee = 0
                        else:
                            __commission_fee = 0.0015 * \
                                float(deal_price) * float(order.amount)
                            if __commission_fee < 5:
                                __commission_fee = 5

                        return {
                            'header': {
                                'source': 'market',
                                'status': 200,
                                'code': str(order.code),
                                'session': {
                                    'user': str(order.user),
                                    'strategy': str(order.strategy)
                                },
                                'order_id': str(order.order_id),
                                'trade_id':  QA_util_random_with_topic('Trade')
                            },
                            'body': {
                                'bid': {
                                    'price': float("%.2f" % float(str(deal_price))),
                                    'code': str(order.code),
                                    'amount': int(order.amount),
                                    'date': str(order.date),
                                    'towards': int(order.towards)
                                },
                                'market': {
                                    'open': market_data['open'],
                                    'high': market_data['high'],
                                    'low': market_data['low'],
                                    'close': market_data['close'],
                                    'volume': market_data['volume'],
                                    'code': market_data['code']
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
                                'code': str(order.code),
                                'session': {
                                    'user': str(order.user),
                                    'strategy': str(order.strategy)
                                },
                                'order_id': str(order.order_id),
                                'trade_id':  QA_util_random_with_topic('Trade')
                            },
                            'body': {
                                'bid': {
                                    'price': 0,
                                    'code': str(order.code),
                                    'amount': 0,
                                    'date': str(order.date),
                                    'towards': order.towards
                                },
                                'market': {
                                    'open': market_data['open'],
                                    'high': market_data['high'],
                                    'low': market_data['low'],
                                    'close': market_data['close'],
                                    'volume': market_data['volume'],
                                    'code': market_data['code']
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
                    'code': str(order.code),
                    'session': {
                        'user': str(order.user),
                        'strategy': str(order.strategy)
                    },
                    'order_id': str(order.order_id),
                    'trade_id':  QA_util_random_with_topic('Trade')
                },
                'body': {
                    'bid': {
                        'price': 0,
                        'code': str(order.code),
                        'amount': 0,
                        'date': str(order.date),
                        'towards': order.towards
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
    return __trading(order, market_data)


if __name__ == '__main__':
    pass
