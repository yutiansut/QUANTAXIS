import datetime

from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_random_with_topic)


"""
需要一个可以被修改和继承的基类

带上所有的回测可能涉及的通用状态

继承的时候只需要修改一些状态

2017/8/12

"""


def market_engine_base(__bid, fp=None):
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
            """
            对于报价进行拦截
            """

            if __bid['price'] == 'market_price':

                __bid_t = __bid
                __bid_t['price'] = (float(__data["high"]) +
                                    float(__data["low"])) * 0.5
                return __trading(__bid_t, __data)

            elif __bid['price'] == 'close_price':
                __bid_t = __bid
                __bid_t['price'] = float(__data["close"])
                return __trading(__bid_t, __data)
            elif __bid['price'] == 'strict_price':
                '加入严格模式'
                __bid_t = __bid
                if __bid_t['towards'] == 1:

                    __bid_t['price'] = float(__data["high"])
                else:
                    __bid_t['price'] = float(__data["low"])

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
                        __commission_fee = 0.0015 * \
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
                            'trade_id': QA_util_random_with_topic(topic='Trade')
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
                    'trade_id': QA_util_random_with_topic(topic='Trade')
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
