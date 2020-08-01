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
"""QUANTAXIS 的error类

"""


class QAError_fetch_data(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'QA FETCH DATA ERROR', res)


class QAError_no_data_in_database(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'QA FETCH NO DATA ERROR', res)


class QAError_crawl_data_web(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'QA CRAWLER ERROR', res)


class QAError_database_connection(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'QA DATABASE CONNECTION ERROR', res)


class QAError_web_connection(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'QA WEB CONNECTION ERROR', res)


class QAError_market_enging_down(RuntimeError):
    def __init__(self, res):
        RuntimeError.__init__(self, 'QA MARKET ENGING DOWN ERROR', res)
