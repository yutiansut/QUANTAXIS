# coding:utf-8
# Author: 阿财（Rgveda@github）（4910163#qq.com）
# Created date: 2020-02-27
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
# The above copyright notice and this permission notice shall be included in
# all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import numpy as np
import pandas as pd
from QUANTAXIS.QAIndicator.base import *

try:
    import talib
except:
    pass
    #print('PLEASE install TALIB to call these methods')
"""
完全用nparray传递参数的talib库，原因是用nparray因为没有 Series MultiIndex 的问题。
处理和补完速度都比pandas更快，转 pd.DataFrame/pd.Series 只需要一个构造函数。

我还引入了一些talib没有，但是写出来不超过10行代码，很容易实现好指标，源自外网(TradingView或者MQ4/5)找到的。
例如
Moving Average ADX
Hull Moving Average
Volume HMA(完成)
"""

# 定义MACD函数


def TA_MACD(prices: np.ndarray,
            fastperiod: int = 12,
            slowperiod: int = 26,
            signalperiod: int = 9) -> np.ndarray:
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
    hist = (macd - signal) * 2
    delta = np.r_[np.nan, np.diff(hist)]
    return np.c_[macd, signal, hist, delta]


# 定义RSI函数
def TA_RSI(prices: np.ndarray,
           timeperiod: int = 12) -> np.ndarray:
    '''
    参数设置:
        timeperiod = 12

    返回: ma
    '''
    rsi = talib.RSI(prices, timeperiod=timeperiod)
    delta = np.r_[np.nan, np.diff(rsi)]
    return np.c_[rsi, delta]


# 定义RSI函数
def TA_BBANDS(prices: np.ndarray,
              timeperiod: int = 5,
              nbdevup: int = 2,
              nbdevdn: int = 2,
              matype: int = 0) -> np.ndarray:
    '''
    参数设置:
        timeperiod = 5
        nbdevup = 2
        nbdevdn = 2

    返回: up, middle, low
    '''
    up, middle, low = talib.BBANDS(prices,
                                   timeperiod,
                                   nbdevup,
                                   nbdevdn,
                                   matype)
    ch = (up - low) / middle
    delta = np.r_[np.nan, np.diff(ch)]
    return np.c_[up, middle, low, ch, delta]


def TA_KDJ(high: np.ndarray,
           low: np.ndarray,
           close: np.ndarray,
           fastk_period: int = 9,
           slowk_matype: int = 0,
           slowk_period: int = 3,
           slowd_period: int = 3) -> np.ndarray:
    '''
    参数设置:
        fastk_period = 9
        lowk_matype = 0, 
        slowk_period = 3, 
        slowd_period = 3

    返回: K, D, J
    '''
    K, D = talib.STOCH(high,
                       low,
                       close,
                       fastk_period=fastk_period,
                       slowk_matype=slowk_matype,
                       slowk_period=slowk_period,
                       slowd_period=slowd_period)
    J = 3 * K - 2 * D
    delta = np.r_[np.nan, np.diff(J)]
    return np.c_[K, D, J, delta]


def TA_ADX(high, low, close, timeperiod=14) -> np.ndarray:
    """
    ADX - Average Directional Movement Index
    """
    real = talib.ADX(high, low, close, timeperiod=timeperiod)
    return np.c_[real]


def TA_ADXR(high, low, close, timeperiod=14) -> np.ndarray:
    """
    名称：平均趋向指数的趋向指数
    简介：使用ADXR指标，指标判断ADX趋势。
    ADXR - Average Directional Movement Index Rating
    """
    real = talib.ADXR(high, low, close, timeperiod=timeperiod)
    return np.c_[real]


def TA_CCI(high: np.ndarray,
           low: np.ndarray,
           close: np.ndarray,
           timeperiod: int = 14) -> np.ndarray:
    """
    名称：平均趋向指数的趋向指数
    简介：使用CCI指标，指标判断CCI趋势。
    CCI - Commodity Channel Index
    """
    real = talib.CCI(high,
                     low,
                     close,
                     timeperiod=timeperiod)
    delta = np.r_[np.nan, np.diff(real)]
    return np.c_[real, delta]


def TA_KAMA(close, timeperiod=30):
    """
    请直接用 talib.KAMA(close, timeperiod)
    KAMA - Kaufman Adaptive Moving Average
    """
    real = talib.KAMA(close, timeperiod=timeperiod)
    return np.c_[real]


