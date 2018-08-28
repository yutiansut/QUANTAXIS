# coding:utf-8

import time
import unittest

import pandas as pd

from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAApplication.QABacktest import QA_Backtest
from QUANTAXIS.QAFetch import QAQuery_Advance
from QUANTAXIS.QAIndicator import QA_indicator_BOLL
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_get_last_day,
                                           QA_util_get_real_date,
                                           trade_date_sse)
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, DATASOURCE, FREQUENCE,
                                          MARKET_TYPE, ORDER_DIRECTION,
                                          ORDER_MODEL, OUTPUT_FORMAT)


class BollingerBandsStrategy(QA_Strategy):
    '''
    布林带策略：
    股价运行
    '''

    def __init__(self, code, start, end):
        super().__init__()
        self.frequence = FREQUENCE.DAY
        self.market_type = MARKET_TYPE.STOCK_CN
        self.backtest_stock_code = code
        start = QA_util_get_last_day(
            QA_util_get_real_date(start, trade_date_sse, -1), 100)
        self.stock_day_data = QAQuery_Advance.QA_fetch_stock_day_adv(
            self.backtest_stock_code, start, end)
        self.stock_day_data_qfq = self.stock_day_data.to_qfq()

        # print(self.stock_day_data)
        self.stock_bollinger_bands = QA_indicator_BOLL(
            self.stock_day_data_qfq())
        # print(len(self.stock_bollinger_bands))
        # print(self.stock_bollinger_bands)

        self.current_state = 0

    def on_bar(self, event):
        # print("on bar 当前日期是:", current_date )

        today_on_bar = pd.Timestamp(self.current_time.date())

        for item in event.market_data.code:
            market_data = event.market_data
            # QA_DataStruct_Stock_day
            print()
            # print( market_data.high )
            # print( market_data.low  )
            # print( market_data.open )
            # print( market_data.close )

            # pandas 不熟悉 可能有更加好的 方法获取数据
            bollingerBandsSeries = self.stock_bollinger_bands.xs(
                (today_on_bar, item))
            bollValue = bollingerBandsSeries.to_dict()
            print(bollValue)
            #{'BOLL': 55.32273295612507, 'LB': 26.899453479933527, 'UB': 83.74601243231662}
            middlePrice = bollValue['BOLL']
            lowPrice = bollValue['LB']
            highPrice = bollValue['UB']

            market_data_type = type(market_data)
            closePrice_type = type(market_data.close)

            closePriceDict = market_data.close.to_dict()
            closePrice = closePriceDict[(today_on_bar, item)]

            last_state = self.current_state

            if closePrice > middlePrice:
                # print(today_on_bar,closePrice,"中轨上方运行",middlePrice)
                self.current_state = 1

            elif closePrice < middlePrice:
                # print(today_on_bar,closePrice,"中轨下方运行",middlePrice)
                self.current_state = -1

            else:
                # print(today_on_bar,closePrice,"中轨价格",middlePrice)
                pass

            if last_state == -1 and self.current_state == 1:
                print(today_on_bar, "上穿中轨道")

                if self.sell_available is not None and self.sell_available.get(item, 0) == 0:
                    event.send_order(account_cookie=self.account_cookie,
                                     amount=1000,
                                     amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time,
                                     code=item,
                                     price=0,
                                     order_model=ORDER_MODEL.MARKET,
                                     towards=ORDER_DIRECTION.BUY,
                                     market_type=self.market_type,
                                     frequence=self.frequence,
                                     broker_name=self.broker)

            elif last_state == 1 and self.current_state == -1:
                print(today_on_bar, "下穿中轨道")

                if self.sell_available is not None and self.sell_available.get(item, 0) > 0:
                    event.send_order(account_cookie=self.account_cookie,
                                     amount=self.sell_available[item],
                                     amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time,
                                     code=item,
                                     price=0,
                                     order_model=ORDER_MODEL.MARKET,
                                     towards=ORDER_DIRECTION.SELL,
                                     market_type=self.market_type,
                                     frequence=self.frequence,
                                     broker_name=self.broker)

            # 最后一天卖出
            #last_dau_on_bar = pd.Timestamp('2018-05-20')
            type1 = type(self.current_time.date())
            date1 = self.current_time.date()
            # todo 🛠 改成日期函数的比较
            if date1.year == 2018 and date1.month == 5 and date1.day == 16:
                if self.sell_available is not None and self.sell_available.get(item, 0) > 0:
                    event.send_order(account_cookie=self.account_cookie,
                                     amount=self.sell_available[item],
                                     amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time,
                                     code=item,
                                     price=0,
                                     order_model=ORDER_MODEL.MARKET,
                                     towards=ORDER_DIRECTION.SELL,
                                     market_type=self.market_type,
                                     frequence=self.frequence,
                                     broker_name=self.broker)
                print("结束回测，卖出所有股份！")

                # print(up)
            # print(lb)

        # time.sleep(1)
        pass


class BacktestBollingerBands(QA_Backtest):
    def __init__(self, market_type, frequence, start, end, code_list, commission_fee):
        super().__init__(market_type,  frequence, start, end, code_list, commission_fee)
        self.user = QA_User()
        bool_strategy = BollingerBandsStrategy(
            code=code_list, start=start, end=end)
        self.portfolio, self.account = self.user.register_account(
            bool_strategy)

    def after_success(self):
        QA_util_log_info(self.account.history_table)
        # check if the history_table is empty list
        if len(self.account.history_table) == 0:
            # 没有交易历史记录，直接返回
            return
        risk = QA_Risk(self.account, benchmark_code='000300',
                       benchmark_type=MARKET_TYPE.INDEX_CN)
        print(risk().T)
        risk.plot_assets_curve()
        risk.plot_dailyhold()
        risk.plot_signal()
        performance = QA_Performance(self.account)
        performance.plot_pnlmoney(performance.pnl_fifo)
        performance.plot_pnlratio(performance.pnl_fifo)
        self.account.save()
        risk.save()


class Test_QABacktest_BollingerBands(unittest.TestCase):

    def setUp(self):
        # 准备数据
        self.time_to_Market_300439 = '2016-05-01'
        self.time_to_day = '2018-05-17'

    def testBacktestBollingerBands(self):

        backtest = BacktestBollingerBands(market_type=MARKET_TYPE.STOCK_CN,
                                          frequence=FREQUENCE.DAY,
                                          start=self.time_to_Market_300439,
                                          end=self.time_to_day,
                                          code_list=['300439', '000001',
                                                     '600000', '600426', '600637'],
                                          commission_fee=0.00015)
        backtest.start_market()

        backtest.run()
        backtest.stop()
        print("结束回测！")

        pass


if __name__ == '__main__':
    t = Test_QABacktest_BollingerBands()
    t.setUp()
    t.testBacktestBollingerBands()
