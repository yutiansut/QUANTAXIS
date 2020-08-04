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


from functools import reduce
import math
import numpy as np
import pandas as pd


"""
Series 类

这个是下面以DataFrame为输入的基础函数
return pd.Series format
"""


def EMA(Series, N):
    return pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()


def MA(Series, N):
    return pd.Series.rolling(Series, N).mean()

# 威廉SMA  参考https://www.joinquant.com/post/867


def SMA(Series, N, M=1):
    """
    威廉SMA算法

    本次修正主要是对于返回值的优化,现在的返回值会带上原先输入的索引index
    2018/5/3
    @yutiansut
    """
    ret = []
    i = 1
    length = len(Series)
    # 跳过X中前面几个 nan 值
    while i < length:
        if np.isnan(Series.iloc[i]):
            i += 1
        else:
            break
    preY = Series.iloc[i]  # Y'
    ret.append(preY)
    while i < length:
        Y = (M * Series.iloc[i] + (N - M) * preY) / float(N)
        ret.append(Y)
        preY = Y
        i += 1
    return pd.Series(ret, index=Series.tail(len(ret)).index)


def DIFF(Series, N=1):
    return pd.Series(Series).diff(N)


def HHV(Series, N):
    return pd.Series(Series).rolling(N).max()


def LLV(Series, N):
    return pd.Series(Series).rolling(N).min()


def SUM(Series, N):
    return pd.Series.rolling(Series, N).sum()


def ABS(Series):
    return abs(Series)


def MAX(A, B):
    var = IF(A > B, A, B)
    return var


def MIN(A, B):
    var = IF(A < B, A, B)
    return var


def SINGLE_CROSS(A, B):
    if A.iloc[-2] < B.iloc[-2] and A.iloc[-1] > B.iloc[-1]:
        return True
    else:
        return False


