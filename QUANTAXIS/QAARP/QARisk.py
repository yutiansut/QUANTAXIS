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
import os
import platform

from collections import deque
from functools import lru_cache
from queue import LifoQueue

import matplotlib
import numpy as np
import pandas as pd

from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_index_day_adv,
                                               QA_fetch_stock_day_adv)
from QUANTAXIS.QASU.save_account import save_riskanalysis
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_trade_gap, QA_util_get_trade_range
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE

# FIXED: no display found
"""
在无GUI的电脑上,会遇到找不到_tkinter的情况 兼容处理
@尧 2018/05/28
@喜欢你 @尧 2018/05/29
"""
if platform.system() != 'Windows' and os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    print("if you use ssh, you can use ssh with -X parmas to avoid this issue")
    matplotlib.use('Agg')
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
    print("centos 6: sudo yum install tk-devel tcl-devel sqlite-devel gdbm-devel xz-devel readline-devel")
    print("cnetos 7: sudo yum install tk-devel tcl-devel sqlite-devel gdbm-devel xz-devel readline-devel python3-tk")
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

    def __init__(self, account, benchmark_code='000300', benchmark_type=MARKET_TYPE.INDEX_CN, if_fq=True, market_data=None):
        """
        account: QA_Account类/QA_PortfolioView类
        benchmark_code: [str]对照参数代码
        benchmark_type: [QA.PARAM]对照参数的市场
        if_fq: [Bool]原account是否使用复权数据
        if_fq选项是@尧提出的,关于回测的时候成交价格问题(如果按不复权撮合 应该按不复权价格计算assets)
        """
        self.account = account
        self.benchmark_code = benchmark_code  # 默认沪深300
        self.benchmark_type = benchmark_type

        self.fetch = {MARKET_TYPE.STOCK_CN: QA_fetch_stock_day_adv,
                      MARKET_TYPE.INDEX_CN: QA_fetch_index_day_adv}
        if self.account.market_type == MARKET_TYPE.STOCK_CN:
            self.market_data = QA_fetch_stock_day_adv(
                self.account.code, self.account.start_date, self.account.end_date)
        elif self.account.market_type == MARKET_TYPE.FUTURE_CN:
            self.market_data = market_data
        self.if_fq = if_fq

        if self.market_value is not None:
            self._assets = (self.market_value.sum(
                axis=1) + self.account.daily_cash.set_index('date').cash).fillna(method='pad')
        else:
            self._assets = self.account.daily_cash.set_index(
                'date').cash.fillna(method='pad')

        self.time_gap = QA_util_get_trade_gap(
            self.account.start_date, self.account.end_date)
        self.init_cash = self.account.init_cash
        self.init_assets = self.account.init_assets

    def __repr__(self):
        return '< QA_RISK ANALYSIS ACCOUNT/PORTFOLIO >'

    def __call__(self):
        return pd.DataFrame([self.message])

    @property
    @lru_cache()
    def total_timeindex(self):
        return self.account.trade_range

    @property
    @lru_cache()
    def market_value(self):
        """每日每个股票持仓市值表

        Returns:
            pd.DataFrame -- 市值表
        """
        if self.account.daily_hold is not None:
            if self.if_fq:

                return self.market_data.to_qfq().pivot('close').fillna(method='ffill') * self.account.daily_hold.apply(abs)
            else:
                return self.market_data.pivot('close').fillna(
                    method='ffill') * self.account.daily_hold.apply(abs)
        else:
            return None

    @property
    @lru_cache()
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
        return x1.assign(date=pd.to_datetime(x1.date)).set_index('date')[0]

    @property
    def max_dropback(self):
        """最大回撤
        """
        return round(float(max([(self.assets.iloc[idx] - self.assets.iloc[idx::].min())/self.assets.iloc[idx] for idx in range(len(self.assets))])), 2)

    @property
    def total_commission(self):
        """总手续费
        """
        return float(-abs(round(self.account.history_table.commission.sum(), 2)))

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
            'total_buyandsell': round(self.profit_money-self.total_commission-self.total_tax, 2),
            'total_tax': self.total_tax,
            'total_commission': self.total_commission,
            'total_profit': self.profit_money
        }

    @property
    def profit_money(self):
        """盈利额

        Returns:
            [type] -- [description]
        """

        return float(round(self.assets.iloc[-1]-self.init_cash, 2))

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

        return round(float(self.calc_annualize_return(self.assets, self.time_gap)), 2)

    @property
    def volatility(self):
        """波动率

        Returns:
            [type] -- [description]
        """
        return round(float(self.profit_pct.std() * math.sqrt(250)), 2)

    @property
    def ir(self):
        return self.calc_IR()

    @property
    @lru_cache()
    def message(self):
        return {
            'account_cookie': self.account.account_cookie,
            'portfolio_cookie': self.account.portfolio_cookie,
            'user_cookie': self.account.user_cookie,
            'annualize_return': round(self.annualize_return, 2),
            'profit': round(self.profit, 2),
            'max_dropback': self.max_dropback,
            'time_gap': self.time_gap,
            'volatility': self.volatility,
            'benchmark_code': self.benchmark_code,
            'bm_annualizereturn': self.benchmark_annualize_return,
            'bm_profit': self.benchmark_profit,
            'beta': self.beta,
            'alpha': self.alpha,
            'sharpe': self.sharpe,
            'init_cash': "%0.2f" % (float(self.init_cash)),
            'last_assets': "%0.2f" % (float(self.assets.iloc[-1])),
            'total_tax': self.total_tax,
            'total_commission': self.total_commission,
            'profit_money': self.profit_money,
            'assets': list(self.assets),
            'benchmark_assets': list(self.benchmark_assets),
            'timeindex': self.account.trade_day,
            'totaltimeindex': self.total_timeindex,
            'ir': self.ir
            # 'init_assets': round(float(self.init_assets), 2),
            # 'last_assets': round(float(self.assets.iloc[-1]), 2)
        }

    @property
    def benchmark_data(self):
        """
        基准组合的行情数据(一般是组合,可以调整)
        """
        return self.fetch[self.benchmark_type](
            self.benchmark_code, self.account.start_date, self.account.end_date)

    @property
    def benchmark_assets(self):
        """
        基准组合的账户资产队列
        """
        return (self.benchmark_data.close / float(self.benchmark_data.open.iloc[0]) * float(self.init_cash))

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

        return round(float(self.calc_annualize_return(self.benchmark_assets, self.time_gap)), 2)

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
        return round(float(self.calc_beta(self.profit_pct.dropna(), self.benchmark_profitpct.dropna())), 2)

    @property
    def alpha(self):
        """
        alpha比率 与市场基准收益无关的超额收益率
        """
        return round(float(self.calc_alpha(self.annualize_return, self.benchmark_annualize_return, self.beta, 0.05)), 2)

    @property
    def sharpe(self):
        """
        夏普比率

        """
        return round(float(self.calc_sharpe(self.annualize_return, self.volatility, 0.05)), 2)

    @property
    def sortino(self):
        """
        索提诺比率 投资组合收益和下行风险比值

        """
        pass

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
        return round((float(assets.iloc[-1]) / float(assets.iloc[0]) - 1)/(float(days) / 250), 2)

    def calc_profitpctchange(self, assets):
        return self.assets[::-1].pct_change()

    def calc_beta(self, assest_profit, benchmark_profit):

        calc_cov = np.cov(assest_profit, benchmark_profit)
        beta = calc_cov[0, 1] / calc_cov[1, 1]
        return beta

    def calc_alpha(self, annualized_returns, benchmark_annualized_returns, beta, r=0.05):

        alpha = (annualized_returns - r) - (beta) *\
            (benchmark_annualized_returns - r)
        return alpha

    def calc_IR(self):
        """计算信息比率

        Returns:
            [type] -- [description]
        """

        return self.annualize_return/self.volatility

    def calc_profit(self, assets):
        """
        计算账户收益
        期末资产/期初资产 -1
        """
        return (float(assets.iloc[-1]) / float(self.init_cash)) - 1

    def calc_sharpe(self, annualized_returns, volatility_year, r=0.05):
        """
        计算夏普比率
        r是无风险收益
        """
        # 会出现0
        if volatility_year == 0:
            return 0
        return (annualized_returns - r) / volatility_year

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
            plt.text(i, 0.5, '{} : {}'.format(
                item, self.message[item]), fontsize=10, rotation=0, wrap=True)
            i += (length/2.8)
        i = 0
        for item in ['benchmark_code', 'time_gap', 'max_dropback']:
            plt.text(i, 0.4, '{} : {}'.format(
                item, self.message[item]), fontsize=10, ha='left', rotation=0, wrap=True)
            i += (length/2.8)
        i = 0
        for item in ['annualize_return', 'bm_annualizereturn', 'profit']:
            plt.text(i, 0.3, '{} : {} %'.format(item, self.message.get(
                item, 0)*100), fontsize=10, ha='left', rotation=0, wrap=True)
            i += length/2.8
        i = 0
        for item in ['init_cash', 'last_assets', 'volatility']:
            plt.text(i, 0.2, '{} : {} '.format(
                item, self.message[item]), fontsize=10, ha='left', rotation=0, wrap=True)
            i += length/2.8
        i = 0
        for item in ['alpha', 'beta', 'sharpe']:
            plt.text(i, 0.1, '{} : {}'.format(
                item, self.message[item]), ha='left', fontsize=10, rotation=0, wrap=True)
            i += length/2.8
        plt.subplot(212)
        self.assets.plot()
        self.benchmark_assets.xs(self.benchmark_code, level=1).plot()

        asset_p = mpatches.Patch(
            color='red', label='{}'.format(self.account.account_cookie))
        asset_b = mpatches.Patch(
            label='benchmark {}'.format(self.benchmark_code))
        plt.legend(handles=[asset_p, asset_b], loc=1)
        plt.title('ASSET AND BENCKMARK')

        return plt

    def plot_dailyhold(self, start=None, end=None):
        """
        使用热力图画出每日持仓
        """
        start = self.account.start_date if start is None else start
        end = self.account.end_date if end is None else end
        _, ax = plt.subplots(figsize=(20, 8))
        sns.heatmap(self.account.daily_hold.reset_index().drop('account_cookie', axis=1).set_index(
            'date').loc[start:end], cmap="YlGnBu", linewidths=0.05, ax=ax)
        ax.set_title(
            'HOLD TABLE --ACCOUNT: {}'.format(self.account.account_cookie))
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
        sns.heatmap(self.account.trade.reset_index().drop('account_cookie', axis=1).set_index(
            'datetime').loc[start:end], cmap="YlGnBu", linewidths=0.05, ax=ax)
        ax.set_title(
            'SIGNAL TABLE --ACCOUNT: {}'.format(self.account.account_cookie))
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
    """

    def __init__(self, account):

        self.account = account
        self._style_title = ['beta', 'momentum', 'size', 'earning_yield',
                             'volatility', 'growth', 'value', 'leverage', 'liquidity', 'reversal']

    def __repr__(self):
        return 'QA_PERFORMANCE ANYLYSIS PLUGIN'

    @property
    def prefer(self):
        pass

    @property
    def style(self):
        """风格分析
        """
        pass

    @property
    @lru_cache()
    def pnl_lifo(self):
        """
        使用后进先出法配对成交记录
        """
        X = dict(zip(self.account.code, [LifoQueue()
                                         for i in range(len(self.account.code))]))
        pair_table = []
        for _, data in self.account.history_table.iterrows():
            if data.amount > 0:
                X[data.code].put((data.datetime, data.amount, data.price))
            elif data.amount < 0:
                while True:
                    l = X[data.code].get()
                    if l[1] == abs(data.amount):
                        pair_table.append(
                            [data.code, data.datetime, l[0], abs(data.amount), data.price, l[2]])
                        break
                    if l[1] > abs(data.amount):
                        temp = (l[0], l[1]+data.amount, l[2])
                        X[data.code].put_nowait(temp)
                        pair_table.append(
                            [data.code, data.datetime, l[0], abs(data.amount), data.price, l[2]])
                        break
                    elif l[1] < (abs(data.amount)):
                        data.amount = data.amount+l[1]
                        pair_table.append(
                            [data.code, data.datetime, l[0], l[1], data.price, l[2]])
        pair_title = ['code', 'sell_date', 'buy_date',
                      'amount', 'sell_price', 'buy_price']
        pnl = pd.DataFrame(pair_table, columns=pair_title).set_index('code')
        pnl = pnl.assign(pnl_ratio=(pnl.sell_price/pnl.buy_price) -
                         1)
        pnl = pnl.assign(pnl_money=pnl.pnl_ratio*pnl.amount)
        return pnl

    @property
    @lru_cache()
    def pnl_fifo(self):
        X = dict(zip(self.account.code, [deque()
                                         for i in range(len(self.account.code))]))
        pair_table = []
        for _, data in self.account.history_table.iterrows():
            if data.amount > 0:
                X[data.code].append((data.datetime, data.amount, data.price))
            elif data.amount < 0:
                while True:
                    l = X[data.code].popleft()
                    if l[1] == abs(data.amount):
                        pair_table.append(
                            [data.code, data.datetime, l[0], abs(data.amount), data.price, l[2]])
                        break
                    if l[1] > abs(data.amount):
                        temp = (l[0], l[1]+data.amount, l[2])
                        X[data.code].appendleft(temp)
                        pair_table.append(
                            [data.code, data.datetime, l[0], abs(data.amount), data.price, l[2]])
                        break
                    elif l[1] < (abs(data.amount)):
                        data.amount = data.amount+l[1]
                        pair_table.append(
                            [data.code, data.datetime, l[0], l[1], data.price, l[2]])

        pair_title = ['code', 'sell_date', 'buy_date',
                      'amount', 'sell_price', 'buy_price']
        pnl = pd.DataFrame(pair_table, columns=pair_title).set_index('code')

        pnl = pnl.assign(pnl_ratio=(pnl.sell_price/pnl.buy_price) -
                         1).assign(buy_date=pd.to_datetime(pnl.buy_date)).assign(sell_date=pd.to_datetime(pnl.sell_date))
        pnl = pnl.assign(pnl_money=(pnl.sell_price-pnl.buy_price)*pnl.amount)
        return pnl

    def plot_pnlratio(self, pnl):
        """
        画出pnl比率散点图
        """
        plt.scatter(x=pnl.sell_date.apply(str), y=pnl.pnl_ratio)
        plt.gcf().autofmt_xdate()
        return plt

    def plot_pnlmoney(self, pnl):
        """
        画出pnl盈亏额散点图
        """
        plt.scatter(x=pnl.sell_date.apply(str), y=pnl.pnl_money)
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

    def win_rate(self, methods='FIFO'):
        """胜率

        胜率
        盈利次数/总次数
        """
        data = self.pnl_lifo if methods in ['LIFO', 'lifo'] else self.pnl_fifo
        return round(len(data.query('pnl_money>0'))/len(data), 2)

    def average_profit(self, methods='FIFO'):
        data = self.pnl_lifo if methods in ['LIFO', 'lifo'] else self.pnl_fifo
        return (data.pnl_money.mean())

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
