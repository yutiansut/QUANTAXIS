# coding:utf-8
import QUANTAXIS as QA
import random
import pymongo
import datetime
from strategy import predict

# 2个地方进行了优化:
"""
1. 对于时间获取队列进行优化
2. 对于数据获取进行优化
"""


class backtest(QA.QA_Backtest):
    # 继承回测类
    def init(self):
        """
        线程间参数设置,全局的
        """

        # 对账户进行初始化
        self.account = QA.QA_Account()

        # 设置回测的开始结束时间
        self.strategy_start_date = '2017-03-01'
        self.strategy_end_date = '2017-05-01'

        # 设置回测标的,是一个list对象,不过建议只用一个标的
        self.strategy_stock_list = ['603588.SZ']

        # gap是回测时,每日获取数据的前推日期(交易日)
        self.strategy_gap = 6

        # 设置全局的数据库地址,回测用户名,密码,并初始化
        self.setting.QA_util_sql_mongo_ip = '127.0.0.1'
        self.setting.QA_setting_user_name = 'admin'
        self.setting.QA_setting_user_password = 'admin'
        self.setting.QA_setting_init()

        # 回测的名字
        self.strategy_name = 'example-strategy'

       # 股票的交易日历,真实回测的交易周期,和交易周期在交易日历中的id
        self.trade_list = QA.QA_fetch_trade_date(
            QA.QA_Setting().client.quantaxis.trade_date)
        """
        这里会涉及一个区间的问题,开始时间是要向后推,而结束时间是要向前推,1代表向后推,-1代表向前推
        """
        self.start_real_date = QA.QA_util_get_real_date(
            self.strategy_start_date, self.trade_list, 1)
        self.start_real_id = self.trade_list.index(self.start_real_date)
        self.end_real_date = QA.QA_util_get_real_date(
            self.strategy_end_date, self.trade_list, -1)
        self.end_real_id = self.trade_list.index(self.end_real_date)
        
        


    def init_stock(self):
        """
        线程内设置,局部
        """
        # 进行账户初始化
        self.account.init_assest= 2500000
        self.account.init()

        # 重新初始账户资产
        
        # 重新初始化账户的cookie
        self.account.account_cookie = str(random.random())
        print(self.strategy_stock_list)
        # 初始化股票池的市场数据
        self.market_data = QA.QA_fetch_stocklist_day(
            self.strategy_stock_list, self.setting.client.quantaxis.stock_day,[self.trade_list[self.start_real_id-self.strategy_gap],self.trade_list[self.end_real_id]])
    # 从市场中获取数据(基于gap),你也可以不急于gap去自定义自己的获取数据的代码
    # 调用的数据接口是
    # data=QA.QA_fetch_data(回测标的代码,开始时间,结束时间,数据库client)

    def BT_get_data_from_market(self, id,stock_id):
        # x=[x[6] for x in self.market_data]
        if id > 7:
            index_of_day = id
            index_of_start = index_of_day - self.strategy_gap + 1
            return self.market_data[stock_id][index_of_start:index_of_day + 1]

         # 从账户中更新数据

    def BT_data_handle(self, id,stock_id):
        market_data = self.BT_get_data_from_market(id,stock_id)
        message = self.account.message

        return {'market': market_data, 'account': message}
    # 把从账户,市场的数据组合起来,你也可以自定义自己的指标,数据源,以dict的形式插入进来
    # 策略开始

    def handle_data(self):
        # QA.QA_util_log_info(self.account.message['body'])

        # 首先判断是否能满足回测的要求

        self.stop = [0, 0]
        # 策略的交易日循环
        for i in range(int(self.start_real_id), int(self.end_real_id), 1):
            # 正在进行的交易日期
            running_date = self.trade_list[i]
            for j in range(0,len(self.strategy_stock_list)):
                if running_date in [l[6] for l in self.market_data[j]] and [l[6] for l in self.market_data[j]].index(running_date) > self.strategy_gap + 1:

                    data = self.BT_data_handle(
                        [l[6] for l in self.market_data[j]].index(running_date),j)
                    amount=0
                    for item in data['account']['body']['account']['hold']:
                        
                        if self.strategy_stock_list[j] in  item:
                            amount=amount+item[3]
                    if amount>0:
                        hold=1
                    else : hold=0
                    
                    result = predict(data['market'],0,hold, 0,self.stop)


                    if result['if_buy'] == 1 :
                        #self.stop = [result['stop_high'], result['stop_low']]
                        
                        self.bid.bid['amount'] =250
                        self.bid.bid['price'] = float(data['market'][-1][4])
                        self.bid.bid['code'] = str(
                            self.strategy_stock_list[j])[0:6]
                        self.bid.bid['date'] = data['market'][-1][6]
                        self.bid.bid['towards'] = 1
                        self.bid.bid['user'] = self.setting.QA_setting_user_name
                        self.bid.bid['strategy'] = self.strategy_name
                        print(self.bid.bid)
                        message = self.market.market_make_deal(
                            self.bid.bid, self.setting.client)
                        messages = self.account.QA_account_receive_deal(message)

                    elif result['if_buy'] == 0 and hold == 0:
                        pass
                    elif result['if_buy'] == 0 and hold == 1:
                        self.bid.bid['amount'] = int(amount)
                        self.bid.bid['price'] = float(data['market'][-1][4])
                        self.bid.bid['code'] = str(
                            self.strategy_stock_list[j])[0:6]
                        self.bid.bid['date'] = data['market'][-1][6]
                        self.bid.bid['towards'] = -1
                        self.bid.bid['user'] = self.setting.QA_setting_user_name
                        self.bid.bid['strategy'] = self.strategy_name

                        message = self.market.market_make_deal(
                            self.bid.bid, self.setting.client)


                        messages = self.account.QA_account_receive_deal(
                            message)


           
                else:
                    pass

        # 把这个协议发送给分析引擎,进行分析
        # 只有当交易历史大于1,才有存储的价值

        QA.QA_util_log_info('start analysis===='+str(self.strategy_stock_list))
        exist_time = int(self.end_real_id) - int(self.start_real_id) + 1
        
        QA.QA_SU_save_account_message(
            messages, self.setting.client)
        print(QA.QA_backtest_analysis_start(self.setting.client,messages,self.trade_list[self.start_real_id:self.end_real_id],self.market_data))
        




stock_lists = pymongo.MongoClient().quantaxis.stock_list.find_one()
stock_list = stock_lists['stock']['code'][1:5]

BT = backtest()
BT.init()

ti1 = datetime.datetime.now().timestamp()
BT.strategy_stock_list = stock_list
BT.init_stock()
BT.handle_data()

QA.QA_util_log_info(
    float(datetime.datetime.now().timestamp()) - float(ti1))



