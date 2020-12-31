# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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
    pass
    #print('PLEASE install TALIB to call these methods')
import pandas as pd


def CMO(Series, timeperiod=14):
    res = talib.CMO(Series.values, timeperiod)
    return pd.Series(res, index=Series.index)


def BBANDS(Series, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
    up, middle, low = talib.BBANDS(
        Series.values, timeperiod, nbdevup, nbdevdn, matype)
    return pd.Series(up, index=Series.index), pd.Series(middle, index=Series.index), pd.Series(low, index=Series.index)


def BETA(SeriesA, SeriesB, timeperiod=5):
    res = talib.BETA(SeriesA.values, SeriesB.values, timeperiod)
    return pd.Series(res, index=SeriesA.index)


def CORREL(SeriesA, SeriesB, timeperiod=5):
    res = talib.BETA(SeriesA.values, SeriesB.values, timeperiod)
    return pd.Series(res, index=SeriesA.index)


def DEMA(Series, timeperiod=30):
    res = talib.DEMA(Series.values, timeperiod)
    return pd.Series(res, index=Series.index)


# def EMA(Series, timeperiod=30):
#     res = talib.EMA(Series.values, timeperiod)
#     return pd.Series(res, index=Series.index)


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


def KAMA(Series, timeperiod=30):
    res = talib.KAMA(Series.values, timeperiod)
    return pd.Series(res, index=Series.index)


def LINEARREG(Series, timeperiod=14):
    res = talib.LINEARREG(Series.values, timeperiod)
    return pd.Series(res, index=Series.index)


def LINEARREG_ANGLE(Series, timeperiod=14):
    res = talib.LINEARREG_ANGLE(Series.values, timeperiod)
    return pd.Series(res, index=Series.index)


def LINEARREG_INTERCEPT(Series, timeperiod=14):
    res = talib.LINEARREG_INTERCEPT(Series.values, timeperiod)
    return pd.Series(res, index=Series.index)


def LINEARREG_SLOPE(Series, timeperiod=14):
    res = talib.LINEARREG_SLOPE(Series.values, timeperiod)
    return pd.Series(res, index=Series.index)


# def MA(Series,):
#   废弃* 因为和QA的MA函数冲突

# def MACD(Series):
#   废弃* 因为和QA的MACD函数冲突

def MACDEXT(Series, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0):
    macd, macdsignal, macdhist = talib.MACDEXT(
        Series.values, fastperiod, fastmatype, slowperiod, slowmatype, signalperiod, signalmatype)
    return pd.Series(macd, index=Series.index), pd.Series(macdsignal, index=Series.index), pd.Series(macdhist, index=Series.index)


def MACDFIX(Series, timeperiod=9):
    macd, macdsignal, macdhist = talib.MACDFIX(Series.values, timeperiod)
    return pd.Series(macd, index=Series.index), pd.Series(macdsignal, index=Series.index), pd.Series(macdhist, index=Series.index)


def MAMA(Series, fastlimit=0.5, slowlimit=0.05):
    mama, fama = talib.MAMA(Series.values, fastlimit, slowlimit)
    return pd.Series(mama, index=Series.index), pd.Series(fama, index=Series.index)


# # MAVP - Moving average with variable period
# real = talib.MAVP(close, periods, minperiod=2, maxperiod=30, matype=0)

# # MIDPOINT - MidPoint over period
# real = talib.MIDPOINT(close, timeperiod=14)

# # MIDPRICE - Midpoint Price over period
# real = talib.MIDPRICE(high, low, timeperiod=14)


# # SAREXT - Parabolic SAR - Extended
# real = SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0,
#               accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)


# # T3 - Triple Exponential Moving Average (T3)
# real = T3(close, timeperiod=5, vfactor=0)

# # TEMA - Triple Exponential Moving Average
# real = TEMA(close, timeperiod=30)

# # TRIMA - Triangular Moving Average
# real = TRIMA(close, timeperiod=30)

# # WMA - Weighted Moving Average
# real = WMA(close, timeperiod=30)


def SMA(Series, timeperiod=30):
    return pd.Series(talib.SMA(Series.values, timeperiod), index=Series.index)


def STDDEV(Series, timeperiod=5, nbdev=1):
    return pd.Series(talib.STDDEV(Series.values, timeperiod, nbdev), index=Series.index)


def STOCHRSI(Series, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0):
    fastk, fastd = talib.STOCHRSI(
        Series.values, fastk_period, fastd_period, fastd_matype)
    return pd.Series(fastk, index=Series.index), pd.Series(fastd, index=Series.index)
