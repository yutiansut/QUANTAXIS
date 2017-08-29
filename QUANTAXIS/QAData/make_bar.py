# coding:utf-8
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

from QUANTAXIS.QAUtil import QA_util_make_bar
from QUANTAXIS.QAFetch import QA_fetch_get_stock_transaction
from datetime import time


def QA_data_tick_resample(tick,type='1min'):
    

    data_ = QA_util_make_bar(type, str(tick.index[0])[
                             0:10], str(tick.index[-1])[0:10])
    data = tick['price'].resample(type, label='right').ohlc()
    data['volume'] = tick['vol'].resample(type, label='right').sum()

    data = data.reindex(data_.index)
    return data


if __name__ == '__main__':
    tick = QA_fetch_get_stock_transaction(
        'tdx', '000001', '2017-01-03', '2017-01-05')
    print(QA_data_tick_resample(tick))
