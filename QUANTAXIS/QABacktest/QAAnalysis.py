#Encoding:UTF-8
"""
Analysis Center for Backtest
we will give some function
"""
import  numpy
import math
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_data

def QA_backtest_analysis_start(client,message,days):
    # 主要要从message_history分析
    # 1.收益率
    # 2.胜率
    # 3.回撤
    #print(message)
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
    # 这个benchmark是和第一次bid买入报价同时买入,然后一直持仓,计算账户价值

    trade_history=message['body']['account']['history']
    #计算交易日
    trade_date=QA_backtest_calc_trade_date(trade_history)
    total_date=message['body']['account']['total_date']
    
    #benchmark资产
    benchmark_assest=QA_backtest_calc_benchmark(message['header']['session']['code'],total_date,trade_history,client.quantaxis.stock_day)
    #benchmark年化收益
    benchmark_annualized_returns=QA_backtest_calc_profit_per_year(benchmark_assest,days)

    assest_history=message['body']['account']['assest_history'][1::]
    #days=len(assest_history)-1
    #策略年化收益
    annualized_returns=QA_backtest_calc_profit_per_year(assest_history,days)
    
    #收益矩阵
    assest_profit=QA_backtest_calc_profit_matrix(assest_history)
    benchmark_profit=QA_backtest_calc_profit_matrix(benchmark_assest)
    

    #策略日收益
    profit_day=message['body']['account']['cur_profit_present_total']
    #胜率
    win_rate=QA_backtest_calc_win_rate(profit_day)
    #年化波动率
    volatility_year=QA_backtest_calc_volatility(assest_profit)
    benchmark_volatility_year=QA_backtest_calc_volatility(benchmark_profit)
    #夏普比率
    sharpe=QA_backtest_calc_sharpe(annualized_returns,benchmark_annualized_returns,volatility_year)
    historys=message['body']['account']['assest_history']
    #最大回撤
    max_drop=QA_backtest_calc_dropback_max(historys)
    
    #计算beta
    beta=QA_backtest_calc_beta(assest_profit,benchmark_profit,benchmark_volatility_year)
    #计算Alpha
    alpha=QA_backtest_calc_alpha(annualized_returns,benchmark_annualized_returns,beta,0.05)
    message= {
        'code':message['header']['session']['code'],
        'annualized_returns':annualized_returns,
        'benchmark_annualized_returns':benchmark_annualized_returns,
        'benchmark_assest':benchmark_assest,
        'vol':volatility_year,
        'benchmark_vol':benchmark_volatility_year,
        'sharpe':sharpe,
        'alpha':alpha,
        'beta':beta,
        'total_date':total_date,
        'trade_date':trade_date,
        'max_drop':max_drop,
        'win_rate':win_rate}
    #print(message)
    return message


def QA_backtest_result_check(datelist,message):
     #list(set(datelist).difference(set(trade_list)))
    #print(message['body']['account']['history']['date'])
    pass

def QA_backtest_calc_benchmark(code,date,history,coll):
    
    data=QA_fetch_data(code,date[0],date[-1],coll)
    #print(data)
    benchmark_assest=[]
    for i in range(0,len(data),1):
        assest=float(data[i][4])*float(history[1][3])
        benchmark_assest.append(assest)
    #print('===history===')
    #print(history)
    #print('===benchmark===')
    
    #print(benchmark_assest)
    return benchmark_assest

def QA_backtest_calc_alpha(annualized_returns,benchmark_annualized_returns,beta,r):

    alpha=(annualized_returns-r)-(beta)*(benchmark_annualized_returns-r)
    return alpha
def QA_backtest_calc_beta(assest_profit,benchmark_profit,benchmark_volatility_year):
    if len(assest_profit)<len(benchmark_profit):
        for i in range(0,len(benchmark_profit)-len(assest_profit),1):
            assest_profit.append(0)
    elif len(assest_profit)>len(benchmark_profit):
         for i in range(0,len(assest_profit)-len(benchmark_profit),1):
            assest_profit.append(0)


    #print(assest_profit)
    #print(benchmark_profit)
    calc_cov=numpy.cov(assest_profit,benchmark_profit)[0,1]
    beta=calc_cov/benchmark_volatility_year
    return beta
def QA_backtest_calc_profit(assest_history):
    return (assest_history[-1]/assest_history[1])-1
def QA_backtest_calc_profit_per_year(assest_history,days):

    return float(float(assest_history[-1])/float(assest_history[0])-1)/int(days)*250

def QA_backtest_calc_profit_matrix(assest_history):
    assest_profit=[]
    #print(assest_history)
    for i in range(0,len(assest_history)-2,1):
        assest_profit.append(float(assest_history[i+1])/float(assest_history[i])-1)
    return assest_profit
def QA_backtest_calc_volatility(assest_profit_matrix):
    #策略每日收益的年化标准差
    #print(assest_profit_matrix)
    assest_profit=assest_profit_matrix
    #print(assest_profit)
    #print(len(assest_profit))
    volatility_day=numpy.std(assest_profit)
    #print(var)
   
    #print(volatility_day)
    volatility_year=volatility_day*math.sqrt(250)
    return volatility_year

def QA_backtest_calc_dropback_max(history):
    drops=[]
    for i in range(1,len(history),1):
        #print(historys[i-1])
        maxs=max(history[:i])
        cur=history[i-1]
        drop=1-cur/maxs
        drops.append(drop)
    max_drop=max(drops)
    return max_drop

def QA_backtest_calc_sharpe(annualized_returns,benchmark_annualized_returns,volatility_year):
    return (annualized_returns-benchmark_annualized_returns)/volatility_year


def QA_backtest_calc_trade_date(history):
    trade_date=[]
    for i in range(1,len(history)-1,1):
        trade_date.append(history[i][0])
    return trade_date
def QA_backtest_calc_trade_time_profit():
    pass
def QA_backtest_calc_trade_time_loss():
    pass
def QA_backtest_calc_win_rate(profit_day):
    # 大于0的次数
    abovez=0
    belowz=0
    for i in range(0,len(profit_day)-1,1):
        #print(profit_day[i])
        if profit_day[i]>0:
            abovez=abovez+1
        elif profit_day[i]<0:
            belowz=belowz+1
    if belowz==0:
        belowz=1
    win_rate=abovez/len(profit_day)
    return win_rate

def QA_backtest_plot_assest():
    pass