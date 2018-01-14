# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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

"""
QA fetch module

@yutiansut

QAFetch is Under [QAStandard#0.0.2@10x] Protocol


"""
from QUANTAXIS.QAFetch import QAWind as QAWind
from QUANTAXIS.QAFetch import QATushare as QATushare
from QUANTAXIS.QAFetch import QATdx as QATdx
from QUANTAXIS.QAFetch import QAThs as QAThs
from QUANTAXIS.QAFetch import QAQuery_Advance as QAMongo
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE, DATASOURCE, OUTPUT_FORMAT


def QA_fetch(code, start, end, frequence, market, source, output):
    """一个统一的fetch

    Arguments:
        code {[type]} -- 证券/股票的代码
        start {[type]} -- 开始日期
        end {[type]} -- 结束日期
        frequence {[type]} -- 频率()
        market {[type]} -- 市场
        source {[type]} -- 来源


    """
    if market is MARKET_TYPE.STOCK_CN:
        if frequence is FREQUENCE.DAY:
            if source is DATASOURCE.MONGO:
                res = QAMongo.QA_fetch_stock_day_adv(code, start, end)
            elif source is DATASOURCE.TDX:
                res = QATdx.QA_fetch_get_stock_day(code, start, end, '00')
            elif source is DATASOURCE.TUSHARE:
                res = QATushare.QA_fetch_get_stock_day(code, start, end, '00')
        elif frequence in [FREQUENCE.ONE_MIN, FREQUENCE.FIVE_MIN, FREQUENCE.FIFTEEN_MIN, FREQUENCE.THIRTY_MIN, FREQUENCE.SIXTY_MIN]:
            if source is DATASOURCE.MONGO:
                res = QAMongo.QA_fetch_stock_min_adv(
                    code, start, end, type_=frequence)
            elif source is DATASOURCE.TDX:
                res = QATdx.QA_fetch_get_stock_min(
                    code, start, end, level=frequence)
        elif frequence is FREQUENCE.TICK:
            if source is DATASOURCE.TDX:
                res = QATdx.QA_fetch_get_stock_transaction(code, start, end)

    return res


if __name__ == '__main__':
    print(QA_fetch('000001', '2017-01-01', '2017-01-31', frequence=FREQUENCE.DAY,
                   market=MARKET_TYPE.STOCK_CN, source=DATASOURCE.TDX, output=OUTPUT_FORMAT.DATAFRAME))
