#coding :utf-8
from QUANTAXIS.QAUtil import QA_util_log_info
from ..QAMarket import QAMarket_core,QABid

class QA_Account:
    def __init__(self):
        self.assets=0
        self.portfolio=[]

    def QA_account_get_cash(self):
        return self.assets
    def QA_account_get_portfolio(self):
        return self.portfolio
    def QA_account_get_amount(self):
        pass
    def QA_account_receive_deal(self,message):
        pass
    def QA_account_renew(self):
        pass