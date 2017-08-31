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
import apscheduler
import numpy as np
import pandas as pd
import pymongo
from QUANTAXIS import *
from QUANTAXIS import (QA_Market, QA_Portfolio, QA_QAMarket_bid, QA_Risk,
                       __version__)
from QUANTAXIS.QAMarket.QABid import QA_QAMarket_bid_list
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_start
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_index_day, QA_fetch_stock_day,
                                       QA_fetch_stock_info,
                                       QA_fetch_stocklist_day,
                                       QA_fetch_trade_date)
from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_stocklist_day_adv, QA_fetch_stock_day_adv,
                                               QA_fetch_stock_min_adv, QA_fetch_stocklist_min_adv)

from QUANTAXIS.QASU.save_backtest import (QA_SU_save_account_message,
                                          QA_SU_save_account_to_csv)
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_get_real_date, trade_date_sse,
                              QA_util_log_info, QA_util_log_expection)
from QUANTAXIS.QAData import QA_DataStruct_Stock_min,QA_DataStruct_Stock_day
from QUANTAXIS.QATask import QA_Queue

from tabulate import tabulate

import configparser
import queue
from functools import wraps, update_wrapper, reduce


class QA_Backtest():
    '最终目的还是实现一个通用的回测类'
    backtest_type = 'day'
    account = QA_Account()
    market = QA_Market()
    bid = QA_QAMarket_bid()
    order = QA_QAMarket_bid_list()
    setting = QA_Setting()
    clients = setting.client
    user = setting.QA_setting_user_name
    market_data = []
    now = ''
    today = ''

    def __init__(self):

        self.backtest_type = 'day'
        self.account = QA_Account()
        self.market = QA_Market()
        self.order = QA_QAMarket_bid_list()
        self.bid = QA_QAMarket_bid()
        self.setting = QA_Setting()
        self.clients = self.setting.client
        self.user = self.setting.QA_setting_user_name
        self.market_data = []
        self.now = ''
        self.today = ''

    def __QA_backtest_init(self):
        """既然是被当做装饰器使用,就需要把变量设置放在装饰函数的前面,把函数放在装饰函数的后面"""
        # 设置回测的开始结束时间
        self.strategy_start_date = str('2017-01-05')
        self.strategy_end_date = str('2017-07-01')
        # 设置回测标的,是一个list对象,不过建议只用一个标的
        # gap是回测时,每日获取数据的前推日期(交易日)
        self.strategy_gap = int(60)
        # 设置全局的数据库地址,回测用户名,密码,并初始化
        self.setting.QA_util_sql_mongo_ip = str('127.0.0.1')
        self.setting.QA_setting_user_name = str('admin')
        self.setting.QA_setting_user_password = str('admin')
        self.setting.QA_setting_init()
        # 回测的名字
        self.strategy_name = str('example_min')
       # 股票的交易日历,真实回测的交易周期,和交易周期在交易日历中的id
        self.trade_list = trade_date_sse
        self.benchmark_code = 'hs300'
        """
        这里会涉及一个区间的问题,开始时间是要向后推,而结束时间是要向前推,1代表向后推,-1代表向前推
        """

        self.strategy_stock_list = ['000001', '000002', '000004']
        self.account.init_assest = 1000000
        self.backtest_bid_model = 'market_price'

    def __QA_backtest_prepare(self):
        """
        这是模型内部的 初始化,主要是初始化一些账户和市场资产
        写成了私有函数
        @yutiansut
        2017/7/20
        """

        # 重新初始账户资产

        self.setting.QA_setting_init()
        self.account.init()
        self.start_real_date = QA_util_get_real_date(
            self.strategy_start_date, self.trade_list, 1)
        self.start_real_id = self.trade_list.index(self.start_real_date)
        self.end_real_date = QA_util_get_real_date(
            self.strategy_end_date, self.trade_list, -1)
        self.end_real_id = self.trade_list.index(self.end_real_date)
        # 重新初始化账户的cookie
        self.account.account_cookie = str(random.random())
        # 初始化股票池的市场数据

        if self.backtest_type in ['day', 'd', '0x00']:
            self.market_data = QA_fetch_stocklist_day_adv(
                self.strategy_stock_list, self.trade_list[self.start_real_id - int(
                    self.strategy_gap)], self.trade_list[self.end_real_id])

        elif self.backtest_type in ['min', 'm', '0x01']:
            self.market_data = QA_fetch_stocklist_min_adv(
                self.strategy_stock_list, self.trade_list[
                    self.start_real_id - int(self.strategy_gap)],
                self.trade_list[self.end_real_id], self.backtest_type)

    def __QA_backtest_start(self, *args, **kwargs):
        """
        这个是回测流程开始的入口
        """
        assert len(self.strategy_stock_list) > 0
        assert len(self.trade_list) > 0
        assert isinstance(self.start_real_date, str)
        assert isinstance(self.end_real_date, str)
        assert len(self.market_data) == len(self.strategy_stock_list)

        QA_util_log_info('QUANTAXIS Backtest Engine Initial Successfully')
        QA_util_log_info('Basical Info: \n' + tabulate(
            [[str(__version__), str(self.strategy_name)]], headers=('Version', 'Strategy_name')))
        QA_util_log_info('BACKTEST Cookie_ID is:  ' +
                         str(self.account.account_cookie))
        QA_util_log_info('Stock_List: \n' +
                         tabulate([self.strategy_stock_list]))

        # 初始化报价模式
        self.__messages = []

    def __check_state(self, bid_price, bid_amount):
        pass

    def __QA_bid_amount(self, __strategy_amount, __amount):
        if __strategy_amount == 'mean':
            return float(float(self.account.message['body']['account']['cash'][-1]) /
                         len(self.strategy_stock_list)), 'price'
        elif __strategy_amount == 'half':
            return __amount * 0.5, 'amount'
        elif __strategy_amount == 'all':
            return __amount, 'amount'

    def __end_of_trading(self, *arg, **kwargs):
        # 在回测的最后一天,平掉所有仓位(回测的最后一天是不买入的)
        # 回测最后一天的交易处理

        while len(self.account.hold) > 1:
            __hold_list = self.account.hold[1::]
            pre_del_id = []
            for item_ in range(0, len(__hold_list)):
                if __hold_list[item_][3] > 0:
                    __last_bid = self.bid
                    __last_bid.amount = int(__hold_list[item_][3])
                    __last_bid.order_id = str(random.random())
                    __last_bid.price = 'close_price'
                    __last_bid.code = str(__hold_list[item_][1])
                    __last_bid.date = self.trade_list[self.end_real_id]
                    __last_bid.towards = -1
                    __last_bid.user = self.setting.QA_setting_user_name
                    __last_bid.strategy = self.strategy_name
                    __last_bid.bid_model = 'auto'
                    __last_bid.type = '0x01'
                    __last_bid.amount_model = 'amount'

                    __message = self.market.receive_bid(
                        __last_bid)
                    _remains_day = 0
                    while __message['header']['status'] == 500:
                        # 停牌状态,这个时候按停牌的最后一天计算价值(假设平仓)

                        __last_bid.date = self.trade_list[self.end_real_id - _remains_day]
                        _remains_day += 1
                        __message = self.market.receive_bid(
                            __last_bid)

                        # 直到市场不是为0状态位置,停止前推日期

                    self.__messages = self.account.QA_account_receive_deal(
                        __message)
                else:
                    pre_del_id.append(item_)
            pre_del_id.sort()
            pre_del_id.reverse()
            for item_x in pre_del_id:
                __hold_list.pop(item_x)

    def __warp_bid(self, __bid, __order):
        __market_data_for_backtest = self.QA_backtest_get_market_data(
            self, __bid.code, __bid.date, 'np', 1)
        __O, __H, __L, __C, __V = self.QA_backtest_get_OHLCV(
            self, __market_data_for_backtest) if len(__market_data_for_backtest) > 0 else(None, None, None, None, None)
        if __O is not None:
            if __order['bid_model'] in ['limit', 'Limit', 'Limited', 'limited', 'l', 'L', 0, '0']:
                    # 限价委托模式
                __bid.price = __order['price']
            elif __order['bid_model'] in ['Market', 'market', 'MARKET', 'm', 'M', 1, '1']:
                __bid.price = 0.5 * (float(__O[0]) + float(__C[0]))
            elif __order['bid_model'] in ['strict', 'Strict', 's', 'S', '2', 2]:
                __bid.price = float(
                    __H[0]) if __bid.towards == 1 else float(__L[0])
            elif __order['bid_model'] in ['close', 'close_price', 'c', 'C', '3', 3]:
                __bid.price = float(__C[0])

            __bid.price = float('%.2f' % __bid.price)
            return __bid
        else:
            return None

    def __end_of_backtest(self, *arg, **kwargs):

        # 开始分析
        QA_util_log_info('start analysis====\n' +
                         str(self.strategy_stock_list))
        QA_util_log_info('=' * 10 + 'Trade History' + '=' * 10)
        QA_util_log_info('\n' + tabulate(self.account.history,
                                         headers=('date', 'code', 'price', 'towards',
                                                  'amounts', 'order_id', 'trade_id', 'commission')))
        QA_util_log_info('\n' + tabulate(self.account.detail,
                                         headers=('date', 'code', 'price', 'amounts', 'order_id',
                                                  'trade_id', 'sell_price', 'sell_order_id',
                                                  'sell_trade_id', 'sell_date', 'left_amount',
                                                  'commission')))
        __exist_time = int(self.end_real_id) - int(self.start_real_id) + 1
        self.__benchmark_data = QA_fetch_index_day(
            self.benchmark_code, self.start_real_date,
            self.end_real_date)
        if len(self.__messages) > 1:
            performace = QA_backtest_analysis_start(
                self.setting.client, self.strategy_stock_list, self.__messages,
                self.trade_list[self.start_real_id:self.end_real_id + 1],
                self.market_data, self.__benchmark_data)
            _backtest_mes = {
                'user': self.setting.QA_setting_user_name,
                'strategy': self.strategy_name,
                'stock_list': performace['code'],
                'start_time': self.strategy_start_date,
                'end_time': self.strategy_end_date,
                'account_cookie': self.account.account_cookie,
                'annualized_returns': performace['annualized_returns'],
                'benchmark_annualized_returns': performace['benchmark_annualized_returns'],
                'assets': performace['assets'],
                'benchmark_assets': performace['benchmark_assets'],
                'trade_date': performace['trade_date'],
                'total_date': performace['total_date'],
                'win_rate': performace['win_rate'],
                'alpha': performace['alpha'],
                'beta': performace['beta'],
                'sharpe': performace['sharpe'],
                'vol': performace['vol'],
                'benchmark_vol': performace['benchmark_vol'],
                'max_drop': performace['max_drop'],
                'exist': __exist_time,
                'time': datetime.datetime.now()
            }
            QA_SU_save_backtest_message(_backtest_mes, self.setting.client)
            QA_SU_save_account_message(self.__messages, self.setting.client)
            QA_SU_save_account_to_csv(self.__messages)

    def QA_backtest_get_market_data(self, code, date, gap_=None):
        '这个函数封装了关于获取的方式'
        gap_ = self.strategy_gap if gap_ is None else gap_
        index_of_code = self.strategy_stock_list.index(code)
        self.market_data.select_code(index_of_code).select_time('',date)
        __res = self.market_data.data[index_of_code][:date].tail(gap_)


    def QA_backtest_hold_amount(self, __code):
        # return sum(list(map(lambda item: item[3] if __code in item else 0,
        # self.account.hold)))
        try:
            return self.account.hold_available[__code]
        except:
            return 0

    def __sell_from_order_queue(self):
        __result = []
        self.order.__init__()
        __bid_list = self.order.from_dataframe(self.account.order_queue)
        for item in __bid_list:
            __result.append(self.__QA_backtest_send_bid(
                self, item)['header']['status'])

        self.account.order_queue['status'] = __result
        return self.account.order_queue[self.account.order_queue['status'] != 200]

    def QA_backtest_get_OHLCV(self, __data):
        '快速返回 OHLCV格式'
        return (__data.T[1].astype(float).tolist(), __data.T[2].astype(float).tolist(),
                __data.T[3].astype(float).tolist(
        ), __data.T[4].astype(float).tolist(),
            __data.T[5].astype(float).tolist())

    def QA_backtest_send_order(self, __code, __amount, __towards, __order):
        """
        2017/8/4
        委托函数
        在外部封装的一个报价接口,尽量满足和实盘一样的模式

        输入
        =============
        买入/卖出
        股票代码
        买入/卖出数量
        委托模式*
            0 限价委托 LIMIT ORDER
            1 市价委托 MARKET ORDER
            2 严格模式(买入按最高价 卖出按最低价) STRICT ORDER
        """
        # 只需要维护未成交队列即可,无非是一个可用资金和可卖股票数量的调整

        # 必须是100股的倍数
        __amount = int(__amount / 100) * 100

        # self.__QA_backtest_set_bid_model()

        __bid = self.bid

        (__bid.order_id, __bid.user, __bid.strategy,
         __bid.code, __bid.date, __bid.datetime,
         __bid.sending_time,
         __bid.amount, __bid.towards) = (str(random.random()),
                                         self.setting.QA_setting_user_name, self.strategy_name,
                                         __code, self.running_date, self.running_date,
                                         self.running_date, __amount, __towards)
        __bid = self.__warp_bid(self, __bid, __order)
        if __bid is not None:
            # return self.__QA_backtest_send_bid(self, __bid)
            self.account.order_queue = self.account.order_queue.append(
                __bid.to_df())
        # 先进行处理:

    def __sync_assets_status(self):
        '交易前需要同步持仓状态/现金'
        self.account.cash_available = self.account.cash[-1]
        __temp_hold = pd.DataFrame(
            self.account.hold[1::], columns=self.account.hold[0])
        __temp_hold = __temp_hold.set_index('code', drop=False)
        self.account.hold_available = __temp_hold['amount'].groupby(
            'code').sum()

        __wait_for_deal = self.account.order_queue[self.account.order_queue['status'] != 200] if len(
            self.account.order_queue) > 0 else pd.DataFrame()
        __wait_for_deal = __wait_for_deal['amount'].groupby(
            'code').sum() if len(__wait_for_deal) > 0 else pd.DataFrame()

    def __QA_backtest_send_bid(self, __bid):
        if __bid.towards == 1:
            # 扣费以下这个订单时的bar的open扣费

            if self.account.cash_available > (__bid.price * __bid.amount):
                # 这是买入的情况 买入的时候主要考虑的是能不能/有没有足够的钱来买入
                __message = self.market.receive_bid(__bid)
                self.account.cash_available -= (__bid.price * __bid.amount)
                # 先扔进去买入,再通过返回的值来判定是否成功
                if __message['header']['status'] == 200 and __message['body']['bid']['amount'] > 0:
                    # 这个判断是为了 如果买入资金不充足,所以买入报了一个0量单的情况
                    # 如果买入量>0, 才判断为成功交易
                    QA_util_log_info('BUY %s Price %s Date %s Amount %s' % (
                        __bid.code, __bid.price, __bid.datetime, __bid.amount))
                    self.account.QA_account_receive_deal(__message)
                    return __message
                else:
                    self.account.order_queue = self.account.order_queue.append(
                        __bid.to_df())

        # 下面是卖出操作,这里在卖出前需要考虑一个是否有仓位的问题:
        # 因为在股票中是不允许卖空操作的,所以这里是股票的交易引擎和期货的交易引擎的不同所在

        elif __bid.towards == -1:
            # 如果是卖出操作 检查是否有持仓
            # 股票中不允许有卖空操作
            # 检查持仓面板
            __amount_hold = self.QA_backtest_hold_amount(self, __bid.code)

            if __amount_hold > 0:

                __bid.amount = __amount_hold if __amount_hold < __bid.amount else __bid.amount
                __message = self.market.receive_bid(__bid)
                if __message['header']['status'] == 200:
                    self.account.QA_account_receive_deal(__message)
                    QA_util_log_info('SELL %s Price %s Date %s Amount %s' % (
                        __bid.code, __bid.price, __bid.datetime, __bid.amount))
                    return __message
                else:
                    # self.account.order_queue=self.account.order_queue.append(__bid.to_df())
                    return __message

            else:
                err_info = 'Error: Not Enough amount for code %s in hold list' % str(
                    __bid.code)
                QA_util_log_expection(err_info)
                return err_info

        else:
            return "Error: No buy/sell towards"

    def QA_backtest_check_order(self, order):
        '用于检查委托单的状态'
        """
        委托单被报入交易所会有一个回报,回报状态就是交易所返回的字段:
        字段目前 2xx 是成功  4xx是失败 5xx是交易所无数据(停牌)

        随着回测框架的不断升级,会有更多状态需要被管理:


        200 委托成功,交易成功
        203 委托成功,待成交
        20
        """
        pass

    def QA_backtest_status(self):
        return vars(self)

    def QA_backtest_sell_all(self):
        while len(self.account.hold) > 1:
            __hold_list = self.account.hold[1::]
            pre_del_id = []

            def __sell(id_):
                if __hold_list[item_][3] > 0:
                    __last_bid = self.bid
                    __last_bid.amount = int(__hold_list[id_][3])
                    __last_bid.order_id = str(random.random())
                    __last_bid.price = 'close_price'
                    __last_bid.code = str(__hold_list[id_][1])
                    __last_bid.date = self.now
                    __last_bid.towards = -1
                    __last_bid.user = self.setting.QA_setting_user_name
                    __last_bid.strategy = self.strategy_name
                    __last_bid.bid_model = 'auto'
                    __last_bid.type = '0x01'
                    __last_bid.amount_model = 'amount'

                    __message = self.market.receive_bid(
                        __last_bid)
                    _remains_day = 0
                    while __message['header']['status'] == 500:
                        # 停牌状态,这个时候按停牌的最后一天计算价值(假设平仓)

                        __last_bid.date = self.trade_list[self.end_real_id - _remains_day]
                        _remains_day += 1
                        __message = self.market.receive_bid(
                            __last_bid)

                        # 直到市场不是为0状态位置,停止前推日期

                    self.__messages = self.account.QA_account_receive_deal(
                        __message)
                else:
                    pre_del_id.append(id_)
                return pre_del_id

            pre_del_id = reduce(lambda _, x: __sell(x),
                                range(len(__hold_list)))
            pre_del_id.sort()
            pre_del_id.reverse()
            for item_x in pre_del_id:
                __hold_list.pop(item_x)

    @classmethod
    def load_strategy(__backtest_cls, func, *arg, **kwargs):
        '策略加载函数'

        # 首先判断是否能满足回测的要求`
        __messages = {}
        __backtest_cls.__init_cash_per_stock = int(
            float(__backtest_cls.account.init_assest) / len(__backtest_cls.strategy_stock_list))

        # 策略的交易日循环
        for i in range(int(__backtest_cls.start_real_id), int(__backtest_cls.end_real_id) - 1, 1):
            __backtest_cls.running_date = __backtest_cls.trade_list[i]
            QA_util_log_info(
                '=================daily hold list====================')
            QA_util_log_info('in the begining of ' +
                             __backtest_cls.running_date)
            QA_util_log_info(
                tabulate(__backtest_cls.account.message['body']['account']['hold']))
            __backtest_cls.now = __backtest_cls.running_date
            __backtest_cls.today = __backtest_cls.running_date
            # 交易前同步持仓状态

            if __backtest_cls.backtest_type in ['day', 'd']:
                __backtest_cls.__sync_assets_status(__backtest_cls)
                func(*arg, **kwargs)  # 发委托单
                __backtest_cls.account.order_queue = __backtest_cls.__sell_from_order_queue(
                    __backtest_cls)

            elif __backtest_cls.backtest_type in ['min', 'm']:
                func(*arg, **kwargs)  # 发委托单

            # 队列循环批量发单

        # 最后一天
        __backtest_cls.__end_of_trading(__backtest_cls)

    @classmethod
    def backtest_init(__backtest_cls, func, *arg, **kwargs):
        def __init_backtest(__backtest_cls, *arg, **kwargs):
            __backtest_cls.__QA_backtest_init(__backtest_cls)
            func(*arg, **kwargs)
            __backtest_cls.__QA_backtest_prepare(__backtest_cls)
        return __init_backtest(__backtest_cls)

    @classmethod
    def before_backtest(__backtest_cls, func, *arg, **kwargs):
        func(*arg, **kwargs)
        __backtest_cls.__QA_backtest_start(__backtest_cls)

    @classmethod
    def end_backtest(__backtest_cls, func, *arg, **kwargs):
        # yield __backtest_cls.cash
        __backtest_cls.__end_of_backtest(__backtest_cls, func, *arg, **kwargs)
        return func(*arg, **kwargs)


if __name__ == '__main__':

    pass
