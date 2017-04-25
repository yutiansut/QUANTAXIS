#coding:utf-8

#首先引入QUANTAXIS
import QUANTAXIS as QA
#引入random模块是为了如果用到多账户的时候的初始化
import random
#import (你的策略)

#继承QUANTAXIS的backtest类,backtest会自带account类,market(报价对象,撮合类),setting类(全局设置,局域网数据库,回测账户等等)
class backtest(QA.QA_Backtest):
    #对回测过程进行初始化
    def init(self):
        #对账户进行初始化
        self.account=QA.QA_Account()
        #设置初始账户资产
        self.account.assets=10000
        #初始化一个cookie
        self.account.account_cookie=str(random.random())
        #设置回测的开始结束时间
        self.strategy_start_date='2015-01-10'
        self.strategy_end_date='2017-1-28'
        #设置回测标的,是一个list对象,不过建议只用一个标的
        self.strategy_stock_list=['600592.SZ']
        #gap是回测时,每日获取数据的前推日期(交易日)
        self.strategy_gap=90

        #设置全局的数据库地址,回测用户名,密码
        self.setting.QA_util_sql_mongo_ip='127.0.0.1'
        self.setting.QA_setting_user_name='admin'
        self.setting.QA_setting_user_password='admin'
        #回测的名字
        self.strategy_name='Test-strategy'

        #进行全局初始化和账户初始化
        self.setting.QA_setting_init()
        self.account.init()
       
        #input()
        #在log中记录数据库信息
        QA.QA_util_log_info(self.setting.client)
        #根据回测设置计算真实交易的开始和结束时间
        self.start_mes=QA.QA_util_realtime(self.strategy_start_date,self.setting.client)
        self.end_mes=QA.QA_util_realtime(self.strategy_end_date,self.setting.client)


    #从市场中获取数据(基于gap),你也可以不急于gap去自定义自己的获取数据的代码
    #调用的数据接口是
    #data=QA.QA_fetch_data(回测标的代码,开始时间,结束时间,数据库client)
    def BT_get_data_from_market(self,id):
        self.coll=self.setting.client.quantaxis.trade_date
        start=self.coll.find_one({'num':int(id)-int(self.strategy_gap)})
        end=self.coll.find_one({'num':int(id)})
        start_date=str(start['date'])[0:10]
        end_date=str(end['date'])[0:10]
        self.coll2=self.setting.client.quantaxis.stock_day
        data=QA.QA_fetch_data(self.strategy_stock_list[0],start_date,end_date,self.coll2)
        return data
    #从账户中更新数据
    def BT_get_data_from_ARP(self):
        return self.account.QA_Account_get_message()

    #把从账户,市场的数据组合起来,你也可以自定义自己的指标,数据源,以dict的形式插入进来    
    def BT_data_handle(self,id):
        market_data=self.BT_get_data_from_market(id)
        message=self.BT_get_data_from_ARP()
        #print(message['body']['account']['cur_profit_present'])
        return {'market':market_data,'account':message}

    #策略开始
    def handle_data(self):
        QA.QA_util_log_info(self.account.message['body'])
        #策略的交易日循环
        for i in range(int(self.start_mes['id']),int(self.end_mes['id']),1):
            QA.QA_util_log_info('===day start===')
            #从组合出来的数据中拿数据
            data=self.BT_data_handle(i)
            #print(data)
            #print(data['market'])
            #print(data['account']['body']['account']['profit'])
            #print(data['account']['body']['account']['hold'])
            #print(data['account']['body']['account']['cur_profit_present'])
            #print(data['market'][-1][6])



            # 这里是你的策略,你的策略拿到数据后进行买卖判断,再返还回来(示例代码只是返还买卖与否,你可以将其改造成dict格式,返还买卖点等
            # 如 
            # result={
            #    'ifbuy':1,
            #    'price'=9.2,
            #    'amount'=10000
            # }
            result=predict(data['market'],data['account']['body']['account']['profit']*100,data['account']['body']['account']['hold'],data['account']['body']['account']['cur_profit_present']*100)
            # print(result)


            # 以下都是基于策略返还回来的结果,进行报价准备
            print(data['account']['body']['account']['hold'])
            if result==1 and int(data['account']['body']['account']['hold'])==0:
                #print(data['account']['body']['account']['assest_free'])
                #print(data['market'][-1][4])
                #self.bid.bid['amount']=int(float(data['account']['body']['account']['assest_free'])/float(data['market'][-1][4]))


                #报价准备
                self.bid.bid['amount']=float(data['account']['body']['account']['assest_free'])/float(data['market'][-1][4])
                #self.bid.bid['amount']=1000
                #print(self.bid.bid['amount'])
                self.bid.bid['price']=float(data['market'][-1][4])
                self.bid.bid['code']=str(self.strategy_stock_list[0])[0:6]
                self.bid.bid['time']=data['market'][-1][6]
                self.bid.bid['towards']=1
                self.bid.bid['user']=self.setting.QA_setting_user_name
                self.bid.bid['strategy']=self.strategy_name


                #报价被发送到市场撮合引擎,撮合引擎会返还一个协议格式,具体参见QASprotocol
                message=self.market.market_make_deal(self.bid.bid,self.setting.client)
                #直接把这个返回的协议发送给账户,进行处理,账户也会返还一个协议格式,具体参见QASprotocol
                message=self.account.QA_account_receive_deal(message,self.setting.client)
                self.backtest_message=message

                #存贮判断
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

        #把这个协议发送给分析引擎,进行分析
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
        # 策略的汇总存储(会存在backtest_info下)
        QA.QA_SU_save_backtest_message(backtest_mes,self.setting.client)


#这里就是我们的假策略,你也可以从外部引入
def predict(market,account_profit,if_hold,profit_per_trade):
    #简单的策略 示例就是如果持有就买入,空仓就卖出
    if if_hold==0:
        return 1
    else:
        return 0



#这里是外部定义的回测标的列表
stock_list=['600592']
# 可以是多个股票,也可以从数据库拿
for item in stock_list:
    #调用刚才写好的回测框架    
    BT=backtest()
    #进行初始化
    BT.init()
    #修改回测标的
    BT.strategy_stock_list=[item]
    #运行策略
    BT.handle_data()
