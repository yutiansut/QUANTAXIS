#coding=utf-8
from QUANTAXIS import  QA_Market, QA_Portfolio, QA_Risk, QA_QAMarket_bid
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QAUtil import QA_util_log_info
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_data

import random
class QA_Backtest():
    
    account=QA_Account()
    market=QA_Market()
    bid=QA_QAMarket_bid()
    setting=QA_Setting()
    clients=setting.client
    user=setting.QA_setting_user_name
    def QA_backtest_init(self):
        pass

    def QA_backtest_start(self):
        QA_util_log_info('backtest start')


    def QA_backtest_day_start(self):
        pass

    def QA_backtest_handle(self):
        pass

    def QA_backtest_day_end(self):
        pass

    def QA_get_data(self):
        self.QA_get_data_from_market()
        self.QA_get_data_from_ARP()
    
    def QA_get_data_from_market(self):
        db=self.clients.quantaxis
        
    def QA_get_data_from_ARP(self):
        pass
    def QA_strategy_update(self):
        pass


