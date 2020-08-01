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

from datetime import time
from QUANTAXIS.QAUtil.QAParameter import EXCHANGE_ID
import pandas as pd
import numpy as np


def QA_data_tick_resample_1min(tick, type_='1min', if_drop=True):
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
    tick = tick.assign(amount=tick.price * tick.vol)
    resx = pd.DataFrame()
    _dates = set(tick.date)

    for date in sorted(list(_dates)):
        _data = tick.loc[tick.date == date]
        # morning min bar
        _data1 = _data[time(9,
                            25):time(11,
                                     30)].resample(
                                         type_,
                                         closed='left',
                                         base=30,
                                         loffset=type_
                                     ).apply(
                                         {
                                             'price': 'ohlc',
                                             'vol': 'sum',
                                             'code': 'last',
                                             'amount': 'sum'
                                         }
                                     )
        _data1.columns = _data1.columns.droplevel(0)
        # do fix on the first and last bar
        # 某些股票某些日期没有集合竞价信息，譬如 002468 在 2017 年 6 月 5 日的数据
        if len(_data.loc[time(9, 25):time(9, 25)]) > 0:
            _data1.loc[time(9,
                            31):time(9,
                                     31),
                       'open'] = _data1.loc[time(9,
                                                 26):time(9,
                                                          26),
                                            'open'].values
            _data1.loc[time(9,
                            31):time(9,
                                     31),
                       'high'] = _data1.loc[time(9,
                                                 26):time(9,
                                                          31),
                                            'high'].max()
            _data1.loc[time(9,
                            31):time(9,
                                     31),
                       'low'] = _data1.loc[time(9,
                                                26):time(9,
                                                         31),
                                           'low'].min()
            _data1.loc[time(9,
                            31):time(9,
                                     31),
                       'vol'] = _data1.loc[time(9,
                                                26):time(9,
                                                         31),
                                           'vol'].sum()
            _data1.loc[time(9,
                            31):time(9,
                                     31),
                       'amount'] = _data1.loc[time(9,
                                                   26):time(9,
                                                            31),
                                              'amount'].sum()
        # 通达信分笔数据有的有 11:30 数据，有的没有
        if len(_data.loc[time(11, 30):time(11, 30)]) > 0:
            _data1.loc[time(11,
                            30):time(11,
                                     30),
                       'high'] = _data1.loc[time(11,
                                                 30):time(11,
                                                          31),
                                            'high'].max()
            _data1.loc[time(11,
                            30):time(11,
                                     30),
                       'low'] = _data1.loc[time(11,
                                                30):time(11,
                                                         31),
                                           'low'].min()
            _data1.loc[time(11,
                            30):time(11,
                                     30),
                       'close'] = _data1.loc[time(11,
                                                  31):time(11,
                                                           31),
                                             'close'].values
            _data1.loc[time(11,
                            30):time(11,
                                     30),
                       'vol'] = _data1.loc[time(11,
                                                30):time(11,
                                                         31),
                                           'vol'].sum()
            _data1.loc[time(11,
                            30):time(11,
                                     30),
                       'amount'] = _data1.loc[time(11,
                                                   30):time(11,
                                                            31),
                                              'amount'].sum()
        _data1 = _data1.loc[time(9, 31):time(11, 30)]

        # afternoon min bar
        _data2 = _data[time(13,
                            0):time(15,
                                    0)].resample(
                                        type_,
                                        closed='left',
                                        base=30,
                                        loffset=type_
                                    ).apply(
                                        {
                                            'price': 'ohlc',
                                            'vol': 'sum',
                                            'code': 'last',
                                            'amount': 'sum'
                                        }
                                    )

        _data2.columns = _data2.columns.droplevel(0)
        # 沪市股票在 2018-08-20 起，尾盘 3 分钟集合竞价
        if (pd.Timestamp(date) <
                pd.Timestamp('2018-08-20')) and (tick.code.iloc[0][0] == '6'):
            # 避免出现 tick 数据没有 1:00 的值
            if len(_data.loc[time(13, 0):time(13, 0)]) > 0:
                _data2.loc[time(15,
                                0):time(15,
                                        0),
                           'high'] = _data2.loc[time(15,
                                                     0):time(15,
                                                             1),
                                                'high'].max()
                _data2.loc[time(15,
                                0):time(15,
                                        0),
                           'low'] = _data2.loc[time(15,
                                                    0):time(15,
                                                            1),
                                               'low'].min()
                _data2.loc[time(15,
                                0):time(15,
                                        0),
                           'close'] = _data2.loc[time(15,
                                                      1):time(15,
                                                              1),
                                                 'close'].values
        else:
            # 避免出现 tick 数据没有 15:00 的值
            if len(_data.loc[time(13, 0):time(13, 0)]) > 0:
                if (len(_data2.loc[time(15, 1):time(15, 1)]) > 0):
                    _data2.loc[time(15,
                                    0):time(15,
                                            0)] = _data2.loc[time(15,
                                                                  1):time(15,
                                                                          1)].values
                else:
                    # 这种情况下每天下午收盘后15:00已经具有tick值，不需要另行额外填充
                    #  -- 阿财 2020/05/27
                    #print(_data2.loc[time(15,
                    #                0):time(15,
                    #                        0)])
                    pass
        _data2 = _data2.loc[time(13, 1):time(15, 0)]
        resx = resx.append(_data1).append(_data2)
    resx['vol'] = resx['vol'] * 100.0
    resx['volume'] = resx['vol']
    resx['type'] = '1min'
    if if_drop:
        resx = resx.dropna()
    return resx.reset_index().drop_duplicates().set_index(['datetime', 'code'])


