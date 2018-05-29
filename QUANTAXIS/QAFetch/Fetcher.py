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
from QUANTAXIS.QAFetch import QAQuery
from QUANTAXIS.QAFetch import QAQuery_Advance as QAQueryAdv
from QUANTAXIS.QAFetch import QAEastMoney as QAEM
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE, DATASOURCE, OUTPUT_FORMAT, DATABASE_TABLE
from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting


class QA_Fetcher():
    def __init__(self, ip='127.0.0.1', port=27017, username='',password=''):
        """
        初始化的时候 会初始化
        """
        self.ip = ip
        self.port = port
        self.database = QA_util_sql_mongo_setting(ip, port).quantaxis
        self.history = {}
        self.best_ip=QATdx.select_best_ip()

    def change_ip(self, ip, port):
        self.database = QA_util_sql_mongo_setting(ip, port).quantaxis
        return self

    def get_quotation(self, code=None, start=None, end=None, frequence=None, market=None, source=None, output=None):
        """        
        Arguments:
            code {str/list} -- 证券/股票的代码
            start {str} -- 开始日期
            end {str} -- 结束日期
            frequence {enum} -- 频率 QA.FREQUENCE
            market {enum} -- 市场 QA.MARKET_TYPE
            source {enum} -- 来源 QA.DATASOURCE
            output {enum} -- 输出类型 QA.OUTPUT_FORMAT
        """
        pass

    def get_info(self,code,frequence,market,source,output):
        if source is DATASOURCE.TDX:
            res=QATdx.QA_fetch_get_stock_info(code,self.best_ip)
            return res
        elif source is DATASOURCE.MONGO:
            res=QAQuery.QA_fetch_stock_info(code,format=output,collections=self.database.stock_info)
            return res

def QA_quotation(code, start, end, frequence, market, source, output):
    """一个统一的fetch

    Arguments:
        code {str/list} -- 证券/股票的代码
        start {str} -- 开始日期
        end {str} -- 结束日期
        frequence {enum} -- 频率 QA.FREQUENCE
        market {enum} -- 市场 QA.MARKET_TYPE
        source {enum} -- 来源 QA.DATASOURCE
        output {enum} -- 输出类型 QA.OUTPUT_FORMAT

    """
    if market is MARKET_TYPE.STOCK_CN:
        if frequence is FREQUENCE.DAY:
            if source is DATASOURCE.MONGO:
                res = QAQueryAdv.QA_fetch_stock_day_adv(code, start, end)
            elif source is DATASOURCE.TDX:
                res = QATdx.QA_fetch_get_stock_day(code, start, end, '00')
            elif source is DATASOURCE.TUSHARE:
                res = QATushare.QA_fetch_get_stock_day(code, start, end, '00')
        elif frequence in [FREQUENCE.ONE_MIN, FREQUENCE.FIVE_MIN, FREQUENCE.FIFTEEN_MIN, FREQUENCE.THIRTY_MIN, FREQUENCE.SIXTY_MIN]:
            if source is DATASOURCE.MONGO:
                res = QAQueryAdv.QA_fetch_stock_min_adv(
                    code, start, end, frequence=frequence)
            elif source is DATASOURCE.TDX:
                res = QATdx.QA_fetch_get_stock_min(
                    code, start, end, frequence=frequence)
        elif frequence is FREQUENCE.TICK:
            if source is DATASOURCE.TDX:
                res = QATdx.QA_fetch_get_stock_transaction(code, start, end)
    #print(type(res))
    return res


if __name__ == '__main__':
    print(QA_quotation('000001', '2017-01-01', '2017-01-31', frequence=FREQUENCE.DAY,
                       market=MARKET_TYPE.STOCK_CN, source=DATASOURCE.TDX, output=OUTPUT_FORMAT.DATAFRAME))
