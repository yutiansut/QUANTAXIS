# coding:utf-8
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
# The above copyright notice and this permission notice shall be included in
# all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""收益性的包括年化收益率、净利润、总盈利、总亏损、有效年化收益率、资金使用率。

风险性主要包括胜率、平均盈亏比、最大回撤比例、最大连续亏损次数、最大连续盈利次数、持仓时间占比、贝塔。

综合性指标主要包括风险收益比，夏普比例，波动率，VAR，偏度，峰度等"""

import datetime
import math
import os
import platform
from collections import deque
from functools import lru_cache
from queue import LifoQueue

import matplotlib
import numpy as np
import pandas as pd
from pymongo import ASCENDING, DESCENDING

from QUANTAXIS.QAARP.market_preset import MARKET_PRESET
from QUANTAXIS.QAFetch.QAQuery_Advance import (
    QA_fetch_future_day_adv,
    QA_fetch_index_day_adv,
    QA_fetch_stock_day_adv,
    QA_fetch_cryptocurrency_day_adv
)
from QUANTAXIS.QASU.save_account import save_riskanalysis
from QUANTAXIS.QAUtil.QADate_trade import (
    QA_util_get_trade_gap,
    QA_util_get_trade_range
)
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE
from QUANTAXIS.QAUtil.QASetting import DATABASE

# FIXED: no display found
"""
在无GUI的电脑上,会遇到找不到_tkinter的情况 兼容处理
@尧 2018/05/28
@喜欢你 @尧 2018/05/29


QARISK的更新策略:

1. 如果遇到请求: 
    1. 去数据库找到这个account的risk信息
    2. 检查交易是否出现更新

    ==>  更新>> 重新评估
    ==>  未更新>> 直接加载
    

