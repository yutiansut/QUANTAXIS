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


import pandas as pd
try:
    import talib
except:
    print('请安装TALIB后再调用此函数')


def CDL2CROWS(data):
    res = talib.CDL2CROWS(data.open.values, data.high.values,
                          data.low.values, data.close.values)
    return pd.DataFrame({'CDL2CROWS': res}, index=data.index)


def CDL3BLACKCROWS(data):
    res = talib.CDL3BLACKCROWS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3BLACKCROWS': res}, index=data.index)


def CDL3INSIDE(data):
    res = talib.CDL3INSIDE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3INSIDE': res}, index=data.index)


def CDL3LINESTRIKE(data):
    res = talib.CDL3LINESTRIKE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3LINESTRIKE': res}, index=data.index)


def CDL3OUTSIDE(data):
    res = talib.CDL3OUTSIDE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3OUTSIDE': res}, index=data.index)


def CDL3STARSINSOUTH(data):
    res = talib.CDL3STARSINSOUTH(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3STARSINSOUTH': res}, index=data.index)


def CDL3WHITESOLDIERS(data):
    res = talib.CDL3WHITESOLDIERS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3WHITESOLDIERS': res}, index=data.index)


def CDLABANDONEDBABY(data):
    res = talib.CDLABANDONEDBABY(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLABANDONEDBABY': res}, index=data.index)


def CDLADVANCEBLOCK(data):
    res = talib.CDLADVANCEBLOCK(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLADVANCEBLOCK': res}, index=data.index)


def CDLBELTHOLD(data):
    res = talib.CDLBELTHOLD(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLBELTHOLD': res}, index=data.index)


def CDLBREAKAWAY(data):
    res = talib.CDLBREAKAWAY(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLBREAKAWAY': res}, index=data.index)

