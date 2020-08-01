# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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

"""单线程的实时获取
""" 


from QUANTAXIS.QAFetch.QATdx import select_best_ip, QA_fetch_get_stock_day, QA_fetch_get_stock_list
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Stock_day
import pandas as pd
import datetime


def get_today_all(output='pd'):
    """today all

    Returns:
        [type] -- [description]
    """

    data = []
    today = str(datetime.date.today())
    codes = QA_fetch_get_stock_list('stock').code.tolist()
    bestip = select_best_ip()['stock']
    for code in codes:
        try:
            l = QA_fetch_get_stock_day(
                code, today, today, '00', ip=bestip)
        except:
            bestip = select_best_ip()['stock']
            l = QA_fetch_get_stock_day(
                code, today, today, '00', ip=bestip)
        if l is not None:
            data.append(l)

    res = pd.concat(data)
    if output in ['pd']:
        return res
    elif output in ['QAD']:
        return QA_DataStruct_Stock_day(res.set_index(['date', 'code'], drop=False))
