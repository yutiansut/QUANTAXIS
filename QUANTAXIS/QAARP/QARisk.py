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

from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv, QA_fetch_index_day_adv
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_trade_gap


class QA_Risk():
    """QARISK 是一个风险插件

    """

    def __init__(self, account, benchmark_code='000300', benchmark_type=MARKET_TYPE.INDEX_CN):
        self.account = account
        self.benchmark_code = benchmark_code  # 默认沪深300
        self.benchmark_type = benchmark_type

        self.fetch = {MARKET_TYPE.STOCK_CN: QA_fetch_stock_day_adv,
                      MARKET_TYPE.INDEX_CN: QA_fetch_index_day_adv}
        self.market_data = QA_fetch_stock_day_adv(
            self.account.code, self.account.start_date, self.account.end_date)

        self.assets = ((self.market_data.to_qfq().pivot('close') * self.account.daily_hold).sum(
            axis=1) + self.account.daily_cash.set_index('date').cash).fillna(method='pad')

        self.time_gap = QA_util_get_trade_gap(
            self.account.start_date, self.account.end_date)

    def __repr__(self):
        return '< QA_RISK ANALYSIS ACCOUNT-{} >'.format(self.account.account_cookie)

    def __call__(self):
        return pd.DataFrame([self.message])

    @property
    def max_dropback(self):
        """最大回撤
        """
        return max([self.assets.iloc[idx::].max() - self.assets.iloc[idx::].min() for idx in range(len(self.assets))]) / float(self.assets.iloc[0])

    @property
    def profit(self):
        return self.calc_profit(self.assets)

    @property
    def profit_pct(self):
        """利润
        """
        return self.calc_profitpctchange(self.assets)

    @property
    def annualize_return(self):
        """年化收益

        Returns:
            [type] -- [description]
        """

        return self.calc_annualize_return(self.assets, self.time_gap)

    @property
    def volatility(self):
        """波动率

        Returns:
            [type] -- [description]
        """
        return self.profit_pct.std() * math.sqrt(250)

    @property
    def message(self):
        return {
            'account_cookie': self.account.account_cookie,
            'portfolio_cookie': self.account.portfolio_cookie,
            'user_cookie': self.account.user_cookie,
            'annualize_return': self.annualize_return,
            'profit': self.profit,
            'max_dropback': self.max_dropback,
            'time_gap': self.time_gap,
            'volatility': self.volatility,
            'benchmark_code': self.benchmark_code,
            'beta': self.beta,
            'alpha': self.alpha,
            'sharpe': self.sharpe
        }

    @property
    def benchmark_data(self):
        return self.fetch[self.benchmark_type](
            self.benchmark_code, self.account.start_date, self.account.end_date)

    @property
    def benchmark_assets(self):
        return (self.benchmark_data.open / float(self.benchmark_data.open.iloc[0]) * float(self.account.init_assets))

    @property
    def benchmark_annualize_return(self):
        """年化收益

        Returns:
            [type] -- [description]
        """

        return self.calc_annualize_return(self.benchmark_assets, self.time_gap)

    @property
    def benchmark_profitpct(self):
        return self.calc_profitpctchange(self.benchmark_assets)

    @property
    def beta(self):
        return self.calc_beta(self.profit_pct.dropna(), self.benchmark_profitpct.dropna())

    @property
    def alpha(self):
        return self.calc_alpha(self.annualize_return, self.benchmark_annualize_return, self.beta, 0.05)

    @property
    def sharpe(self):
        return self.calc_sharpe(self.annualize_return, self.volatility, 0.05)

    def set_benchmark(self, code, market_type):
        self.benchmark_code = code
        self.benchmark_type = market_type

    def calc_annualize_return(self, assets, days):
        return math.pow(float(assets.iloc[-1]) / float(assets.iloc[0]), 250.0 / float(days)) - 1.0

    # def calc_profit(self, assets):
    #     return (assets.iloc[-1] / assets.iloc[1]) - 1

    def calc_profitpctchange(self, assets):
        return self.assets[::-1].pct_change()

    def calc_beta(self, assest_profit, benchmark_profit):

        calc_cov = np.cov(assest_profit, benchmark_profit)
        beta = calc_cov[0, 1] / calc_cov[1, 1]
        return beta

    def calc_alpha(self, annualized_returns, benchmark_annualized_returns, beta, r=0.05):

        alpha = (annualized_returns - r) - (beta) * \
            (benchmark_annualized_returns - r)
        return alpha

    def calc_profit(self, assets):
        return (float(assets.iloc[-1]) / float(assets.iloc[0])) - 1

    def calc_sharpe(self, annualized_returns, volatility_year, r=0.05):
        '计算夏普比率'
        return (annualized_returns - r) / volatility_year


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
