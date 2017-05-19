#coding:utf-8
import QUANTAXIS as QA
import random
import pymongo
import datetime,time

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from six.moves import queue
import threading

time1=datetime.datetime.now().timestamp()
class backtest(QA.QA_Backtest):
    #对回测过程进行初始化
    def init(self):
        #对账户进行初始化
        self.account=QA.QA_Account()
        #设置初始账户资产
        self.account.assets=100000
        #设置回测的开始结束时间
        self.strategy_start_date='2015-05-01'
        self.strategy_end_date='2017-04-01'
        #设置回测标的,是一个list对象,不过建议只用一个标的
        self.strategy_stock_list=['600592.SZ']
        #gap是回测时,每日获取数据的前推日期(交易日)
        self.strategy_gap=90
        #初始化一个cookie
        self.account.account_cookie=str(random.random())
        #设置全局的数据库地址,回测用户名,密码
        self.setting.QA_util_sql_mongo_ip='127.0.0.1'
        self.setting.QA_setting_user_name='admin'
        self.setting.QA_setting_user_password='admin'
        #回测的名字
        self.strategy_name='test-simple'
        #进行全局初始化和账户初始化
        self.setting.QA_setting_init()
        self.account.init()
        #print(self.account.history_trade)
        #input()
        #在log中记录数据库信息
       # QA.QA_util_log_info(self.setting.client)
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
        i=2
        while len(data)<self.strategy_gap:

            #print(-int(self.strategy_gap)*2+len(data))
            start=self.coll.find_one({'num':int(id)-int(self.strategy_gap)*i+len(data)+1})

            start_date=str(start['date'])[0:10]
            #print(self.strategy_gap)
            
            #print(start_date)
            data=QA.QA_fetch_data(self.strategy_stock_list[0],start_date,end_date,self.coll2)
            #print(len(data))
            i=i+1
            #input()
        if len(data)>self.strategy_gap:
            data=data[len(data)-self.strategy_gap:]
        #print('end')
        #print(len(data))
        #input()
        return data
     #从账户中更新数据
    def BT_get_data_from_ARP(self):
        return self.account.QA_Account_get_message()
    def BT_data_handle(self,id):
        market_data=self.BT_get_data_from_market(id)
        message=self.BT_get_data_from_ARP()
        #print(message['body']['account']['cur_profit_present'])
        return {'market':market_data,'account':message}
    #把从账户,市场的数据组合起来,你也可以自定义自己的指标,数据源,以dict的形式插入进来  
    #策略开始
    def handle_data(self):
        backtest_history=[]
        #QA.QA_util_log_info(self.account.message['body'])
        #策略的交易日循环
        for i in range(int(self.start_mes['id']),int(self.end_mes['id']),1):
            #QA.QA_util_log_info('===day start===')
            running_date=QA.QA_util_id2date(i,self.setting.client)
            #QA.QA_util_log_info(running_date)
            is_trade=QA.QA_util_is_trade(running_date,self.strategy_stock_list[0],self.setting.client)
            if is_trade==False:
                #QA.QA_util_log_info('停牌中')
                pass
            else:
                data=self.BT_data_handle(i)
            

                result=predict(data['market'],data['account']['body']['account']['profit']*100,data['account']['body']['account']['hold'],data['account']['body']['account']['cur_profit_present']*100)
                # print(result)

               # print(data['account']['body']['account']['hold'])
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
                   # QA.QA_util_log_info(message)
                    
                    message=self.account.QA_account_receive_deal(message,self.setting.client)
                    self.backtest_message=message
                    backtest_history.append(message)
                  #  QA.QA_SU_save_account_message(message,self.setting.client)
                    #print('buy----------------------------------------------')
                    #QA.QA_util_log_info(message)
                    #input()
                elif result==1 and int(data['account']['body']['account']['hold'])==1:
                    #QA.QA_util_log_info('Hold and Watch!!!!!!!!!!!!')
                    ##
                    self.bid.bid['amount']=int(data['account']['body']['account']['portfolio']['amount'])
                    self.bid.bid['price']=0
                    self.bid.bid['code']=str(self.strategy_stock_list[0])[0:6]
                    self.bid.bid['time']=data['market'][-1][6]
                    self.bid.bid['towards']=-1
                    self.bid.bid['user']=self.setting.QA_setting_user_name
                    self.bid.bid['strategy']=self.strategy_name
                    message=self.market.market_make_deal(self.bid.bid,self.setting.client)
                    message=self.account.QA_account_receive_deal(message,self.setting.client)
                    self.backtest_message=message
                    backtest_history.append(message)
                  #  QA.QA_SU_save_account_message(message,self.setting.client)

                    # todo  hold profit change
                elif result==0 and int(data['account']['body']['account']['hold'])==0:
                   # QA.QA_util_log_info('ZERO and Watch!!!!!!!!!!!!')
                    self.bid.bid['amount']=int(data['account']['body']['account']['portfolio']['amount'])
                    self.bid.bid['price']=0
                    self.bid.bid['code']=str(self.strategy_stock_list[0])[0:6]
                    self.bid.bid['time']=data['market'][-1][6]
                    self.bid.bid['towards']=1
                    self.bid.bid['user']=self.setting.QA_setting_user_name
                    self.bid.bid['strategy']=self.strategy_name
                    message=self.market.market_make_deal(self.bid.bid,self.setting.client)
                    message=self.account.QA_account_receive_deal(message,self.setting.client)
                    self.backtest_message=message
                    backtest_history.append(message)
                    #QA.QA_SU_save_account_message(message,self.setting.client)
                elif result==0 and int(data['account']['body']['account']['hold'])==1:
                    self.bid.bid['amount']=int(data['account']['body']['account']['portfolio']['amount'])
                    self.bid.bid['price']=float(data['market'][-1][4])
                    self.bid.bid['code']=str(self.strategy_stock_list[0])[0:6]
                    self.bid.bid['time']=data['market'][-1][6]
                    self.bid.bid['towards']=-1
                    self.bid.bid['user']=self.setting.QA_setting_user_name
                    self.bid.bid['strategy']=self.strategy_name

                    message=self.market.market_make_deal(self.bid.bid,self.setting.client)

                   # QA.QA_util_log_info(message)
                    #print('=================sell start')
                   # print(message)
                   # print('sell end==============')
                    message=self.account.QA_account_receive_deal(message,self.setting.client)
                    backtest_history.append(message)
                    self.backtest_message=message
                   # QA.QA_SU_save_account_message(message,self.setting.client)
                    #print('sell----------------------------------------------')
                    #QA.QA_util_log_info(message) 
                    #input()
                    #print(message)
                    #QA.QA_SU_save_account_message(message,self.setting.client)
                    #self.backtest_message=message
                # input()
                else:print('not enough data')
        
        try:
        # 性能分析

            exist_time=int(self.end_mes['id'])-int(self.start_mes['id'])+1
            #print(self.backtest_message)
            #把这个协议发送给分析引擎,进行分析
            QA.QA_SU_save_account_message_many(backtest_history,self.setting.client)
            performace=QA.QABacktest.QAAnalysis.QA_backtest_analysis_start(self.setting.client,self.backtest_message,exist_time)
            backtest_mes={
                'user':self.setting.QA_setting_user_name,
                'strategy':self.strategy_name,
                'stock_list': self.strategy_stock_list,
                'start_time':self.strategy_start_date,
                'end_time':self.strategy_end_date,
                'account_cookie':self.account.account_cookie,
                'total_returns':self.backtest_message['body']['account']['profit'],
                'annualized_returns':performace['annualized_returns'],
                'benchmark_annualized_returns':performace['benchmark_annualized_returns'],
                'benchmark_assest':performace['benchmark_assest'],
                'trade_date':performace['trade_date'],
                'total_date':performace['total_date'],
                'win_rate':performace['win_rate'],
                'alpha':performace['alpha'],
                'beta':performace['beta'],
                'sharpe':performace['sharpe'],
                'vol':performace['vol'],
                'benchmark_vol':performace['benchmark_vol'],
                'max_drop':performace['max_drop'],
                'exist':exist_time
            }

            # 策略的汇总存储(会存在backtest_info下)
            QA.QA_SU_save_backtest_message(backtest_mes,self.setting.client)
        except:
            QA.QA_util_log_expection('wrong with performance')

#这里就是我们的假策略,你也可以从外部引入
def predict(market,account_profit,if_hold,profit_per_trade):
    #简单的策略 示例就是如果持有就买入,空仓就卖出
    if if_hold==0:
        return 1
    else:
        return 0




if __name__ == '__main__':
    stock_list=['600592','600538','603588','000001','000002','601801','600613','002138','600010']
    #stock_list=['600538','603588','600613']

    """
    for item in stock_list:
        try:
                
            BT=backtest()
            BT.init()
            BT.strategy_stock_list=[item]
            BT.handle_data()
        except:
            pass

    """
    #pool=Pool(2)
    pool = ThreadPool(4) # Sets the pool size to 4
    def start_unit(item):

        try:
            BT=backtest()
            BT.init()
            BT.strategy_stock_list=[item]
            BT.handle_data()
        except:
            #QA.QA_util_log_expection('wrong')
        # QA.QA_util_log_expection('item')
            pass
    
    pool.map(start_unit,stock_list)
    pool.close()
    pool.join()
    time2=datetime.datetime.now().timestamp()
    time_x=float(time2)-float(time1)

    print(time_x)