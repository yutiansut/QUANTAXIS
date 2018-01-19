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


class QA_Backtest():
    """BACKTEST

    BACKTEST的主要目的:

    - 引入时间轴环境,获取全部的数据,然后按生成器将数据迭代插入回测的BROKER
        (这一个过程是模拟在真实情况中市场的时间变化和价格变化)

    - BROKER有了新数据以后 会通知MARKET交易前置,MARKET告知已经注册的所有的ACCOUNT 有新的市场数据

    - ACCOUNT 获取了新的市场函数,并将其插入他已有的数据中(update)

    - ACCOUNT 底下注册的策略STRATEGY根据新的市场函数,产生新的买卖判断,综合生成信号

    - 买卖判断通过交易前置发送给对应的BROKER,进行交易

    - BROKER发送SETTLE指令 结束这一个bar的所有交易,进行清算

    - 账户也进行清算,更新持仓,可卖,可用现金等

    - 迭代循环直至结束回测

    - 回测去计算这段时间的各个账户收益,并给出综合的最终结果

    """

    def __init__(self, market_type, frequence, start, end, code_list, commission_fee,):
        self.user = QA_User()
        self.if_settled = False
        self.account = None
        self.portfolio = None

        self.market = QA_Market()
        self.market_type = market_type
        self.frequence = frequence
        self.broker = QA_BacktestBroker(commission_fee)
        self.broker_name = 'backtest_broker'

        self.start = start
        self.end = end
        self.code_list = code_list

        if self.market_type is MARKET_TYPE.STOCK_CN and self.frequence is FREQUENCE.DAY:
            self.ingest_data = QA_fetch_stock_day_adv(
                self.code_list, self.start, self.end).to_qfq().panel_gen
        elif self.market_type is MARKET_TYPE.STOCK_CN and self.frequence[-3:] == 'min':
            self.ingest_data = QA_fetch_stock_min_adv(
                self.code_list, self.start, self.end, self.frequence).to_qfq().panel_gen

    def _generate_account(self):
        """generate a simple account
        """

        self.account, self.portfolio = self.user.generate_simpleaccount()

    def start_market(self):
        """start the market thread and register backtest broker thread
        """

        self.market.start()
        self.market.register(self.broker_name, self.broker)
        self.market.login(self.broker_name, self.account,
                          self.user.get_portfolio(self.portfolio).get_account(self.account))

    def run(self):
        """generator driven data flow
        """
        _date=None
        for data in self.ingest_data:
            date=data.date[0]
            if self.market_type is MARKET_TYPE.STOCK_CN :
                if _date!=date:
                    self.market._settle(self.broker_name)
            elif self.market_type in [MARKET_TYPE.FUND_CN,MARKET_TYPE.INDEX_CN,MARKET_TYPE.FUTURE_CN]:
                self.market._settle(self.broker_name)
            self.broker.run(QA_Event(
                event_type=ENGINE_EVENT.UPCOMING_DATA,
                market_data=data))
            self.market.upcoming_data(
                self.broker_name, data)
            self.market.trade_engine.queue.join()
            self.market.trade_engine.kernals[self.broker_name].queue.join()

            _date=date

        self.after_success()

    def after_success(self):
        """called when all trading fininshed, for performance analysis
        """

        for po in self.user.portfolio_list.keys():
            for ac in self.user.get_portfolio(po).accounts.keys():
                accounts = self.user.get_portfolio(po).get_account(ac)
                print(accounts.hold)

                print(accounts.history_table)

        self.stop()

    def stop(self):
        """stop all the market trade enging threads and all subthreads
        """

        self.market.trade_engine.stop_all()
        self.market.trade_engine.stop()


if __name__ == '__main__':
    backtest = QA_Backtest(market_type=MARKET_TYPE.STOCK_CN,
                           frequence=FREQUENCE.DAY,
                           start='2017-01-01',
                           end='2017-01-31',
                           code_list=['000001', '600010'],
                           commission_fee=0.00015)
    backtest._generate_account()
    backtest.start_market()
    backtest.run()

    # backtest.run()
