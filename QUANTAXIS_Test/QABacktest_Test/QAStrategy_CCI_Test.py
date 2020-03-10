import QUANTAXIS as QA
from QAStrategy.qastockbase import QAStrategyStockBase
import QUANTAXIS as QA
import pprint
import talib
import numpy as np
import pandas as pd


class CCI_Strategy(QAStrategyStockBase):

    def on_bar(self, bar):
        print(bar)
        code = bar.name[1]
        print(self.get_positions(code))
        print(self.market_data)

        res = self.cci()
        # 股票基类没有 self.get_position(code)
        #self.positions = self.get_position(code)
        print(res.iloc[-1])

        if res.CCI[-1] < -100:

            #print('LONG')
            # 股票基类没有 elf.positions 仓位设定？ 依然没有一个能回测的成功案例
            if self.positions.volume_long == 0:
                self.send_order('BUY', 'OPEN', price=bar['close'], volume=1)

            if self.positions.volume_short > 0:
                self.send_order('BUY', 'CLOSE', price=bar['close'], volume=1)

        else:
            #print('SHORT')
            if self.positions.volume_short == 0:
                self.send_order('SELL', 'OPEN', price=bar['close'], volume=1)
            if self.positions.volume_long > 0:
                self.send_order('SELL', 'CLOSE', price=bar['close'], volume=1)

    def cci(self,):
        return QA.QA_indicator_CCI(self.market_data, 61)

    def risk_check(self):
        pass
        # pprint.pprint(self.qifiacc.message)


if __name__ == '__main__':
    user = QA.QA_User(username ='rgveda', password = '123456')
    portfolio=user.new_portfolio('cci_super_trend')
    account = portfolio.new_account(account_cookie='stock_cn_test1')

    strategy =CCI_Strategy(
        code=["000001", "000002", "600000"],
        frequence='day',
        strategy_id="QA_STRATEGY_DEMO",
        risk_check_gap=1,
        portfolio="cci_super_trend",
        start="2019-10-01",
        end="2020-03-09",)
    #strategy.debug()
    strategy.run_backtest()
