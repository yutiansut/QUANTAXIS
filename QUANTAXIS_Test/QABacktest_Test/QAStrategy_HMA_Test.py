import QUANTAXIS as QA
from QAStrategy.qastockbase import QAStrategyStockBase
import QUANTAXIS as QA
import pprint
import talib
import numpy as np
import pandas as pd


def Timeline_Integral_with_cross_before(Tm,):
    """
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)不清零，金叉(0-->1)清零)
    """
    T = [Tm[0]]
    for i in range(1,len(Tm)):
        T.append(T[i - 1] + 1) if (Tm[i] != 1) else T.append(0)
    return np.array(T)


def hma_cross_func(data):
    """
    HMA均线金叉指标
    """
    HMA10 = talib.WMA(2 * talib.WMA(data.close, int(10 / 2)) - talib.WMA(data.close, 10), int(np.sqrt(10)))
    MA30 = talib.MA(data.close, 30)
    
    MA30_CROSS = pd.DataFrame(columns=['MA30_CROSS', 'MA30_CROSS_JX', 'MA30_CROSS_SX'], index=data.index)
    MA30_CROSS_JX = CROSS(HMA10, MA30)
    MA30_CROSS_SX = CROSS(MA30, HMA10)
    MA30_CROSS['MA30_CROSS'] = 1 if (MA30_CROSS_JX == 1) else (-1 if (MA30_CROSS_SX == 1) else 0)
    MA30_CROSS['MA30_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_CROSS_JX)
    MA30_CROSS['MA30_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_CROSS_SX)
    MA30_CROSS['HMA_RETURN'] = np.log(HMA10 / pd.Series(HMA10).shift(1))
    return MA30_CROSS


class HMA_Strategy(QAStrategyStockBase):

    def on_bar(self, data):
        print(data)
        print(self.get_positions('000001'))
        print(self.market_data)
        
        code = data.name[1]
        print('---------------under is 当前全市场的market_data --------------')
        
        print(self.get_current_marketdata())
        print('---------------under is 当前品种的market_data --------------')
        print(self.get_code_marketdata(code))
        print(code)
        print(self.running_time)
        #input()

        #res = self.hma(data)
        #print(res.iloc[-1])

        #if (res.HMA_CROSS['HMA_RETURN'][-1] > 0) and (res.HMA_CROSS['MA30_CROSS_JX'][-1] < res.HMA_CROSS['MA30_CROSS_SX'][-1]):
        #    print('LONG')
        #    if self.positions.volume_long == 0:
        #        self.send_order('BUY', 'OPEN', price=bar['close'], volume=1)

        #    if self.positions.volume_short > 0:
        #        self.send_order('BUY', 'CLOSE', price=bar['close'], volume=1)
        #elif (res.HMA_CROSS['HMA_RETURN'][-1] < 0) and (res.HMA_CROSS['MA30_CROSS_JX'][-1] > res.HMA_CROSS['MA30_CROSS_SX'][-1]):
        #    print('SHORT')
        #    if self.positions.volume_short == 0:
        #        self.send_order('SELL', 'OPEN', price=bar['close'], volume=1)
        #    if self.positions.volume_long > 0:
        #        self.send_order('SELL', 'CLOSE', price=bar['close'], volume=1)

    def hma(self, data):
        # 这里我想加一个add_func的指标，不知道怎么做
        print(data)
        klines = QA.QA_DataStruct_Stock_day(data)
        return pd.DataFrame({'HMA_CROSS': klines.add_func(hma_cross_func)})


    def risk_check(self):
        pass
        # pprint.pprint(self.qifiacc.message)


if __name__ == '__main__':
    user = QA.QA_User(username ='rgveda', password = '123456')
    portfolio=user.new_portfolio('hma_super_trend')
    account = portfolio.new_account(account_cookie='stock_cn_test1')

    strategy =HMA_Strategy(
        code=["000001", "000002", "600000"],
        frequence='day',
        strategy_id="QA_STRATEGY_DEMO",
        risk_check_gap=1,
        portfolio="hma_super_trend",
        start="2019-10-01",
        end="2020-03-09",)
    #strategy.debug()
    strategy.run_backtest()
