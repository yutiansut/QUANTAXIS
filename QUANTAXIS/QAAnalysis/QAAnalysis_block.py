# coding:utf-8

import datetime
from functools import lru_cache

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

from QUANTAXIS.QAAnalysis.QAAnalysis_dataframe import QAAnalysis_stock
from QUANTAXIS.QAData.data_marketvalue import QA_data_marketvalue
from QUANTAXIS.QAFetch.Fetcher import QA_quotation
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_info
from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_stock_block_adv,
                                               QA_fetch_stock_day_adv,
                                               QA_fetch_stock_min_adv)
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_info
from QUANTAXIS.QAFetch.QATdx_adv import QA_Tdx_Executor
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_real_datelist
from QUANTAXIS.QAUtil.QAParameter import (DATASOURCE, FREQUENCE, MARKET_TYPE,
                                          OUTPUT_FORMAT)


def get_gap_trade(gap):
    return QA_util_get_real_datelist(datetime.date.today() + datetime.timedelta(days=-int(gap)), datetime.date.today())


#from QUANTAXIS.QAAnalysis.QAAnalysis_dataframe import QAAnalysis_stock
class QAAnalysis_block():
    def __init__(self, code=[], name=None, start=None, end=None, frequence=FREQUENCE.DAY,  *args, **kwargs):

        self.code = code
        self.start = start
        self.end = end
        self.frequence = frequence
        self.name = name

    def __repr__(self):
        return '< QAAnalysis_Block {} with {} code >'.format(self.name, len(self.code))

    @property
    @lru_cache()
    def market_data(self):
        return QA_quotation(self.code, self.start, self.end, self.frequence,
                            market=MARKET_TYPE.STOCK_CN, source=DATASOURCE.MONGO, output=OUTPUT_FORMAT.DATASTRUCT).to_qfq()

    @property
    @lru_cache()
    def market_value(self):
        return QA_data_marketvalue(self.market_data.data)

    @property
    def week_data(self):
        'this weekly data'
        'return a QUANTAXIS DATASTRUCT'

        return self.market_data.to_week()

    @property
    def month_data(self):
        'this monthly data'
        'return a QUANTAXIS DATASTRUCT'

        return self.market_data.to_month()

    def block_index(self, methods='mv'):
        
        if methods == 'mv':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x.close, weights=x.shares))
        elif methods == 'lv':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x.close, weights=x.lshares))
        elif methods == 'close':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x.close))
        elif methods == 'volume':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x.close, weights=x.volume))
        else:
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x.close, weights=x.shares))
            print(
                'wrong methods: only support [mv,lv,close,volume] methods \n use default mv methods')

        return res/res.iloc[0]*1000

    def stock_turnover(self):

        return self.market_value.volume/self.market_value.lshares

    def block_turnover(self):
        return self.stock_turnover().groupby(level=0).mean()

    def plot_index(self, methods='mv'):
        block_index=self.block_index('close')
        def format_date(x, pos=None):
            # 保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示
            thisind = np.clip(int(x+0.5), 0, N-1)
            # print(thisind)
            return block_index.index[thisind].strftime('%Y-%m-%d %H:%M')
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(1, 1, 1)
        plt.style.use('ggplot')

        plt.title('QUANTAXIS BLOCK ANA {}'.format(
            self.name), fontproperties="SimHei")
        N = len(block_index)
        block_index.reset_index()[0].plot()
        self.block_index('lv').reset_index()[0].plot()
        self.block_index('close').reset_index()[0].plot()
        self.block_index('volume').reset_index()[0].plot()
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        plt.legend(['market_value', 'liquidity_value', 'close', 'volume'])
        plt.show()


if __name__ == "__main__":
    import QUANTAXIS as QA
    ana = QAAnalysis_block(
        QA.QA_fetch_stock_block_adv().get_block('国产软件').code, '国产软件', '2018-01-01', '2018-08-21')
    ana.plot_index()

    ana = QAAnalysis_block(['000001', '000002', '600356'],
                           '自定义', '2018-01-01', '2018-08-21')
    ana.plot_index()

    ana = QAAnalysis_block(['000001', '000002', '600356'],
                           '自定义15分钟级别指数', '2018-08-01', '2018-08-21', FREQUENCE.FIFTEEN_MIN)
    ana.plot_index()
