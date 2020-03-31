# Encoding:UTF-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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


"""
Analysis Center for Backtest
we will give some function
"""
import math
import sys

import numpy
import pandas as pd

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day
from QUANTAXIS.QAUtil import QA_util_log_info, trade_date_sse


def QA_backtest_analysis_backtest(client, code_list, assets_d, account_days, message, total_date, benchmark_data):

    # 主要要从message_history分析
    # 1.收益率
    # 2.胜率
    # 3.回撤
    """
    Annualized Returns: 策略年化收益率。表示投资期限为一年的预期收益率。
    具体计算方式为 (策略最终价值 / 策略初始价值)^(250 / 回测交易日数量) - 1

    Alpha：阿尔法
    具体计算方式为 (策略年化收益 - 无风险收益) - beta × (参考标准年化收益 - 无风险收益)，这里的无风险收益指的是中国固定利率国债收益率曲线上10年期国债的年化到期收益率。

    Beta：贝塔
    具体计算方法为 策略每日收益与参考标准每日收益的协方差 / 参考标准每日收益的方差 。

    Sharpe Ratio：夏普比率。表示每承受一单位总风险，会产生多少的超额报酬。
    具体计算方法为 (策略年化收益率 - 回测起始交易日的无风险利率) / 策略收益波动率 。

    Volatility：策略收益波动率。用来测量资产的风险性。
    具体计算方法为 策略每日收益的年化标准差 。

    Information Ratio：信息比率。衡量超额风险带来的超额收益。
    具体计算方法为 (策略每日收益 - 参考标准每日收益)的年化均值 / 年化标准差 。

    Max Drawdown：最大回撤。描述策略可能出现的最糟糕的情况。
    具体计算方法为 max(1 - 策略当日价值 / 当日之前虚拟账户最高价值)


    单次交易收益
    收益/次数的频次直方图
    单日最大持仓
    """
    # 数据检查
    if (len(benchmark_data)) < 1:
        QA_util_log_info('Wrong with benchmark data ! ')
        sys.exit()

    # 计算一个benchmark
    # 这个benchmark 是在开始的那天 市价买入和策略所选标的一致的所有股票,然后一直持仓
    data = pd.concat([pd.DataFrame(message['body']['account']['history'],
                                   columns=['time', 'code', 'price', 'towards', 'amount', 'order_id', 'trade_id', 'commission']),
                      pd.DataFrame(message['body']['account']['assets'], columns=['assets'])], axis=1)
    data['time'] = pd.to_datetime(data['time'])
    data.set_index('time', drop=False, inplace=True)

    trade_history = message['body']['account']['history']
    cash = message['body']['account']['cash']
    assets = message['body']['account']['assets']

    #assets_= data.resample('D').last().dropna()
    # 计算交易日
    trade_date = account_days
    # benchmark资产
    benchmark_assets = QA_backtest_calc_benchmark(
        benchmark_data, assets[0])
    # d2=pd.concat([data.resample('D').last(),pd.DataFrame(benchmark_assets,columns=['benchmark'])])
    # benchmark年化收益
    benchmark_annualized_returns = QA_backtest_calc_profit_per_year(
        benchmark_assets, len(total_date))
    # 计算账户的收益

    # days=len(assest_history)-1
    # 策略年化收益
    annualized_returns = QA_backtest_calc_profit_per_year(
        assets_d, len(total_date))

    # 收益矩阵
    assest_profit = QA_backtest_calc_profit_matrix(assets)
    benchmark_profit = QA_backtest_calc_profit_matrix(benchmark_assets)

    # 策略日收益
    profit_day = QA_backtest_calc_profit_matrix(assets_d)
    # 胜率
    win_rate = QA_backtest_calc_win_rate(assest_profit)
    # 日胜率
    win_rate_day = QA_backtest_calc_win_rate(profit_day)
    # 年化波动率
    volatility_year = QA_backtest_calc_volatility(profit_day)
    benchmark_volatility_year = QA_backtest_calc_volatility(benchmark_profit)
    # 夏普比率
    sharpe = QA_backtest_calc_sharpe(
        annualized_returns, 0.05, volatility_year)

    # 最大回撤
    max_drop = QA_backtest_calc_dropback_max(assets_d)

    # 计算beta
    beta = QA_backtest_calc_beta(profit_day, benchmark_profit)
    # 计算Alpha
    alpha = QA_backtest_calc_alpha(
        annualized_returns, benchmark_annualized_returns, beta, 0.05)
    message = {
        'code': code_list,
        'annualized_returns': annualized_returns,
        'benchmark_annualized_returns': benchmark_annualized_returns,
        'assets': assets_d[1:],
        'benchmark_assets': benchmark_assets[1:],
        'vol': volatility_year,
        'benchmark_vol': benchmark_volatility_year,
        'sharpe': sharpe,
        'alpha': alpha,
        'beta': beta,
        'total_date': total_date,
        'trade_date': trade_date,
        'max_drop': max_drop,
        'win_rate': win_rate}
    return message


