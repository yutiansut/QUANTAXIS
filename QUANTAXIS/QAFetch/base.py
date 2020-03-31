# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
        #   'If-Modified-Since': 'Thu, 11 Jan 2018 07:05:01 GMT',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}


def _select_bond_market_code(code):

    if code[0:3] in ['101', '104', '105', '106', '107', '108', '109',
                        '111', '112', '114', '115', '116', '117', '118', '119',
                        '123', '127', '128',
                        '131', '139', ]:
        return 0
    else:
        return 1

def _select_market_code(code):
    """
    1- sh
    0 -sz
    """
    code = str(code)
    if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
        return 1
    return 0


def _select_index_code(code):
    """
    1 - sh
    0 - sz
    """
    code = str(code)
    if code[0] == '3':
        return 0
    return 1

def get_stock_market(code):
    return 'SH' if _select_market_code(code) == 1 else 'SZ'


def _select_type(frequence):
    if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
        frequence = 9
    elif frequence in ['w', 'W', 'Week', 'week']:
        frequence = 5
    elif frequence in ['month', 'M', 'm', 'Month']:
        frequence = 6
    elif frequence in ['Q', 'Quarter', 'q']:
        frequence = 10
    elif frequence in ['y', 'Y', 'year', 'Year']:
        frequence = 11
    elif str(frequence) in ['5', '5m', '5min', 'five']:
        frequence, type_ = 0, '5min'
    elif str(frequence) in ['1', '1m', '1min', 'one']:
        frequence, type_ = 8, '1min'
    elif str(frequence) in ['15', '15m', '15min', 'fifteen']:
        frequence, type_ = 1, '15min'
    elif str(frequence) in ['30', '30m', '30min', 'half']:
        frequence, type_ = 2, '30min'
    elif str(frequence) in ['60', '60m', '60min', '1h']:
        frequence, type_ = 3, '60min'

    return frequence