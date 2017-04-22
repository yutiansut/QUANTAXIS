#coding:utf-8
import QUANTAXIS as QA
import random
import pymongo
class backtest(QA.QA_Backtest):
    def init(self):
        self.account=QA.QA_Account()
        self.account.assets=10000
        self.strategy_start_date='2015-01-10'
        self.strategy_end_date='2017-1-28'
        self.strategy_stock_list=['600592.SZ']
        self.strategy_gap=90
        self.account.account_cookie=str(random.random())
        self.setting.QA_util_sql_mongo_ip='127.0.0.1'
        self.setting.QA_setting_user_name='admin'
        self.setting.QA_setting_user_password='admin'
        self.strategy_name='Test-strategy'
        self.setting.QA_setting_init()
        self.account.init()
        print(self.account.history_trade)
        #input()
        QA.QA_util_log_info(self.setting.client)
        self.start_mes=QA.QA_util_realtime(self.strategy_start_date,self.setting.client)
        self.end_mes=QA.QA_util_realtime(self.strategy_end_date,self.setting.client)

    def BT_get_data_from_market(self,id):
        self.coll=self.setting.client.quantaxis.trade_date
        start=self.coll.find_one({'num':int(id)-int(self.strategy_gap)})
        end=self.coll.find_one({'num':int(id)})
        start_date=str(start['date'])[0:10]
        end_date=str(end['date'])[0:10]
        self.coll2=self.setting.client.quantaxis.stock_day
        data=QA.QA_fetch_data(self.strategy_stock_list[0],start_date,end_date,self.coll2)
        return data
    def BT_get_data_from_ARP(self):
        return self.account.QA_Account_get_message()
    def BT_data_handle(self,id):
        market_data=self.BT_get_data_from_market(id)
        message=self.BT_get_data_from_ARP()
        #print(message['body']['account']['cur_profit_present'])
        return {'market':market_data,'account':message}
    def handle_data(self):
        QA.QA_util_log_info(self.account.message['body'])
        for i in range(int(self.start_mes['id']),int(self.end_mes['id']),1):
            QA.QA_util_log_info('===day start===')
            data=self.BT_data_handle(i)
            #print(data)
            #print(data['market'])
            #print(data['account']['body']['account']['profit'])
            #print(data['account']['body']['account']['hold'])
            #print(data['account']['body']['account']['cur_profit_present'])
            #print(data['market'][-1][6])
            
            result=predict(data['market'],data['account']['body']['account']['profit']*100,data['account']['body']['account']['hold'],data['account']['body']['account']['cur_profit_present']*100)
            # print(result)

            print(data['account']['body']['account']['hold'])
            if result==1 and int(data['account']['body']['account']['hold'])==0:
                #print(data['account']['body']['account']['assest_free'])
                #print(data['market'][-1][4])
                #self.bid.bid['amount']=int(float(data['account']['body']['account']['assest_free'])/float(data['market'][-1][4]))
                self.bid.bid['amount']=float(data['account']['body']['account']['assest_free'])/float(data['market'][-1][4])
                #self.bid.bid['amount']=1000
                #print(self.bid.bid['amount'])
                self.bid.bid['price']=float(data['market'][-1][4])
                self.bid.bid['code']=str(self.strategy_stock_list[0])[0:6]
                self.bid.bid['time']=data['market'][-1][6]
                self.bid.bid['towards']=1
                self.bid.bid['user']=self.setting.QA_setting_user_name
                self.bid.bid['strategy']=self.strategy_name
                message=self.market.market_make_deal(self.bid.bid,self.setting.client)
                message=self.account.QA_account_receive_deal(message,self.setting.client)
                self.backtest_message=message
                QA.QA_SU_save_account_message(message,self.setting.client)
                #print('buy----------------------------------------------')
                #QA.QA_util_log_info(message)
                #input()
            elif result==1 and int(data['account']['body']['account']['hold'])==1:
                QA.QA_util_log_info('Hold and Watch!!!!!!!!!!!!')
                ##
                self.bid.bid['amount']=int(data['account']['body']['account']['portfolio']['amount'])
                self.bid.bid['price']=0
                self.bid.bid['code']=str(self.strategy_stock_list[0])[0:6]
                self.bid.bid['time']=data['market'][-1][6]
                self.bid.bid['towards']=1
                self.bid.bid['user']=self.setting.QA_setting_user_name
                self.bid.bid['strategy']=self.strategy_name
                message=self.market.market_make_deal(self.bid.bid,self.setting.client)
                message=self.account.QA_account_receive_deal(message,self.setting.client)

                # todo  hold profit change
            elif result==0 and int(data['account']['body']['account']['hold'])==0:
                QA.QA_util_log_info('ZERO and Watch!!!!!!!!!!!!')
            elif result==0 and int(data['account']['body']['account']['hold'])==1:
                self.bid.bid['amount']=int(data['account']['body']['account']['portfolio']['amount'])
                self.bid.bid['price']=float(data['market'][-1][4])
                self.bid.bid['code']=str(self.strategy_stock_list[0])[0:6]
                self.bid.bid['time']=data['market'][-1][6]
                self.bid.bid['towards']=-1
                self.bid.bid['user']=self.setting.QA_setting_user_name
                self.bid.bid['strategy']=self.strategy_name

                message=self.market.market_make_deal(self.bid.bid,self.setting.client)
                print('=================sell start')
                print(message)
                print('sell end==============')
                message=self.account.QA_account_receive_deal(message,self.setting.client)
                self.backtest_message=message
                QA.QA_SU_save_account_message(message,self.setting.client)
                #print('sell----------------------------------------------')
                #QA.QA_util_log_info(message) 
                #input()
                #print(message)
                #QA.QA_SU_save_account_message(message,self.setting.client)
                #self.backtest_message=message
               # input()
            else:print('not enough data')
        
        # 性能分析
        exist_time=int(self.end_mes['id'])-int(self.start_mes['id'])+1
        print(self.backtest_message)
        performace=QA.QABacktest.QAAnalysis.QA_backtest_analysis_start(self.backtest_message,exist_time)
        backtest_mes={
            'user':self.setting.QA_setting_user_name,
            'strategy':self.strategy_name,
            'stock_list': self.strategy_stock_list,
            'start_time':self.strategy_start_date,
            'end_time':self.strategy_end_date,
            'account_cookie':self.account.account_cookie,
            'profit':self.backtest_message['body']['account']['profit'],
            'performance':performace,
            'exist':exist_time
        }
        # 策略的汇总存储
        QA.QA_SU_save_backtest_message(backtest_mes,self.setting.client)



def predict(market,account_profit,if_hold,profit_per_trade):
    #简单的策略 示例就是如果持有就买入,空仓就卖出
    if if_hold==0:
        return 1
    else:
        return 0


stock_list=['600592']
# 可以是多个股票,也可以从数据库拿
for item in stock_list:
        
    BT=backtest()
    BT.init()
    BT.strategy_stock_list=[item]
    BT.handle_data()
