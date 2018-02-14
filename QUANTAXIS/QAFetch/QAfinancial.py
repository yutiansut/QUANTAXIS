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

import requests
from pytdx.reader.history_financial_reader import HistoryFinancialReader
from pytdx.crawler.history_financial_crawler import HistoryFinancialCrawler, HistoryFinancialListCrawler
"""
参见PYTDX 1.65
"""

FINANCIAL_URL = 'http://down.tdx.com.cn:8001/fin/gpcw.txt'


def get_filename():
    """
    get_filename
    """
    return [l[0] for l in [line.strip().split(",") for line in requests.get(FINANCIAL_URL).text.strip().split('\n')]]


def download():
    """
    会创建一个download/文件夹
    """
    result = get_filename()
    for item in result:
        r = requests.get('http://down.tdx.com.cn:8001/fin/{}'.format(item))
        with open(item, "wb") as code:
            code.write(r.content)


def get_and_parse(filename):
    return HistoryFinancialReader.get_df(filename)
