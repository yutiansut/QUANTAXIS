#coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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


from QUANTAXIS.QAFetch import QA_fetch_get_stock_day
import pandas as pd


def QA_data_fq_factor(code):
    bfq=QA_fetch_get_stock_day('ts',code,'1991-01-01','','00','pd')
    qfq=QA_fetch_get_stock_day('ts',code,'1991-01-01','','01','pd')
    hfq=QA_fetch_get_stock_day('ts',code,'1991-01-01','','02','pd')

    factor_frame=pd.DataFrame()
    factor_frame['qfqfactor']=qfq['open']/bfq['open']
    factor_frame['hfqfactor']=hfq['open']/bfq['open']
    #factor_frame['bfqfactor']=bfq['open']/bfq['open']
    return factor_frame