# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAMarket.QAMarket import QA_Market
from QUANTAXIS.QAUtil.QAParameter import (AMOUNT_MODEL, BROKER_EVENT,
                                          BROKER_TYPE, ENGINE_EVENT,
                                          MARKET_TYPE, MARKETDATA_TYPE,
                                          ORDER_DIRECTION, ORDER_MODEL)


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

    def __init__(self, market_type, start, end, code_list, commission_fee,):
        self.user = QA_User()
        self.if_settled = False
        ac, po = self.user.generate_simpleaccount()
        print(ac)
        self.market = QA_Market()
        self.market.start()
        # self.market.connect(BROKER_TYPE.BACKETEST)

        self.broker = QA_BacktestBroker(commission_fee)
        self.broker_name = 'backtest_broker'
        self.market.register(self.broker_name, self.broker)
        print(self.market)
        self.market.login(self.broker_name, ac,
                          self.user.get_portfolio(po).get_account(ac))
        self.start = start
        self.end = end
        self.code_list = code_list
        self.ingest_data = QA_fetch_stock_day_adv(
            code_list, start, end).panel_gen

    def run(self):
        data = next(self.ingest_data)
        #self.market.running_time = str(data.date[0])[0:10]
        # print(data)
        self.broker.run(QA_Event(
            event_type=ENGINE_EVENT.UPCOMING_DATA,
            market_data=data))
        self.market.upcoming_data(data)
        # print(self.broker._quotation)
        # print(self.broker.broker_data)

        # print(self.market.query_currentbar(
        #     broker_name=self.broker_name,
        #     market_type=MARKET_TYPE,
        #     code=self.code_list[0]))
        # print(self.market.get_account_id())
        for ac in self.market.get_account_id():
            self.market.insert_order(
                account_id=ac, amount=1000, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                time=self.market.running_time, code=self.code_list[0], price=0,
                order_model=ORDER_MODEL.MARKET, towards=ORDER_DIRECTION.BUY,
                market_type=MARKET_TYPE.STOCK_DAY, data_type=MARKETDATA_TYPE.DAY,
                broker_name=self.broker_name
            )
        self.market._trade(self.broker_name)
        self.market._settle(self.broker_name, callback=self.if_settle)

    def if_settle(self, data):
        if data is 'settle':
            self.if_settled = True
            self.risk_control()

    def risk_control(self):
        if self.if_settled:
            for po in self.user.portfolio_list.keys():
                for ac in self.user.get_portfolio(po).accounts.keys():
                    accounts = self.user.get_portfolio(po).get_account(ac)
                    print(accounts.assets)
                    print(accounts.cash)

        # print(self.market.query_data)


if __name__ == '__main__':
    backtest = QA_Backtest(market_type=MARKET_TYPE.STOCK_DAY,
                           start='2017-01-01',
                           end='2017-01-31',
                           code_list=['000001', '600010'],
                           commission_fee=0.00015)
    backtest.run()
    # backtest.run()
