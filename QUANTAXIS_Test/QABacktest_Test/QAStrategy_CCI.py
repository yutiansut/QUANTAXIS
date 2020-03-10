import QUANTAXIS as QA
from QAStrategy.qastockbase import QAStrategyStockBase
import QUANTAXIS as QA
import pprint


class CCI(QAStrategyStockBase):

    def on_bar(self, data):
        print(data)
        print(self.get_positions('000001'))
        print(self.market_data)
        
        code = data.name[1]
        print('---------------under is 当前全市场的market_data --------------')
        print(self.market_data.sort_index(level=[0, 1], ascending=[1, 0], inplace=True))
        print(self.market_data.loc[(self.running_time, slice(None)), :])
        print(self.get_current_marketdata())
        print('---------------under is 当前品种的market_data --------------')
        print(self.get_code_marketdata(code))
        print(code)
        #print(self.running_time)

if __name__ == '__main__':
    strategy =CCI(
        code=["000001", "000002", "600000"],
        frequence='day',
        strategy_id="QA_STRATEGY_DEMO",
        risk_check_gap=1,
        portfolio="QA_DEMO",
        start="2019-07-02 09:30:00",
        end="2019-07-05 15:00:00",)
    strategy.debug()
    strategy.run_backtest()
