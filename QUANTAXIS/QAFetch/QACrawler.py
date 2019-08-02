# coding: utf-8
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


import pandas as pd
from QUANTAXIS.QAUtil.QADate_trade import trade_date_sse
from QUANTAXIS.QAUtil.QADate import QA_util_date_str2int

_sh_url = 'http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk{}.xls'
_sz_url = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1837_xxpl&txtDate={}&tab2PAGENO=1&ENCODE=1&TABKEY=tab2'


def QA_fetch_get_sh_margin(date):
    """return shanghai margin data

    Arguments:
        date {str YYYY-MM-DD} -- date format

    Returns:
        pandas.DataFrame -- res for margin data
    """
    if date in trade_date_sse:
        data= pd.read_excel(_sh_url.format(QA_util_date_str2int
                                            (date)), 1).assign(date=date).assign(sse='sh')             
        data.columns=['code','name','leveraged_balance','leveraged_buyout','leveraged_payoff','margin_left','margin_sell','margin_repay','date','sse']
        return data
    else:
        pass


def QA_fetch_get_sz_margin(date):
    """return shenzhen margin data

    Arguments:
        date {str YYYY-MM-DD} -- date format

    Returns:
        pandas.DataFrame -- res for margin data
    """

    if date in trade_date_sse:
        return pd.read_excel(_sz_url.format(date)).assign(date=date).assign(sse='sz')

#http://data.eastmoney.com/zjlx/002433.html
def QA_fetch_zjlx(code=None):
    #获取资金流向



    pass

if __name__ == "__main__":
    print(QA_fetch_get_sz_margin('2018-01-25'))
    print(QA_fetch_get_sh_margin('2018-01-25'))
