# coding:utf-8
import QUANTAXIS as QA
import random
import pymongo
import datetime


# 2个地方进行了优化:
"""
1. 对于时间获取队列进行优化
2. 对于数据获取进行优化
"""


def predict(market,profit,hold,cur_profit_present,stop):
    """
    一个极其简单的示例策略,如果空仓则买入,如果有仓位就卖出
    """
    if hold==0:
        return {'if_buy':1}
    else:
        return {'if_buy':0}





class backtest(QA.QA_Backtest):
    # 继承回测类
    def init(self):
        """
        线程间参数设置,全局的
        """

        # 对账户进行初始化
        self.account = QA.QA_Account()

        # 设置回测的开始结束时间
        self.strategy_start_date = '2015-05-01'
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
        
        self.account.init()

        # 重新初始账户资产
        self.account.assets = 25000
        self.trade_history = []
        # 重新初始化账户的cookie
        self.account.account_cookie = str(random.random())

        # 初始化单个股票标的单元的市场数据
        self.market_data = QA.QA_fetch_stock_day(
            self.strategy_stock_list[0], self.setting.client.quantaxis.stock_day)

    # 从市场中获取数据(基于gap),你也可以不急于gap去自定义自己的获取数据的代码
    # 调用的数据接口是
    # data=QA.QA_fetch_data(回测标的代码,开始时间,结束时间,数据库client)

    def BT_get_data_from_market(self, id):
        # x=[x[6] for x in self.market_data]
        if id > 7:
            index_of_day = id
            index_of_start = index_of_day - self.strategy_gap + 1
            return self.market_data[index_of_start:index_of_day + 1]

         # 从账户中更新数据
    def BT_get_data_from_ARP(self):
        return self.account.QA_Account_get_message()

    def BT_data_handle(self, id):
        market_data = self.BT_get_data_from_market(id)
        message = self.BT_get_data_from_ARP()
        # print(message['body']['account']['cur_profit_present'])
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
            # 这里是判断交易日那天,测试的股票是否交易, 以及前测数据量是否满足需求
            if running_date in [l[6] for l in self.market_data] and [l[6] for l in self.market_data].index(running_date) > self.strategy_gap + 1:

                data = self.BT_data_handle(
                    [l[6] for l in self.market_data].index(running_date))

                result = predict(data['market'], data['account']['body']['account']['total_profit'], data['account']
                                 ['body']['account']['hold'], data['account']['body']['account']['cur_profit_present'] * 100, self.stop)


                if result['if_buy'] == 1 and int(data['account']['body']['account']['hold']) == 0:
                    #self.stop = [result['stop_high'], result['stop_low']]
                    self.bid.bid['amount'] = float(
                        data['account']['body']['account']['assest_free']) / float(data['market'][-1][4])
                    self.bid.bid['price'] = float(data['market'][-1][4])
                    self.bid.bid['code'] = str(
                        self.strategy_stock_list[0])[0:6]
                    self.bid.bid['time'] = data['market'][-1][6]
                    self.bid.bid['towards'] = 1
                    self.bid.bid['user'] = self.setting.QA_setting_user_name
                    self.bid.bid['strategy'] = self.strategy_name
                    message = self.market.market_make_deal(
                        self.bid.bid, self.setting.client)
                    # QA.QA_util_log_info(message)

                    message = self.account.QA_account_receive_deal(
                        message, self.setting.client)
                    self.backtest_message = message
                    # print('*'*6+'buy'+'*'*6)
                    # print(message)
                    # input()
                    # QA.QA_SU_save_account_message(message,self.setting.client)
                    self.trade_history.append(message)
                    # print('buy----------------------------------------------')
                    # QA.QA_util_log_info(message)
                    # input()
                elif result['if_buy'] == 1 and int(data['account']['body']['account']['hold']) == 1:
                    #QA.QA_util_log_info('Hold and Watch!!!!!!!!!!!!')
                    ##
                    self.bid.bid['amount'] = int(
                        data['account']['body']['account']['portfolio']['amount'])
                    self.bid.bid['price'] = 0
                    self.bid.bid['code'] = str(
                        self.strategy_stock_list[0])[0:6]
                    self.bid.bid['time'] = data['market'][-1][6]
                    self.bid.bid['towards'] = -1
                    self.bid.bid['user'] = self.setting.QA_setting_user_name
                    self.bid.bid['strategy'] = self.strategy_name
                    message = self.market.market_make_deal(
                        self.bid.bid, self.setting.client)
                    message = self.account.QA_account_receive_deal(
                        message, self.setting.client)
                    self.backtest_message = message
                    # print('*'*6+'hold'+'*'*6)
                    # print(message)
                    # input()
                   # QA.QA_SU_save_account_message(message,self.setting.client)
                    self.trade_history.append(message)
                    # todo  hold profit change
                elif result['if_buy'] == 0 and int(data['account']['body']['account']['hold']) == 0:
                    #QA.QA_util_log_info('ZERO and Watch!!!!!!!!!!!!')
                    self.bid.bid['amount'] = int(
                        data['account']['body']['account']['portfolio']['amount'])
                    self.bid.bid['price'] = 0
                    self.bid.bid['code'] = str(
                        self.strategy_stock_list[0])[0:6]
                    self.bid.bid['time'] = data['market'][-1][6]
                    self.bid.bid['towards'] = 1
                    self.bid.bid['user'] = self.setting.QA_setting_user_name
                    self.bid.bid['strategy'] = self.strategy_name
                   # print(self.bid.bid)
                    message = self.market.market_make_deal(
                        self.bid.bid, self.setting.client)
                    message = self.account.QA_account_receive_deal(
                        message, self.setting.client)
                    self.backtest_message = message
                    # print('*'*6+'zero'+'*'*6)
                    # print(message)
                    # input()
                    # QA.QA_SU_save_account_message(message,self.setting.client)
                    self.trade_history.append(message)
                elif result['if_buy'] == 0 and int(data['account']['body']['account']['hold']) == 1:
                    self.bid.bid['amount'] = int(
                        data['account']['body']['account']['portfolio']['amount'])
                    self.bid.bid['price'] = float(data['market'][-1][4])
                    self.bid.bid['code'] = str(
                        self.strategy_stock_list[0])[0:6]
                    self.bid.bid['time'] = data['market'][-1][6]
                    self.bid.bid['towards'] = -1
                    self.bid.bid['user'] = self.setting.QA_setting_user_name
                    self.bid.bid['strategy'] = self.strategy_name

                    message = self.market.market_make_deal(
                        self.bid.bid, self.setting.client)

                    # QA.QA_util_log_info(message)
                    #print('=================sell start')
                    # print(message)
                    #print('sell end==============')
                    message = self.account.QA_account_receive_deal(
                        message, self.setting.client)
                    self.trade_history.append(message)
                    self.backtest_message = message
                    # print('*'*6+'sell'+'*'*6)
                    # print(message)
                    # input()
                    # QA.QA_SU_save_account_message(message,self.setting.client)
                   # print('sell----------------------------------------------')
                    # QA.QA_util_log_info(message)
                    # input()
                    # print(message)
                    # QA.QA_SU_save_account_message(message,self.setting.client)

        # 性能分析
            else:
                pass

        # 把这个协议发送给分析引擎,进行分析
        # 只有当交易历史大于1,才有存储的价值
        if len(self.trade_history) > 1:
            try:
                QA.QA_util_log_info('start analysis===='+str(self.strategy_stock_list[0]))
                exist_time = int(self.end_real_id) - int(self.start_real_id) + 1
                QA.QA_SU_save_account_message_many(
                    self.trade_history, self.setting.client)
                #print(self.trade_history[-1])

                performace = QA.QABacktest.QAAnalysis.QA_backtest_analysis_start(
                    self.setting.client, self.backtest_message, exist_time)
                #print(performace)

                backtest_mes = {
                    'user': self.setting.QA_setting_user_name,
                    'strategy': self.strategy_name,
                    'stock_list': self.strategy_stock_list,
                    'start_time': self.strategy_start_date, 
                    'end_time': self.strategy_end_date,
                    'account_cookie': self.account.account_cookie,
                    'total_returns': self.backtest_message['body']['account']['profit'],
                    'annualized_returns': performace['annualized_returns'],
                    'benchmark_annualized_returns': performace['benchmark_annualized_returns'],
                    'benchmark_assest': performace['benchmark_assest'],
                    'trade_date': performace['trade_date'],
                    'total_date': performace['total_date'],
                    'win_rate': performace['win_rate'],
                    'alpha': performace['alpha'],
                    'beta': performace['beta'],
                    'sharpe': performace['sharpe'],
                    'vol': performace['vol'],
                    'benchmark_vol': performace['benchmark_vol'],
                    'max_drop': performace['max_drop'],
                    'exist': exist_time
                }

                # 策略的汇总存储(会存在backtest_info下)
                QA.QA_SU_save_backtest_message(backtest_mes, self.setting.client)
                #self.setting.client.close()
            except:
                QA.QA_util_log_info(self.strategy_stock_list[0])
                QA.QA_util_log_info('wrong')


if __name__=='__main__':

    stock_lists = pymongo.MongoClient().quantaxis.stock_list.find_one()
    stock_list = stock_lists['stock']['code']

    BT = backtest()
    BT.init()
    def start_unit(item):
        ti1 = datetime.datetime.now().timestamp()
        BT.strategy_stock_list = [item]
        BT.init_stock()
        BT.handle_data()

        QA.QA_util_log_info(
            float(datetime.datetime.now().timestamp()) - float(ti1))

    for item in stock_list:
        start_unit(item)