"""
if platform.system() not in ['Windows',
                             'Darwin'] and os.environ.get('DISPLAY',
                                                          '') == '':
    print('you are using non-interactive mdoel quantaxis')
    # print('no display found.  Using non-interactive Agg backend')
    # print("if you use ssh, you can use ssh with -X parmas to avoid this
    # issue")
    # try:
    #     pass
    # except expression as identifier:
    #     pass
    # matplotlib.use('Agg')
    """
    matplotlib可用模式:
    ['GTK', 'GTKAgg', 'GTKCairo', 'MacOSX', 'Qt4Agg', 'Qt5Agg', 'TkAgg', 'WX',
    'WXAgg', 'GTK3Cairo', 'GTK3Agg', 'WebAgg', 'nbAgg', 'agg', 'cairo',
    'gdk', 'pdf', 'pgf', 'ps', 'svg', 'template']
    """
try:
    import tkinter
except ImportError:
    '''
    ModuleNotFoundError: No module named 'tkinter'
    maybe you should install tk, tcl library
    '''
    print("ModuleNotFoundError: No module named 'tkinter'")
    print(
        "centos 6: sudo yum install tk-devel tcl-devel sqlite-devel gdbm-devel xz-devel readline-devel"
    )
    print(
        "cnetos 7: sudo yum install tk-devel tcl-devel sqlite-devel gdbm-devel xz-devel readline-devel python3-tk"
    )
    print("ubuntu: sudo apt install python3-tk")
finally:
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    import seaborn as sns


class QA_Risk():
    """QARISK 是一个风险插件

    需要加载一个account/portfolio类进来:
    需要有
    code,start_date,end_date,daily_cash,daily_hold

    TODO:
    资金利用率 反应资金的利用程度
    股票周转率 反应股票的持仓天数
    预期PNL/统计学PNL
    """

    def __init__(
        self,
        account,
        benchmark_code='000300',
        benchmark_type=MARKET_TYPE.INDEX_CN,
        if_fq=True,
        market_data=None,
        auto_reload=False
    ):
        """
        account: QA_Account类/QA_PortfolioView类
        benchmark_code: [str]对照参数代码
        benchmark_type: [QA.PARAM]对照参数的市场
        if_fq: [Bool]原account是否使用复权数据
        if_fq选项是@尧提出的,关于回测的时候成交价格问题(如果按不复权撮合 应该按不复权价格计算assets)
        """
        self.account = account
        self.benchmark_code = benchmark_code # 默认沪深300
        self.benchmark_type = benchmark_type
        self.client = DATABASE.risk

        self.client.create_index(
            [
                ("account_cookie",
                 ASCENDING),
                ("user_cookie",
                 ASCENDING),
                ("portfolio_cookie",
                 ASCENDING)
            ],
            unique=True
        )
        if auto_reload:
            pass
        else:
            self.fetch = {
                MARKET_TYPE.STOCK_CN: QA_fetch_stock_day_adv,
                MARKET_TYPE.INDEX_CN: QA_fetch_index_day_adv,
                MARKET_TYPE.CRYPTOCURRENCY: QA_fetch_cryptocurrency_day_adv
            }
            if market_data == None:
                if self.account.market_type == MARKET_TYPE.STOCK_CN:
                    self.market_data = QA_fetch_stock_day_adv(
                        self.account.code,
                        self.account.start_date,
                        self.account.end_date
                    )
                elif self.account.market_type == MARKET_TYPE.FUTURE_CN:
                    self.market_data = QA_fetch_future_day_adv(
                        [item.upper() for item in self.account.code],
                        self.account.start_date,
                        self.account.end_date
                    )
                elif self.account.market_type == MARKET_TYPE.CRYPTOCURRENCY:
                    self.market_data = QA_fetch_cryptocurrency_day_adv(
                        [item for item in self.account.code],
                        self.account.start_date,
                        self.account.end_date
                    )
            else:
                self.market_data = market_data.select_time(
                    self.account.start_date,
                    self.account.end_date
                )
            self.if_fq = if_fq
            if (self.account.market_type == MARKET_TYPE.FUTURE_CN) or (
                    self.account.market_type == MARKET_TYPE.CRYPTOCURRENCY):
                self.if_fq = False # 如果是期货， 默认设为FALSE

            if self.market_value is not None:
                if self.account.market_type == MARKET_TYPE.FUTURE_CN and self.account.allow_margin == True:
                    print('margin!')
                    self._assets = (
                        self.account.daily_frozen
                        +                                                        # self.market_value.sum(axis=1) +
                        self.account.daily_cash.set_index('date').cash
                    ).dropna()
                else:
                    self._assets = (
                        self.market_value.sum(axis=1) +
                        self.account.daily_cash.set_index('date').cash
                    ).fillna(method='pad')
            else:
                self._assets = self.account.daily_cash.set_index('date'
                                                                ).cash.fillna(
                                                                    method='pad'
                                                                )

            self.time_gap = QA_util_get_trade_gap(
                self.account.start_date,
                self.account.end_date
            )
            self.init_cash = self.account.init_cash
            self.init_assets = self.account.init_assets

    def __repr__(self):
        return '< QA_RISK ANALYSIS ACCOUNT/PORTFOLIO >'

    def __call__(self):
        return pd.DataFrame([self.message])

    @property
    def total_timeindex(self):
        return self.account.trade_range

    @property
    def market_value(self):
        """每日每个股票持仓市值表

        Returns:
            pd.DataFrame -- 市值表
        """
        if self.account.daily_hold is not None:
            if self.if_fq:

                return (
                    self.market_data.to_qfq().pivot('close').fillna(
                        method='ffill'
                    ) * self.account.daily_hold.apply(abs)
                ).fillna(method='ffill')
            else:
                return (
                    self.market_data.pivot('close').fillna(method='ffill') *
                    self.account.daily_hold.apply(abs)
                ).fillna(method='ffill')
        else:
            return None

    @property
    def daily_market_value(self):
        """每日持仓总市值表

        Returns:
            pd.DataFrame -- 市值表
        """
        if self.market_value is not None:
            return self.market_value.sum(axis=1)
        else:
            return None

    @property
    def assets(self):
        x1 = self._assets.reset_index()
        return x1.assign(
            date=pd.to_datetime(x1.date, utc=False)
        ).set_index('date')[0]

    @property
    def max_dropback(self):
        """最大回撤
        """
        return round(
            float(
                max(
                    [
                        (self.assets.iloc[idx] - self.assets.iloc[idx::].min())
                        / self.assets.iloc[idx]
                        for idx in range(len(self.assets))
                    ]
                )
            ),
            2
        )

    @property
    def total_commission(self):
        """总手续费
        """
        return float(
            -abs(round(self.account.history_table.commission.sum(),
                       2))
        )

    @property
    def total_tax(self):
        """总印花税

        """

        return float(-abs(round(self.account.history_table.tax.sum(), 2)))

    @property
    def profit_construct(self):
        """利润构成

        Returns:
            dict -- 利润构成表
        """

        return {
            'total_buyandsell':
                round(
                    self.profit_money - self.total_commission - self.total_tax,
                    2
                ),
            'total_tax':
                self.total_tax,
            'total_commission':
                self.total_commission,
            'total_profit':
                self.profit_money
        }

    @property
    def profit_money(self):
        """盈利额

        Returns:
            [type] -- [description]
        """

        return float(round(self.assets.iloc[-1] - self.assets.iloc[0], 2))

    @property
    def profit(self):
        """盈利率(百分比)

        Returns:
            [type] -- [description]
        """

        return round(float(self.calc_profit(self.assets)), 2)

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

        return round(
            float(self.calc_annualize_return(self.assets,
                                             self.time_gap)),
            2
        )

    @property
    def volatility(self):
        """波动率

        Returns:
            [type] -- [description]
        """
        return round(float(self.profit_pct.std() * math.sqrt(250)), 2)

    @property
    def ir(self):
        return round(self.calc_IR(), 2)

    @property
    @lru_cache()
    def message(self):
        return {
            'account_cookie': self.account.account_cookie,
            'portfolio_cookie': self.account.portfolio_cookie,
            'user_cookie': self.account.user_cookie,
            'annualize_return': round(self.annualize_return,
                                      2),
            'profit': round(self.profit,
                            2),
            'max_dropback': self.max_dropback,
            'time_gap': self.time_gap,
            'volatility': self.volatility,
            'benchmark_code': self.benchmark_code,
            'bm_annualizereturn': self.benchmark_annualize_return,
            'bm_profit': self.benchmark_profit,
            'beta': self.beta,
            'alpha': self.alpha,
            'sharpe': self.sharpe,
            'sortino': self.sortino,
            'init_cash': "%0.2f" % (float(self.assets[0])),
            'last_assets': "%0.2f" % (float(self.assets.iloc[-1])),
            'total_tax': self.total_tax,
            'total_commission': self.total_commission,
            'profit_money': self.profit_money,
            'assets': list(self.assets),
            'benchmark_assets': list(self.benchmark_assets),
            'timeindex': self.account.trade_day,
            'totaltimeindex': self.total_timeindex,
            'ir': self.ir,
            'month_profit': self.month_assets_profit.to_dict()
                                                                      # 'init_assets': round(float(self.init_assets), 2),
                                                                      # 'last_assets': round(float(self.assets.iloc[-1]), 2)
        }

    @property
    def benchmark_data(self):
        """
        基准组合的行情数据(一般是组合,可以调整)
        """
        return self.fetch[self.benchmark_type](
            self.benchmark_code,
            self.account.start_date,
            self.account.end_date
        )

    @property
    def benchmark_assets(self):
        """
        基准组合的账户资产队列
        """
        return (
            self.benchmark_data.close /
            float(self.benchmark_data.close.iloc[0]) * float(self.assets[0])
        )

    @property
    def benchmark_profit(self):
        """
        基准组合的收益
        """
        return round(float(self.calc_profit(self.benchmark_assets)), 2)

    @property
    def benchmark_annualize_return(self):
        """基准组合的年化收益

        Returns:
            [type] -- [description]
        """

        return round(
            float(
                self.calc_annualize_return(
                    self.benchmark_assets,
                    self.time_gap
                )
            ),
            2
        )

    @property
    def benchmark_profitpct(self):
        """
        benchmark 基准组合的收益百分比计算
        """
        return self.calc_profitpctchange(self.benchmark_assets)

    @property
    def beta(self):
        """
        beta比率 组合的系统性风险
        """
        try:
            # res = round(float(self.calc_beta(self.profit_pct.dropna(),
            #             self.benchmark_profitpct.dropna())),
            #     2)

            res = round(
                float(
                    self.calc_beta(
                        self.assets.pct_change().dropna().values,
                        self.benchmark_assets.pct_change().dropna().values
                    )
                ),
                2
            )
        except:
            print('贝塔计算错误。。')
            res = 0

        return res

    @property
    def alpha(self):
        """
        alpha比率 与市场基准收益无关的超额收益率
        """
        return round(
            float(
                self.calc_alpha(
                    self.annualize_return,
                    self.benchmark_annualize_return,
                    self.beta,
                    0.05
                )
            ),
            2
        )

    @property
    def sharpe(self):
        """
        夏普比率

        """
        return round(
            float(
                self.calc_sharpe(self.annualize_return,
                                 self.volatility,
                                 0.05)
            ),
            2
        )

    @property
    def sortino(self):
        """
        索提诺比率 投资组合收益和下行风险比值

        """
        return round(
            float(
                self.calc_sortino(self.annualize_return,
                                  self.volatility,
                                  0.05)
            ),
            2
        )

    @property
    def calmar(self):
        """
        卡玛比率
        """
        pass

    def set_benchmark(self, code, market_type):
        self.benchmark_code = code
        self.benchmark_type = market_type

    def calc_annualize_return(self, assets, days):
        return round(
            (float(assets.iloc[-1]) / float(assets.iloc[0]) - 1) /
            (float(days) / 250),
            2
        )

    def calc_profitpctchange(self, assets):
        # return assets[::-1].pct_change()[::-1]
        return assets.pct_change().fillna(1)

    def calc_beta(self, assest_profit, benchmark_profit):

        calc_cov = np.cov(assest_profit, benchmark_profit)
        beta = calc_cov[0, 1] / calc_cov[1, 1]
        return beta

    def calc_alpha(
        self,
        annualized_returns,
        benchmark_annualized_returns,
        beta,
        r=0.05
    ):

        alpha = (annualized_returns) - (beta) * \
            (benchmark_annualized_returns)
        return alpha

    def calc_IR(self):
        """计算信息比率

        Returns:
            [type] -- [description]
        """
        if self.volatility == 0:
            return 0
        else:
            return self.annualize_return / self.volatility

    def calc_profit(self, assets):
        """
        计算账户收益
        期末资产/期初资产 -1
        """
        return (float(assets.iloc[-1]) / float(assets.iloc[0])) - 1

    def calc_sharpe(self, annualized_returns, volatility_year, r=0.05):
        """
        计算夏普比率
        r是无风险收益
        """
        # 会出现0
        if volatility_year == 0:
            return 0
        return (annualized_returns - r) / volatility_year

    def calc_sortino(self, annualized_returns, volatility_year, rfr=0.00):
        """
        计算索提诺比率
        在网上找到代码，感觉计算的结果不太对，数值偏小 -阿财 2020/03/28
        """
        # 会出现0
        if volatility_year == 0:
            return 0

        # Define risk free rate and target return of 0
        target = 0

        # Calcualte the daily returns from price data
        df = pd.DataFrame(
            columns=['Returns',
                     'downside_returns'],
            index=self.assets.index
        )
        df['Returns'] = (self.assets.values / self.assets.shift(1).values) - 1
        df['downside_returns'] = 0

        # Select the negative returns only
        df.loc[df['Returns'] < target, 'downside_returns'] = df['Returns']**2
        expected_return = df['Returns'].mean()

        # Calculate expected return and std dev of downside returns
        down_stdev = np.sqrt(df['downside_returns'].mean())

        # Calculate the sortino ratio
        sortino_ratio = (expected_return - rfr) / down_stdev

        # 这里不知道计算年化率如何
        return sortino_ratio

    @property
    def max_holdmarketvalue(self):
        """最大持仓市值

        Returns:
            [type] -- [description]
        """
        if self.daily_market_value is not None:
            return self.daily_market_value.max()
        else:
            return 0

    @property
    def min_holdmarketvalue(self):
        """最小持仓市值

        Returns:
            [type] -- [description]
        """
        if self.daily_market_value is not None:
            return self.daily_market_value.min()
        else:
            return 0

    @property
    def average_holdmarketvalue(self):
        """平均持仓市值

        Returns:
            [type] -- [description]
        """
        if self.daily_market_value is not None:
            return self.daily_market_value.mean()
        else:
            return 0

    @property
    def max_cashhold(self):
        """最大闲置资金
        """

        return self.account.daily_cash.cash.max()

    @property
    def min_cashhold(self):
        """最小闲置资金
        """

        return self.account.daily_cash.cash.min()

    @property
    def average_cashhold(self):
        """平均闲置资金

        Returns:
            [type] -- [description]
        """

        return self.account.daily_cash.cash.mean()

    def save(self):
        """save to mongodb

        """
        save_riskanalysis(self.message)

    def plot_assets_curve(self, length=14, height=12):
        """
        资金曲线叠加图
        @Roy T.Burns 2018/05/29 修改百分比显示错误
        """
        plt.style.use('ggplot')
        plt.figure(figsize=(length, height))
        plt.subplot(211)
        plt.title('BASIC INFO', fontsize=12)
        plt.axis([0, length, 0, 0.6])
        plt.axis('off')
        i = 0
        for item in ['account_cookie', 'portfolio_cookie', 'user_cookie']:
            plt.text(
                i,
                0.5,
                '{} : {}'.format(item,
                                 self.message[item]),
                fontsize=10,
                rotation=0,
                wrap=True
            )
            i += (length / 2.8)
        i = 0
        for item in ['benchmark_code', 'time_gap', 'max_dropback']:
            plt.text(
                i,
                0.4,
                '{} : {}'.format(item,
                                 self.message[item]),
                fontsize=10,
                ha='left',
                rotation=0,
                wrap=True
            )
            i += (length / 2.8)
        i = 0
        for item in ['annualize_return', 'bm_annualizereturn', 'profit']:
            plt.text(
                i,
                0.3,
                '{} : {} %'.format(item,
                                   self.message.get(item,
                                                    0) * 100),
                fontsize=10,
                ha='left',
                rotation=0,
                wrap=True
            )
            i += length / 2.8
        i = 0
        for item in ['init_cash', 'last_assets', 'volatility']:
            plt.text(
                i,
                0.2,
                '{} : {} '.format(item,
                                  self.message[item]),
                fontsize=10,
                ha='left',
                rotation=0,
                wrap=True
            )
            i += length / 2.8
        i = 0
        for item in ['alpha', 'beta', 'sharpe']:
            plt.text(
                i,
                0.1,
                '{} : {}'.format(item,
                                 self.message[item]),
                ha='left',
                fontsize=10,
                rotation=0,
                wrap=True
            )
            i += length / 2.8
        plt.subplot(212)
        self.assets.plot()
        if (self.benchmark_type == MARKET_TYPE.CRYPTOCURRENCY):
            self.benchmark_assets.xs(self.benchmark_code, level=1).plot()
        else:
            self.benchmark_assets.xs(self.benchmark_code, level=1).plot()

        asset_p = mpatches.Patch(
            color='red',
            label='{}'.format(self.account.account_cookie)
        )
        asset_b = mpatches.Patch(
            label='benchmark {}'.format(self.benchmark_code)
        )
        plt.legend(handles=[asset_p, asset_b], loc=0)
        plt.title('ASSET AND BENCKMARK')

        return plt

    @property
    def month_assets(self):
        return self.assets.resample('M').last()

    @property
    def month_assets_profit(self):

        res = pd.concat([pd.Series(self.assets.iloc[0]),
                         self.month_assets]).diff().dropna()
        res.index = res.index.map(str)
        return res

    @property
    def daily_assets_profit(self):
        return self.assets.diff()

    def plot_dailyhold(self, start=None, end=None):
        """
        使用热力图画出每日持仓
        """
        start = self.account.start_date if start is None else start
        end = self.account.end_date if end is None else end
        _, ax = plt.subplots(figsize=(20, 8))
        sns.heatmap(
            self.account.daily_hold.reset_index().set_index('date'
                                                           ).loc[start:end],
            cmap="YlGnBu",
            linewidths=0.05,
            ax=ax
        )
        ax.set_title(
            'HOLD TABLE --ACCOUNT: {}'.format(self.account.account_cookie)
        )
        ax.set_xlabel('Code')
        ax.set_ylabel('DATETIME')

        return plt

    def plot_signal(self, start=None, end=None):
        """
        使用热力图画出买卖信号
        """
        start = self.account.start_date if start is None else start
        end = self.account.end_date if end is None else end
        _, ax = plt.subplots(figsize=(20, 18))
        sns.heatmap(
            self.account.trade.reset_index().drop(
                'account_cookie',
                axis=1
            ).set_index('datetime').loc[start:end],
            cmap="YlGnBu",
            linewidths=0.05,
            ax=ax
        )
        ax.set_title(
            'SIGNAL TABLE --ACCOUNT: {}'.format(self.account.account_cookie)
        )
        ax.set_xlabel('Code')
        ax.set_ylabel('DATETIME')
        return plt

    def generate_plots(self):
        """
        生成图像
        """
        self.plot_assets_curve()
        self.plot_dailyhold()
        self.plot_signal()


class QA_Performance():
    """
    QA_Performance是一个绩效分析插件

    需要加载一个account/portfolio类进来:
    需要有
    code,start_date,end_date,daily_cash,daily_hold


    QAPERFORMANCE 的评估字段

    1. 对于多头开仓/ 空头开仓的分析
    2. 总盈利(对于每个单笔而言)
    3. 总亏损(对于每个单笔而言)
    4. 总盈利/总亏损
    5. 交易手数
    6. 盈利比例
    7. 盈利手数
    8. 亏损手数
    9. 持平手数
    10. 平均利润
    11. 平均盈利
    12. 平均亏损
    13. 平均盈利/平均亏损
    14. 最大盈利(单笔)
    15. 最大亏损(单笔)
    16. 最大盈利/总盈利
    17. 最大亏损/总亏损
    18. 净利润/最大亏损
    19. 最大连续盈利手数
    20. 最大连续亏损手数
    21. 平均持仓周期
    22. 平均盈利周期
    23. 平均亏损周期
    24. 平均持平周期
    25. 最大使用资金
    26. 最大持仓手数
    27. 交易成本合计
    28. 收益率
    29. 年化收益率
    30. 有效收益率
    31. 月度平均盈利
    32. 收益曲线斜率
    33. 收益曲线截距
    34. 收益曲线R2值
    35. 夏普比例
    36. 总交易时间
    37. 总持仓时间
    38. 持仓时间比例
    39. 最大空仓时间
    40. 持仓周期
    41. 资产最大升水
    42. 发生时间
    43. 最大升水/前期低点
    44. 单日最大资产回撤比率
    45. 最大资产回撤值
    46. 最大资产回撤发生时间
    47. 回撤值/前期高点
    48. 净利润/回撤值


    """

    def __init__(self, target):

        self.target = target
        self._style_title = [
            'beta',
            'momentum',
            'size',
            'earning_yield',
            'volatility',
            'growth',
            'value',
            'leverage',
            'liquidity',
            'reversal'
        ]
        self.market_preset = MARKET_PRESET()
        self.pnl = self.pnl_fifo

    def __repr__(self):
        return '< QA_PERFORMANCE ANYLYSIS PLUGIN >'

    def set_pnl(self, model='fifo'):
        if model == 'fifo':
            self.pnl = self.pnl_fifo
        elif model == 'lifo':
            self.pnl = self.pnl_lifo

    def base_message(self, pnl):
        return {'total_profit': round(self.total_profit(pnl), 2),  # 总盈利(对于每个单笔而言)
                'total_loss': round(self.total_loss(pnl), 2),  # 总亏损(对于每个单笔而言)
                'total_pnl': round(self.total_pnl(pnl), 2),  # 总盈利/总亏损
                'trading_amounts': round(self.trading_amounts(pnl), 2),  # 交易手数
                'profit_amounts': round(self.profit_amounts(pnl), 2),  # 盈利手数
                'loss_amounts': round(self.loss_amounts(pnl), 2),  # 亏损手数
                'even_amounts': round(self.even_amounts(pnl), 2),  # 持平手数
                'profit_precentage': round(self.profit_precentage(pnl), 2),
                'loss_precentage': round(self.loss_precentage(pnl), 2),
                'even_precentage': round(self.even_precentage(pnl), 2),
                'average_profit': round(self.average_profit(pnl), 2),
                'average_loss': round(self.average_loss(pnl), 2),
                'average_pnl': round(self.average_pnl(pnl), 2),
                'max_profit': round(self.max_profit(pnl), 2),
                'max_loss': round(self.max_loss(pnl), 2),
                'max_pnl': round(self.max_pnl(pnl), 2),
                'netprofio_maxloss_ratio': round(self.netprofio_maxloss_ratio(pnl), 2),
                'continue_profit_amount': round(self.continue_profit_amount(pnl), 2),
                'continue_loss_amount': round(self.continue_loss_amount(pnl), 2),
                'average_holdgap': self.average_holdgap(pnl),
                'average_profitholdgap': self.average_profitholdgap(pnl),
                'average_losssholdgap': self.average_losssholdgap(pnl)}

    @property
    def message(self):
        """[summary]
            2. 
            3. 
            4. 
            5. 
            6. 
            7. 盈利手数
            8. 亏损手数
            9. 持平手数
            10. 平均利润
            11. 平均盈利
            12. 平均亏损
            13. 平均盈利/平均亏损
            14. 最大盈利(单笔)
            15. 最大亏损(单笔)
            16. 最大盈利/总盈利
            17. 最大亏损/总亏损
            18. 净利润/最大亏损
            19. 最大连续盈利手数
            20. 最大连续亏损手数
            21. 平均持仓周期
            22. 平均盈利周期
            23. 平均亏损周期
            24. 平均持平周期
            25. 最大使用资金
            26. 最大持仓手数
            27. 交易成本合计
            28. 收益率
            29. 年化收益率
            30. 有效收益率
            31. 月度平均盈利
            32. 收益曲线斜率
            33. 收益曲线截距
            34. 收益曲线R2值
            35. 夏普比例
            36. 总交易时间
            37. 总持仓时间
            38. 持仓时间比例
            39. 最大空仓时间
            40. 持仓周期
            41. 资产最大升水
            42. 发生时间
            43. 最大升水/前期低点
            44. 单日最大资产回撤比率
            45. 最大资产回撤值
            46. 最大资产回撤发生时间
            47. 回撤值/前期高点
            48. 净利润/回撤值
        Returns:
            [type] -- [description]
        """

        return {
            # 总盈利(对于每个单笔而言)
            'total_profit': round(self.total_profit(self.pnl), 2),
            'total_loss': round(self.total_loss(self.pnl), 2),  # 总亏损(对于每个单笔而言)
            'total_pnl': round(self.total_pnl(self.pnl), 2),  # 总盈利/总亏损
            # 交易手数
            'trading_amounts': round(self.trading_amounts(self.pnl), 2),
            'profit_amounts': round(self.profit_amounts(self.pnl), 2),  # 盈利手数
            'loss_amounts': round(self.loss_amounts(self.pnl), 2),  # 亏损手数
            'even_amounts': round(self.even_amounts(self.pnl), 2),  # 持平手数
            'profit_precentage': round(self.profit_precentage(self.pnl), 2),
            'loss_precentage': round(self.loss_precentage(self.pnl), 2),
            'even_precentage': round(self.even_precentage(self.pnl), 2),
            'average_profit': round(self.average_profit(self.pnl), 2),
            'average_loss': round(self.average_loss(self.pnl), 2),
            'average_pnl': round(self.average_pnl(self.pnl), 2),
            'max_profit': round(self.max_profit(self.pnl), 2),
            'max_loss': round(self.max_loss(self.pnl), 2),
            'max_pnl': round(self.max_pnl(self.pnl), 2),
            'netprofio_maxloss_ratio': round(self.netprofio_maxloss_ratio(self.pnl), 2),
            'continue_profit_amount': round(self.continue_profit_amount(self.pnl), 2),
            'continue_loss_amount': round(self.continue_loss_amount(self.pnl), 2),
            'average_holdgap': self.average_holdgap(self.pnl),
            'average_profitholdgap': self.average_profitholdgap(self.pnl),
            'average_losssholdgap': self.average_losssholdgap(self.pnl),
            'buyopen': self.base_message(self.pnl_buyopen),
            'sellopen': self.base_message(self.pnl_sellopen)
        }

    @property
    def prefer(self):
        pass

    @property
    def style(self):
        """风格分析
        """
        pass

    @property
    def pnl_lifo(self):
        """
        使用后进先出法配对成交记录
        """
        X = dict(
            zip(
                self.target.code,
                [
                    {
                        'buy': LifoQueue(),
                        'sell': LifoQueue()
                    } for i in range(len(self.target.code))
                ]
            )
        )
        pair_table = []
        for _, data in self.target.history_table_min.iterrows():

            if abs(data.amount) < 1:
                pass
            else:
                while True:
                    if data.direction in [1, 2, -2]:
                        if data.direction in [1, 2]:
                            X[data.code]['buy'].put(
                                (
                                    data.datetime,
                                    data.amount,
                                    data.price,
                                    data.direction
                                )
                            )
                        elif data.direction in [-2]:
                            X[data.code]['sell'].put(
                                (
                                    data.datetime,
                                    data.amount,
                                    data.price,
                                    data.direction
                                )
                            )
                        break
                    elif data.direction in [-1, 3, -3]:

                        rawoffset = 'buy' if data.direction in [
                            -1,
                            -3
                        ] else 'sell'

                        l = X[data.code][rawoffset].get()
                        if abs(l[1]) > abs(data.amount):
                            """
                            if raw> new_close:
                            """
                            temp = (l[0], l[1] + data.amount, l[2])
                            X[data.code][rawoffset].put_nowait(temp)
                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        abs(data.amount),
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                                break
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        abs(data.amount),
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                                break

                        elif abs(l[1]) < abs(data.amount):
                            data.amount = data.amount + l[1]

                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        l[1],
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        l[1],
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                        else:
                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        abs(data.amount),
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                                break
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        abs(data.amount),
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                                break

        pair_title = [
            'code',
            'sell_date',
            'buy_date',
            'amount',
            'sell_price',
            'buy_price',
            'rawdirection'
        ]
        pnl = pd.DataFrame(pair_table, columns=pair_title)

        pnl = pnl.assign(
            unit=pnl.code.apply(lambda x: self.market_preset.get_unit(x)),
            pnl_ratio=(pnl.sell_price / pnl.buy_price) - 1,
            sell_date=pd.to_datetime(
                pnl.sell_date
            , utc=False),
            buy_date=pd.to_datetime(
                pnl.buy_date
            , utc=False)
        )
        pnl = pnl.assign(
            pnl_money=(pnl.sell_price - pnl.buy_price) * pnl.amount * pnl.unit,
            hold_gap=abs(pnl.sell_date - pnl.buy_date),
            if_buyopen=pnl.rawdirection == 'buy'
        )
        pnl = pnl.assign(
            openprice=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
            pnl.buy_price +
            pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) * pnl.sell_price,
            opendate=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
            pnl.buy_date.map(str) +
            pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
            pnl.sell_date.map(str),
            closeprice=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
            pnl.buy_price +
            pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) * pnl.sell_price,
            closedate=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
            pnl.buy_date.map(str) +
            pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
            pnl.sell_date.map(str)
        )
        return pnl.set_index('code')

    @property
    def pnl_buyopen(self):
        return self.pnl[self.pnl.if_buyopen]

    @property
    def pnl_sellopen(self):
        return self.pnl[~self.pnl.if_buyopen]

    @property
    def pnl_fifo(self):
        X = dict(
            zip(
                self.target.code,
                [
                    {
                        'buy': deque(),
                        'sell': deque()
                    } for i in range(len(self.target.code))
                ]
            )
        )
        pair_table = []
        for _, data in self.target.history_table_min.iterrows():
            if abs(data.amount) < 1:
                pass
            else:
                while True:
                    if data.direction in [1, 2, -2]:
                        if data.direction in [1, 2]:
                            X[data.code]['buy'].append(
                                (
                                    data.datetime,
                                    data.amount,
                                    data.price,
                                    data.direction
                                )
                            )
                        elif data.direction in [-2]:
                            X[data.code]['sell'].append(
                                (
                                    data.datetime,
                                    data.amount,
                                    data.price,
                                    data.direction
                                )
                            )
                        break
                    elif data.direction in [-1, 3, -3]:

                        rawoffset = 'buy' if data.direction in [
                            -1,
                            -3
                        ] else 'sell'

                        l = X[data.code][rawoffset].popleft()
                        if abs(l[1]) > abs(data.amount):
                            """
                            if raw> new_close:
                            """
                            temp = (l[0], l[1] + data.amount, l[2])
                            X[data.code][rawoffset].appendleft(temp)
                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        abs(data.amount),
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                                break
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        abs(data.amount),
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                                break

                        elif abs(l[1]) < abs(data.amount):
                            data.amount = data.amount + l[1]

                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        l[1],
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        l[1],
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                        else:
                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        abs(data.amount),
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                                break
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        abs(data.amount),
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                                break

        pair_title = [
            'code',
            'sell_date',
            'buy_date',
            'amount',
            'sell_price',
            'buy_price',
            'rawdirection'
        ]
        pnl = pd.DataFrame(pair_table, columns=pair_title)

        pnl = pnl.assign(
            unit=pnl.code.apply(lambda x: self.market_preset.get_unit(x)),
            pnl_ratio=(pnl.sell_price / pnl.buy_price) - 1,
            sell_date=pd.to_datetime(
                pnl.sell_date
            , utc=False),
            buy_date=pd.to_datetime(
                pnl.buy_date
            , utc=False)
        )
        pnl = pnl.assign(
            pnl_money=(pnl.sell_price - pnl.buy_price) * pnl.amount * pnl.unit,
            hold_gap=abs(pnl.sell_date - pnl.buy_date),
            if_buyopen=pnl.rawdirection == 'buy'
        )
        pnl = pnl.assign(
            openprice=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
            pnl.buy_price +
            pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) * pnl.sell_price,
            opendate=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
            pnl.buy_date.map(str) +
            pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
            pnl.sell_date.map(str),
            closeprice=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
            pnl.buy_price +
            pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) * pnl.sell_price,
            closedate=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
            pnl.buy_date.map(str) +
            pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
            pnl.sell_date.map(str)
        )
        return pnl.set_index('code')

    def plot_pnlratio(self):
        """
        画出pnl比率散点图
        """

        plt.scatter(x=self.pnl.sell_date.apply(str), y=self.pnl.pnl_ratio)
        plt.gcf().autofmt_xdate()
        return plt

    def plot_pnlmoney(self):
        """
        画出pnl盈亏额散点图
        """
        plt.scatter(x=self.pnl.sell_date.apply(str), y=self.pnl.pnl_money)
        plt.gcf().autofmt_xdate()
        return plt

    def abnormal_active(self):
        """
        账户的成交发生异常成交记录的分析
        """
        pass

    def brinson(self):
        """Brinson Model analysis
        """
        pass

    def hold(self):
        """持仓分析
        """
        pass

    def win_rate(self):
        """胜率

        胜率
        盈利次数/总次数
        """
        data = self.pnl
        try:
            return round(len(data.query('pnl_money>0')) / len(data), 2)
        except ZeroDivisionError:
            return 0

    @property
    def accumulate_return(self):
        """
        returns a pd-Dataframe format accumulate return for different periods
        """
        pass

    def save(self):
        """save the performance analysis result to database
        """
        pass

    def profit_pnl(self, pnl):
        return pnl.query('pnl_money>0')

    def loss_pnl(self, pnl):
        return pnl.query('pnl_money<0')

    def even_pnl(self, pnl):
        return pnl.query('pnl_money==0')

    def total_profit(self, pnl):
        if len(self.profit_pnl(pnl)) > 0:
            return self.profit_pnl(pnl).pnl_money.sum()
        else:
            return 0

    def total_loss(self, pnl):
        if len(self.loss_pnl(pnl)) > 0:
            return self.loss_pnl(pnl).pnl_money.sum()
        else:
            return 0

    def total_pnl(self, pnl):
        try:
            return abs(self.total_profit(pnl) / self.total_loss(pnl))
        except ZeroDivisionError:
            return 0

    def trading_amounts(self, pnl):
        return len(pnl)

    def profit_amounts(self, pnl):
        return len(self.profit_pnl(pnl))

    def loss_amounts(self, pnl):
        return len(self.loss_pnl(pnl))

    def even_amounts(self, pnl):
        return len(self.even_pnl(pnl))

    def profit_precentage(self, pnl):
        try:
            return self.profit_amounts(pnl) / self.trading_amounts(pnl)
        except ZeroDivisionError:
            return 0

    def loss_precentage(self, pnl):
        try:
            return self.loss_amounts(pnl) / self.trading_amounts(pnl)
        except ZeroDivisionError:
            return 0

    def even_precentage(self, pnl):
        try:
            return self.even_amounts(pnl) / self.trading_amounts(pnl)
        except ZeroDivisionError:
            return 0

    def average_loss(self, pnl):
        if len(self.loss_pnl(pnl)) > 0:
            return self.loss_pnl(pnl).pnl_money.mean()
        else:
            return 0

    def average_profit(self, pnl):
        if len(self.profit_pnl(pnl)) > 0:
            return self.profit_pnl(pnl).pnl_money.mean()
        else:
            return 0

    def average_pnl(self, pnl):
        if len(self.loss_pnl(pnl)) > 0 and len(self.profit_pnl(pnl)) > 0:
            try:
                return abs(self.average_profit(pnl) / self.average_loss(pnl))
            except ZeroDivisionError:
                return 0
        else:
            return 0

    def max_profit(self, pnl):
        if len(self.profit_pnl(pnl)) > 0:
            return self.profit_pnl(pnl).pnl_money.max()
        else:
            return 0

    def max_loss(self, pnl):
        if len(self.loss_pnl(pnl)) > 0:
            return self.loss_pnl(pnl).pnl_money.min()
        else:
            return 0

    def max_pnl(self, pnl):
        try:
            return abs(self.max_profit(pnl) / self.max_loss(pnl))
        except ZeroDivisionError:
            return 0

    def netprofio_maxloss_ratio(self, pnl):
        if len(self.loss_pnl(pnl)) > 0:
            try:
                return abs(pnl.pnl_money.sum() / self.max_loss(pnl))
            except ZeroDivisionError:
                return 0
        else:
            return 0

    def continue_profit_amount(self, pnl):
        """最大连续利润单数

        Arguments:
            pnl {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        w = []
        w1 = 0
        for _, item in pnl.pnl_money.iteritems():
            if item > 0:
                w1 += 1
            elif item < 0:
                w.append(w1)
                w1 = 0
        if len(w) == 0:
            return 0
        else:
            return max(w)

    def continue_loss_amount(self, pnl):
        """最大连续亏损单数

        Arguments:
            pnl {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        l = []
        l1 = 0
        for _, item in pnl.pnl_money.iteritems():
            if item > 0:
                l.append(l1)
                l1 = 0
            elif item < 0:
                l1 += 1
        if len(l) == 0:
            return 0
        else:
            return max(l)

    def average_holdgap(self, pnl):
        if len(pnl.hold_gap) > 0:
            return str(pnl.hold_gap.mean())
        else:
            return 'no trade'

    def average_profitholdgap(self, pnl):
        if len(self.profit_pnl(pnl).hold_gap) > 0:
            return str(self.profit_pnl(pnl).hold_gap.mean())
        else:
            return 'no trade'

    def average_losssholdgap(self, pnl):
        if len(self.loss_pnl(pnl).hold_gap) > 0:
            return str(self.loss_pnl(pnl).hold_gap.mean())
        else:
            return 'no trade'

    def average_evenholdgap(self, pnl):
        if len(self.even_pnl(pnl).hold_gap) > 0:
            return self.even_pnl(pnl).hold_gap.mean()
        else:
            return 'no trade'

    @property
    def max_cashused(self):
        return self.target.init_cash - min(self.target.cash)

    @property
    def total_taxfee(self):
        return self.target.history_table_min.commission.sum(
        ) + self.target.history_table_min.tax.sum()
