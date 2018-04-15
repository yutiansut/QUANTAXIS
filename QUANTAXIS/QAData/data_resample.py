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

from datetime import time

import pandas as pd

from QUANTAXIS.QAFetch import QA_fetch_get_stock_transaction


def QA_data_tick_resample(tick, type_='1min'):
    """tick采样成任意级别分钟线

    Arguments:
        tick {[type]} -- transaction

    Returns:
        [type] -- [description]
    """

    data = tick['price'].resample(
        type_, label='right', closed='left').ohlc()

    data['volume'] = tick['vol'].resample(
        type_, label='right', closed='left').sum()
    data['code'] = tick['code'][0]

    #data = pd.DataFrame()
    _temp = tick.drop_duplicates('date')['date']
    for item in _temp:
        _data = data[item]
        _data = _data[time(9, 31):time(11, 30)].append(
            _data[time(13, 1):time(15, 0)])
        data = data.append(_data)

    data['datetime'] = data.index
    data['date'] = data['datetime'].apply(lambda x: str(x)[0:10])

    return data.fillna(method='ffill').set_index(['datetime', 'code'], drop=False)


if __name__ == '__main__':
    tickz = QA_fetch_get_stock_transaction(
        'tdx', '000001', '2017-01-03', '2017-01-05')
    print(QA_data_tick_resample(tickz))
