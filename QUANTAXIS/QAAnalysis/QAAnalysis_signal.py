# coding:utf-8
# Author: 阿财（Rgveda@github）（11652964@qq.com）
# Created date: 2020-02-27
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
import numba as nb

import scipy.signal as signal
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter, savgol_filter
from QUANTAXIS.QAIndicator.base import *
from QUANTAXIS.QAData.base_datastruct import *
try:
    import peakutils
except:
    print('PLEASE run "pip install peakutils" to call these modules')
    pass
try:
    from QUANTAXIS.QAIndicator.talib_numpy import *
    import QUANTAXIS as QA
    from QUANTAXIS.QAIndicator.base import *
    from QUANTAXIS.QAUtil.QADate_Adv import (
        QA_util_timestamp_to_str,
        QA_util_datetime_to_Unix_timestamp,
        QA_util_print_timestamp
    )
except:
    print('PLEASE run "pip install QUANTAXIS" to call these modules')
    pass

"""
时序信号处理，公共函数
"""

def time_series_momemtum(price, n=24, rf=0.02):
    """
    时间序列动量指标
    Time Series Momentum strategy
    """
    return (price / price.shift(n) - 1) - rf


def find_peak_vextors_eagerly(price, offest=0):
    """
    （饥渴的）在 MACD 上坡的时候查找更多的极值点
    """
    xn = price

    # pass 0
    window_size, poly_order = 5, 1
    yy_sg = savgol_filter(xn, window_size, poly_order)

    # pass 1
    x_tp_min, x_tp_max = signal.argrelextrema(yy_sg, np.less)[0], signal.argrelextrema(yy_sg, np.greater)[0]
    n = int(len(price) / (len(x_tp_min) + len(x_tp_max))) * 2

    # peakutils 似乎一根筋只能查最大极值，通过曲线反相的方式查找极小点
    mirrors = (yy_sg * -1) + np.mean(price) * 2

    # pass 2 使用 peakutils 查找
    x_tp_max = peakutils.indexes(yy_sg, thres=0.01 / max(price), min_dist=n)
    x_tp_min = peakutils.indexes(mirrors, thres=0.01 / max(price), min_dist=n)

    return x_tp_min + offest, x_tp_max + offest


def find_peak_vextors(price, return_ref=False, offest=0):
    """
    采用巴特沃斯信号滤波器，自适应寻找最佳极值点，决定平均周期分段数量。
    使用 scipy.Gaussian 机器学习统计算法进行第二次分析
    If you meet a Warning message, To slove this need upgrade scipy=>1.2. 
    but QUANTAXIS incompatible scipy=>1.2

    Parameters
    ----------
    price : (N,) array_like
        传入需要查找极值点的价格-时间序列。
        The numerator coefficient vector of the filter.
    return_ref : bool or None, optional
        返回作为参照的平滑曲线，平滑曲线的目的是减少锯齿抖动，减少计算的极值点。
        Return the smoothed line for reference.
    offest : int or None, optional
        传递参数时可能会被 .dropna() 或者 price[t:0] 等切片手段移除 nparray 头部
        的 np.nan 元素，因为此函数返回的是向量节点的数组索引，为了跟原始参数对应，调用者
        可以指定一个补偿偏移量，在返回的最大最小值中每个索引都会追加这个偏移量。
        The number of elements index offest, for jump np.nan in price's head.

    Returns
    -------
    x_tp_min, x_tp_max : ndarray
        包含最大值和最少值索引的数组
        The min/max peakpoint's index in array.

    """
    xn = price

    # Create an order 3 lowpass butterworth filter.
    b, a = butter(3, 0.05)

    # Apply the filter to xn.  Use lfilter_zi to choose the initial condition
    # of the filter.
    zi = lfilter_zi(b, a)
    z, _ = lfilter(b, a, xn, zi=zi * xn[0])

    # Apply the filter again, to have a result filtered at an order
    # the same as filtfilt.
    z2, _ = lfilter(b, a, z, zi=zi * z[0])

    # Use filtfilt to apply the filter.  If you meet a Warning need upgrade to
    # scipy=>1.2 but QUANTAXIS incompatible scipy=>1.2
    y = filtfilt(b, a, xn)

    # pass 1
    x_tp_min, x_tp_max = signal.argrelextrema(y, np.less)[0], signal.argrelextrema(y, np.greater)[0]
    n = int(len(price) / (len(x_tp_min) + len(x_tp_max))) * 2

    # peakutils 似乎一根筋只能查最大极值，通过曲线反相的方式查找极小点
    mirrors = (price * -1) + np.mean(price) * 2

    # pass 2 使用 peakutils 查找
    x_tp_max = peakutils.indexes(price, thres=0.01 / max(price), min_dist=n)
    x_tp_min = peakutils.indexes(mirrors, thres=0.01 / max(price), min_dist=n)

    if (return_ref):
        return x_tp_min + offest, x_tp_max + offest, y
    else:
        return x_tp_min + offest, x_tp_max + offest


