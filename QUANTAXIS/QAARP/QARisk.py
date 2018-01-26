# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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


"""收益性的包括年化收益率、净利润、总盈利、总亏损、有效年化收益率、资金使用率。

风险性主要包括胜率、平均盈亏比、最大回撤比例、最大连续亏损次数、最大连续盈利次数、持仓时间占比、贝塔。

综合性指标主要包括风险收益比，夏普比例，波动率，VAR，偏度，峰度等"""

import math
from functools import lru_cache

import numpy as np
import pandas as pd

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv, QA_fetch_index_day_adv
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE


class QA_Risk():
    def __init__(self, account):
        self.account = account
        self.benchmark = None

        self.fetch = {MARKET_TYPE.STOCK_CN: QA_fetch_stock_day_adv,
                      MARKET_TYPE.INDEX_CN: QA_fetch_index_day_adv}

    
    @property
    @lru_cache()
    def market_data(self):
        return QA_fetch_stock_day_adv(self.account.code, self.account.start_date, self.account.end_date)

    
    @property
    @lru_cache()
    def assets(self):
        '惰性计算 日市值'
        return ((self.market_data.to_qfq().pivot('close') * self.account.daily_hold).sum(axis=1) + self.account.daily_cash.set_index('date').cash).fillna(method='pad')

    @property
    def max_dropback(self):
        """最大回撤
        """

        pass

    @property
    def profit(self):
        """利润
        """

        pass

    @property
    def annualize_return(self):
        pass

    @property
    def volatility(self):
        pass

    def set_benchmark(self, code, market_type):
        self.benchmark = self.fetch[market_type](
            code, self.account.start_date, self.account.end_date)




class QA_Performace(QA_Risk):
    def __init__(self, account):
        super().__init__(account)

    @property
    def benchmark_assets(self):
        pass

    def set_benchmark(self):
        pass

    @property
    def alpha(self):
        pass

    @property
    def beta(self):
        pass

    @property
    def sharpe(self):
        pass


def annualize_return(assets, days):
    return math.pow(float(assets[-1]) / float(assets[0]), 250.0 / float(days)) - 1.0


def profit(assets):
    return (assets[-1] / assets[1]) - 1
