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

def QA_data_tick_resample_1min(tick, type_='1min'):
    """
    tick 采样为 分钟数据
    1. 仅使用将 tick 采样为 1 分钟数据
    2. 仅测试过，与通达信 1 分钟数据达成一致
    3. 经测试，可以匹配 QA.QA_fetch_get_stock_transaction 得到的数据，其他类型数据未测试
    demo:
    df = QA.QA_fetch_get_stock_transaction(package='tdx', code='000001', 
                                           start='2018-08-01 09:25:00',
                                           end='2018-08-03 15:00:00')
    df_min = QA_data_tick_resample_1min(df)
    """
    tick = tick.assign(amount=tick.price*tick.vol)
    resx = pd.DataFrame()
    _dates = set(tick.date)

    for date in sorted(list(_dates)):
        _data = tick.loc[tick.date==date]
        # morning min bar
        _data1 = _data[time(9, 25): time(11, 30)].resample(
                type_, closed='left', base=30, loffset=type_).apply({'price': 'ohlc', 'vol': 'sum', 'code': 'last', 'amount': 'sum'})
        _data1.columns = _data1.columns.droplevel(0)
        # do fix on the first and last bar
        _data1.loc[time(9, 31): time(9, 31), 'open'] = _data1.loc[time(9, 26): time(9, 26), 'open'].values
        _data1.loc[time(9, 31): time(9, 31), 'high'] = _data1.loc[time(9, 26): time(9, 31), 'high'].max()
        _data1.loc[time(9, 31): time(9, 31), 'low'] = _data1.loc[time(9, 26): time(9, 31), 'low'].min()
        _data1.loc[time(9, 31): time(9, 31), 'vol'] = _data1.loc[time(9, 26): time(9, 31), 'vol'].sum()
        _data1.loc[time(9, 31): time(9, 31), 'amount'] = _data1.loc[time(9, 26): time(9, 31), 'amount'].sum()
        _data1.loc[time(11, 30): time(11, 30), 'vol'] = _data1.loc[time(11, 30): time(11, 31), 'vol'].sum()
        _data1.loc[time(11, 30): time(11, 30), 'amount'] = _data1.loc[time(11, 30): time(11, 31), 'amount'].sum()
        _data1 = _data1.loc[time(9, 31): time(11, 30)]

        # afternoon min bar
        _data2 = _data[time(13,0): time(15,0)].resample(
                type_, closed='left', base=30, loffset=type_).apply({'price': 'ohlc', 'vol': 'sum', 'code': 'last', 'amount': 'sum'})
        print(_data2)
        _data2.loc[time(15, 0): time(15, 0)] = _data2.loc[time(15, 1): time(15, 1)].values
        _data2 = _data2.loc[time(13, 1): time(15, 0)]
        _data2.columns = _data2.columns.droplevel(0)
        resx = resx.append(_data1).append(_data2)
        print(resx)
    return resx.reset_index().drop_duplicates().set_index(['datetime', 'code'])


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
