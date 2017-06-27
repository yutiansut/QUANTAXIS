import QUANTAXIS as QA

class backtest(QA.QA_Backtest):

    def start(self):
        #self.account.__init__()
        #首先测试能拿到的数据
        # 首先测试账户的初始化
        print('===test account init===')
        self.account.init()
        print(self.account.account_cookie)
        print(self.account.assets)
        print(self.account.portfolio)
        print(self.account.cash)
        print(self.account.bid)
        print('===test market init===')
        print(self.bid)
        print(self.bid.bid['code'])
        print(self.bid.bid['amount'])
        print(self.bid.bid['price'])
        print(self.bid.bid['time'])
        print('===test setting ===')
        print(self.clients)
        print(self.setting.QA_setting_user_name)
        self.setting.QA_setting_user_name='admin'
        self.setting.QA_setting_user_password='admin'
        print(self.setting.QA_setting_login())
        #self.setting.QA_util_sql_mongo_ip='192.168.4.189'
        self.setting.QA_util_sql_mongo_ip='127.0.0.1'
        self.setting.QA_setting_init()
        print(self.setting.client)
        print('===finish test init===')

        print('===start test get data====')
        self.get_data_from_market()
        print('===start a strategy====')
        print('==check the account==')
        print(self.account.assets_free)
        print('==set the date==')
        self.strategy_start_date='2015-01-01'
        print(self.strategy_start_date)
        print('==make a bid==')
        self.bid.bid['price']=10.846
        self.bid.bid['time']='2015-01-05'
        self.bid.bid['amount']=100
        print(self.bid.bid)
        message=self.market.market_make_deal(self.bid.bid,self.setting.client)
        print('==market responds')
        print(message)
        print('==update account==')
        self.account.QA_account_receive_deal(message,self.setting.client)
        print('==at the end of day')
        print(self.account.message)

        
        print('===next Day===')

        print('==make a bid==')
        self.bid.bid['price']=10.751
        self.bid.bid['time']='2015-01-06'
        self.bid.bid['amount']=100
        self.bid.bid['towards']=-1
        print(self.bid.bid)
        message=self.market.market_make_deal(self.bid.bid,self.setting.client)
        print('==market responds')
        print(message)
        print('==update account==')
        self.account.QA_account_receive_deal(message,self.setting.client)
        print('==at the end of day')
        print(self.account.message)



        print('===at the end of strategy===')
        
    def get_data_from_market(self):
        self.coll=self.setting.client.quantaxis.stock_day
        data=QA.QA_fetch_data('000001','2015-05-01','2016-05-04',self.coll)
        print(data)
    def get_data_from_ARP(self):
        return self.account.QA_Account_get_message()
    def settings(self):
        # 设置数据库位置,用户名
        self.setting.QA_util_sql_mongo_ip='127.0.0.1'
        self.setting.QA_util_sql_mongo_port=27017
        self.setting.QA_setting_user_name='yutiansut'
        self.setting.QA_setting_user_password='yutiansut'
        # 初始化设置
        self.setting.QA_setting_init()


back=backtest()
back.start()
