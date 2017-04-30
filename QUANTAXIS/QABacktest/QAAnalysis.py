#Encoding:UTF-8
"""
Analysis Center for Backtest
we will give some function
"""
import  numpy

def QA_backtest_analysis_start(message,days):
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
    # 这个benchmark是和第一次bid买入报价同时买入,然后一直持仓,计算账户价值
    trade_history=message['body']['account']['history']
    benchmark_assert=QA_backtest_calc_benchmark(trade_history)

    assert_history=message['body']['account']['assert_history']
    days=len(assert_history)-1
    profit_year=QA_backtest_calc_profit_per_year(assert_history)

    profit_day=message['body']['account']['cur_profit_present_total']
    win_rate=QA_backtest_calc_win_rate(profit_day)
    Var=QA_backtest_calc_volatility(profit_day)

    historys=message['body']['account']['assest_history']
    max_drops=QA_backtest_calc_dropback_max(historys)
   


    return {'annualized_returns':profit_year,'vol':var,'max_drop':max_drop,'win_rate':win_rate}


def QA_backtest_result_check(datelist,message):
     #list(set(datelist).difference(set(trade_list)))
    print(message['body']['account']['history']['date'])


def QA_backtest_calc_benchmark(history):
    print(history)
    benchmark_assest=[]
    for i in range(1,len(history)-1,1):
        assest=history[i][2]*history[1][3]
        benchmark_assest.append(assest)
    return benchmark_assest
def QA_backtest_calc_alpha(assert_history,benchmark_history,):
    pass
def QA_backtest_calc_beta():
    pass

def QA_backtest_calc_profit(assert_history):
    return (assert_history[-1]/assert_history[1])-1
def QA_backtest_calc_profit_per_year(assert_history):
    
    return (assert_history[-1]/assert_history[1]-1)/(len(assert_history)-1)*250

def QA_backtest_calc_profit_per_trade():
    pass
def QA_backtest_calc_volatility(profit_day):
    narray=numpy.array(profit_day)
    sum1=narray.sum()
    narray2=narray*narray
    sum2=narray2.sum()
    mean=sum1/days
    Var=sum2/days-mean**2
    return Var

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

def QA_backtest_calc_sharpe():
    pass


def QA_backtest_calc_trade_time():
    pass
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
    win_rate=abovez/belowz
    return win_rate

def QA_backtest_plot_assest():
    pass