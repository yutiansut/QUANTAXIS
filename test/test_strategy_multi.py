# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import datetime
import json
import os
import pprint
import random
import sys

import pymongo
from tabulate import tabulate

import QUANTAXIS as QA


#from strategy import predict

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

        # 设置回测的开始结束时间
        self.strategy_start_date = '2017-03-01'
        self.strategy_end_date = '2017-03-11'

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
            self.setting.client.quantaxis.trade_date)
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
        self.account.init_assest = 2500000
        self.account.init()

        # 重新初始账户资产

        # 重新初始化账户的cookie
        self.account.account_cookie = str(random.random())
        # print(self.strategy_stock_list)
        # 初始化股票池的市场数据
        self.market_data = QA.QA_fetch_stocklist_day(
            self.strategy_stock_list, self.setting.client.quantaxis.stock_day, [self.trade_list[self.start_real_id - self.strategy_gap], self.trade_list[self.end_real_id]])
        # print(self.market_data)
    # 从市场中获取数据(基于gap),你也可以不急于gap去自定义自己的获取数据的代码
    # 调用的数据接口是
    # __data=QA.QA_fetch_data(回测标的代码,开始时间,结束时间,数据库client)

    def BT_get_data_from_market(self, id, stock_id):
        # x=[x[6] for x in self.market_data]
        if id > 7:
            index_of_day = id
            index_of_start = index_of_day - self.strategy_gap + 1
            return self.market_data[stock_id][index_of_start:index_of_day + 1]

         # 从账户中更新数据

    def BT_data_handle(self, id, stock_id):
        market_data = self.BT_get_data_from_market(id, stock_id)
        message = self.account.message

        return {'market': market_data, 'account': message}
    # 把从账户,市场的数据组合起来,你也可以自定义自己的指标,数据源,以dict的形式插入进来
    # 策略开始

    def handle_data(self):
        # 首先判断是否能满足回测的要求

        self.stop = [0, 0]
        # 策略的交易日循环
        for i in range(int(self.start_real_id), int(self.end_real_id) - 1, 1):
            # 正在进行的交易日期
            __running_date = self.trade_list[i]
            print('=================daily hold list====================')
            print('in the begining of ' + __running_date)
            print(tabulate(self.account.message['body']['account']['hold']))

            for __j in range(0, len(self.strategy_stock_list)):
                if __running_date in [l[6] for l in self.market_data[__j]] and \
                        [l[6] for l in self.market_data[__j]].index(__running_date) > self.strategy_gap + 1:

                    __data = self.BT_data_handle(
                        [__l[6] for __l in self.market_data[__j]].index(__running_date), __j)
                    __amount = 0
                    for item in __data['account']['body']['account']['hold']:

                        if self.strategy_stock_list[__j] in item:
                            __amount = __amount + item[3]
                    if __amount > 0:
                        __hold = 1
                    else:
                        __hold = 0

                    __result = predict(__data['market'], __hold)
                    if __result['if_buy'] == 1:
                        self.bid.bid['amount'] = int((
                            float(self.account.cash[-1]) / float(__data['market'][-1][4])) / 1000) * 100
                        self.bid.bid['price'] = str('market_price')
                        self.bid.bid['code'] = str(
                            self.strategy_stock_list[__j])[0:6]
                        self.bid.bid['date'] = __data['market'][-1][6]
                        self.bid.bid['towards'] = 1
                        self.bid.bid['order_id'] = str(random.random())
                        self.bid.bid['user'] = self.setting.QA_setting_user_name
                        self.bid.bid['strategy'] = self.strategy_name
                        __message = self.market.receive_bid(
                            self.bid.bid, self.setting.client)
                        # print(__message)
                        __messages = self.account.QA_account_receive_deal(
                            __message)
                    elif __result['if_buy'] == 0 and __hold == 0:
                        pass
                    elif __result['if_buy'] == 0 and __hold == 1:
                        self.bid.bid['amount'] = int(__amount)
                        self.bid.bid['order_id'] = str(random.random())
                        self.bid.bid['price'] = 'market_price'
                        self.bid.bid['code'] = str(
                            self.strategy_stock_list[__j])[0:6]
                        self.bid.bid['date'] = __data['market'][-1][6]
                        self.bid.bid['towards'] = -1
                        self.bid.bid['user'] = self.setting.QA_setting_user_name
                        self.bid.bid['strategy'] = self.strategy_name
                        __message = self.market.receive_bid(
                            self.bid.bid, self.setting.client)
                        __messages = self.account.QA_account_receive_deal(
                            __message)

                else:
                    pass

        print('=================daily hold list====================')
        print('in the begining of ' + self.trade_list[self.end_real_id])
        print(tabulate(self.account.message['body']['account']['hold']))

        # 在回测的最后一天,平掉所有仓位(回测的最后一天是不买入的)
        while len(self.account.hold) > 1:
            __hold_list = self.account.hold[1::]

            for item in __hold_list:
                self.bid.bid['amount'] = int(item[3])
                self.bid.bid['order_id'] = str(random.random())
                self.bid.bid['price'] = 'market_price'
                self.bid.bid['code'] = str(item[1])
                self.bid.bid['date'] = self.trade_list[self.end_real_id]
                self.bid.bid['towards'] = -1
                self.bid.bid['user'] = self.setting.QA_setting_user_name
                self.bid.bid['strategy'] = self.strategy_name
                __message = self.market.receive_bid(
                    self.bid.bid, self.setting.client)

                __messages = self.account.QA_account_receive_deal(
                    __message)

        # 开始分析
        QA.QA_util_log_info('start analysis====' +
                            str(self.strategy_stock_list))
        QA.QA_util_log_info('=' * 10 + 'Trade History' + '=' * 10)
        QA.QA_util_log_info(tabulate(self.account.history, headers=('date', 'code',
                                                      'price', 'towards', 'amounts', 'order_id', 'trade_id','commission')))
        QA.QA_util_log_info('start analysis====' +
                            str(self.strategy_stock_list))
        QA.QA_util_log_info(tabulate(self.account.detail, headers=('date', 'code', 'price',
                                                                   'amounts', 'order_id', 'trade_id', 'sell_price', 'sell_order_id', 'sell_trade_id','sell_date','left_amount','commission')))
        __exist_time = int(self.end_real_id) - int(self.start_real_id) + 1
        self.benchmark_data = QA.QA_fetch_index_day(
            'hs300', self.start_real_date, self.end_real_date)
        # print(json.dumps(messages,indent=2))
        # QA.QA_SU_save_account_message(
        # messages, self.setting.client)
        analysis_message = QA.QA_backtest_analysis_start(
            self.setting.client, self.strategy_stock_list, __messages, self.trade_list[self.start_real_id:self.end_real_id], self.market_data, self.benchmark_data)
        QA.QA_util_log_info(json.dumps(analysis_message, indent=2))
        QA.QA_util_log_info(json.dumps(__messages, indent=2))
        #QA.QA_SU_save_backtest_message(analysis_message, self.setting.client)


def predict(market, hold):
    """
    一个极其简单的示例策略,随机 随机真的随机
    """
    if hold == 0:
        __dat = random.random()
        if __dat > 0.5:

            return {'if_buy': 1}
        else:
            return {'if_buy': 0}
    else:
        __dat = random.random()
        if __dat > 0.5:
            return {'if_buy': 1}
        else:
            return {'if_buy': 0}


__stock_lists = pymongo.MongoClient(
    '192.168.4.189', 27017).quantaxis.stock_list.find_one()
__stock_list = __stock_lists['stock']['code'][0:3]

BT = backtest()
BT.init()

BT.strategy_stock_list = __stock_list
BT.init_stock()
BT.handle_data()