def QA_data_tick_resample(tick, type_='1min'):
    """tick采样成任意级别分钟线

    Arguments:
        tick {[type]} -- transaction

    Returns:
        [type] -- [description]
    """
    tick = tick.assign(amount=tick.price * tick.vol)
    resx = pd.DataFrame()
    _temp = set(tick.index.date)

    for item in _temp:
        _data = tick.loc[str(item)]
        _data1 = _data[time(9,
                            31):time(11,
                                     30)].resample(
                                         type_,
                                         closed='right',
                                         base=30,
                                         loffset=type_
                                     ).apply(
                                         {
                                             'price': 'ohlc',
                                             'vol': 'sum',
                                             'code': 'last',
                                             'amount': 'sum'
                                         }
                                     )

        _data2 = _data[time(13,
                            1):time(15,
                                    0)].resample(
                                        type_,
                                        closed='right',
                                        loffset=type_
                                    ).apply(
                                        {
                                            'price': 'ohlc',
                                            'vol': 'sum',
                                            'code': 'last',
                                            'amount': 'sum'
                                        }
                                    )

        resx = resx.append(_data1).append(_data2)
    resx.columns = resx.columns.droplevel(0)
    return resx.reset_index().drop_duplicates().set_index(['datetime', 'code'])


def QA_data_ctptick_resample(tick, type_='1min'):
    """tick采样成任意级别分钟线

    Arguments:
        tick {[type]} -- transaction

    Returns:
        [type] -- [description]
    """

    resx = pd.DataFrame()
    _temp = set(tick.TradingDay)

    for item in _temp:

        _data = tick.query('TradingDay=="{}"'.format(item))
        try:
            _data.loc[time(20, 0):time(21, 0), 'volume'] = 0
        except:
            pass

        _data.volume = _data.volume.diff()
        _data = _data.assign(amount=_data.LastPrice * _data.volume)
        _data0 = _data[time(0,
                            0):time(2,
                                    30)].resample(
                                        type_,
                                        closed='right',
                                        base=30,
                                        loffset=type_
                                    ).apply(
                                        {
                                            'LastPrice': 'ohlc',
                                            'volume': 'sum',
                                            'code': 'last',
                                            'amount': 'sum'
                                        }
                                    )

        _data1 = _data[time(9,
                            0):time(11,
                                    30)].resample(
                                        type_,
                                        closed='right',
                                        base=30,
                                        loffset=type_
                                    ).apply(
                                        {
                                            'LastPrice': 'ohlc',
                                            'volume': 'sum',
                                            'code': 'last',
                                            'amount': 'sum'
                                        }
                                    )

        _data2 = _data[time(13,
                            1):time(15,
                                    0)].resample(
                                        type_,
                                        closed='right',
                                        base=30,
                                        loffset=type_
                                    ).apply(
                                        {
                                            'LastPrice': 'ohlc',
                                            'volume': 'sum',
                                            'code': 'last',
                                            'amount': 'sum'
                                        }
                                    )

        _data3 = _data[time(21,
                            0):time(23,
                                    59)].resample(
                                        type_,
                                        closed='left',
                                        loffset=type_
                                    ).apply(
                                        {
                                            'LastPrice': 'ohlc',
                                            'volume': 'sum',
                                            'code': 'last',
                                            'amount': 'sum'
                                        }
                                    )

        resx = resx.append(_data0).append(_data1).append(_data2).append(_data3)
    resx.columns = resx.columns.droplevel(0)
    return resx.reset_index().drop_duplicates().set_index(['datetime',
                                                           'code']).sort_index()


