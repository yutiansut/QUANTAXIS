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


from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, MARKET_TYPE,
                                          FREQUENCE, ORDER_DIRECTION,
                                          ORDER_MODEL)
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info

class MAStrategy(QA_Strategy):
    def __init__(self):
        super().__init__()
        self.frequence = FREQUENCE.DAY
        self.market_type = MARKET_TYPE.STOCK_CN

    def on_bar(self, event):
        sellavailable=self.sell_available
        try:
            for item in event.market_data.code:
                if sellavailable is None:

                    event.send_order(account_id=self.account_cookie,
                                     amount=100, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                     time=self.current_time, code=item, price=0,
                                     order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                                     market_type=self.market_type, frequence=self.frequence,
                                     broker_name=self.broker)

                else:
                    if sellavailable.get(item, 0) > 0:
                        event.send_order(account_id=self.account_cookie,
                                         amount=sellavailable[item], amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                         time=self.current_time, code=item, price=0,
                                         order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.SELL,
                                         market_type=self.market_type, frequence=self.frequence,
                                         broker_name=self.broker
                                         )
                    else:
                        event.send_order(account_id=self.account_cookie,
                                         amount=100, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                                         time=self.current_time, code=item, price=0,
                                         order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                                         market_type=self.market_type, frequence=self.frequence,
                                         broker_name=self.broker)

        except:
            pass



class Test_QABacktest(unittest.TestCase):

    def testBacktraceTest(self):
        backtest = QA_Backtest(market_type=MARKET_TYPE.STOCK_CN,
                               frequence=FREQUENCE.DAY,
                               start='2017-01-01',
                               end='2017-1-30',
                               code_list=['000001', '600010'],
                               commission_fee=0.00015)
        #backtest.
        backtest._generate_account()
        backtest.start_market()
        backtest.run()

        # backtest.run()
        pass