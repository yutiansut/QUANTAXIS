import QUANTAXIS as QA

class backtest(QA.QA_Backtest):
    def settings(self):
        
        self.setting.QA_util_sql_mongo_ip='127.0.0.1'
        self.setting.QA_util_sql_mongo_port=27017
        self.setting.QA_setting_user_name='yutiansut'
        self.setting.QA_setting_user_password='yutiansut'
    def start(self):
        
        self.QA_backtest_init()
        self.settings()
        self.QA_backtest_start()

        

back=backtest()
back.start()