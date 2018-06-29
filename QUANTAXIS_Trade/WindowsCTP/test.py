
import datetime
import logging
import math
import multiprocessing as mp
import os
import pickle
import shutil

import numpy as np
import pandas as pd

from ParadoxTrading.Chart import Wizard
from ParadoxTrading.Engine import (MarketEvent, SettlementEvent,
                                   StrategyAbstract)
from ParadoxTrading.EngineExt.Futures import (BacktestEngine,
                                              BacktestMarketSupply,
                                              CTAEqualFundPortfolio,
                                              CTAEqualRiskATRPortfolio,
                                              CTAEqualRiskGARCHPortfolio,
                                              InterDayBacktestExecution,
                                              InterDayPortfolio)
from ParadoxTrading.EngineExt.Futures.Trend import CTAStatusType, CTAStrategy
from ParadoxTrading.Fetch.ChineseFutures import (FetchDominantIndex,
                                                 FetchInstrumentDayData,
                                                 FetchProductIndex,
                                                 RegisterIndex)
from ParadoxTrading.Indicator import (BIAS, CCI, EFF, EMA, KDJ, MA, RSI, SAR,
                                      BBands, StepDrawdownStop)
from ParadoxTrading.Utils import DataStruct


class GetTradingday(object):

    def __init__(self, _start, _end, _symbol='a'):
        self.start = _start
        self.end = _end
        self.symbol = _symbol
        self.fetcherindex = FetchProductIndex()
        self.fetcherindex.psql_host = '192.168.4.103'
        self.fetcherindex.psql_user = 'ubuntu'
        self.fetcherindex.mongo_host = '192.168.4.103'

    def gettradingday(self):
        market_data = self.fetcherindex.fetchDayData(
            self.start, self.end, self.symbol)
        tradingday_list = market_data['tradingday']
        return tradingday_list


fetcher = FetchInstrumentDayData()
fetcher.psql_host = '192.168.4.103'
fetcher.psql_user = 'ubuntu'
fetcher.mongo_host = '192.168.4.103'


start = '20150101'
end = '20180428'
get_tradingday = GetTradingday(start, end)
tradingday_list = get_tradingday.gettradingday()

symbollist = ['oi', 'y']
for symbol in symbollist:

    data_df = pd.DataFrame()
    for index in range(1, len(tradingday_list)):

        pricelist = []
        day = tradingday_list[index]
        yesterday = tradingday_list[index-1]
        domian_instrument = fetcher.fetchDominant(symbol, day)
        data = fetcher.fetchDayData(yesterday, day, domian_instrument)

        pricelist.append(data['tradingday'][0])
        pricelist.append(data['openprice'][0])
        pricelist.append(data['highprice'][0])
        pricelist.append(data['lowprice'][0])
        pricelist.append(data['closeprice'][0])

        df = pd.DataFrame(pricelist).T
        df.columns = ['tradingday', 'openprice',
                      'highprice', 'lowprice', 'closeprice']
        data_df = pd.concat([data_df, df])

    pd.DataFrame.to_csv(data_df, '.\\data\\{0}.csv'.format(symbol))
