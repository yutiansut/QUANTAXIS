# coding=utf-8
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


from statistics import mean

import pandas as pd

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_backtest_history,
                                       QA_fetch_backtest_info)
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_date_gap,
                                           QA_util_get_next_day)
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, ORDER_DIRECTION,
                                          ORDER_MODEL)


class QAAnalysis_trade():

    """
    Account/Portfolio是一个标准单元,所有成交记录分析 都会被加载到该单元中进行分析
    当我们只有一个成交记录的时候,我们会创建一个账户单元
    """

    def __init__(self, init_cash, *args, **kwargs):
        self.account = QA_Account(init_cash=init_cash)
        self.backtest_broker = QA_BacktestBroker()

    def import_trade(self, trade):
        """
        trade是一个可迭代的list/generator
        """
        for item in trade:
            self.make_deal(item.code, item.datetime, item.amount,
                           item.towards, item.price.item.order_model, item.amount_model)

    def make_deal(self, code, datetime, amount=100, towards=ORDER_DIRECTION.BUY, price=0, order_model=ORDER_MODEL.MARKET, amount_model=AMOUNT_MODEL.BY_AMOUNT):
        """
        这是一个一定会成交,并且立刻结转(及t+0)的交易入口
        """
        self.account.receive_deal(self.backtest_broker.receive_order(QA_Event(order=self.account.send_order(
            code=code, time=datetime, amount=amount, towards=towards, price=price, order_model=order_model, amount_model=amount_model
        ))))
        self.account.settle()



    # @property
    # def codes(self):
    #     return self.code

    # def get_stock_tradehistory(self, code):
    #     return self.history.query('code=="{}"'.format(code))

    # def get_stock_tradedetail(self, code):
    #     return self.detail.query('code=="{}"'.format(code))

    # def get_loss_trade(self, num=5):
    #     return self.detail[self.detail.pnl_precentage <= 0].sort_values(by=['pnl_precentage'], ascending=True).head(num)

    # def get_profit_trade(self, num=5):
    #     return self.detail[self.detail.pnl_precentage >= 0].sort_values(by=['pnl_precentage'], ascending=False).head(num)

    # def get_trade_marketdata(self, rx, gap=3):
    #     return QA_fetch_stock_day_adv(rx.code.values[0], QA_util_date_gap(rx.date.values[0], gap, methods='lt'), QA_util_date_gap(rx.sell_date.values[0][-1], gap, methods='gt'))

    # def get_trade_before_and_after_pnl(self, rx, N=3, M=10):
    #     data = self.get_trade_marketdata(rx, M)


def _mean(list_):
    if len(list_) > 0:
        return mean(list_)
    else:
        return 'No Data'
