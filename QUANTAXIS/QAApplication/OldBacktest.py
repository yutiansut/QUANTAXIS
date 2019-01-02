# @Hakase
import QUANTAXIS as QA
import numpy as np
import pandas as pd
import datetime
import sys
import random


class backtest():
    """依据回测场景的建模

    """

    def __init__(self, start_time='2015-01-01', end_time='2018-09-24', init_cash=500000, code='RBL8', frequence=QA.FREQUENCE.FIFTEEN_MIN):
        self.start_time = start_time
        self.end_time = end_time
        self.frequence = frequence
        self.code = code
        self.init_cach = init_cash
        self.time_ = None
        self.market_data_ = None
        self.res = False

    @property
    def position(self):
        return self.account.sell_available.get(self.code, 0)

    @property
    def time(self):
        return self.time_

    @property
    def market_data(self):
        return self.market_data_
    # 自定义函数-------------------------------------------------------------------

    @property
    def hold_judge(self):
        """仓位判断器

        Returns:
            [type] -- [description]
        """

        if self.account.cash/self.account.init_cash < 0.3:
            return False
        else:
            return True

    def before_backtest(self):
        raise NotImplementedError

    def before(self, *args, **kwargs):
        self.before_backtest()
        self.data_min = QA.QA_fetch_future_min_adv(
            self.code, self.start_time, self.end_time, frequence=self.frequence)

        self.data_day = QA.QA_fetch_future_day_adv(
            self.code, self.start_time, self.end_time)

        self.Broker = QA.QA_BacktestBroker()

    def model(self, *arg, **kwargs):
        raise NotImplementedError

    def load_strategy(self, *arg, **kwargs):
        # self.load_model(func1)
        raise NotImplementedError

    def run(self, *arg, **kwargs):
        raise NotImplementedError

    def buy(self, pos, towards):

        self.account.receive_simpledeal(code=self.code,
                                        trade_price=self.market_data.open, trade_amount=pos,
                                        trade_towards=towards, trade_time=self.time,
                                        message=towards)

    def sell(self, pos, towards):
        self.account.receive_simpledeal(code=self.code,
                                        trade_price=self.market_data.open, trade_amount=pos,
                                        trade_towards=towards, trade_time=self.time,
                                        message=towards)

    def main(self,  *arg, **kwargs):
        print(vars(self))
        self.identity_code = '_'.join([str(x) for x in list(kwargs.values())])

        self.backtest_cookie = 'future_{}_{}'.format(
            datetime.datetime.now().time().__str__()[:8], self.identity_code)
        self.account = QA.QA_Account(allow_sellopen=True, allow_t0=True, account_cookie=self.backtest_cookie,
                                     market_type=QA.MARKET_TYPE.FUTURE_CN, frequence=self.frequence, init_cash=self.init_cash)

        self.gen = self.data_min.reindex(
            self.res) if self.res else self.data_min

        for ind, item in self.gen.iterrows:
            self.time_ = ind[0]
            self.code = ind[1]

            self.market_data_ = item
            self.run()
