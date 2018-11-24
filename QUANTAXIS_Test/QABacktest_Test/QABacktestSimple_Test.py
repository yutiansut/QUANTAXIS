import unittest

import numpy as np
import pandas as pd

import QUANTAXIS as QA


class QABacktestSimple_Test(unittest.TestCase):

    # define the MACD strategy
    def MACD_JCSC(self, dataframe, SHORT=12, LONG=26, M=9):
        """
        1.DIF向上突破DEA，买入信号参考。
        2.DIF向下跌破DEA，卖出信号参考。
        """
        CLOSE = dataframe.close
        DIFF = QA.EMA(CLOSE, SHORT) - QA.EMA(CLOSE, LONG)
        DEA = QA.EMA(DIFF, M)
        MACD = 2 * (DIFF - DEA)

        CROSS_JC = QA.CROSS(DIFF, DEA)
        CROSS_SC = QA.CROSS(DEA, DIFF)
        ZERO = 0
        return pd.DataFrame(
            {'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD, 'CROSS_JC': CROSS_JC, 'CROSS_SC': CROSS_SC, 'ZERO': ZERO})

    def setUp(self):
        # 准备数据

        # create account
        self.Account = QA.QA_Account()
        self.Broker = QA.QA_BacktestBroker()

        self.Account.reset_assets(1000000)
        self.Account.account_cookie = 'user_admin_macd'

        # get data from mongodb
        self.data = QA.QA_fetch_stock_day_adv(
            ['000001', '000002', '000004', '600000'], '2017-09-01', '2018-05-20')
        self.data = self.data.to_qfq()

        # add indicator
        self.ind = self.data.add_func(self.MACD_JCSC)
        # ind.xs('000001',level=1)['2018-01'].plot()

        self.data_forbacktest = self.data.select_time(
            '2018-01-01', '2018-05-20')

    def tearDown(self):

        print(self.Account.history)
        print(self.Account.history_table)
        print(self.Account.daily_hold)

        # create Risk analysis
        Risk = QA.QA_Risk(self.Account)
        print(Risk.message)
        print(Risk.assets)
        Risk.plot_assets_curve()
        Risk.plot_dailyhold()
        Risk.plot_signal()
        # Risk.assets.plot()
        # Risk.benchmark_assets.plot()

        # save result
        self.Account.save()
        Risk.save()

        account_info = QA.QA_fetch_account(
            {'account_cookie': 'user_admin_macd'})
        account = QA.QA_Account().from_message(account_info[0])
        print(account)

    def test_simpleQABacktest(self):

        for items in self.data_forbacktest.panel_gen:
            for item in items.security_gen:
                daily_ind = self.ind.loc[item.index]
                if daily_ind.CROSS_JC.iloc[0] > 0:
                    order = self.Account.send_order(
                        code=item.code[0],
                        time=item.date[0],
                        amount=1000,
                        towards=QA.ORDER_DIRECTION.BUY,
                        price=0,
                        order_model=QA.ORDER_MODEL.CLOSE,
                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                    if order:
                        self.Broker.receive_order(QA.QA_Event(order=order, market_data=item))
                        trade_mes = self.Broker.query_orders(self.Account.account_cookie, 'filled')
                        res = trade_mes.loc[order.account_cookie, order.realorder_id]
                        order.trade(res.trade_id, res.trade_price,
                                    res.trade_amount, res.trade_time)
                elif daily_ind.CROSS_SC.iloc[0] > 0:
                    if self.Account.sell_available.get(item.code[0], 0) > 0:
                        order = self.Account.send_order(
                            code=item.code[0],
                            time=item.date[0],
                            amount=self.Account.sell_available.get(
                                item.code[0], 0),
                            towards=QA.ORDER_DIRECTION.SELL,
                            price=0,
                            order_model=QA.ORDER_MODEL.MARKET,
                            amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                        )
                        if order:
                            self.Broker.receive_order(QA.QA_Event(order=order, market_data=item))
                            trade_mes = self.Broker.query_orders(self.Account.account_cookie, 'filled')
                            res = trade_mes.loc[order.account_cookie, order.realorder_id]
                            order.trade(res.trade_id, res.trade_price,
                                        res.trade_amount, res.trade_time)
        self.Account.settle()
