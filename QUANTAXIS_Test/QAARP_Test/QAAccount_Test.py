import unittest;

from QUANTAXIS.QAUtil import (QADate)
from QUANTAXIS.QAARP import ( QAAccount )
from QUANTAXIS import *;
import QUANTAXIS as QA
import random as rnd

import numpy as np
import pandas as pd


class Test_QAAccount(unittest.TestCase):


    def test_BuyAndSell(self):
        # 测试买卖事件

        QA_Account()


        pass


    def test_QAAccount_class(self):

        #测试流程 获取 美康生物 300439 的走势 从 2017年10月01日开始 到 2018年 4月30日
        #

        test_stock_code = '300439'
        stock_price_list = QA.QA_fetch_stock_day(code = test_stock_code, start = '2017-10-01', end = '2018-04-30')
        #buy_list = []

        print(stock_price_list)
        print("---------开始测试买入------------")
        #price_list_size = stock_price_list.size

        #生成随机数种子
        rnd.seed(QA.QA_util_time_now().timestamp())

        Account = QA.QA_Account()
        B = QA.QA_BacktestBroker()

        for aday_stock_price in stock_price_list:
            stock_code  = aday_stock_price[0]
            price_open  = aday_stock_price[1]
            price_high  = aday_stock_price[2]
            price_low   = aday_stock_price[3]
            price_close = aday_stock_price[4]
            stock_volume = aday_stock_price[5]
            stock_turn   = aday_stock_price[6]
            stock_timestamp = aday_stock_price[7]

            #print(type(stock_timestamp))

            dt = QADate.QA_util_pands_timestamp_to_datetime(stock_timestamp);
            date_time_to_buy = QADate.QA_util_datetime_to_strdatetime(dt);

            dt = QADate.QA_util_to_datetime(date_time_to_buy)

            if price_low != price_high:
                price_diff = (price_high - price_low);
                self.assertTrue(price_diff >= 0, "最高价一定是非负数")

                rand_value = rnd.random()
                buy_price = price_low + price_diff * rand_value
                print("{} 申报买入的成交价格 {}".format(dt, buy_price))
                #每天随机在开盘价格和收盘价格直接买入


                Order = Account.send_order(code=test_stock_code,
                                           price=buy_price,
                                           amount=100,
                                           money=Account.cash_available,  # 全仓买入， AMOUNT_MODEL.BY_AMOUNT 忽略该参数
                                           time=date_time_to_buy,
                                           towards=QA.ORDER_DIRECTION.BUY,
                                           order_model=QA.ORDER_MODEL.LIMIT,
                                           amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                           )



                print('ORDER的占用资金: {}'.format((Order.amount * Order.price) * (1 + Account.commission_coeff)))
                print('账户剩余资金 :{}'.format(Account.cash_available)) ## ??
                cash_available = Account.cash_available
                print(cash_available)


                rec_mes=B.receive_order(QA.QA_Event(order=Order))
                print(rec_mes)
                Account.receive_deal(rec_mes)

                knock_down_price = rec_mes['body']['order']['price'];
                bid_price = round(buy_price, 2);

                print("{} 获取订单的价格 {}".format(dt, buy_price))

                self.assertEqual(knock_down_price, bid_price)

                print('账户的可用资金 {}'.format(Account.cash_available))
                print('-----------------------------------------------')



        