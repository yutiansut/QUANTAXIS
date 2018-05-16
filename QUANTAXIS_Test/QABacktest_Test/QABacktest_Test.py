import unittest


import time
from functools import lru_cache

from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv, QA_fetch_stock_min_adv
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAMarket.QAMarket import QA_Market
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, BROKER_EVENT,
                                          BROKER_TYPE, ENGINE_EVENT, FREQUENCE,
                                          MARKET_TYPE, ORDER_DIRECTION,
                                          ORDER_MODEL)


from QUANTAXIS.QABacktest.QABacktest import (QA_Backtest)

class Test_QABacktest(unittest.TestCase):

    def testBacktraceTest(self):
        backtest = QA_Backtest(market_type=MARKET_TYPE.STOCK_CN,
                               frequence=FREQUENCE.DAY,
                               start='2017-01-01',
                               end='2017-1-30',
                               code_list=['000001', '600010'],
                               commission_fee=0.00015)
        backtest._generate_account()
        backtest.start_market()
        backtest.run()

        # backtest.run()
        pass