def QA_data_min_resample(min_data, type_='5min'):
    """分钟线采样成大周期


    分钟线采样成子级别的分钟线


    time+ OHLC==> resample
    Arguments:
        min {[type]} -- [description]
        raw_type {[type]} -- [description]
        new_type {[type]} -- [description]
    """

    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'vol': 'sum',
        'amount': 'sum'
    } if 'vol' in min_data.columns else {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'amount': 'sum'
    }
    min_data = min_data.loc[:, list(CONVERSION.keys())]
    idx = min_data.index
    part_1 = min_data.iloc[idx.indexer_between_time('9:30', '11:30')]
    part_1_res = part_1.resample(
        type_,
        base=30,
        closed='right',
        loffset=type_
    ).apply(CONVERSION)
    part_2 = min_data.iloc[idx.indexer_between_time('13:00', '15:00')]
    part_2_res = part_2.resample(
        type_,
        base=0,
        closed='right',
        loffset=type_
    ).agg(CONVERSION)
    part_1_res['type'] = part_2_res['type'] = type_ if (type_ !='1D') else 'day'
    return pd.concat(
        [part_1_res,
         part_2_res]
    ).dropna().sort_index().reset_index().set_index(['datetime',
                                                     'code'])


def QA_data_stockmin_resample(min_data, period=5):
    """
    1min 分钟线采样成 period 级别的分钟线
    :param min_data:
    :param period:
    :return:
    """
    if isinstance(period, float):
        period = int(period)
    elif isinstance(period, str):
        period = period.replace('min', '')
    elif isinstance(period, int):
        pass
    _period = '%sT' % period
    min_data = min_data.reset_index()
    if 'datetime' not in min_data.columns:
        return None
    # 9:30 - 11:30
    min_data_morning = min_data.set_index("datetime"
                                         ).loc[time(9,
                                                    30):time(11,
                                                             30)].reset_index()
    min_data_morning.index = pd.DatetimeIndex(min_data_morning.datetime
                                             ).to_period('T')
    # 13:00 - 15:00
    min_data_afternoon = min_data.set_index("datetime").loc[
        time(13,
             00):time(15,
                      00)].reset_index()
    min_data_afternoon.index = pd.DatetimeIndex(min_data_afternoon.datetime
                                               ).to_period('T')

    _conversion = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
    }
    if 'vol' in min_data.columns:
        _conversion["vol"] = "sum"
    elif 'volume' in min_data.columns:
        _conversion["volume"] = "sum"
    if 'amount' in min_data.columns:
        _conversion['amount'] = 'sum'

    res = pd.concat(
        [
            min_data_morning.resample(_period,
                                      closed="right",
                                      kind="period").apply(_conversion
                                                          ).dropna(),
            min_data_afternoon.resample(_period,
                                        closed="right",
                                        kind="period").apply(_conversion
                                                            ).dropna()
        ]
    )
    # 10:31:00 => 10:30:00
    res.index = (res.index + res.index.freq).to_timestamp() - \
        pd.Timedelta(minutes=1)
    return res.reset_index().set_index(["datetime", "code"]).sort_index()


def QA_data_min_to_day(min_data, type_='1D'):
    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'vol': 'sum',
        'amount': 'sum'
    } if 'vol' in min_data.columns else {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'amount': 'sum'
    }

    return min_data.reset_index(1).resample(
        type_,
        base=0,
        closed='right'
    ).agg(CONVERSION).dropna()


