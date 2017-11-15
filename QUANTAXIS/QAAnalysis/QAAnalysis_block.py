# coding:utf-8

# 输入一个stock_list/stock_block
# 生成相关因子

import datetime

import pandas as pd

from QUANTAXIS.QAAnalysis.QAAnalysis_dataframe import QA_Analysis_stock
from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_stock_day_adv,
                                               QA_fetch_stock_min_adv,
                                               QA_fetch_stock_block_adv)
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_info
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_real_datelist


def get_gap_trade(gap):
    return QA_util_get_real_datelist(datetime.date.today() + datetime.timedelta(days=-int(gap)), datetime.date.today())


#from QUANTAXIS.QAAnalysis.QAAnalysis_dataframe import QA_Analysis_stock
class QA_Analysis_block():
    def __init__(self, block=None, block_name=None, *args, **kwargs):

        try:
            self.block_code = block.code
        except:
            self.block_code = block

        if block_name is not None:
            self.block_code = QA_fetch_stock_block_adv().get_block(block_name).code

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
        _start, _end = get_gap_trade(30)
        return self.market_data(_start, _end)

    def block_price(self, market_data=None):
        if market_data is None:
            market_data=self.month_data.to_qfq()
        else:
            market_data=market_data.to_qfq()
        return QA_Analysis_stock(market_data).price.groupby('date').mean()
    
    def block_pcg(self, market_data=None):
        return self.block_price(market_data).pct_change()

    def stock_turnover(self,market_data=None):
        if market_data is None:
            market_data=self.month_data.to_qfq()
        else:
            market_data=market_data.to_qfq()
        _data=market_data.data
        _info=self.stock_info()
        _data['ltgb']=_data.code.apply(lambda x: _info.liutongguben[x])
        _data['turnover']=100*_data['volume']/ _data['ltgb']
        return _data

    def block_turnover(self,market_data=None):
        return self.stock_turnover(market_data).turnover.groupby('date').mean()
    def stock_info(self):
        return pd.concat([QA_fetch_get_stock_info(item) for item in self.block_code]).set_index('code',drop=False)

    def res(self):
        import matplotlib.pyplot as plt
        self.block_pcg().plot()
        self.block_turnover().plot()
        plt.show()


    


if __name__ == "__main__":
    import QUANTAXIS as QA
    # print(get_this_week())
    ana = QA_Analysis_block(
        QA.QA_fetch_stock_block_adv().get_block('昨日涨停').code)
    print(ana.block_pcg())

    data=QA.QA_fetch_get_stock_info('tdx','000001')
    js=QA.QA_util_to_json_from_pandas(data)


    """
    计算换手率
    d=QA.QA_fetch_get_stock_day('tdx','000001','2017-11-14','2017-11-15','00').vol.values[0]*100  # 一手100股
    f=QA.QA_fetch_get_stock_info('tdx','000001').liutongguben.values[0]
    turnover=d/f
    """
    print(js)
