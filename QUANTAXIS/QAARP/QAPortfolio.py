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


        pass

    def cookie_mangement(self):
        pass
        
    def QA_portfolio_get_free_cash(self):
        pass