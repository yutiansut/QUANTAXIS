# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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


from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv, QA_fetch_stock_min_adv
from QUANTAXIS.QAMarket.QABacktestBroker import QA_BacktestBroker
from QUANTAXIS.QAMarket.QAMarket import QA_Market
from QUANTAXIS.QAUtil.QAParameter import (
    AMOUNT_MODEL,
    BROKER_EVENT,
    BROKER_TYPE,
    ENGINE_EVENT,
    FREQUENCE,
    MARKET_TYPE,
    ORDER_DIRECTION,
    ORDER_MODEL
)

from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting, QA_util_mongo_initial


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

    def __init__(
            self,
            market_type,
            frequence,
            start,
            end,
            code_list,
            commission_fee,
            username='quantaxis',
            password='quantaxis',
            portfolio_cookie='qatestportfolio'
    ):
        """
        :param market_type: 回测的市场 MARKET_TYPE.STOCK_CN ，
        :param frequence: 'day' '1min' '5min' '15min' '30min' '60min'
        :param start:     开始日期
        :param end:       结束日期
        :param code_list: 股票代码池
        :param commission_fee: 交易佣金
        """
        self.user = QA_User(username=username, password=password)
        self.if_settled = False
        self.account = None
        self.portfolio = self.user.new_portfolio(portfolio_cookie)
        # 🛠todo market_type 应该放在 QA_Market对象里的一个属性
        self.market = QA_Market(if_start_orderthreading=True)
        self.market_type = market_type

        self.frequence = frequence
        self.broker = QA_BacktestBroker(commission_fee)
        self.broker_name = 'backtest_broker'

        self.start = start
        self.end = end
        self.code_list = code_list

        # 🛠todo 检查start日期和结束end日期是否正确
        # 🛠todo 检查code list 是否合法

        # 根据 市场类型，回测周期频率， 和股票代码列表 获取回测数据
        if self.market_type is MARKET_TYPE.STOCK_CN and self.frequence is FREQUENCE.DAY:
            # 获取日线级别的回测数据
            self.ingest_data = QA_fetch_stock_day_adv(
                self.code_list,
                self.start,
                self.end
            ).to_qfq().panel_gen
        elif self.market_type is MARKET_TYPE.STOCK_CN and self.frequence[
                -3:] == 'min':
            # 获取分钟级别的回测数据
            self.ingest_data = QA_fetch_stock_min_adv(
                self.code_list,
                self.start,
                self.end,
                self.frequence
            ).to_qfq().panel_gen

        else:
            QA_util_log_info("{} 的市场类型没有实现！".format(market_type))

    def _generate_account(self):
        """
        generate a simple account
        """
        self.account = self.portfolio.new_account()

    def start_market(self):
        """
        start the market thread and register backtest broker thread
        QAMarket 继承QATrader， QATrader 中有 trade_engine属性 ， trade_engine类型是QA_Engine从 QA_Thread继承
        """
        # 启动 trade_engine 线程
        self.market.start()
        print('market start')

        # 注册 backtest_broker ，并且启动和它关联线程QAThread 存放在 kernels 词典中， { 'broker_name': QAThread }
        self.market.register(self.broker_name, self.broker)

        # 通过 broke名字 新建立一个 QAAccount 放在的中 session字典中 session 是 { 'cookie' , QAAccount }
        self.market.login(
            self.broker_name,
            self.account.account_cookie,
            self.account
        )

        self.market._sync_orders()

    def run(self):
        """generator driven data flow
        """
        # 如果出现了日期的改变 才会进行结算的事件
        print('start: running')
        _date = None
        for data in self.ingest_data:                    # 对于在ingest_data中的数据
                                                         # <class 'QUANTAXIS.QAData.QADataStruct.QA_DataStruct_Stock_day'>
            date = data.date[0]
            print('current date : {}'.format(date))
            print('current time : {}'.format(data.datetime[0]))
            if self.market_type is MARKET_TYPE.STOCK_CN: # 如果是股票市场
                if _date != date:                        # 如果新的date

                    # 前一天的交易日已经过去
                    # 往 broker 和 account 发送 settle 事件

                    try:
                        print('try to settle')
                        self.market._settle(self.broker_name)
                        self.market.next_tradeday()
                    except Exception as e:
                        raise e
            # 基金 指数 期货
            elif self.market_type in [MARKET_TYPE.FUND_CN,
                                      MARKET_TYPE.INDEX_CN,
                                      MARKET_TYPE.FUTURE_CN]:
                                      
                self.market._settle(self.broker_name)

            self.broker.run(
                QA_Event(
                    event_type=ENGINE_EVENT.UPCOMING_DATA,
                    market_data=data
                )
            )
            # 生成 UPCOMING_DATA 事件放到 队列中去执行
            self.market.upcoming_data(self.broker_name, data)

            _date = date

        # 最后收盘的平仓
        self.market._settle(self.broker_name)
        self.after_success()

    def after_success(self):
        """called when all trading fininshed, for performance analysis
        """
        print('after success')
        for po in self.user.portfolio_list.values():
            for ac in po.accounts.values():

                print(ac.hold)

                print(ac.history_table)
                ac.save()
        self.stop()

    def stop(self):
        """stop all the market trade enging threads and all subthreads
        """

        self.market.trade_engine.stop_all()
        self.market.trade_engine.stop()


if __name__ == '__main__':
    backtest = QA_Backtest(
        market_type=MARKET_TYPE.STOCK_CN,
        frequence=FREQUENCE.DAY,
        start='2017-01-01',
        end='2017-01-10',
        code_list=['000001',
                   '600010'],
        commission_fee=0.00015
    )
    backtest._generate_account()
    backtest.start_market()
    backtest.run()

    # backtest.run()
