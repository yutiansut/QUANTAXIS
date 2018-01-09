# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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


from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QABacktest.QABacktest import QA_Backtest
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAMarket.QAMarket import QA_Market
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, BROKER_EVENT,
                                          BROKER_TYPE, ENGINE_EVENT,
                                          MARKET_TYPE, MARKETDATA_TYPE,
                                          ORDER_DIRECTION, ORDER_MODEL)

from test_backtest.strategy import MAStrategy


class Backtest(QA_Backtest):

    def __init__(self, market_type, start, end, code_list, commission_fee):
        super().__init__(market_type, start, end, code_list, commission_fee)
        self.user = QA_User()
        mastrategy = MAStrategy()
        self.portfolio, self.account = self.user.register_account(mastrategy)
        print(self.user.get_portfolio(self.portfolio).accounts)
        print(self.user.get_portfolio(
            self.portfolio).get_account(self.account).cash)
        #self.market._settle(self.broker_name, callback=self.if_settle)

        # print(self.market.query_data)


if __name__ == '__main__':
    import QUANTAXIS as QA
    backtest = Backtest(market_type=MARKET_TYPE.STOCK_DAY,
                        start='2017-01-01',
                        end='2017-01-31',
                        code_list=QA.QA_fetch_stock_block_adv().code[0:5],
                        commission_fee=0.00015)
    backtest.start_market()

    backtest.run()
    

    # backtest._settle()

    # backtest.run()
