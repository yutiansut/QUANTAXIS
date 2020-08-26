# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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

import pandas as pd

from QUANTAXIS.QAUtil import QA_util_log_info, QA_util_random_with_topic
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, TRADE_STATUS
"""撮合类

一个无状态的 Serverless Dealer

输入是

self.market_data
self.order
rules

输出是

standard message

"""


class commission():
    if_buyside_commission = False
    if_sellside_commission = True
    if_commission = if_buyside_commission and if_sellside_commission


class QA_Dealer():
    """[summary]


    对于不同的市场规则:
    股票市场 t+1
    期货/期权/加密货币市场 t+0

    股票/加密货币市场不允许卖空
    期货/期权市场允许卖空

    t+1的市场是
    当日的买入 更新持仓- 不更新可卖数量- 资金冻结
    当日的卖出 及时更新可用资金

    t+0市场是:
    当日买入 即时更新持仓和可卖
    当日卖出 即时更新

    卖空的规则是
    允许无仓位的时候卖出证券(按市值和保证金比例限制算)
    """

    def __init__(self, *args, **kwargs):
        self.deal_name = ''
        self.session = {}
        self.order = None
        self.market_data = None
        self.commission_fee = None
        self.tax = None
        self.trade_time = None
        self.status = None
        self.trade_money = 0
        self.dealheader = [
            'account_cookie',
            'order_time',
            'trade_time',
            'code',
            'name',
            'towards',
            'trade_price',
            'order_price',
            'status',
            'order_amount',
            'trade_amount',
            'trade_money',
            'cancel_amount',
            'realorder_id',
            'trade_id'
        ]
        self.deal_message = {}

    def deal(self, order, market_data):
        self.order = order
        self.market_data = market_data
        self.deal_price = 0
        self.deal_amount = 0
        self.order.tax_coeff = order.tax_coeff
        self.order.realorder_id = self.order.order_id

        res = self.backtest_dealer()
        self.deal_message[self.order.realorder_id] = res


    @property
    def deal_df(self):
        return pd.DataFrame(
            data=list(self.deal_message.values()),
            columns=self.dealheader
        )

    def settle(self):
        """撮合部分settle事件
        """

        self.deal_message = {}

    @property
    def callback_message(self):
        # 这是标准的return back message

        return [
            self.order.account_cookie,
            self.order.sending_time,
            self.trade_time,
            self.order.code,
            None,
            self.order.towards,
            float("%.2f" % float(self.deal_price)),
            self.order.price,
            self.status,
            self.order.amount,
            self.deal_amount,
            self.trade_money,
            0,
            self.order.order_id,
            QA_util_random_with_topic('Trade')
        ]

    def cal_fee(self):
        if self.order.market_type == MARKET_TYPE.STOCK_CN:
            if int(self.order.towards) > 0:
                commission_fee = self.order.commission_coeff * \
                    float(self.deal_price) * float(self.order.amount)
                self.commission_fee = 5 if commission_fee < 5 else commission_fee

                self.tax = 0                                     # 买入不收印花税
            else:
                commission_fee = self.order.commission_coeff * \
                    float(self.deal_price) * float(self.order.amount)

                self.commission_fee = 5 if commission_fee < 5 else commission_fee

                self.tax = self.order.tax_coeff * \
                    float(self.deal_price) * float(self.order.amount)

            self.trade_money = self.deal_price * \
                self.deal_amount + self.commission_fee + self.tax
        elif self.order.market_type == MARKET_TYPE.FUTURE_CN:
            # 期货不收税
            # 双边手续费 也没有最小手续费限制
            self.commission_fee = self.order.commission_coeff * \
                float(self.deal_price) * float(self.order.amount)
            #self.commission_fee = 5 if commission_fee < 5 else commission_fee

            self.tax = 0 # 买入不收印花税

    def backtest_dealer(self):
        # 新增一个__commission_fee_coeff 手续费系数
        """MARKET ENGINE STOCK

        在拿到市场数据后对于订单的撮合判断 生成成交信息


        trading system
        step1: check self.market_data
        step2: deal
        step3: return callback
        """
        try:
            if float(self.market_data.get('open')) == float(self.market_data.get('high')) == float(self.market_data.get('close')) == float(self.market_data.get('low')) and \
                    self.market_data.get('volume',self.market_data.get('position')) < 4*self.order.amount:
                # 调整 : 分钟线 经常处于一个价位 但不代表不能交易 所以加入量的判断(但是不能影响市场, 所以加上4倍量限制)

                self.status = TRADE_STATUS.PRICE_LIMIT
                self.deal_price = 0
                self.deal_amount = 0

            elif float(self.order.price) <= float(self.market_data.get('high')) and \
                   float(self.order.price) >= float(self.market_data.get('low')):
                '能成功交易的情况 有滑点调整'
                if float(self.order.amount) < float(self.market_data.get(
                        'volume',
                        self.market_data.get('position'))) * 100 / 16:
                    self.deal_price = self.order.price
                    self.deal_amount = self.order.amount
                elif float(self.order.amount) >= float(self.market_data.get('volume',self.market_data.get('position'))) * 100 / 16 and \
                        float(self.order.amount) < float(self.market_data.get('volume',self.market_data.get('position'))) * 100 / 8:
                    """
                    add some slippers

                    buy_price=mean(max{open,close},high)
                    sell_price=mean(min{open,close},low)
                    """
                    if int(self.order.towards) > 0:
                        self.deal_price = (
                            max(
                                float(self.market_data.get('open')),
                                float(self.market_data.get('close'))
                            ) + float(self.market_data.get('high'))
                        ) * 0.5
                    else:
                        self.deal_price = (
                            min(
                                float(self.market_data.get('open')),
                                float(self.market_data.get('close'))
                            ) + float(self.market_data.get('low'))
                        ) * 0.5
                    self.deal_amount = self.order.amount

                else:
                    self.deal_amount = float(
                        self.market_data
                        .get('volume',
                             self.market_data.get('position'))
                    ) / 8
                    if int(self.order.towards) > 0:
                        self.deal_price = float(self.market_data.get('high'))
                    else:
                        self.deal_price = float(self.market_data.get('low'))
                self.status = TRADE_STATUS.SUCCESS
                # print(self.market_data)
                self.trade_time = self.market_data.get(
                    'datetime',
                    self.market_data.get('date',
                                         None)
                )
            elif float(self.order.price) > float(self.market_data.get('high')) and int(self.order.towards) > 0:
                # 买入价格> 最高价
                #==> 按最高价成交
                self.order.price = self.market_data.get('high')
                self.backtest_dealer()
            
            elif float(self.order.price) < float(self.market_data.get('low')) and int(self.order.towards) < 0:
                # 卖出价格< 最低价 

                #==> 按最低价成交
                self.order.price = self.market_data.get('low')
                self.backtest_dealer()
            
            else:
                print('failed to deal this order')
                print(self.order.to_dict())
                print(self.order.price)
                print(self.market_data)
                self.status = TRADE_STATUS.FAILED
                self.deal_price = 0
                self.deal_amount = 0

            self.cal_fee()
            return self.callback_message

        except Exception as e:
            QA_util_log_info('MARKET ENGINE ERROR: {}'.format(e))
            self.status = TRADE_STATUS.NO_MARKET_DATA
            return self.callback_message


if __name__ == '__main__':
    pass