def Timeline_Integral_with_lambda(Tm,):
    """
    explanation:
       计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)		

    params:
        * Tm ->:
            meaning: 数据
            type: null
            optional: [null]

    return:
        np.array

    demonstrate:
        Not described

    output:
        Not described
    """
    T = [Tm[0]]
    #Ti = list(map(lambda x: reduce(lambda z,y: y * (z + y), Tm[0:x]), Tm))
    #Ti = list(map(lambda x,y: x * (y + x), Ti[1:], Tm))
    # print(Ti)
    #list(map(lambda x,y: x * (y + x), Tm[1:], T))
    return np.array(T)


@nb.jit(nopython=True)
def Timeline_Integral(Tm:np.ndarray,):
    """
    explanation:
        计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)，经测试for实现最快，比reduce快	

    params:
        * Tm ->:
            meaning:
            type: null
            optional: [null]

    return:
        np.array

    demonstrate:
        Not described

    output:
        Not described
    """
    T = np.zeros(len(Tm)).astype(np.int32)
    for i, Tmx in enumerate(Tm):
        T[i] = Tmx * (T[i - 1] + Tmx)
    return T


def Timeline_Integral_with_reduce(Tm,):
    """
    explanation:
        计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)，经测试for实现最快，比reduce快		

    params:
        * Tm ->:
            meaning: 数据
            type: null
            optional: [null]

    return:
        np.array

    demonstrate:
        Not described

    output:
        Not described
    """
    T = []
    for i in range(1,len(Tm)):
        T.append(reduce(lambda x,y: int(y * (y + x)), Tm[0:i]))
    return np.array(T)


@nb.jit(nopython=True)
def Timeline_Integral_with_cross_before(Tm:np.ndarray,):
    """
    explanation:
         计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)不清零，金叉(0-->1)清零)		
         经测试for最快，比reduce快(无jit，jit的话for就更快了)

    params:
        * Tm ->:
            meaning: 数据
            type: null
            optional: [null]

    return:
        np.array
	
    demonstrate:
        Not described
	
    output:
        Not described
    """
    T = np.zeros(len(Tm)).astype(np.int32)
    for i, Tmx in enumerate(Tm):
        T[i] = (T[i - 1] + 1) if (Tmx != 1) else 0
    return T


@nb.jit(nopython=True)
def LIS(X):
    """
    explanation:
        计算最长递增子序列		
        Longest increasing subsequence
		
    params:
        * X ->:
            meaning: 序列
            type: null
            optional: [null]

    return:
        (子序列开始位置, 子序列结束位置)

    demonstrate:
        Not described

    output:
        Not described
    """
    N = len(X)
    P = [0] * N
    M = [0] * (N + 1)
    L = 0
    for i in range(N):
        lo = 1
        hi = L
        while lo <= hi:
            mid = (lo + hi) // 2
            if (X[M[mid]] < X[i]):
                lo = mid + 1
            else:
                hi = mid - 1

        newL = lo
        P[i] = M[newL - 1]
        M[newL] = i

        if (newL > L):
            L = newL

    S = []
    pos = []
    k = M[L]
    for i in range(L - 1, -1, -1):
        S.append(X[k])
        pos.append(k)
        k = P[k]
    return S[::-1], pos[::-1]