def TA_HMA(close, period):
    """
    赫尔移动平均线(HMA) 
    Hull Moving Average.
    Formula:
    HMA = WMA(2*WMA(n/2) - WMA(n)), sqrt(n)
    """
    hma = talib.WMA(2 * talib.WMA(close, int(period / 2)) -
                    talib.WMA(close, period), int(np.sqrt(period)))
    return hma


def ADX_MA(data, period=14, smooth=14, limit=18):
    """
    Moving Average ADX
    ADX Smoothing Trend Color Change on Moving Average and ADX Cross. Use on Hourly Charts - Green UpTrend - Red DownTrend - Black Choppy No Trend

    Source: https://www.tradingview.com/script/owwws7dM-Moving-Average-ADX/
    Translator: 阿财（Rgveda@github）（4910163#qq.com）

    Parameters
    ----------
    data : (N,) array_like
        传入 OHLC Kline 序列。
        The OHLC Kline.
    period : int or None, optional
        DI 统计周期 默认值为 14
        DI Length period. Default value is 10. 
    smooth : int or None, optional
        ADX 平滑周期 默认值为 14
        ADX smoothing length period. Default value is 10.
    limit : int or None, optional
        ADX 限制阈值 默认值为 18
        ADX MA Active limit threshold. Default value is 18.

    Returns
    -------
    adx, ADXm : ndarray
        ADXm 指标和趋势指示方向 (-1, 0, 1) 分别代表 (下跌, 无明显趋势, 上涨)
        ADXm indicator and thread directions sequence. (-1, 0, 1) means for (Neagtive, No Trend, Positive)

    """
    up = data.high.pct_change()
    down = data.low.pct_change() * -1

    trur = TA_HMA(talib.TRANGE(data.high.values,
                               data.low.values, data.close.values), period)
    plus = 100 * TA_HMA(np.where(((up > down) & (up > 0)),
                                 up, 0), period) / trur
    minus = 100 * \
        TA_HMA(np.where(((down > up) & (down > 0)), down, 0), period) / trur

    # 这里是dropna的替代解决办法，因为我觉得nparray的传递方式如果随便drop了可能会跟 data.index
    # 对不上，所以我选择补零替代dropna
    plus = np.r_[np.zeros(period + 2), plus[(period + 2):]]
    minus = np.r_[np.zeros(period + 2), minus[(period + 2):]]
    sum = plus + minus
    adx = 100 * TA_HMA(abs(plus - minus) /
                       (np.where((sum == 0), 1, sum)), smooth)
    adx = np.r_[np.zeros(smooth + 2), adx[(smooth + 2):]]
    ADXm = np.where(((adx > limit) & (plus > minus)), 1,
                    np.where(((adx > limit) & (plus < minus)), -1, 0))
    return adx, ADXm


def ATR_RSI_Stops(data, period=10):
    """
    ATR 趋势判断指标 RSI在40~60区间实现牛熊趋势变化指示
    This simple indicator gives you a bias on the market that can be used as a filter, an entry indicator for pullbacks,...

    It shows the special relationship I discovered between the rsi and the 27 period ema
    and the relation between the 40/60 levels of the rsi and the atr offset of the 27 ema line 

    Source: https://cn.tradingview.com/script/rqzryhZ2-Rsi-Stops-JD/
    Translator: 阿财（Rgveda@github）（4910163#qq.com）

    Parameters
    ----------
    data : (N,) array_like
        传入 OHLC Kline 序列。
        The OHLC Kline.
    period : int or None, optional
        DI 统计周期 默认值为 10
        DI Length period. Default value is 10. 

    Returns
    -------
    rsi_ma, stop_line, directions : ndarray
        rsi_ma, stop_line 指标和 directions 趋势指示方向 (-1, 0, 1) 分别代表 (下跌, 无明显趋势, 上涨)
        rsi_ma, stop_line indicator and thread directions sequence. (-1, 0, 1) means for (Neagtive, No Trend, Positive)

    """
    rsi_ma = talib.EMA((data.open + data.high + data.low + data.close) / 4, 10)
    ATR = talib.ATR(data.high, data.low, data.close, 10)
    top_line = rsi_ma + ATR
    bottom_line = rsi_ma - ATR
    rsi_ma = pd.Series(rsi_ma, index=data.index)
    PRICE_PREDICT = pd.DataFrame(columns=['POSITION'], index=data.index)
    PREDICT_JX = (CROSS(data.close, top_line) == 1)
    PREDICT_SX = (CROSS(bottom_line, data.close) == 1)
    PREDICT_JX = PREDICT_JX[PREDICT_JX.apply(
        lambda x: x == True)]  # eqv.  Trim(x == False)
    PREDICT_SX = PREDICT_SX[PREDICT_SX.apply(
        lambda x: x == True)]  # eqv.  Trim(x == False)
    PRICE_PREDICT.loc[PREDICT_JX.index, 'POSITION'] = 1
    PRICE_PREDICT.loc[PREDICT_SX.index, 'POSITION'] = -1
    PRICE_PREDICT['POSITION'] = PRICE_PREDICT['POSITION'].ffill()
    stop_line = rsi_ma - PRICE_PREDICT['POSITION'] * ATR
    return rsi_ma, stop_line, PRICE_PREDICT['POSITION'].values


