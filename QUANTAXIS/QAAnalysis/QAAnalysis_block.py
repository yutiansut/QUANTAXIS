# coding:utf-8

# 输入一个stock_list/stock_block
# 生成相关因子

import datetime

import pandas as pd

from QUANTAXIS.QAAnalysis.QAAnalysis_dataframe import QAAnalysis_stock
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_info
from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_stock_block_adv,
                                               QA_fetch_stock_day_adv,
                                               QA_fetch_stock_min_adv)
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_info
from QUANTAXIS.QAFetch.QATdx_adv import QA_Tdx_Executor
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_real_datelist


def get_gap_trade(gap):
    return QA_util_get_real_datelist(datetime.date.today() + datetime.timedelta(days=-int(gap)), datetime.date.today())


#from QUANTAXIS.QAAnalysis.QAAnalysis_dataframe import QAAnalysis_stock
class QAAnalysis_block():
    def __init__(self, block=None, block_name=None, lens=90, *args, **kwargs):

        try:
            self.block_code = block.code
        except:
            self.block_code = block

        if block_name is not None:
            self.block_code = QA_fetch_stock_block_adv().get_block(block_name).code
        self.lens = lens
        # self.Executor=QA_Tdx_Executor()


    def __repr__(self):
        return '< QAAnalysis_Block >'

    def market_data(self, start, end, _type='day'):
        return QA_fetch_stock_day_adv(self.block_code, start, end)

    @property
    def week_data(self):
        'this weekly data'
        'return a QUANTAXIS DATASTRUCT'
        _start, _end = get_gap_trade(7)
        return self.market_data(_start, _end)

    @property
    def month_data(self):
        'this monthly data'
        'return a QUANTAXIS DATASTRUCT'
        _start, _end = get_gap_trade(90)
        return self.market_data(_start, _end)

    @property
    def _data(self):
        _start, _end = get_gap_trade(self.lens)
        return self.market_data(_start, _end)

    def block_price(self, market_data=None):
        if market_data is None:
            market_data = self._data.to_qfq()
        else:
            market_data = market_data.to_qfq()
        return QAAnalysis_stock(market_data).price.groupby('date').mean()

    def block_pcg(self, market_data=None):
        if market_data is None:
            market_data = self._data.to_qfq()
        else:
            market_data = market_data.to_qfq()
        return QAAnalysis_stock(market_data).day_pct_change.groupby('date').mean()

    def stock_turnover(self, market_data=None):
        if market_data is None:
            market_data = self._data.to_qfq()
        else:
            market_data = market_data.to_qfq()
        _data = market_data.data
        _info = self.stock_info()
        _data['ltgb'] = _data.code.apply(lambda x: _info.liutongguben[x])
        _data['turnover'] = 100 * _data['volume'] / _data['ltgb']
        return _data

    def block_turnover(self, market_data=None):
        return self.stock_turnover(market_data).turnover.groupby('date').mean()

    def stock_info(self):
        data = []

        for item in self.block_code:
            try:
                _data = QA_fetch_stock_info(item)
            except:
                _data = QA_fetch_get_stock_info(item)
            data.append(_data)

        return pd.concat(data).set_index('code', drop=False)

    def res(self):
        import matplotlib.pyplot as plt
        self.block_pcg().plot()
        self.block_turnover().plot()
        plt.show()



class QAAnalysis_codewithblock():
    def __init__(self, block):
        self.block = block
        self.code = block.code





if __name__ == "__main__":
    import QUANTAXIS as QA
    # print(get_this_week())
    ana = QAAnalysis_block(
        QA.QA_fetch_stock_block_adv().get_block('昨日涨停').code)

    """
    计算换手率
    d=QA.QA_fetch_get_stock_day('tdx','000001','2017-11-14','2017-11-15','00').vol.values[0]*100  # 一手100股
    f=QA.QA_fetch_get_stock_info('tdx','000001').liutongguben.values[0]
    turnover=d/f
    """
    # print(js)

    x = []
    y = []
    block = QA.QA_fetch_stock_block_adv().getdtype('gn').block_name
    for item in block:
        print(item)
        data = QAAnalysis_block(block_name=item)
        x.append(data.block_pcg())
        y.append(data.block_turnover())
    print(len(x))
    print(len(y))