@nb.jit(nopython=True)
def LDS(X):
    """
    explanation:
        计算最长递减子序列		
        Longest decreasing subsequence
		
    params:
        * X ->:
            meaning: 序列
            type: null
            optional: [null]

    return:
         (子序列开始位置, 子序列结束位置)


    demonstrate:
        Not described

    output:
        Not described
    """
    N = len(X)
    P = [0] * N
    M = [0] * (N + 1)
    L = 0
    for i in range(N):
        lo = 1
        hi = L
        while lo <= hi:
            mid = (lo + hi) // 2
            if (X[M[mid]] > X[i]):
                lo = mid + 1
            else:
                hi = mid - 1

        newL = lo
        P[i] = M[newL - 1]
        M[newL] = i

        if (newL > L):
            L = newL

    S = []
    pos = []
    k = M[L]
    for i in range(L - 1, -1, -1):
        S.append(X[k])
        pos.append(k)
        k = P[k]
    return S[::-1], pos[::-1]



def price_predict_with_macd_trend_func(data):
    """
    价格趋势，基于巴特沃斯带通滤波器和scipy.Gaussian机器学习统计算法预测
    它包含了macd_cross_func()全部功能（没办法，重复计算2次MACD似乎很蠢）
    """
    MACD = TA_MACD(data.close)
    
    PRICE_PREDICT = pd.DataFrame(columns=['PRICE_PRED_CROSS', 'PRICE_PRED_CROSS_JX', 'PRICE_PRED_CROSS_SX', 'MACD_CROSS', 'MACD_CROSS_JX', 'MACD_CROSS_SX'], index=data.index)
    PRICE_PREDICT = PRICE_PREDICT.assign(DIF=MACD[:,0])
    PRICE_PREDICT = PRICE_PREDICT.assign(DEA=MACD[:,1])
    PRICE_PREDICT = PRICE_PREDICT.assign(MACD=MACD[:,2])
    PRICE_PREDICT = PRICE_PREDICT.assign(DELTA=MACD[:,3])

    dea_tp_min, dea_tp_max = find_peak_vextors(PRICE_PREDICT['DEA'].values[33:], offest=33)
    PRICE_PREDICT.iloc[dea_tp_min, PRICE_PREDICT.columns.get_loc('MACD_CROSS')] = 1
    PRICE_PREDICT.iloc[dea_tp_max, PRICE_PREDICT.columns.get_loc('MACD_CROSS')] = -1
    MACD_CROSS_JX = CROSS(PRICE_PREDICT['DIF'], PRICE_PREDICT['DEA'])
    DEA_CROSS_JX = CROSS(PRICE_PREDICT['DEA'], 0)
    MACD_CROSS_SX = CROSS(PRICE_PREDICT['DEA'], PRICE_PREDICT['DIF'])
    DEA_CROSS_SX = CROSS(0, PRICE_PREDICT['DEA'])
    PRICE_PREDICT.loc[MACD_CROSS_JX == 1, 'MACD_CROSS_JX'] = 1
    PRICE_PREDICT.loc[MACD_CROSS_SX == 1, 'MACD_CROSS_SX'] = -1
    PRICE_PREDICT.iloc[dea_tp_min, PRICE_PREDICT.columns.get_loc('MACD_CROSS_JX')] = 1
    PRICE_PREDICT.iloc[dea_tp_max, PRICE_PREDICT.columns.get_loc('MACD_CROSS_SX')] = 1
    PRICE_PREDICT['MACD_CROSS_JX'] = Timeline_Integral_with_cross_before(PRICE_PREDICT['MACD_CROSS_JX'])
    PRICE_PREDICT['MACD_CROSS_SX'] = Timeline_Integral_with_cross_before(PRICE_PREDICT['MACD_CROSS_SX'])

    # pass 1
    x_tp_min, x_tp_max = find_peak_vextors(data.close.values)
    PRICE_PREDICT.iloc[x_tp_min, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS')] = x_tp_min
    PRICE_PREDICT.iloc[x_tp_max, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS')] = -x_tp_max
    PRICE_PREDICT.iloc[x_tp_min, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS_JX')] = 1
    PRICE_PREDICT.iloc[x_tp_max, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS_SX')] = 1

    # pass 2 MACD 金叉的时候寻找更多的极值点，创造更多买入条件
    x_tp_min, x_tp_max = find_peak_vextors_eagerly(data.close.values)
    macd_up_trend_PEAKPOINT_MIN = (PRICE_PREDICT.iloc[x_tp_min, PRICE_PREDICT.columns.get_loc('MACD_CROSS_JX')] < PRICE_PREDICT.iloc[x_tp_min, PRICE_PREDICT.columns.get_loc('MACD_CROSS_SX')])
    macd_up_trend_PEAKPOINT_MAX = (PRICE_PREDICT.iloc[x_tp_max, PRICE_PREDICT.columns.get_loc('MACD_CROSS_JX')] < PRICE_PREDICT.iloc[x_tp_max, PRICE_PREDICT.columns.get_loc('MACD_CROSS_SX')])
    macd_up_trend_PEAKPOINT_MIN = macd_up_trend_PEAKPOINT_MIN[macd_up_trend_PEAKPOINT_MIN.apply(lambda x: x == True)]  # eqv.  Trim(x == False)
    macd_up_trend_PEAKPOINT_MAX = macd_up_trend_PEAKPOINT_MAX[macd_up_trend_PEAKPOINT_MAX.apply(lambda x: x == True)]  # eqv.  Trim(x == False)
    PRICE_PREDICT.loc[macd_up_trend_PEAKPOINT_MIN.index, 'PRICE_PRED_CROSS_JX'] = 1
    PRICE_PREDICT.loc[macd_up_trend_PEAKPOINT_MAX.index, 'PRICE_PRED_CROSS_SX'] = 1
    PRICE_PREDICT.loc[macd_up_trend_PEAKPOINT_MIN.index, 'PRICE_PRED_CROSS'] = PRICE_PREDICT.loc[macd_up_trend_PEAKPOINT_MIN.index].apply(lambda x: PRICE_PREDICT.index.get_level_values(level=0).get_loc(x.name[0]), axis=1)
    PRICE_PREDICT.loc[macd_up_trend_PEAKPOINT_MAX.index, 'PRICE_PRED_CROSS'] = PRICE_PREDICT.loc[macd_up_trend_PEAKPOINT_MAX.index].apply(lambda x: PRICE_PREDICT.index.get_level_values(level=0).get_loc(x.name[0]) * -1, axis=1)

    PRICE_PREDICT['PRICE_PRED_CROSS_JX'] = Timeline_Integral_with_cross_before(PRICE_PREDICT['PRICE_PRED_CROSS_JX'])
    PRICE_PREDICT['PRICE_PRED_CROSS_SX'] = Timeline_Integral_with_cross_before(PRICE_PREDICT['PRICE_PRED_CROSS_SX'])
    if (len(PRICE_PREDICT.index.names) > 2):
        return PRICE_PREDICT.reset_index([1,2])
    elif (len(PRICE_PREDICT.index.names) > 1):
        return PRICE_PREDICT.reset_index([1])
    else:
        return PRICE_PREDICT


def macd_cross_func(data):
    """
    神一样的指标：MACD
    """
    MACD = TA_MACD(data.close)
    
    MACD_CROSS = pd.DataFrame(columns=['MACD_CROSS', 'MACD_CROSS_JX', 'MACD_CROSS_SX'], index=data.index)
    MACD_CROSS = MACD_CROSS.assign(DIF=MACD[:,0])
    MACD_CROSS = MACD_CROSS.assign(DEA=MACD[:,1])
    MACD_CROSS = MACD_CROSS.assign(MACD=MACD[:,2])
    MACD_CROSS = MACD_CROSS.assign(DELTA=MACD[:,3])

    dea_tp_min, dea_tp_max = find_peak_vextors(MACD_CROSS['DEA'].values[33:], offest=33)
    MACD_CROSS.iloc[dea_tp_min, MACD_CROSS.columns.get_loc('MACD_CROSS')] = 1
    MACD_CROSS.iloc[dea_tp_max, MACD_CROSS.columns.get_loc('MACD_CROSS')] = -1
    MACD_CROSS_JX = CROSS(MACD_CROSS['DIF'], MACD_CROSS['DEA'])
    MACD_CROSS_SX = CROSS(MACD_CROSS['DEA'], MACD_CROSS['DIF'])
    MACD_CROSS.loc[MACD_CROSS_JX == 1, 'MACD_CROSS_JX'] = 1
    MACD_CROSS.loc[MACD_CROSS_SX == 1, 'MACD_CROSS_SX'] = -1
    MACD_CROSS.iloc[dea_tp_min, MACD_CROSS.columns.get_loc('MACD_CROSS_JX')] = 1
    MACD_CROSS.iloc[dea_tp_max, MACD_CROSS.columns.get_loc('MACD_CROSS_SX')] = 1

    MACD_CROSS['MACD_CROSS_JX'] = Timeline_Integral_with_cross_before(MACD_CROSS['MACD_CROSS_JX'])
    MACD_CROSS['MACD_CROSS_SX'] = Timeline_Integral_with_cross_before(MACD_CROSS['MACD_CROSS_SX'])
    return MACD_CROSS


def maxfactor_cross_func(data):
    """
    自创指标：MAXFACTOR
    """
    RSI = QA.TA_RSI(data.close, timeperiod=12)
    CCI = QA.TA_CCI(data.high, data.low, data.close)
    KDJ = QA.TA_KDJ(data.high, data.low, data.close)    
    MAX_FACTOR = CCI[:,0] + (RSI[:,0] - 50) * 4 + (KDJ[:,2] - 50) * 4
    MAX_FACTOR_delta = np.r_[np.nan, np.diff(MAX_FACTOR)]
    REGRESSION_BASELINE = pd.Series((RSI[:,0] - 50) * 4, index=data.index)

    MAXFACTOR_CROSS = pd.DataFrame(columns=['MAXFACTOR_CROSS', 'MAXFACTOR_CROSS_JX', 'MAXFACTOR_CROSS_SX'], index=data.index)
    MAXFACTOR_CROSS = MAXFACTOR_CROSS.assign(MAXFACTOR=MAX_FACTOR)
    MAXFACTOR_CROSS = MAXFACTOR_CROSS.assign(MAXFACTOR_DELTA=MAX_FACTOR_delta)
    MAXFACTOR_CROSS = MAXFACTOR_CROSS.assign(REGRESSION_BASELINE=REGRESSION_BASELINE)

    MAXFACTOR_CROSS_JX1 = CROSS(MAX_FACTOR + MAX_FACTOR_delta, REGRESSION_BASELINE - 133)
    MAXFACTOR_CROSS_JX2 = CROSS(MAX_FACTOR + MAX_FACTOR_delta, REGRESSION_BASELINE)
    MAXFACTOR_CROSS_JX3 = CROSS(MAX_FACTOR + MAX_FACTOR_delta, REGRESSION_BASELINE + 133)
    MAXFACTOR_CROSS_JX_JUNCTION = (MAXFACTOR_CROSS_JX1 | MAXFACTOR_CROSS_JX2 | MAXFACTOR_CROSS_JX3)
    MAXFACTOR_CROSS_SX1 = CROSS(REGRESSION_BASELINE + 133, MAX_FACTOR + MAX_FACTOR_delta)
    MAXFACTOR_CROSS_SX2 = CROSS(REGRESSION_BASELINE, MAX_FACTOR + MAX_FACTOR_delta)
    MAXFACTOR_CROSS_SX3 = CROSS(REGRESSION_BASELINE - 133, MAX_FACTOR + MAX_FACTOR_delta)
    MAXFACTOR_CROSS_SX_JUNCTION = (MAXFACTOR_CROSS_SX1 | MAXFACTOR_CROSS_SX2 | MAXFACTOR_CROSS_SX3)
    MAXFACTOR_CROSS.loc[(MAXFACTOR_CROSS_JX1 | MAXFACTOR_CROSS_JX2 | MAXFACTOR_CROSS_JX3) == 1, 'MAXFACTOR_CROSS'] = 1
    MAXFACTOR_CROSS.loc[(MAXFACTOR_CROSS_SX1 | MAXFACTOR_CROSS_SX2 | MAXFACTOR_CROSS_SX3) == 1, 'MAXFACTOR_CROSS'] = -1
    MAXFACTOR_CROSS['MAXFACTOR_CROSS_JX'] = Timeline_Integral_with_cross_before(MAXFACTOR_CROSS_JX_JUNCTION)
    MAXFACTOR_CROSS['MAXFACTOR_CROSS_SX'] = Timeline_Integral_with_cross_before(MAXFACTOR_CROSS_SX_JUNCTION)
    return MAXFACTOR_CROSS


def dual_cross_func(data):
    """
    自创指标：CCI/KDJ 对 偏移后的 RSI 双金叉
    为了避免 Warning，计算时忽略了前13个 NaN 的，最后 加入DataFrame 的时候补回来
    """
    RSI = TA_RSI(data.close, timeperiod=12)
    CCI = TA_CCI(data.high, data.low, data.close)
    KDJ = TA_KDJ(data.high, data.low, data.close)
    
    CCI_CROSS_JX = CROSS_STATUS(CCI[13:,0], (RSI[13:,0] - 50) * 4)
    KDJ_J_CROSS_JX = CROSS_STATUS(KDJ[13:,2], RSI[13:,0])
    KDJ_J_CROSS_JX_PLUS = CROSS_STATUS(KDJ[13:,2] + KDJ[13:,3], RSI[13:,0])
    DUAL_CROSS_JX = np.r_[np.zeros(13), CROSS_STATUS(CCI_CROSS_JX * (CCI_CROSS_JX + KDJ_J_CROSS_JX + KDJ_J_CROSS_JX_PLUS), 1)]
    
    CCI_CROSS_SX = CROSS_STATUS((RSI[13:,0] - 50) * 4, CCI[13:,0])
    KDJ_J_CROSS_SX = CROSS_STATUS(RSI[13:,0], KDJ[13:,2])
    KDJ_J_CROSS_SX_PLUS = CROSS_STATUS(RSI[13:,0], KDJ[13:,2] + KDJ[13:,3])
    DUAL_CROSS_SX = np.r_[np.zeros(13), CROSS_STATUS(CCI_CROSS_SX * (CCI_CROSS_SX + KDJ_J_CROSS_SX + KDJ_J_CROSS_SX_PLUS), 1)]

    DUAL_CROSS = pd.DataFrame(columns=['DUAL_CROSS', 'DUAL_CROSS_JX', 'DUAL_CROSS_SX'], index=data.index)
    DUAL_CROSS.loc[DUAL_CROSS_JX == 1, 'DUAL_CROSS'] = 1
    DUAL_CROSS.loc[DUAL_CROSS_SX == 1, 'DUAL_CROSS'] = -1
    DUAL_CROSS['DUAL_CROSS_JX'] = Timeline_Integral(DUAL_CROSS_JX)
    DUAL_CROSS['DUAL_CROSS_SX'] = Timeline_Integral(DUAL_CROSS_SX)
    return DUAL_CROSS


def ma30_cross_func(data):
    """
    MA均线金叉指标
    """
    MA5 = talib.MA(data.close, 5)
    MA30 = talib.MA(data.close, 30)
    
    MA30_CROSS_JX = CROSS(MA5, MA30)
    MA30_CROSS_JX_Integral = Timeline_Integral_with_cross_before(MA30_CROSS_JX)
    MA30_CROSS_SX = CROSS(MA30, MA5)
    MA30_CROSS_SX_Integral = Timeline_Integral_with_cross_before(MA30_CROSS_SX)
    
    MA30_CROSS = pd.DataFrame(columns=['MA30_CROSS', 'MA30_CROSS_JX', 'MA30_CROSS_SX', 'MA30_TP_CROSS_JX', 'MA30_TP_CROSS_SX'], index=data.index)
    MA30_CROSS.loc[MA30_CROSS_JX == 1, 'MA30_CROSS'] = 1
    MA30_CROSS.loc[MA30_CROSS_SX == 1, 'MA30_CROSS'] = -1
    MA30_CROSS['MA30_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_CROSS_JX)
    MA30_CROSS['MA30_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_CROSS_SX)
    
    # MA30 前29个是 NaN，处理会抛出 Warning，使用 [29:] 则不会计算 NaN，相应的 return_index+29
    MA30_tp_min, MA30_tp_max = find_peak_vextors(MA30.values[29:], offest=29)
    MA30_TP_CROSS = pd.DataFrame(columns=['MA30_TP_CROSS_JX', 'MA30_TP_CROSS_SX'], index=data.index)
    MA30_TP_CROSS['MA30_TP_CROSS_SX'] = MA30_TP_CROSS['MA30_TP_CROSS_JX'] = 0
    MA30_TP_CROSS.iloc[MA30_tp_min, MA30_TP_CROSS.columns.get_loc('MA30_TP_CROSS_JX')] = 1
    MA30_TP_CROSS.iloc[MA30_tp_max, MA30_TP_CROSS.columns.get_loc('MA30_TP_CROSS_SX')] = 1
    MA30_CROSS['MA30_TP_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_TP_CROSS['MA30_TP_CROSS_JX'])
    MA30_CROSS['MA30_TP_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_TP_CROSS['MA30_TP_CROSS_SX'])
    return MA30_CROSS


def boll_cross_func(data):
    """
    布林线和K线金叉死叉 状态分析
    """
    BBANDS = TA_BBANDS(data.close, timeperiod=20, nbdevup=2)
    BOLL_CROSS = pd.DataFrame(columns=['min_peak', 'max_peak', 'BOLL_CROSS', 'BOLL_CROSS_JX', 'BOLL_CROSS_SX'], index=data.index)
    data = data.assign(BOLL_MA=BBANDS[:,1])
        
    # 防止插针行情突然搞乱故
    data['smooth_low'] = talib.MA(data.low, 2)
    data['smooth_high'] = talib.MA(data.high, 2)
    BOLL_CROSS['min_peak'] = data.apply(lambda x: min(x['open'], x['close'], x['low'] if x['open'] < x['BOLL_MA'] else x['smooth_low']), axis=1)
    BOLL_CROSS['max_peak'] = data.apply(lambda x: max(x['open'], x['close'], x['high'] if x['open'] > x['BOLL_MA'] else x['smooth_high']), axis=1)

    BOLL_CROSS_JX = CROSS(BOLL_CROSS['min_peak'], BBANDS[:,2])
    BOLL_CROSS_SX = CROSS(BBANDS[:,0], BOLL_CROSS['max_peak'])
    BOLL_CROSS.loc[BOLL_CROSS_JX == 1, 'BOLL_CROSS'] = 1
    BOLL_CROSS.loc[BOLL_CROSS_SX == 1, 'BOLL_CROSS'] = -1
    
    BOLL_TP_CROSS = pd.DataFrame(columns=['BOLL_TP_CROSS_JX', 'BOLL_TP_CROSS_SX'], index=data.index)
    BOLL_TP_CROSS['BOLL_TP_CROSS_SX'] = BOLL_TP_CROSS['BOLL_TP_CROSS_JX'] = 0
    BOLL_TP_CROSS.loc[BOLL_CROSS_JX == 1, 'BOLL_TP_CROSS_JX'] = 1
    BOLL_TP_CROSS.loc[BOLL_CROSS_SX == 1, 'BOLL_TP_CROSS_SX'] = 1

    BOLL_CROSS = BOLL_CROSS.assign(BOLL_UB=BBANDS[:,0])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_MA=BBANDS[:,1])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_LB=BBANDS[:,2])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_WIDTH=BBANDS[:,3])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_DELTA=BBANDS[:,4])
    BOLL_CROSS = BOLL_CROSS.assign(BBW_MA20=talib.MA(BBANDS[:,3], 20))
    BOLL_CROSS['BOLL_CROSS_JX'] = Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_JX'])
    BOLL_CROSS['BOLL_CROSS_SX'] = Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_SX'])
    return BOLL_CROSS

