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


import numpy as np
try:
    import talib
except:
    pass
    #print('PLEASE install TALIB to call these methods')


# 定义MACD函数
def TA_MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    参数设置:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    返回: macd - dif, signal - dea, hist * 2 - bar, delta
    '''
    macd, signal, hist = talib.MACD(prices, 
                                    fastperiod=fastperiod, 
                                    slowperiod=slowperiod, 
                                    signalperiod=signalperiod)
    delta = np.r_[np.nan, np.diff(hist * 2)]
    return np.c_[macd, signal, hist * 2, delta]


# 定义RSI函数
def TA_RSI(prices, timeperiod=12):
    '''
    参数设置:
        timeperiod = 12

    返回: ma
    '''
    rsi = talib.RSI(prices, timeperiod=timeperiod)
    delta = np.r_[np.nan, np.diff(rsi)]
    return np.c_[rsi, delta]


# 定义RSI函数
def TA_BBANDS(prices, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
    '''
    参数设置:
        timeperiod = 5
        nbdevup = 2
        nbdevdn = 2

    返回: up, middle, low
    '''
    up, middle, low = talib.BBANDS(prices, timeperiod, nbdevup, nbdevdn, matype)
    ch = (up - low) / low
    delta = np.r_[np.nan, np.diff(ch)]
    return np.c_[up, middle, low, ch, delta]


def TA_KDJ(hight, low, close, fastk_period=9, slowk_matype=0, slowk_period=3, slowd_period=3):
    '''
    参数设置:
        fastk_period = 0
        lowk_matype = 0, 
        slowk_period = 3, 
        slowd_period = 3

    返回: K, D, J
    '''
    K, D = talib.STOCH(hight, low, close, fastk_period=fastk_period, slowk_matype=slowk_matype, slowk_period=slowk_period, slowd_period=slowd_period)
    J = 3 * K - 2 * D
    delta = np.r_[np.nan, np.diff(J)]
    return np.c_[K, D, J, delta]


def TA_CCI(high, low, close, timeperiod=14):
    """
    名称：平均趋向指数的趋向指数
    简介：使用CCI指标，指标判断CCI趋势。
    """
    real = talib.CCI(high, low, close, timeperiod=14)
    delta = np.r_[np.nan, np.diff(real)]
    return np.c_[real, delta]