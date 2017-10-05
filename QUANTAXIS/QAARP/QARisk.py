# coding:utf-8
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

from QUANTAXIS.QABacktest import QAAnalysis
from QUANTAXIS.QAUtil import QA_util_log_expection, QA_util_log_info
import math
import numpy
import pandas
"""收益性的包括年化收益率、净利润、总盈利、总亏损、有效年化收益率、资金使用率。

风险性主要包括胜率、平均盈亏比、最大回撤比例、最大连续亏损次数、最大连续盈利次数、持仓时间占比、贝塔。

综合性指标主要包括风险收益比，夏普比例，波动率，VAR，偏度，峰度等"""

"""
the account datastruct should be a standard struct which can be directly sended to another function
"""


def QA_risk_eva_account(message, days, client):
    cookie = message['header']['cookie']
    account = message['body']['account']
    # 绩效表现指标分析
    """ 
    message= {
            'annualized_returns':annualized_returns,
            'benchmark_annualized_returns':benchmark_annualized_returns,
            'benchmark_assest':benchmark_assest,
            'vol':volatility_year,
            'benchmark_vol':benchmark_volatility_year,
            'sharpe':sharpe,
            'alpha':alpha,
            'beta':beta,
            'max_drop':max_drop,
            'win_rate':win_rate}
    """
    try:
        # 1.可用资金占当前总资产比重
        risk_account_freeCash_currentAssest = QA_risk_account_freeCash_currentAssest(
            float(account['assest_free']), float(account['assest_now']))
        # 2.当前策略速动比率(流动资产/流动负债)
        risk_account_freeCash_initAssest = QA_risk_account_freeCash_initAssest(
            account['assest_free'], account['init_assest'])
        risk_account_freeCash_frozenAssest = QA_risk_account_freeCash_frozenAssest(
            float(account['assest_free']), float(account['assest_fix']))

        return {""}

    except:
        QA_util_log_expection('error in risk evaluation')


def QA_risk_account_freeCash_initAssest(freeCash, initAssest):
    try:
        result = float(freeCash) / float(initAssest)
        return result
    except:
        return 0
        QA_util_log_expection('error in QA_risk_account_freeCash_initAssest')
        QA_util_log_expection('freeCash: ' + str(freeCash))
        QA_util_log_expection('currentAssest: ' + str(initAssest))
        QA_util_log_expection('expected result: ' +
                              str(float(freeCash) / float(initAssest)))


def QA_risk_account_freeCash_currentAssest(freeCash, currentAssest):
    try:
        result = float(freeCash) / float(currentAssest)
        return result
    except:
        return 0
        QA_util_log_expection(
            'error in QA_risk_account_freeCash_currentAssest')
        QA_util_log_expection('freeCash: ' + str(freeCash))
        QA_util_log_expection('currentAssest: ' + str(currentAssest))
        QA_util_log_expection('expected result: ' +
                              str(float(freeCash) / float(currentAssest)))


def QA_risk_account_freeCash_frozenAssest(freeCash, frozenAssest):
    try:
        result = float(freeCash) / float(frozenAssest)
        return result
    except:
        return 0
        QA_util_log_expection('error in QA_risk_account_freeCash_frozenAssest')
        QA_util_log_expection('freeCash: ' + str(freeCash))
        QA_util_log_expection('currentAssest: ' + str(frozenAssest))
        QA_util_log_expection('expected result: ' +
                              str(float(freeCash) / float(frozenAssest)))


def QA_risk_calc_assets(trade_history, assets):
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


def QA_risk_result_check(datelist, message):
    pass


def QA_risk_calc_benchmark(benchmark_data, init_assets):

    return list(benchmark_data['close'] / float(benchmark_data['open'][0]) * float(init_assets))


def QA_risk_calc_alpha(annualized_returns, benchmark_annualized_returns, beta, r):

    alpha = (annualized_returns - r) - (beta) * \
        (benchmark_annualized_returns - r)
    return alpha


def QA_risk_calc_beta(assest_profit, benchmark_profit):
    if len(assest_profit) < len(benchmark_profit):
        for i in range(0, len(benchmark_profit) - len(assest_profit), 1):
            assest_profit.append(0)
    elif len(assest_profit) > len(benchmark_profit):
        for i in range(0, len(assest_profit) - len(benchmark_profit), 1):
            benchmark_profit.append(0)
    calc_cov = numpy.cov(assest_profit, benchmark_profit)
    beta = calc_cov[0, 1] / calc_cov[1, 1]
    return beta


def QA_risk_calc_profit(assest_history):
    return (assest_history[-1] / assest_history[1]) - 1


def QA_risk_calc_profit_per_year(assest_history, days):
    return math.pow(float(assest_history[-1]) / float(assest_history[0]), 250.0 / float(days)) - 1.0


def QA_risk_calc_profit_matrix(assest_history):
    assest_profit = []
    if len(assest_history) > 1:
        assest_profit = [assest_history[i + 1] / assest_history[i] -
                         1.0 for i in range(len(assest_history) - 1)]
    return assest_profit


def QA_risk_calc_volatility(assest_profit_matrix):
    # 策略每日收益的年化标准差
    assest_profit = assest_profit_matrix

    volatility_day = numpy.std(assest_profit)
    volatility_year = volatility_day * math.sqrt(250)
    return volatility_year


def QA_risk_calc_dropback_max(history):
    drops = []
    for i in range(1, len(history), 1):
        maxs = max(history[:i])
        cur = history[i - 1]
        drop = 1 - cur / maxs
        drops.append(drop)
    max_drop = max(drops)
    return max_drop


def QA_risk_calc_sharpe(annualized_returns, r, volatility_year):
    '计算夏普比率'
    return (annualized_returns - r) / volatility_year


def QA_risk_calc_trade_date(history):
    '计算交易日期'
    trade_date = []

    # trade_date_sse.index(history[-1][0])-trade_date_sse.index(history[0][0])
    for i in range(0, len(history), 1):
        if history[i][0] not in trade_date:
            trade_date.append(history[i][0])
    return trade_date


def QA_risk_calc_trade_time_profit():
    pass


def QA_risk_calc_trade_time_loss():
    pass


def QA_risk_calc_win_rate(profit_day):
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


class QA_Risk():
    pass
