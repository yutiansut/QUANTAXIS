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


"""QUANTAXIS访问获取QAWEB的行情

233333 结果变成自己访问自己了
"""
import  pandas as pd
from QUANTAXIS.QAUtil.QACode import QA_util_code_tostr


def QA_fetch_get_stock_day(code, start, end, ip='192.168.0.1', port='8010'):
    pass
    # requests.get(


def QA_fetch_get_stock_block():
    """ths的版块数据

    Returns:
        [type] -- [description]
    """

    url = 'http://data.yutiansut.com/self_block.csv'
    try:
        bl = pd.read_csv(url)
        return bl.assign(code=bl['证券代码'].apply(QA_util_code_tostr), blockname=bl['行业'], name=bl['证券名称'], source='outside', type='outside').set_index('code', drop=False)
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    print(QA_fetch_get_stock_block())