import random as rnd
import unittest

import QUANTAXIS as QA
from QUANTAXIS.QAUtil import QADate, QARandom


class Test_QAAccount(unittest.TestCase):

    def test_BuyAndSell(self):
        # 测试买卖事件
        # 测试流程，
        # 随机选中一组股票
        # 随机选中几个交易日 (只测试当前日期）
        # 随机卖出
        # 随机买入
        # 发送订单
        # 从队列中取回订单
        # 比较
        codeCount = 10
        codeList = QARandom.QA_util_random_with_zh_stock_code(codeCount)
        # print(codeList)
        # { code: QA_DataStruct_Stock_day }
        # 如果代码不存在 则 code：None
        codeForDate = {}
        for codeIndex in range(0, codeCount):
            aStockDataStructDay = QA.QA_fetch_stock_day_adv(
                codeList[codeIndex])
            codeForDate[codeList[codeIndex]] = aStockDataStructDay
        # print(codeForDate)

        str = QADate.QA_util_today_str()
        timestamp = QADate.QA_util_to_datetime(str)

        account = QA.QA_Account(strategy_name="TEST策略", user_cookie=None)

        orderList = []
        for a_stock_code in codeForDate.keys():
            anOrder = account.send_order(code=a_stock_code,
                                         amount=100,
                                         time=timestamp,
                                         towards=1,
                                         price=8.8,
                                         order_model=QA.ORDER_MODEL.LIMIT,
                                         amount_model=QA.AMOUNT_MODEL.BY_AMOUNT)
            orderList.append(anOrder)

        orderQueue = account.get_orders()
        print(orderQueue)

        self.assertEqual(len(orderQueue.queue_df), codeCount)

        orderList2 = []
        print(orderQueue.queue_df)
        for orderId in orderQueue.queue_df.index:
            anOrder2 = orderQueue.query_order(orderId)
            orderList2.append(anOrder2)

        self.assertEqual(len(orderList), len(orderList2))

        orderCount = len(orderList)
        for i in range(orderCount):

            order_01 = orderList[i]
            order_02 = orderList2[i]

            # 总是不正确
            #b = order_01 is order_02
            #b = order_01 == order_02
            #b = (order_01.__dict__ == order_02.__dict__)

            dict1 = order_01.__dict__
            for key in dict1.keys():
                v1 = order_01.__dict__[key]
                v2 = order_02.__dict__[key]
                if v1 != v2:
                    print(key)
                    print(v1)
                    print(v2)
                    self.fail("订单数据不正确")
            # todo 继续研究为何不正确
            #self.assertEqual(order_01, order_02)
        pass

    def n0_test_QAAccount_class(self):

        # 测试流程 获取 美康生物 300439 的走势 从 2017年10月01日开始 到 2018年 4月30日
        #
        test_stock_code = '300439'
        stock_price_list = QA.QA_fetch_stock_day(
            code=test_stock_code, start='2017-10-01', end='2018-04-30')
        #buy_list = []

        print(stock_price_list)
        print("---------开始测试买入------------")
        #price_list_size = stock_price_list.size

        # 生成随机数种子
        rnd.seed(QA.QA_util_time_now().timestamp())

        Account = QA.QA_Account()
        B = QA.QA_BacktestBroker()

        for aday_stock_price in stock_price_list:
            stock_code = aday_stock_price[0]
            price_open = aday_stock_price[1]
            price_high = aday_stock_price[2]
            price_low = aday_stock_price[3]
            price_close = aday_stock_price[4]
            stock_volume = aday_stock_price[5]
            stock_turn = aday_stock_price[6]
            stock_timestamp = aday_stock_price[7]

            # print(type(stock_timestamp))

            dt = QADate.QA_util_pands_timestamp_to_datetime(stock_timestamp)
            date_time_to_buy = QADate.QA_util_datetime_to_strdatetime(dt)

            dt = QADate.QA_util_to_datetime(date_time_to_buy)

            if price_low != price_high:
                price_diff = (price_high - price_low)
                self.assertTrue(price_diff >= 0, "最高价一定是非负数")

                rand_value = rnd.random()
                buy_price = price_low + price_diff * rand_value
                print("{} 申报买入的成交价格 {}".format(dt, buy_price))
                # 每天随机在开盘价格和收盘价格直接买入
                Order = Account.send_order(code=test_stock_code,
                                           price=buy_price,
                                           amount=100,
                                           money=Account.cash_available,  # 全仓买入， AMOUNT_MODEL.BY_AMOUNT 忽略该参数
                                           time=date_time_to_buy,
                                           towards=QA.ORDER_DIRECTION.BUY,
                                           order_model=QA.ORDER_MODEL.LIMIT,
                                           amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                           )
                print('ORDER的占用资金: {}'.format(
                    (Order.amount * Order.price) * (1 + Account.commission_coeff)))
                print('账户剩余资金 :{}'.format(Account.cash_available))  # ??
                cash_available = Account.cash_available
                print(cash_available)

                rec_mes = B.receive_order(QA.QA_Event(order=Order))
                print(rec_mes)
                Account.receive_deal(rec_mes)

                knock_down_price = rec_mes['body']['order']['price']
                bid_price = round(buy_price, 2)

                print("{} 获取订单的价格 {}".format(dt, buy_price))

                self.assertEqual(knock_down_price, bid_price)

                print('账户的可用资金 {}'.format(Account.cash_available))
                print('-----------------------------------------------')
