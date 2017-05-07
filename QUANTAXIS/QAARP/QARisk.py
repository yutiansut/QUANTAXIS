#coding:utf-8
from QUANTAXIS.QABacktest import QAAnalysis
from QUANTAXIS.QAUtil import QA_util_log_info,QA_util_log_expection
"""message['body']['account']
'account':{
            'init_assest':self.total_assest[0],
            'portfolio':self.portfolio,
            'history':self.history_trade,
            'assest_now':self.total_assest[-1],
            'assest_history':self.total_assest,
            'assest_free':self.assets_free,
            'total_assest_free':self.total_assest_free,
            'assest_fix':self.assets_market_hold_value,
            'profit':self.total_profit[-1],
            'assets_profit_day':0,
            'assets_profit_total':[0],
            'total_profit':self.total_profit,
            'cur_profit_present':self.cur_profit_present,
            'cur_profit_present_total':self.cur_profit_present_total,
            'hold':self.hold}
"""
"""收益性的包括年化收益率、净利润、总盈利、总亏损、有效年化收益率、资金使用率。

风险性主要包括胜率、平均盈亏比、最大回撤比例、最大连续亏损次数、最大连续盈利次数、持仓时间占比、贝塔。

综合性指标主要包括风险收益比，夏普比例，波动率，VAR，偏度，峰度等"""
def QA_risk_eva_account(client,message,days):
    cookie=message['header']['cookie']
    account=message['body']['account']
    #绩效表现指标分析
    performance= QAAnalysis.QA_backtest_analysis_start(client,message,days)
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
    #1.可用资金占当前总资产比重
        risk_account_freeCash_currentAssest=QA_risk_account_freeCash_currentAssest(float(account['assest_free']),float(account['assest_now']))
        #2.当前策略速动比率(流动资产/流动负债)
        risk_account_freeCash_initAssest=QA_risk_account_freeCash_initAssest(account['assest_free'],account['init_assest'])
        risk_account_freeCash_frozenAssest=QA_risk_account_freeCash_frozenAssest(float(account['assest_free']),float(account['assest_fix']))

        return {""}
        
    except:
        QA_util_log_expection('error in risk evaluation')
    


def QA_risk_account_freeCash_initAssest(freeCash,initAssest):
    try:
        result=float(freeCash)/float(initAssest)
        return result
    except:
        return 0
        QA_util_log_expection('error in QA_risk_account_freeCash_initAssest')
        QA_util_log_expection('freeCash: '+str(freeCash))
        QA_util_log_expection('currentAssest: '+str(initAssest))
        QA_util_log_expection('expected result: '+str(float(freeCash)/float(initAssest)))
def QA_risk_account_freeCash_currentAssest(freeCash,currentAssest):
    try:
        result=float(freeCash)/float(currentAssest)
        return result
    except:
        return 0
        QA_util_log_expection('error in QA_risk_account_freeCash_currentAssest')
        QA_util_log_expection('freeCash: '+str(freeCash))
        QA_util_log_expection('currentAssest: '+str(currentAssest))
        QA_util_log_expection('expected result: '+str(float(freeCash)/float(currentAssest)))

def QA_risk_account_freeCash_frozenAssest(freeCash,frozenAssest):
    try:
        result=float(freeCash)/float(frozenAssest)
        return result
    except:
        return 0
        QA_util_log_expection('error in QA_risk_account_freeCash_frozenAssest')
        QA_util_log_expection('freeCash: '+str(freeCash))
        QA_util_log_expection('currentAssest: '+str(frozenAssest))
        QA_util_log_expection('expected result: '+str(float(freeCash)/float(frozenAssest)))



class QA_Risk():
    pass