def ATR_SuperTrend_cross(klines, length=12, Factor=3):
    """
    ATR 趋势判断指标，可以实现快速而精准的牛熊趋势判断
    the Super Trend ATR allows you to quickly identify trends and the acceleration phase and accumulation

    Source: https://cn.tradingview.com/script/alvd6EHP-Bollinger-Bands-V2-Super-Trend/
    Translator: 阿财（Rgveda@github）（4910163#qq.com）

    Parameters
    ----------
    data : (N,) array_like
        传入 OHLC Kline 序列。
        The OHLC Kline.
    period : int or None, optional
        DI 统计周期 默认值为 10
        DI Length period. Default value is 10. 

    Returns
    -------
    Tsl, Trend : ndarray
        Tsl 指标和 Trend 趋势指示方向 (-1, 0, 1) 分别代表 (下跌, 无明显趋势, 上涨)
        the Tsl indicator and thread directions sequence. (-1, 0, 1) means for (Neagtive, No Trend, Positive)

    """
    src = klines.close.values
    Factor = 3  # Factor of Super Trend
    ATR_period = 12  # ATR period

    Up = (klines.high + klines.low) / 2 - (Factor * talib.ATR(klines.high,
                                                              klines.low,
                                                              klines.close,
                                                              ATR_period))
    Dn = (klines.high + klines.low) / 2 + (Factor * talib.ATR(klines.high,
                                                              klines.low,
                                                              klines.close,
                                                              ATR_period))
    TUp = np.full([len(src)], np.nan)
    for i in np.arange(1, len(src)):
        TUp[i] = max(Up[i], TUp[i - 1]) if (src[i - 1] > TUp[i - 1]) else Up[i]
    TDown = np.full([len(src)], np.nan)
    for i in np.arange(1, len(src)):
        TDown[i] = min(Dn[i], TDown[i - 1]) if (src[i - 1]
                                                < TDown[i - 1]) else Dn[i]

    Trend = np.full([len(src)], np.nan)
    for i in np.arange(1, len(src)):
        Trend[i] = 1 if (src[i] > TDown[i - 1]
                         ) else (-1 if (src[i] < TUp[i - 1]) else Trend[i - 1])

    Tsl = np.where(Trend == 1, TUp, TDown)
    return Tsl, Trend


def Volume_HMA(klines, period=5):
    """
    交易量加权船型移动平均线 HMA，方向指示性类似于 Moving Average ADX，但它们通过不同的指标实现。
    Hull Moving Average with Volume weighted, diretions similar like ADX_MA

    Source: https://www.tradingview.com/script/XTViDINu-VHMA/
    Translator: 阿财（Rgveda@github）（4910163#qq.com）

    Parameters
    ----------
    klines : (N,) array_like
        传入 OHLC Kline 序列。
        The OHLC Kline.
    period : int or None, optional
        DI 统计周期 默认值为 10
        DI Length period. Default value is 10. 

    Returns
    -------
    vhma, Trend : ndarray
        vhma 指标和 Trend 趋势指示方向 (-1/-2, 0, 1/2) 分别代表 (下跌, 无明显趋势, 上涨)
        the vhma indicator and thread directions sequence. (-1/-2, 0, 1/2) means for (Neagtive, No Trend, Positive)

    """
    src1 = talib.EMA(klines.close * klines.volume, period) / \
        talib.EMA(klines.volume, period)
    vhma = TA_HMA(src1, period)
    vhma_s = pd.Series(vhma)

    lineDirection = np.where((vhma > vhma_s.shift(1).values), 1, -1)
    hu = np.where((vhma > vhma_s.shift(2).values), 1, -1)
    return vhma, lineDirection + hu
