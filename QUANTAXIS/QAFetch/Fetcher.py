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
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE


class QA_Fetcher():
    def __init__(self):
        self.datasouce = {'wind': QAWind, 'tushare': QATushare,
                          'tdx': QATdx, 'ths': QAThs, 'mongo': QAMongo}

    def fetch(self, code, start, end, frequence, securitytype, source):
        """一个统一的fetch
        
        Arguments:
            code {[type]} -- 证券/股票的代码
            start {[type]} -- 开始日期
            end {[type]} -- 结束日期
            frequence {[type]} -- 频率()
            securitytype {[type]} -- [description]
            source {[type]} -- [description]
        """

        pass
