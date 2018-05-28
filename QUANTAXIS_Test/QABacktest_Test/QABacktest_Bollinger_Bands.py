import unittest
from QUANTAXIS.QAARP.QARisk import QA_Risk
from QUANTAXIS.QAARP.QAUser import QA_User

from QUANTAXIS.QABacktest.QABacktest import QA_Backtest
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, MARKET_TYPE, FREQUENCE, ORDER_DIRECTION, ORDER_MODEL,DATASOURCE, OUTPUT_FORMAT)

from QUANTAXIS.QAUtil.QALogs import QA_util_log_info

import time

class BollingerBandsStrategy(QA_Strategy):
    '''
    布林带策略：
    初始位置买入 5% 的仓位
    股价运行中间轨道，下轨道， 持仓20% ， 最多不超过30%， 先抛后买， 靠近中轨道附近 卖出
    股价运行中间轨道，上轨道， 持仓10% ， 最多不超过20%， 先买后抛， 靠近中轨道附近 买入

    %b指标
        （一）计算公式：（收盘价-布林线下轨价格）/（布林线上轨价格-布林线下轨价格）
    股价运行
    '''
    def __init__(self):
        super().__init__()
        self.frequence = FREQUENCE.DAY
        self.market_type = MARKET_TYPE.STOCK_CN

        pass

    def on_bar(self, event):
        for item in event.market_data.code:
            market_data = event.market_data
            print(market_data)
            print(item)
            print()
        time.sleep(1)
        pass



class BacktestBollingerBands(QA_Backtest):
    def __init__(self, market_type, frequence, start, end, code_list, commission_fee):
        super().__init__(market_type,  frequence, start, end, code_list, commission_fee)
        self.user = QA_User()
        mastrategy = BollingerBandsStrategy()
        self.portfolio, self.account = self.user.register_account(mastrategy)

    def after_success(self):
        QA_util_log_info(self.account.history_table)
        # check if the history_table is empty list
        if len(self.account.history_table) == 0:
            # 没有交易历史记录，直接返回
            return
        risk = QA_Risk(self.account, benchmark_code='000300', benchmark_type=MARKET_TYPE.INDEX_CN)
        print(risk().T)

        self.account.save()
        risk.save()

class Test_QABacktest_BollingerBands(unittest.TestCase):

    def testBacktestBollingerBands(self):

        self.time_to_Market_300439 = '2015-09-22'
        self.time_to_day = '2016-05-01'

        backtest = BacktestBollingerBands(market_type=MARKET_TYPE.STOCK_CN,
                            frequence=FREQUENCE.DAY,
                            start=self.time_to_Market_300439,
                            end=self.time_to_day,
                            code_list=['300439'],
                            commission_fee=0.00015)
        backtest.start_market()

        backtest.run()
        backtest.stop()
        print("结束回测！")

        pass
