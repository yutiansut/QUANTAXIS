# coding=utf-8
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

import csv
import datetime
import json
import os
import random
import re
import sys
import time

import pymongo
from tabulate import tabulate

import configparser
from QUANTAXIS import *
from QUANTAXIS import QA_Market, QA_Portfolio, QA_QAMarket_bid, QA_Risk
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_start
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_index_day, QA_fetch_stock_day,
                                       QA_fetch_stock_info,
                                       QA_fetch_stocklist_day,
                                       QA_fetch_trade_date)
from QUANTAXIS.QASU.save_backtest import (QA_SU_save_account_message,
                                          QA_SU_save_account_to_csv)
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_get_real_date,
                              QA_util_log_info)


class QA_Backtest():

    account = QA_Account()
    market = QA_Market()
    bid = QA_QAMarket_bid()
    setting = QA_Setting()
    clients = setting.client
    user = setting.QA_setting_user_name

    """
    backtest 类不应该只是一个简单的构造函数,他应该包含一个回测框架常用的方法和一些定制化的需求实现
    @yutiansut
    2017/6/19


    需要做一个内部的setting表,以dict格式,value是函数名
    @yutiansut
    2017/6/27
    """

    def QA_backtest_load_strategy(self,):
        __f_strategy_path = self.__backtest_setting['strategy']['file_path']
        __f_strategy_path = __f_strategy_path.split(':')
        if __f_strategy_path[0] == 'file' and __f_strategy_path[1] == 'py':
            if __f_strategy_path[2] == 'local':

                __current_dir = os.getcwd()
                try:
                    if os.path.exists(os.path.exists(
                            str(__current_dir) + '\\backtest_strategy.py')):
                        __file_path = os.path.exists(
                            str(__current_dir) + '\\backtest_strategy.py')

                except:
                    return "wrong with strategy file in current dir"

            elif os.path.exists(__f_strategy_path[2]):
                __file_path = __f_strategy_path[2]
            else:
                QA_util_log_info('error with loading strategy file')
                sys.exit()

        try:
            import __file_path as QUANTAXIS_Strategy
            QA_util_log_info(dir(QUANTAXIS_Strategy))
        except:
            QA_util_log_info('wrong with loading strategy')

    def QA_backtest_import_setting(self, __setting_file_path='10x'):

        if __setting_file_path == '10x':
            __current_dir = os.getcwd()
            try:
                if os.path.exists(os.path.exists(str(__current_dir) + '\\backtest_setting.ini')):
                    __file_path = str(__current_dir) + '\\backtest_setting.ini'

            except:
                return "wrong with config file in current dir"

        elif os.path.exists(__setting_file_path):
            __file_path = os.path.exists(
                str(__current_dir) + '\\backtest_setting.ini')

        self.__backtest_setting = configparser.ConfigParser()
        self.__backtest_setting.read(__file_path)

    def __QA_backtest_set_stock_list(self):
        self.strategy_stock_list = []
        __t_strategy_stock_list = self.__backtest_setting['account']['stock_list']
        __t_strategy_stock_list = __t_strategy_stock_list.split(':')
        if __t_strategy_stock_list[0] == 'file':
            if __t_strategy_stock_list[1] == 'csv':
                if __t_strategy_stock_list[2] == 'local':
                    __current_dir = os.getcwd()
                    try:
                        if os.path.exists(os.path.exists(str(__current_dir) + '\\stock_list.csv')):
                            __stock_list_file_path = str(__current_dir) + \
                                '\\stock_list.csv'
                        else:
                            QA_util_log_info("wrong with csv file in current dir, \
                                    the name should be \\stock_list.csv")
                    except:
                        QA_util_log_info("wrong with csv file in current dir, \
                                    the name should be \\stock_list.csv")
                else:
                    try:
                        if os.path.exists(__t_strategy_stock_list[2]):
                            __stock_list_file_path = __t_strategy_stock_list[2]
                        else:
                            QA_util_log_info("wrong with csv file in current dir, \
                                    the name should be \\stock_list.csv")
                    except:
                        QA_util_log_info("wrong with csv file in current dir, \
                                    the name should be \\stock_list.csv")
                with open(__stock_list_file_path, 'r') as csv_file:
                    __data = csv.reader(csv_file)

                    for item in __data:
                        self.strategy_stock_list.append(item[0])
            elif __t_strategy_stock_list[1] == 'json':
                if __t_strategy_stock_list[2] == 'local':
                    __current_dir = os.getcwd()
                    try:
                        if os.path.exists(os.path.exists(str(__current_dir) + '\\stock_list.json')):
                            __stock_list_file_path = str(__current_dir) + \
                                '\\stock_list.json'

                    except:
                        return "wrong with csv file in current dir, \
                        the name should be \\stock_list.json"
                else:
                    try:
                        if os.path.exists(__t_strategy_stock_list[2]):
                            __stock_list_file_path = __t_strategy_stock_list[2]
                        else:
                            return "wrong with csv file in current dir, \
                            the name should be \\stock_list.json"
                    except:
                        return "wrong with csv file in current dir, \
                        the name should be \\stock_list.json"
        elif __t_strategy_stock_list[0] == 'mongo':
            try:
                import pymongo

                coll = pymongo.MongoClient().__t_strategy_stock_list[1].split(
                    '-')[0].__t_strategy_stock_list[1].split['-'][1]
                assert isinstance(__t_strategy_stock_list[2], str)
                return coll.find(__t_strategy_stock_list[2])
            except:
                QA_util_log_info(
                    'something wrong with import stock_list from mongodb')
        elif __t_strategy_stock_list[0] == 'data':
            if __t_strategy_stock_list[1] == 'list':
                self.strategy_stock_list = __t_strategy_stock_list[2]

    def __QA_backtest_set_bid_model(self):
        if self.__backtest_setting['bid']['bid_model'] == 'market_price':
            self.bid.bid['price'] = 'market_price'
            self.bid.bid['bid_model'] = 'auto'
        elif self.__backtest_setting['bid']['bid_model'] == 'close_price':
            self.bid.bid['price'] = 'close_price'
            self.bid.bid['bid_model'] = 'auto'
        elif self.__backtest_setting['bid']['bid_model'] == 'strategy':
            self.bid.bid['price'] = 0
            self.bid.bid['bid_model'] = 'strategy'
        else:
            QA_util_log_info('support bid model')
            sys.exit()

    def __QA_backtest_set_save_model(self):
        pass

    def QA_backtest_init(self):
        # 设置回测的开始结束时间

        try:
            self.QA_backtest_import_setting()
        except:
            sys.exit()

        self.strategy_start_date = str(
            self.__backtest_setting['backtest']['strategy_start_date'])
        self.strategy_end_date = str(
            self.__backtest_setting['backtest']['strategy_end_date'])

        # 设置回测标的,是一个list对象,不过建议只用一个标的
        # gap是回测时,每日获取数据的前推日期(交易日)
        self.strategy_gap = int(
            self.__backtest_setting['backtest']['strategy_gap'])

        # 设置全局的数据库地址,回测用户名,密码,并初始化
        self.setting.QA_util_sql_mongo_ip = str(
            self.__backtest_setting['backtest']['database_ip'])
        self.setting.QA_setting_user_name = str(
            self.__backtest_setting['backtest']['username'])
        self.setting.QA_setting_user_password = str(
            self.__backtest_setting['backtest']['password'])
        self.setting.QA_setting_init()

        # 回测的名字
        self.strategy_name = str(
            self.__backtest_setting['backtest']['strategy_name'])

       # 股票的交易日历,真实回测的交易周期,和交易周期在交易日历中的id
        self.trade_list = QA_fetch_trade_date(
            self.setting.client.quantaxis.trade_date)

        self.benchmark_code = self.__backtest_setting['backtest']['benchmark_code']
        """
        这里会涉及一个区间的问题,开始时间是要向后推,而结束时间是要向前推,1代表向后推,-1代表向前推
        """
        self.start_real_date = QA_util_get_real_date(
            self.strategy_start_date, self.trade_list, 1)
        self.start_real_id = self.trade_list.index(self.start_real_date)
        self.end_real_date = QA_util_get_real_date(
            self.strategy_end_date, self.trade_list, -1)
        self.end_real_id = self.trade_list.index(self.end_real_date)

        self.__QA_backtest_set_stock_list()

        self.account.init_assest = self.__backtest_setting['account']['account_assets']

    def QA_backtest_init_ma(self):

        self.account.init()

        # 重新初始账户资产

        # 重新初始化账户的cookie
        self.account.account_cookie = str(random.random())
        # print(self.strategy_stock_list)
        # 初始化股票池的市场数据
        self.__market_data = QA_fetch_stocklist_day(
            self.strategy_stock_list, self.setting.client.quantaxis.stock_day,
            [self.trade_list[self.start_real_id - int(self.strategy_gap)],
             self.trade_list[self.end_real_id]])

    def QA_backtest_start(self, strategy_fp):
        assert len(self.strategy_stock_list) > 0
        assert len(self.trade_list) > 0
        assert isinstance(self.start_real_date, str)
        assert isinstance(self.end_real_date, str)
        self.QA_backtest_init_ma()

        assert len(self.__market_data) == len(self.strategy_stock_list)

        QA_util_log_info('QUANTAXIS Backtest Engine Initial Successfully')
        QA_util_log_info('Basical Info: \n' + tabulate(
            [['0.3.9-gamma-dev20', str(self.strategy_name)]], headers=('Version', 'Strategy_name')))
        QA_util_log_info('Stock_List: \n' +
                         tabulate([self.strategy_stock_list]))
        self.__QA_backtest_set_bid_model()

        #self.bid.QA_bid_insert()
        self.handle_data(strategy_fp)

    def handle_data(self, strategy_fp):
        # 首先判断是否能满足回测的要求`

        __messages = {}
        self.__init_cash_per_stock = int(
            float(self.account.init_assest) / len(self.strategy_stock_list))

        print(self.account.init_assest)
        input()
        # 策略的交易日循环
        for i in range(int(self.start_real_id), int(self.end_real_id) - 1, 1):
            # 正在进行的交易日期
            __running_date = self.trade_list[i]
            QA_util_log_info(
                '=================daily hold list====================')
            QA_util_log_info('in the begining of ' + __running_date)
            QA_util_log_info(
                tabulate(self.account.message['body']['account']['hold']))
            for __j in range(0, len(self.strategy_stock_list)):
                if __running_date in [l[6] for l in self.__market_data[__j]] and \
                        [l[6] for l in self.__market_data[__j]].index(__running_date) \
                        > self.strategy_gap + 1:

                    __data = self.__QA_data_handle(
                        [__l[6] for __l in self.__market_data[__j]].index(__running_date), __j)
                    __amount = 0
                    for item in __data['account']['body']['account']['hold']:

                        if self.strategy_stock_list[__j] in item:
                            __amount = __amount + item[3]
                    if __amount > 0:
                        __hold = 1
                    else:
                        __hold = 0
                    __result = strategy_fp.predict(
                        __data['market'], __data['account'], __hold)

                    if float(self.account.message['body']['account']['cash'][-1]) > 0:

                        self.__QA_backtest_excute_bid(
                            __result, __running_date, __hold,
                            str(self.strategy_stock_list[__j])[0:6], __amount)
                    else:
                        QA_util_log_info('not enough free money')
                else:
                    pass

        # 在回测的最后一天,平掉所有仓位(回测的最后一天是不买入的)
        while len(self.account.hold) > 1:
            __hold_list = self.account.hold[1::]
            for item in __hold_list:

                __last_bid = self.bid.bid
                __last_bid['amount'] = int(item[3])
                __last_bid['order_id'] = str(random.random())
                __last_bid['price'] = 'close_price'
                __last_bid['code'] = str(item[1])
                __last_bid['date'] = self.trade_list[self.end_real_id]
                __last_bid['towards'] = -1
                __last_bid['user'] = self.setting.QA_setting_user_name
                __last_bid['strategy'] = self.strategy_name
                __last_bid['bid_model'] = 'auto'
                __last_bid['status'] = '0x01'
                __last_bid['amount_model'] = 'amount'

                __message = self.market.receive_bid(
                    __last_bid, self.setting.client)

                __messages = self.account.QA_account_receive_deal(
                    __message)

        # 开始分析
        QA_util_log_info('start analysis====\n' +
                         str(self.strategy_stock_list))
        QA_util_log_info('=' * 10 + 'Trade History' + '=' * 10)
        QA_util_log_info('\n' + tabulate(self.account.history,
                                         headers=('date', 'code', 'price', 'towards',
                                                  'amounts', 'order_id', 'trade_id', 'commission')))
        QA_util_log_info(tabulate(self.account.detail,
                                  headers=('date', 'code', 'price', 'amounts', 'order_id',
                                           'trade_id', 'sell_price', 'sell_order_id',
                                           'sell_trade_id', 'sell_date', 'left_amount',
                                           'commission')))
        __exist_time = int(self.end_real_id) - int(self.start_real_id) + 1
        self.__benchmark_data = QA_fetch_index_day(
            self.benchmark_code, self.start_real_date,
            self.end_real_date, self.setting.client.quantaxis.stock_day)

        analysis_message = QA_backtest_analysis_start(
            self.setting.client, self.strategy_stock_list, __messages,
            self.trade_list[self.start_real_id:self.end_real_id],
            self.__market_data, self.__benchmark_data)
        QA_util_log_info(json.dumps(analysis_message, indent=2))
        QA_util_log_info(json.dumps(__messages, indent=2))
        QA_SU_save_account_to_csv(__messages)
        # QA.QA_SU_save_backtest_message(analysis_message, self.setting.client)

    def __QA_backtest_excute_bid(self, __result,  __date, __hold, __code, __amount):
        self.__QA_backtest_set_bid_model()
        if self.bid.bid['bid_model'] == 'strategy':
            __bid_price = __result['price']
        else:
            __bid_price = self.bid.bid['price']

        __bid = self.bid.bid

        __bid['order_id'] = str(random.random())
        __bid['user'] = self.setting.QA_setting_user_name
        __bid['strategy'] = self.strategy_name
        __bid['code'] = __code
        __bid['date'] = __date
        __bid['price'] = __bid_price
        __bid['amount'], __bid['amount_model'] = self.__QA_bid_amount(
            __result['amount'], __amount)

        if __result['if_buy'] == 1:
            __bid['towards'] = 1
            __message = self.market.receive_bid(
                __bid, self.setting.client)

            if float(self.account.message['body']['account']['cash'][-1]) > \
                    float(__message['body']['bid']['price']) * \
                    float(__message['body']['bid']['amount']):
                pass
            else:
                __message['body']['bid']['amount'] = int(float(
                    self.account.message['body']['account']['cash'][-1]) / float(
                        __message['body']['bid']['price'] * 100)) * 100

            if __message['body']['bid']['amount'] > 0:
                self.account.QA_account_receive_deal(__message)

        elif __result['if_buy'] == 0 and __hold == 0:
            pass
        elif __result['if_buy'] == 0 and __hold == 1:
            __bid['towards'] = -1
            __message = self.market.receive_bid(
                __bid, self.setting.client)

            self.account.QA_account_receive_deal(
                __message)

    def __QA_bid_amount(self, __strategy_amount, __amount):
        if __strategy_amount == 'mean':
            return float(float(self.account.message['body']['account']['cash'][-1]) /
                         len(self.strategy_stock_list)), 'price'
        elif __strategy_amount == 'half':
            return __amount * 0.5, 'amount'
        elif __strategy_amount == 'all':
            return __amount, 'amount'

    def __QA_get_data_from_market(self, __id, stock_id):
        # x=[x[6] for x in self.__market_data]
        if __id > self.strategy_gap + 1:
            index_of_day = __id
            index_of_start = index_of_day - self.strategy_gap + 1
            return self.__market_data[stock_id][index_of_start:index_of_day + 1]

         # 从账户中更新数据

    def __QA_data_handle(self, __id, __stock_id):
        __market_data = self.__QA_get_data_from_market(__id, __stock_id)
        __message = self.account.message

        return {'market': __market_data, 'account': __message}


class QA_Backtest_min(QA_Backtest):
    pass
