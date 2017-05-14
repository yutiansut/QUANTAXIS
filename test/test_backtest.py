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
        print(self.account.total_assest)
        print(self.account.message)
        print(self.account.assets_free)
        print(self.account.total_assest)
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

"""
result:

PS C:\quantaxis> python .\test\test_backtest.py
root        : INFO     start QUANTAXIS
root        : INFO     ip:127.0.0.1   port:27017
root        : INFO     Welcome to QUANTAXIS, the Version is 0.3.8-dev-RC-ARP
===test account init===
0.5643322358936594
1000
{'date': '', 'id': 'N', ' price': '', 'amount': ''}
[0]
{}
1000
[0]
===test market init===
<QUANTAXIS.QAMarket.QABid.QA_QAMarket_bid object at 0x00000294D99EEFD0>
000001.SZ
10.0
4.5
2000-01-17
===test setting ===
MongoClient(host=['127.0.0.1:27017'], document_class=dict, tz_aware=False, connect=True)

root        : INFO     username:yutiansut
root        : INFO     success login! your username is:yutiansut
{'username': 'yutiansut', 'password': 'yutiansut', 'login': True}
root        : INFO     ip:192.168.4.189   port:27017
root        : INFO     username:yutiansut
root        : INFO     success login! your username is:yutiansut
MongoClient(host=['192.168.4.189:27017'], document_class=dict, tz_aware=False, connect=True)
===finish test init===
===start test get data====
[['000001' '1.8239196867765888' '1.7395597650596495' ...,
  '1.7715583560557298' '9693911.0' '2005-05-09']
 ['000001' '1.8501003521370185' '1.7366508022418239' ...,
  '1.8355555380478907' '10841413.0' '2005-05-10']
 ['000001' '1.8617362034083205' '1.7802852445092063' ...,
  '1.800647984233985' '10686837.0' '2005-05-11']
 ...,
 ['000001' '2.045000860931327' '1.8704630918617968' ...,
  '2.045000860931327' '22845526.0' '2006-04-26']
 ['000001' '2.1933579646404273' '2.0740904891095817' ...,
  '2.1380876711017427' '85852460.0' '2006-04-27']
 ['000001' '2.35335091962083' '2.111907005741313' ..., '2.2922627004464946'
  '68498093.0' '2006-04-28']]
===start a strategy====
==check the account==
1000
==set the date==
2001-01-01
==make a bid==
root        : INFO     ==== Market Board ====
root        : INFO     day High4.559326959739777
root        : INFO     your bid price4.5
root        : INFO     day Low4.40818904947216
root        : INFO     ==== Market Board ====
root        : INFO     deal success
==market responds
{'header': {'source': 'market', 'status': True, 'session': {'user': 'root', 'strategy': 'root01'}}, 'body': {'bid': {'price': '4.5', 'code': '000001.SZ', 'amount': '10.0', 'time': '2000-01-17', 'towards': '1'}, 'market': {'open': 4.508947656317237, 'high': 4.559326959739777, 'low': 4.40818904947216, 'close': 4.5542890293975224, 'volume': 3450100.0, 'code': '000001'}}}
==update account==
[0]
10.0
4.5
1
root        : INFO     hold-=========================================
4.5542890293975224
4.5
==at the end of day
{'header': {'source': 'account', 'cookie': '0.5643322358936594', 'session': {'user': 'root', 'strategy': 'root01'}}, 'body': {'account': {'init_assest': 0.5428902939752263, 'portfolio': {'date': '2000-01-17', 'id': '000001.SZ', ' price': '', 'amount': '10.0', 'price': '4.5'}, 'history': [['date', 'id', ' price', 'amount', ' towards'], ['2000-01-17', '000001.SZ', '4.5', '10.0', '1']], 'assest_now': 0.5428902939752263, 'assest_history': [0, '0.5428902939752263'], 'assest_free': -45.0, 'assest_fix': 45.542890293975226, 'profit': 0, 'cur_profit': 0.012064228755004989}, 'bid': {'price': '4.5', 'code': '000001.SZ', 'amount': '10.0', 'time': '2000-01-17', 'towards': '1'}, 'market': {'open': 4.508947656317237, 'high': 4.559326959739777, 'low': 4.40818904947216, 'close': 4.5542890293975224, 'volume': 3450100.0, 'code': '000001'}, 'time': datetime.datetime(2017, 4, 12, 14, 50, 3, 717428), 'date_stamp': '1491979803.717428'}}
===at the end of strategy===

"""