# Encoding:UTF-8
"""
Analysis Center for Backtest
we will give some function
"""
import numpy
import math
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day
from QUANTAXIS.QAUtil import QA_util_log_info


def QA_backtest_analysis_start(client, message,total_date, market_data):
    # 主要要从message_history分析
    # 1.收益率
    # 2.胜率
    # 3.回撤
    """
    Annualized Returns: 策略年化收益率。表示投资期限为一年的预期收益率。
    具体计算方式为 (策略最终价值 / 策略初始价值 - 1) / 回测交易日数量 × 250

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
    """
    # 计算一个benchmark
    # 这个benchmark 是在开始的那天 市价买入和策略所选标的一致的所有股票,然后一直持仓

    trade_history = message['body']['account']['history']
    cash=message['body']['account']['cash']
    assets=message['body']['account']['assets']
    # 计算交易日
    trade_date = QA_backtest_calc_trade_date(trade_history)
    assets_d=QA_backtest_calc_asset(trade_history,assets)
    #account_profit=
    # benchmark资产
    benchmark_assets = QA_backtest_calc_benchmark(market_data,total_date,assets)
    # benchmark年化收益
    benchmark_annualized_returns = QA_backtest_calc_profit_per_year(
        benchmark_assets, len(total_date))
    # 计算账户的收益

    
    # days=len(assest_history)-1
    # 策略年化收益
    annualized_returns = QA_backtest_calc_profit_per_year(assets, len(total_date))

    # 收益矩阵
    assest_profit = QA_backtest_calc_profit_matrix(assets)
    benchmark_profit = QA_backtest_calc_profit_matrix(benchmark_assets)

    # 策略日收益
    profit_day = QA_backtest_calc_profit_matrix(assets_d)
    # 胜率
    win_rate = QA_backtest_calc_win_rate(profit_day)
    # 年化波动率
    volatility_year = QA_backtest_calc_volatility(assest_profit)
    benchmark_volatility_year = QA_backtest_calc_volatility(benchmark_profit)
    # 夏普比率
    sharpe = QA_backtest_calc_sharpe(
        annualized_returns, benchmark_annualized_returns, volatility_year)
    
    # 最大回撤
    max_drop = QA_backtest_calc_dropback_max(assets_d)

    # 计算beta
    beta = QA_backtest_calc_beta(
        assest_profit, benchmark_profit, benchmark_volatility_year)
    # 计算Alpha
    alpha = QA_backtest_calc_alpha(
        annualized_returns, benchmark_annualized_returns, beta, 0.05)
    message = {
        'code': message['header']['session']['code'],
        'annualized_returns': annualized_returns,
        'benchmark_annualized_returns': benchmark_annualized_returns,
        'benchmark_assets': benchmark_assets,
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

def QA_backtest_calc_asset(trade_history,assets):
    assets_d=[]
    trade_date = []
    for i in range(0, len(trade_history), 1):
        print(trade_date)
        if trade_history[i][0] not in trade_date:
            trade_date.append(trade_history[i][0])
            assets_d.append(assets[i])
        else:
            assets_d.pop(-1)
            assets_d.append(assets[i])
    
    return assets_d
        
        
def QA_backtest_result_check(datelist, message):
    pass


def QA_backtest_calc_benchmark(market,date_list,assets):    
    benchmark_assest =[float(assets[0])]
    #buy
    buy_date=date_list[0]
    hold_list=[0,0,0,0]
      
    for i in range(0, len(date_list), 1):
        temp_assets=0
        temp_assets_t=0
        for j in range(0,len(market)):
            print(hold_list)
            for items in market[j]:
                print(i)
                print(date_list[i])
                print(items[6])
                print(items[0])
                if date_list[i] == items[6]:
                    if hold_list[j]>0:
                        temp_assets_t = (float(items[1])*float(hold_list[j]))
                    else :
                        hold_list[j]=(benchmark_assest[0]/len(market))/float(items[1])
                        temp_assets_t =benchmark_assest[0]/len(market)
                else:
                   temp_assets_t =benchmark_assest[0]/len(market)

            temp_assets+=temp_assets_t
        benchmark_assest.append(temp_assets)
        
    print(benchmark_assest)
    return benchmark_assest


def QA_backtest_calc_alpha(annualized_returns, benchmark_annualized_returns, beta, r):

    alpha = (annualized_returns - r) - (beta) * \
        (benchmark_annualized_returns - r)
    return alpha


def QA_backtest_calc_beta(assest_profit, benchmark_profit, benchmark_volatility_year):
    if len(assest_profit) < len(benchmark_profit):
        for i in range(0, len(benchmark_profit) - len(assest_profit), 1):
            assest_profit.append(0)
    elif len(assest_profit) > len(benchmark_profit):
        for i in range(0, len(assest_profit) - len(benchmark_profit), 1):
            benchmark_profit.append(0)
    calc_cov = numpy.cov(assest_profit, benchmark_profit)[0, 1]
    beta = calc_cov / benchmark_volatility_year
    return beta


def QA_backtest_calc_profit(assest_history):
    return (assest_history[-1] / assest_history[1]) - 1


def QA_backtest_calc_profit_per_year(assest_history, days):
    return float(float(assest_history[-1]) / float(assest_history[0]) - 1) / int(days) * 250


def QA_backtest_calc_profit_matrix(assest_history):
    assest_profit = []
    for i in range(0, len(assest_history) - 2, 1):
        assest_profit.append(
            float(assest_history[i + 1]) / float(assest_history[i]) - 1)
    return assest_profit


def QA_backtest_calc_volatility(assest_profit_matrix):
    # 策略每日收益的年化标准差
    assest_profit = assest_profit_matrix

    volatility_day = numpy.std(assest_profit)
    volatility_year = volatility_day * math.sqrt(250)
    return volatility_year


def QA_backtest_calc_dropback_max(history):
    drops = []
    print(history)
    for i in range(1, len(history), 1):
        maxs = max(history[:i])
        cur = history[i - 1]
        drop = 1 - cur / maxs
        drops.append(drop)
    max_drop = max(drops)
    return max_drop


def QA_backtest_calc_sharpe(annualized_returns, benchmark_annualized_returns, volatility_year):
    return (annualized_returns - benchmark_annualized_returns) / volatility_year


def QA_backtest_calc_trade_date(history):
    trade_date = []
    for i in range(0, len(history), 1):
        if history[i][0] not in trade_date:
            trade_date.append(history[i][0])
    return trade_date


def QA_backtest_calc_trade_time_profit():
    pass


def QA_backtest_calc_trade_time_loss():
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

