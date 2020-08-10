# coding=utf-8
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

from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Stock_transaction
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_transaction, QA_fetch_get_future_transaction_realtime
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_info


class QAAnalysis_Transaction():
    def __init__(self):
        self.data = None
        self.code = None
        self.stock_info = None

    def get_data(self, code, start, end):
        self.code = code
        try:
            self.data = QA_DataStruct_Stock_transaction(
                QA_fetch_get_stock_transaction(code, start, end))
            return self.data
        except Exception as e:
            raise e

    def get_stock_info(self, code):
        try:
            self.stock_info = QA_fetch_stock_info(code)
        except Exception as e:
            raise e

    def winner(self):
        pass
