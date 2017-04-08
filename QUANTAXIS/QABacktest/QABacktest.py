from QUANTAXIS import QA_Account,QA_Market,QA_Portfolio,QA_Risk,QA_QAMarket_bid
from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QAUtil import QA_util_log_info


class QA_Backtest():
    def QA_backtest_init(self):
        self.account=QA_Account()
        self.market=QA_Market()
        self.bid=QA_QAMarket_bid()
        self.setting=QA_Setting()
    def QA_backtest_start(self):
        QA_util_log_info('backtest start')
    def QA_get_data(self):
        pass
    def QA_get_data_from_market(self):
        pass
    def QA_get_data_from_ARP(self):
        pass
    def QA_strategy_update(self):
        pass
    def QA_strategy_analysis(self):
        pass
    
    