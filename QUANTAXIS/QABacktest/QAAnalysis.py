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

    profit_year=(message['body']['account']['assest_history'][-1]/message['body']['account']['assest_history'][1]-1)/days*250

    profit_day=message['body']['account']['cur_profit_present_total']

    narray=numpy.array(profit_day)
    sum1=narray.sum()
    narray2=narray*narray
    sum2=narray2.sum()
    mean=sum1/days
    var=sum2/days-mean**2

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

    historys=message['body']['account']['assest_history']
    drops=[]
    for i in range(1,len(historys),1):
        #print(historys[i-1])
        maxs=max(historys[:i])
        cur=historys[i-1]
        drop=1-cur/maxs
        drops.append(drop)
    max_drop=max(drops)

    return {'profit_year':profit_year,'vol':var,'max_drop':max_drop,'win_rate':win_rate}


def QA_backtest_result_check(datelist,message):
     #list(set(datelist).difference(set(trade_list)))
    print(message['body']['account']['history']['date'])
def QA_backtest_calc_alpha(check,message):
    pass
def QA_backtest_calc_beta():
    pass

def QA_backtest_calc_profit():
    pass
def QA_backtest_calc_profit_per_year():
    pass
def QA_backtest_calc_profit_per_trade():
    pass
def QA_backtest_calc_volatility():
    pass
def QA_backtest_calc_drowback():
    pass
def QA_backtest_calc_drowback_max():
    pass

def QA_backtest_calc_sharpe():
    pass


def QA_backtest_calc_trade_time():
    pass
def QA_backtest_calc_trade_time_profit():
    pass
def QA_backtest_calc_trade_time_loss():
    pass
def QA_backtest_calc_win_rate():
    pass

def QA_backtest_plot_assest():
    pass