def QA_backtest_calc_assets(trade_history, assets):
    assets_d = []
    trade_date = []
    for i in range(0, len(trade_history), 1):
        if trade_history[i][0] not in trade_date:
            trade_date.append(trade_history[i][0])
            assets_d.append(assets[i])
        else:
            assets_d.pop(-1)
            assets_d.append(assets[i])

    return assets_d


def QA_backtest_calc_benchmark(benchmark_data, init_assets):

    return list(benchmark_data['close'] / float(benchmark_data['open'][0]) * float(init_assets))


def QA_backtest_calc_alpha(annualized_returns, benchmark_annualized_returns, beta, r):

    alpha = (annualized_returns - r) - (beta) * \
        (benchmark_annualized_returns - r)
    return alpha


def QA_backtest_calc_beta(assest_profit, benchmark_profit):
    if len(assest_profit) < len(benchmark_profit):
        for i in range(0, len(benchmark_profit) - len(assest_profit), 1):
            assest_profit.append(0)
    elif len(assest_profit) > len(benchmark_profit):
        for i in range(0, len(assest_profit) - len(benchmark_profit), 1):
            benchmark_profit.append(0)
    calc_cov = numpy.cov(assest_profit, benchmark_profit)
    beta = calc_cov[0, 1] / calc_cov[1, 1]
    return beta


def QA_backtest_calc_profit(assest_history):
    return (assest_history[-1] / assest_history[1]) - 1


def QA_backtest_calc_profit_per_year(assest_history, days):
    return math.pow(float(assest_history[-1]) / float(assest_history[0]), 250.0 / float(days)) - 1.0


def QA_backtest_calc_profit_matrix(assest_history):
    assest_profit = []
    if len(assest_history) > 1:
        assest_profit = [assest_history[i + 1] / assest_history[i] -
                         1.0 for i in range(len(assest_history) - 1)]
    return assest_profit


def QA_backtest_calc_volatility(assest_profit_matrix):
    # 策略每日收益的年化标准差
    assest_profit = assest_profit_matrix

    volatility_day = numpy.std(assest_profit)
    volatility_year = volatility_day * math.sqrt(250)
    return volatility_year


def QA_backtest_calc_dropback_max(history):
    drops = []
    for i in range(1, len(history), 1):
        maxs = max(history[:i])
        cur = history[i - 1]
        drop = 1 - cur / maxs
        drops.append(drop)
    max_drop = max(drops)
    return max_drop


def QA_backtest_calc_sharpe(annualized_returns, r, volatility_year):
    '计算夏普比率'
    return (annualized_returns - r) / volatility_year


def QA_backtest_calc_trade_date(history):
    '计算交易日期'
    trade_date = []

    # trade_date_sse.index(history[-1][0])-trade_date_sse.index(history[0][0])
    for i in range(0, len(history), 1):
        if history[i][0] not in trade_date:
            trade_date.append(history[i][0])
    return trade_date


def calc_trade_time(history):
    return len(history)


def calc_every_pnl(detail):
    pass


def QA_backtest_calc_win_rate(profit_day):
    # 大于0的次数
    abovez = 0
    belowz = 0
    for i in range(0, len(profit_day) - 1, 1):
        if profit_day[i] > 0:
            abovez = abovez + 1
        elif profit_day[i] < 0:
            belowz = belowz + 1
    if belowz == 0:
        belowz = 1
    if abovez == 0:
        abovez = 1
    win_rate = abovez / (abovez + belowz)
    return win_rate