def QA_data_futuremin_resample(
    min_data,
    type_='5min',
    exchange_id=EXCHANGE_ID.SHFE
):
    """期货分钟线采样成大周期


    分钟线采样成子级别的分钟线

    future:

    vol ==> trade
    amount X

    期货一般两种模式:

    中金所 股指期货: 9:30 - 11:30/ 13:00 -15:00

    其他期货: -1 21:00: 2:30  /  9:00 - 11:30 / 13:30-15:00
    (builtins.sum, "sum"),
    (builtins.max, "max"),
    (builtins.min, "min"),
    (np.all, "all"),
    (np.any, "any"),
    (np.sum, "sum"),
    (np.nansum, "sum"),
    (np.mean, "mean"),
    (np.nanmean, "mean"),
    (np.prod, "prod"),
    (np.nanprod, "prod"),
    (np.std, "std"),
    (np.nanstd, "std"),
    (np.var, "var"),
    (np.nanvar, "var"),
    (np.median, "median"),
    (np.nanmedian, "median"),
    (np.max, "max"),
    (np.nanmax, "max"),
    (np.min, "min"),
    (np.nanmin, "min"),
    (np.cumprod, "cumprod"),
    (np.nancumprod, "cumprod"),
    (np.cumsum, "cumsum"),
    (np.nancumsum, "cumsum"),

    """
    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'tradetime': 'last',
        'position': 'last',
        'volume': 'sum'
    }
    min_data = min_data.loc[:, list(CONVERSION.keys())]
    idx = min_data.index
    if exchange_id == EXCHANGE_ID.CFFEX:
        part_1 = min_data.iloc[idx.indexer_between_time('9:30', '11:30')]
        part_1_res = part_1.resample(
            type_,
            base=30,
            closed='right',
            loffset=type_
        ).apply(CONVERSION)
        part_2 = min_data.iloc[idx.indexer_between_time('13:00', '15:00')]
        part_2_res = part_2.resample(
            type_,
            base=0,
            closed='right',
            loffset=type_
        ).agg(CONVERSION)
        return pd.concat(
            [part_1_res,
             part_2_res]
        ).dropna().sort_index().reset_index().set_index(['datetime',
                                                         'code'])
    else:
        part_1 = min_data.iloc[np.append(
            idx.indexer_between_time('0:00',
                                     '11:30'),
            idx.indexer_between_time('0:00',
                                     '11:30')
        )]
        part_1_res = part_1.resample(
            type_,
            base=0,
            closed='right',
            loffset=type_
        ).apply(CONVERSION)
        part_2 = min_data.iloc[idx.indexer_between_time('13:30', '15:00')]
        part_2_res = part_2.resample(
            type_,
            base=30,
            closed='right',
            loffset=type_
        ).agg(CONVERSION)
        part_3 = min_data.iloc[idx.indexer_between_time('21:00', '23:59')]
        part_3_res = part_3.resample(
            type_,
            base=0,
            closed='right',
            loffset=type_
        ).agg(CONVERSION)
        return pd.concat(
            [part_1_res,
             part_2_res,
             part_3_res]
        ).dropna().sort_index().reset_index().set_index(['datetime',
                                                         'code'])


def QA_data_futuremin_resample_tb_kq(
    min_data,
    type_='5min',
    exchange_id=EXCHANGE_ID.SHFE
):
    """期货分钟线采样成大周期

    此采样方法仅适用于tb/快期, 因此单独拿出来

    分钟线采样成子级别的分钟线


    FROM TB 数据

    TO   TB 数据

    """
    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'tradetime': 'last',
        'position': 'last',
        'volume': 'sum'
    }
    min_data = min_data.loc[:, list(CONVERSION.keys())]
    return min_data.resample(
        type_,
        base=0,
        closed='left'
    ).agg(CONVERSION).dropna().sort_index().reset_index().set_index(
        ['datetime',
         'code']
    )


def QA_data_futuremin_resample_tb_kq2(
    min_data,
    type_='5min',
    exchange_id=EXCHANGE_ID.SHFE
):
    """期货分钟线采样成大周期

    此采样方法仅适用于tb/快期, 因此单独拿出来

    FROM TDX 数据

    TO   TB 数据


    """
    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'tradetime': 'last',
        'position': 'last',
        'volume': 'sum'
    }
    min_data = min_data.loc[:, list(CONVERSION.keys())]
    return min_data.resample(
        type_,
        base=0,
        closed='right'
    ).agg(CONVERSION).dropna().sort_index().reset_index().set_index(
        ['datetime',
         'code']
    )