def CROSS(A, B):
    """A<B then A>B  A上穿B B下穿A

    Arguments:
        A {[type]} -- [description]
        B {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    var = np.where(A < B, 1, 0)
    try:
        index = A.index
    except:
        index = B.index
    return (pd.Series(var, index=index).diff() < 0).apply(int)


def CROSS_STATUS(A, B):
    """
    A 穿过 B 产生持续的 1 序列信号
    """
    return np.where(A > B, 1, 0)


def FILTER(COND, N):

    k1 = pd.Series(np.where(COND, 1, 0), index=COND.index)
    idx = k1[k1 == 1].index.codes[0]
    needfilter = pd.Series(idx, index=idx)
    afterfilter = needfilter.diff().apply(lambda x: False if x < N else True)
    k1.iloc[afterfilter[afterfilter].index] = 2
    return k1.apply(lambda x: 1 if x == 2 else 0)


def COUNT(COND, N):
    """
    2018/05/23 修改

    参考https://github.com/QUANTAXIS/QUANTAXIS/issues/429

    现在返回的是series
    """
    return pd.Series(np.where(COND, 1, 0), index=COND.index).rolling(N).sum()


def IF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    try:
        try:
            index = V1.index
        except:
            index = COND.index
    except:
        index = V2.index
    return pd.Series(var, index=index)


def IFAND(COND1, COND2, V1, V2):
    var = np.where(np.logical_and(COND1, COND2), V1, V2)
    return pd.Series(var, index=V1.index)


def IFOR(COND1, COND2, V1, V2):
    var = np.where(np.logical_or(COND1, COND2), V1, V2)
    return pd.Series(var, index=V1.index)


def REF(Series, N):

    return Series.shift(N)


def LAST(COND, N1, N2):
    """表达持续性
    从前N1日到前N2日一直满足COND条件

    Arguments:
        COND {[type]} -- [description]
        N1 {[type]} -- [description]
        N2 {[type]} -- [description]
    """
    N2 = 1 if N2 == 0 else N2
    assert N2 > 0
    assert N1 > N2
    return COND.iloc[-N1:-N2].all()


def STD(Series, N):
    return pd.Series.rolling(Series, N).std()


def AVEDEV(Series, N):
    """
    平均绝对偏差 mean absolute deviation
    修正: 2018-05-25 

    之前用mad的计算模式依然返回的是单值
    """
    return Series.rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean(), raw=True)


def MACD(Series, FAST, SLOW, MID):
    """macd指标 仅适用于Series
    对于DATAFRAME的应用请使用QA_indicator_macd
    """
    EMAFAST = EMA(Series, FAST)
    EMASLOW = EMA(Series, SLOW)
    DIFF = EMAFAST - EMASLOW
    DEA = EMA(DIFF, MID)
    MACD = (DIFF - DEA) * 2
    DICT = {'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD}
    VAR = pd.DataFrame(DICT)
    return VAR


def BBIBOLL(Series, N1, N2, N3, N4, N, M):  # 多空布林线

    bbiboll = BBI(Series, N1, N2, N3, N4)
    UPER = bbiboll + M * STD(bbiboll, N)
    DOWN = bbiboll - M * STD(bbiboll, N)
    DICT = {'BBIBOLL': bbiboll, 'UPER': UPER, 'DOWN': DOWN}
    VAR = pd.DataFrame(DICT)
    return VAR


def BBI(Series, N1, N2, N3, N4):
    '多空指标'

    bbi = (MA(Series, N1) + MA(Series, N2) +
           MA(Series, N3) + MA(Series, N4)) / 4
    DICT = {'BBI': bbi}
    VAR = pd.DataFrame(DICT)
    return VAR


def BARLAST(cond, yes=True):
    """支持MultiIndex的cond和DateTimeIndex的cond
    条件成立  yes= True 或者 yes=1 根据不同的指标自己定

    最后一次条件成立  到 当前到周期数

    Arguments:
        cond {[type]} -- [description]
    """
    if isinstance(cond.index, pd.MultiIndex):
        return len(cond)-cond.index.levels[0].tolist().index(cond[cond == yes].index[-1][0])-1
    elif isinstance(cond.index, pd.DatetimeIndex):
        return len(cond)-cond.index.tolist().index(cond[cond == yes].index[-1])-1


def BARLAST_EXIST(cond, yes=True):
    """
    上一次条件成立   持续到当前到数量


    支持MultiIndex的cond和DateTimeIndex的cond
    条件成立  yes= True 或者 yes=1 根据不同的指标自己定

    Arguments:
        cond {[type]} -- [description]
    """
    if isinstance(cond.index, pd.MultiIndex):
        return len(cond)-cond.index.levels[0].tolist().index(cond[cond != yes].index[-1][0])-1
    elif isinstance(cond.index, pd.DatetimeIndex):
        return len(cond)-cond.index.tolist().index(cond[cond != yes].index[-1])-1

def XARROUND(x, y): return np.round(
    y*(round(x/y-math.floor(x/y)+0.00000000001) + math.floor(x/y)), 2)


def RENKO(Series, N, condensed=True):

    last_price = Series[0]
    chart = [last_price]
    for price in Series:
        bricks = math.floor(abs(price-last_price)/N)
        if bricks == 0:
            if condensed:
                chart.append(chart[-1])
            continue
        sign = int(np.sign(price-last_price))
        chart += [sign*(last_price+(sign*N*x)) for x in range(1, bricks+1)]
        last_price = abs(chart[-1])

    return pd.Series(chart)



def RENKOP(Series, N, condensed=True):
    last_price = Series[0]
    chart = [last_price]
    for price in Series:
        inc = (price-last_price)/last_price
        #print(inc)
        if abs(inc) < N:
            # if condensed:
            #     chart.append(chart[-1])
            continue

        sign = int(np.sign(price-last_price))
        bricks = math.floor(inc/N)
        #print(bricks)
        #print((N * (price-last_price)) / inc)
        step = math.floor((N * (price-last_price)) / inc)
        print(step)
        #print(sign)
        chart += [sign*(last_price+(sign*step*x))
                  for x in range(1, abs(bricks)+1)]
        last_price = abs(chart[-1])
    return pd.Series(chart)