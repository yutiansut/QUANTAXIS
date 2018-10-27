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


try:
    import talib
except:
    print('请安装TALIB后再调用此函数')
import pandas as pd


def CMO(Series, N=14):
    res = talib.CMO(Series.values, N)
    return pd.Series(res, index=Series.index)


def BBANDS(Series, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
    up, middle, low = talib.BBANDS(
        Series.values, timeperiod, nbdevup, nbdevdn, matype)
    return pd.Series(up, index=Series.index), pd.Series(middle, index=Series.index), pd.Series(low, index=Series.index)


def BETA(SeriesA, SeriesB, N=5):
    res = talib.BETA(SeriesA.values, SeriesB.values, N)
    return pd.Series(res, index=SeriesA.index)


def CORREL(SeriesA, SeriesB, N=5):
    res = talib.BETA(SeriesA.values, SeriesB.values, N)
    return pd.Series(res, index=SeriesA.index)


def DEMA(Series, N=30):
    res = talib.DEMA(Series.values, N)
    return pd.Series(res, index=Series.index)


def EMA(Series, N=30):
    res = talib.EMA(Series.values, N)
    return pd.Series(res, index=Series.index)


def HT_DCPERIOD(Series):
    res = talib.HT_DCPERIOD(Series.values)
    return pd.Series(res, index=Series.index)


def HT_DCPHASE(Series):
    res = talib.HT_DCPHASE(Series.values)
    return pd.Series(res, index=Series.index)


def HT_PHASOR(Series):
    res = talib.HT_PHASOR(Series.values)
    return pd.Series(res, index=Series.index)


def HT_SINE(Series):
    res = talib.HT_SINE(Series.values)
    return pd.Series(res, index=Series.index)


def HT_TRENDLINE(Series):
    res = talib.HT_TRENDLINE(Series.values)
    return pd.Series(res, index=Series.index)


def HT_TRENDMODE(Series):
    res = talib.HT_TRENDMODE(Series.values)
    return pd.Series(res, index=Series.index)


def KAMA(Series, N=30):
    res = talib.KAMA(Series.values, N)
    return pd.Series(res, index=Series.index)


def LINEARREG(Series, N=14):
    res = talib.LINEARREG(Series.values, N)
    return pd.Series(res, index=Series.index)


def LINEARREG_ANGLE(Series, N=14):
    res = talib.LINEARREG_ANGLE(Series.values, N)
    return pd.Series(res, index=Series.index)


def LINEARREG_INTERCEPT(Series, N=14):
    res = talib.LINEARREG_INTERCEPT(Series.values, N)
    return pd.Series(res, index=Series.index)


def LINEARREG_SLOPE(Series, N=14):
    res = talib.LINEARREG_SLOPE(Series.values, N)
    return pd.Series(res, index=Series.index)