def QA_data_futuremin_resample_today(
    min_data,
    type_='1D',
    exchange_id=EXCHANGE_ID.SHFE
):
    """期货分钟线采样成大周期


    分钟线采样成子级别的分钟线

    future:

    vol ==> trade
    amount X

    期货一般两种模式:

    中金所 股指期货: 9:30 - 11:30/ 13:00 -15:00

    其他期货: -1 21:00: 2:30  /  9:00 - 11:30 / 13:30-15:00
    (builtins.sum, "sum"),
    (builtins.max, "max"),
    (builtins.min, "min"),
    (np.all, "all"),
    (np.any, "any"),
    (np.sum, "sum"),
    (np.nansum, "sum"),
    (np.mean, "mean"),
    (np.nanmean, "mean"),
    (np.prod, "prod"),
    (np.nanprod, "prod"),
    (np.std, "std"),
    (np.nanstd, "std"),
    (np.var, "var"),
    (np.nanvar, "var"),
    (np.median, "median"),
    (np.nanmedian, "median"),
    (np.max, "max"),
    (np.nanmax, "max"),
    (np.min, "min"),
    (np.nanmin, "min"),
    (np.cumprod, "cumprod"),
    (np.nancumprod, "cumprod"),
    (np.cumsum, "cumsum"),
    (np.nancumsum, "cumsum"),

    """
    return min_data.assign(tradedate=pd.to_datetime(min_data.tradetime.apply(lambda x: x[0:10]))).reset_index().set_index('tradedate').resample(type_).\
        apply({'code': 'first', 'open': 'first', 'high': 'max',
               'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()


def QA_data_futuremin_resample_series(
    min_data,
    key='open',
    type_='5min',
    exchange_id=EXCHANGE_ID.SHFE
):

    if isinstance(min_data.index, pd.MultiIndex):
        min_data = min_data.reset_index(1)
        idx = min_data.index
    else:
        idx = pd.to_datetime(min_data.index)

    CONVERSION = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    if exchange_id == EXCHANGE_ID.CFFEX:
        part_1 = min_data.iloc[idx.indexer_between_time('9:30', '11:30')]
        part_1_res = part_1.resample(
            type_,
            base=30,
            closed='right',
            loffset=type_
        ).apply({key: CONVERSION[key]})
        part_2 = min_data.iloc[idx.indexer_between_time('13:00', '15:00')]
        part_2_res = part_2.resample(
            type_,
            base=0,
            closed='right',
            loffset=type_
        ).agg({key: CONVERSION[key]})
        return pd.concat([part_1_res, part_2_res]).dropna().sort_index()
    else:
        part_1 = min_data.iloc[np.append(
            idx.indexer_between_time('0:00',
                                     '11:30'),
            idx.indexer_between_time('0:00',
                                     '11:30')
        )]
        part_1_res = part_1.resample(
            type_,
            base=0,
            closed='right',
            loffset=type_
        ).apply({key: CONVERSION[key]})
        part_2 = min_data.iloc[idx.indexer_between_time('13:30', '15:00')]
        part_2_res = part_2.resample(
            type_,
            base=30,
            closed='right',
            loffset=type_
        ).agg({key: CONVERSION[key]})
        return pd.concat([part_1_res, part_2_res]).dropna().sort_index()


def QA_data_day_resample(day_data, type_='w'):
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

    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'vol': 'sum',
        'amount': 'sum',
        'date': 'last'
    } if 'vol' in day_data.columns else {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'amount': 'sum',
        'date': 'last'
    }

    data = day_data.resample(type_, closed='right').apply(CONVERSION).dropna()
    return data.assign(date=pd.to_datetime(data.date)
                      ).set_index(['date',
                                   'code'])


def QA_data_futureday_resample(day_data, type_='w'):
    """期货日线降采样

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

    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'vol': 'sum',
        'position': 'sum',
        'date': 'last'
    } if 'vol' in day_data.columns else {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'position': 'sum',
        'date': 'last'
    }

    data = day_data.resample(type_, closed='right').apply(CONVERSION).dropna()
    return data.assign(date=pd.to_datetime(data.date)
                      ).set_index(['date',
                                   'code'])


def QA_data_cryptocurrency_min_resample(min_data, type_='5min'):
    """数字加密资产的分钟线采样成大周期


    分钟线采样成子级别的分钟线


    time+ OHLC==> resample
    Arguments:
        min {[type]} -- [description]
        raw_type {[type]} -- [description]
        new_type {[type]} -- [description]
    """

    CONVERSION = {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'trade': 'sum',
        'vol': 'sum',
        'amount': 'sum'
    } if 'vol' in min_data.columns else {
        'code': 'first',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'trade': 'sum',
        'volume': 'sum',
        'amount': 'sum'
    }
    min_data = min_data.loc[:, list(CONVERSION.keys())]
    data = min_data.resample(
        type_,
        base=0,
        closed='right',
        loffset=type_
    ).apply(CONVERSION).dropna()
    return data.assign(datetime=pd.to_datetime(data.index)
                      ).set_index(['datetime',
                                   'code'])


if __name__ == '__main__':
    import QUANTAXIS as QA
    tick = QA.QA_fetch_get_stock_transaction(
        'tdx',
        '000001',
        '2018-08-01',
        '2018-08-02'
    )
    print(QA_data_tick_resample(tick, '60min'))
    print(QA_data_tick_resample(tick, '15min'))
    print(QA_data_tick_resample(tick, '35min'))

    print("test QA_data_stockmin_resample, level: 120")
    start, end, level = "2019-05-01", "2019-05-08", 120
    data = QA.QA_fetch_stock_min_adv("000001", start, end)
    res = QA_data_stockmin_resample(data.data, level)
    print(res)
    res2 = QA.QA_fetch_stock_min_adv(["000001",
                                      '000002'],
                                     start,
                                     end).add_func(
                                         QA_data_stockmin_resample,
                                         level
                                     )
    print(res2)
