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

"""stock market trading engine"""


def market_stock_day_engine(__bid, client):
    __coll = client.quantaxis.stock_day
    __item = __coll.find_one(
        {"code": str(__bid['code'])[0:6], "date": str(__bid['date'])[0:10]})

    def __trading(__bid, __item):
        """
        trading system
        """
        try:
            if __bid['price'] == 'market_price':
                __bid_t = __bid
                __bid_t['price'] = (float(__item["high"]) +
                                    float(__item["low"])) * 0.5
                return __trading(__bid_t, __item)
            else:
                if ((float(__bid['price']) < float(__item["high"]) and
                     float(__bid['price']) > float(__item["low"])) or
                        float(__bid['price']) == float(__item["low"]) or
                        float(__bid['price']) == float(__item['high'])):

                    if float(__bid['amount']) < float(__item['volume']) * 100 / 16:

                        __deal_price = __bid['price']
                    elif float(__bid['amount']) >= float(__item['volume']) * 100 / 16 and \
                            float(__bid['amount']) < float(__item['volume']) * 100 / 8:
                        """
                        add some slippers

                        buy_price=mean(max{open,close},high)
                        sell_price=mean(min{open,close},low)
                        """
                        if int(__bid['towards']) > 0:
                            __deal_price = (max(float(__item['open']), float(
                                __item['close'])) + float(__item['high'])) * 0.5
                        else:
                            __deal_price = (min(float(__item['open']), float(
                                __item['close'])) + float(__item['low'])) * 0.5

                    else:
                        __bid['amount'] = float(__item['volume']) / 8
                        if int(__bid['towards']) > 0:
                            __deal_price = float(__item['high'])
                        else:
                            __deal_price = float(__item['low'])

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
                                'open': __item['open'],
                                'high': __item['high'],
                                'low': __item['low'],
                                'close': __item['close'],
                                'volume': __item['volume'],
                                'code': __item['code']
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
                    'fee':{
                        'commission':0
                    }
                }
            }
    return __trading(__bid, __item)


def market_stock_min_engine(__bid, client):
    """
    time-delay stock trading engine
    """
    pass


def market_future_day_engine(__bid, client):
    """
    future market daily trading engine
    """

    pass


def market_future_min_engine(__bid, client):
    pass


def market_future_tick_engine(__bid, client):
    pass
