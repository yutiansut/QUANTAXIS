import unittest

import pandas as pd
import tushare as QATs

from QUANTAXIS import QUANTAXIS as QA
from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAApplication.QABacktest import QA_Backtest
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day
from QUANTAXIS.QAIndicator import QA_indicator_MA
from QUANTAXIS.QAUtil.QADate import QA_util_datetime_to_strdate
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, DATASOURCE, FREQUENCE,
                                          MARKET_TYPE, ORDER_DIRECTION,
                                          ORDER_MODEL, OUTPUT_FORMAT)


class MAStrategy(QA_Strategy):
    def __init__(self):
        super().__init__()
        self.frequence = FREQUENCE.DAY
        self.market_type = MARKET_TYPE.STOCK_CN

        # self.stock_basics = QATs.get_stock_basics()
        # self.time_to_Market_300439 = self.stock_basics.loc['300439', 'timeToMarket']
        # self.time_to_Market_300439 = QA.QA_util_date_int2str(self.time_to_Market_300439)
        # self.time_to_day = QA_util_datetime_to_strdate(QA.QA_util_date_today())
        # print(self.time_to_Market_300439)
        # print(self.time_to_day)

        self.time_to_Market_300439 = '2015-04-22'
        self.time_to_day = '2018-05-01'

        self.df_from_Tdx = QA_fetch_stock_day(
            '300439', self.time_to_Market_300439, self.time_to_day, 'pd')
        # print(self.df_from_Tdx)

        self.ma05 = QA_indicator_MA(self.df_from_Tdx, 5)

        self.ma10 = QA_indicator_MA(self.df_from_Tdx, 10)
        self.ma15 = QA_indicator_MA(self.df_from_Tdx, 15)
        self.ma20 = QA_indicator_MA(self.df_from_Tdx, 20)
        # print(self.df5)

    def on_bar(self, event):
        sellavailable = self.sell_available
        # try:
        #strDbg = QA.QA_util_random_with_topic("MAStrategy.on_bar call")
        #print(">-----------------------on bar----------------------------->", strDbg)
        for item in event.market_data.code:

            current_date = self.current_time.date()
            #print("on bar 当前日期是:", current_date )

            today_T = pd.Timestamp(current_date)

            vma05 = self.ma05.at[today_T, 'MA5']
            vma10 = self.ma10.at[today_T, 'MA10']
            vma15 = self.ma15.at[today_T, 'MA15']
            vma20 = self.ma20.at[today_T, 'MA20']

            if vma05 > vma10 and vma10 > vma15 and vma15 > vma20:
                # print("均线多头排列")

                if self.sell_available is not None and self.sell_available.get(item, 0) == 0:
                    print("*>> MAStrategy!on_bar  event.send_order 买入 buy %d" % (100))
                    print(event.send_order)
                    print(type(event.send_order))
                    event.send_order(account_cookie=self.account_cookie,
                                     amount=100,
                                     amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time,
                                     code=item,
                                     price=0,
                                     order_model=ORDER_MODEL.MARKET,
                                     towards=ORDER_DIRECTION.BUY,
                                     market_type=self.market_type,
                                     frequence=self.frequence,
                                     broker_name=self.broker)

            elif vma05 < vma10 and vma10 < vma15 and vma15 < vma20:
                # print("均线空头排列")
                if self.sell_available is not None and self.sell_available.get(item, 0) > 0:

                    print("*>> MAStrategy!on_bar  event.send_order 卖出 buy %d" % 100)
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

            else:
                # print("均线交叉中")
                pass
        #print("<-----------------------on bar-----------------------------<",strDbg)
               #current_date = self.current_time.date
    # except:
    #    pass


class Backtest(QA_Backtest):

    def __init__(self, market_type, frequence, start, end, code_list, commission_fee):
        super().__init__(market_type,  frequence, start, end, code_list, commission_fee)
        self.user = QA_User()
        mastrategy = MAStrategy()
        self.portfolio, self.account = self.user.register_account(mastrategy)

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


class Test_QABacktest(unittest.TestCase):

    def testBacktraceTest(self):
        self.run_daybacktest()
        pass

    def run_daybacktest(self):
        #import QUANTAXIS as QA
        # print(QA.QA_fetch_stock_block_adv().code[0:5])
        # self.stock_basics = QATs.get_stock_basics()
        # self.time_to_Market_300439 = self.stock_basics.loc['300439', 'timeToMarket']
        # self.time_to_Market_300439 = QA.QA_util_date_int2str(self.time_to_Market_300439)
        # self.time_to_day = QA_util_datetime_to_strdate(QA.QA_util_date_today())
        # print(self.time_to_Market_300439)
        # print(self.time_to_day)
        # QA.QA_util_time_now()

        self.time_to_Market_300439 = '2015-04-22'
        self.time_to_day = '2018-05-01'

        backtest = Backtest(market_type=MARKET_TYPE.STOCK_CN,
                            frequence=FREQUENCE.DAY,
                            start=self.time_to_Market_300439,
                            end=self.time_to_day,
                            code_list=['300439'],
                            commission_fee=0.00015)
        backtest.start_market()

        backtest.run()
        backtest.stop()
        print("结束回测！")


if __name__ == '__main__':
    Test_QABacktest().testBacktraceTest()
