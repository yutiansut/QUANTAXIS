#coding:utf-8
from .QAAccount import QA_Account
from .QARisk import QA_Risk
from QUANTAXIS.QAUtil import QA_util_log_info,QA_util_date_stamp,QA_util_date_valid
import threading

class QA_Portfolio():
    
    """
    在portfolio中,我们希望通过cookie来控制account_unit
    对于account的指标,要进行风险控制,组合成最优的投资组合的量

    portfolio通过每天结束的时候,计算总账户可用资金,来更新和计算总账户资金占比情况

    """
    def init(self):
        self.portfolio_code=['']
        self.portfolio_account=[]
        for i in range(0,len(self.portfolio_code)-1,1):
            self.portfolio_account[i]=QA_Account()
    
    def QA_portfolio_get_portfolio(self):
        #QA_util_log_info(self.portfolio_account)
        return self.portfolio_account

    def QA_portfolio_calc(self):
        """
        {
        'init_assest':'self.total_assest[0]',
        'portfolio':'self.portfolio',
        'history':'history_trade',
        'assest_now':'total_assest[-1]',
        'assest_history':'self.total_assest',
        'assest_free':'self.assets_free',
        'total_assest_free':'self.total_assest_free',
        'assest_fix':'self.assets_market_hold_value',
        'profit':'self.total_profit[-1]',
        'account_date':'self.account_date',
        'assets_profit_day':0,
        'assets_profit_total':[0],
        'total_profit':'self.total_profit',
        'total_date':'self.total_date',
        'cur_profit_present':'self.cur_profit_present',
        'cur_profit_present_total':'self.cur_profit_present_total',
        'hold':'hold'}
        """
        pass

    def cookie_mangement(self):
        pass
        
    def QA_portfolio_get_free_cash(self):
        pass