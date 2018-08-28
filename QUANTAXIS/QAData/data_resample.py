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


def QA_data_tick_resample(tick, type_='1min'):
    """tick采样成任意级别分钟线

    Arguments:
        tick {[type]} -- transaction

    Returns:
        [type] -- [description]
    """

    resx = pd.DataFrame()
    _temp = set(tick.index.date)
    for item in _temp:
        _data = tick.loc[str(item)]
        _data1 = _data[time(9, 31):time(11, 30)].resample(
            type_, closed='right', base=30, loffset=type_).apply({'price': 'ohlc', 'vol': 'sum'})

        _data2 = _data[time(13, 1):time(15, 0)].resample(
            type_, closed='right', loffset=type_).apply({'price': 'ohlc', 'vol': 'sum'})

        resx = resx.append(_data1).append(_data2)

    return resx.reset_index().drop_duplicates()


def QA_data_min_resample(min_data,  type_='5min'):
    """分钟线采样成大周期


    分钟线采样成子级别的分钟线


    time+ OHLC==> resample
    Arguments:
        min {[type]} -- [description]
        raw_type {[type]} -- [description]
        new_type {[type]} -- [description]
    """

    # ohlc_data=min_data.loc[:,['open','high','low','close']].stack().reset_index().rename(columns={0:'price'}).drop(['level_2'],axis=1).set_index('datetime',drop=False)
    # vol=min_data.assign(vol1=0,vol2=0,vol3=0)
    # L2=vol.loc[:,['volume','vol1','vol2','vol3']].stack().reset_index().rename(columns={0:'vol'}).drop(['level_2'],axis=1).set_index('datetime')
    # tick=pd.concat([ohlc_data,L2.vol],axis=1)
    # data = tick['price'].resample(
    #     type_, label='right', closed='left').ohlc()

    # data['volume'] = tick['vol'].resample(
    #     type_, label='right', closed='left').sum()
    # data['code'] = tick.code.iloc[1]
    # if 'date' not in tick.columns:
    #     tick=tick.assign(date=tick.datetime.apply(lambda x: str(x)[0:10]))

    # resx=pd.DataFrame()
    # _temp = tick.drop_duplicates('date')['date']
    # for item in _temp:
    #     _data = data[item]
    #     _data = _data[time(9, 31):time(11, 30)].append(
    #         _data[time(13, 1):time(15, 0)])
    #     resx = resx.append(_data)
    # resx=resx.reset_index()
    # data=resx.assign(date=resx['datetime'].apply(lambda x: str(x)[0:10]))

    # return data.fillna(method='ffill').set_index(['datetime', 'code'], drop=False).drop_duplicates()

    try:
        min_data = min_data.reset_index().set_index('datetime', drop=False)
    except:
        min_data = min_data.set_index('datetime', drop=False)

    CONVERSION = {'code': 'first', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'vol': 'sum', 'amount': 'sum'} if 'vol' in min_data.columns else {
        'code': 'first', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum', 'amount': 'sum'}
    resx = pd.DataFrame()

    for item in set(min_data.index.date):
        min_data_p = min_data.loc[str(item)]
        d = min_data_p[:'{} 11:30:00'.format(item)].resample(
            type_, base=30, closed='right', loffset=type_).apply(CONVERSION)
        f = min_data_p['{} 13:00:00'.format(item):].resample(
            type_, closed='right', loffset=type_).apply(CONVERSION)
        resx = resx.append(d).append(f)
    return resx.dropna().reset_index().set_index('datetime')


def QA_data_day_resample(day_data,  type_='w'):
    """日线降采样

    Arguments:
        day_data {[type]} -- [description]

    Keyword Arguments:
        type_ {str} -- [description] (default: {'w'})

    Returns:
        [type] -- [description]
    """
    # return day_data_p.assign(open=day_data.open.resample(type_).first(),high=day_data.high.resample(type_).max(),low=day_data.low.resample(type_).min(),\
    #             vol=day_data.vol.resample(type_).sum() if 'vol' in day_data.columns else day_data.volume.resample(type_).sum(),\
    #             amount=day_data.amount.resample(type_).sum()).dropna().set_index('date')
    try:
        day_data = day_data.reset_index().set_index('date', drop=False)
    except:
        day_data = day_data.set_index('date', drop=False)

    day_data_p = day_data.resample(type_).last()

    CONVERSION = {'code': 'first', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'vol': 'sum', 'amount': 'sum'} if 'vol' in day_data.columns else {
        'code': 'first', 'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum', 'amount': 'sum'}

    return day_data.resample(type_, closed='right').apply(CONVERSION)


if __name__ == '__main__':
    import QUANTAXIS as QA
    tick = QA.QA_fetch_get_stock_transaction(
        'tdx', '000001', '2018-08-01', '2018-08-02')
    print(QA_data_tick_resample(tick, '60min'))
    print(QA_data_tick_resample(tick, '15min'))
    print(QA_data_tick_resample(tick, '35min'))
