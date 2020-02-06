# coding=utf-8
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


import csv
import pandas as pd
import QUANTAXIS as QA


_haitong_traderecord = ['成交日期', '证券代码', '证券名称', '买卖标志', '成交价格', '成交数量', '成交金额', '印花税(￥)', '交易征费￥)',
                        '交易费(￥)', '股份交收费(￥)', '佣金(￥)', '交易系统使用费(￥)', '总费用(￥)', '成交编号', '股东代码', '成交时间']


_haitong_traderecord_eng = ['date', 'code', 'name', 'towards', 'price', 'volume', 'money', 'tax_fee', 'sectrade_fee', 'trde_fee', 'stock_fee',
                            'stock_settlement_fee', 'commission_fee', 'tradesys_fee', 'total_fee', 'trade_id', 'shareholder', 'datetime']


def QA_fetch_get_tdxtraderecord(file):
    """
    QUANTAXIS 读取历史交易记录 通达信 历史成交-输出-xlsfile--转换csvfile
    """
    try:
        with open('./20180606.csv', 'r') as f:
            l = csv.reader(f)
            data = [item for item in l]

        res = pd.DataFrame(data[1:], columns=data[0])
        return res
    except:
        raise IOError('QA CANNOT READ THIS RECORD')
