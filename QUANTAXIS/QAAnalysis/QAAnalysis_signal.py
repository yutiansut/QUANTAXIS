# coding:utf-8
# Author: 阿财（Rgveda@github）（11652964@qq.com）
# Created date: 2020-02-27
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
from datetime import datetime, timezone, timedelta
import scipy.signal as signal
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter, savgol_filter
import peakutils
import QUANTAXIS as QA
from QUANTAXIS.QAIndicator.base import *
from QUANTAXIS.QAIndicator.talib_numpy import *
from QUANTAXIS.QAData.base_datastruct import *

"""
时序信号处理，公共函数
"""

def time_series_momemtum(price, n=24, rf=0.02):
    """
    时间序列动量指标
    Time Series Momentum strategy
    """
    return (price / price.shift(n) - 1) - rf


def find_peak_vextors_eagerly(price, smooth_ma5=[], offest=0):
    """
    （饥渴的）在 MACD 上坡的时候查找更多的极值点
    """
    xn = price

    # pass 0
    if (len(smooth_ma5) == len(price)):
        yy_sg = smooth_ma5
    else:
        yy_sg = np.r_[np.zeros(11), TA_HMA(xn, 10)[11:]]

    # pass 1
    x_tp_min, x_tp_max = signal.argrelextrema(yy_sg, np.less)[0], signal.argrelextrema(yy_sg, np.greater)[0]
    n = int(len(price) / (len(x_tp_min) + len(x_tp_max)))

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
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)
    """
    T = [Tm[0]]
    #Ti = list(map(lambda x: reduce(lambda z,y: y * (z + y), Tm[0:x]), Tm))
    #Ti = list(map(lambda x,y: x * (y + x), Ti[1:], Tm))
    #print(Ti)
    #list(map(lambda x,y: x * (y + x), Tm[1:], T))
    return np.array(T)


def Timeline_Integral(Tm,):
    """
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)，经测试for实现最快，比reduce快
    """
    T = [Tm[0]]
    for i in range(1,len(Tm)):
        T.append(Tm[i] * (T[i - 1] + Tm[i]))
    return np.array(T)


def Timeline_Integral_with_reduce(Tm,):
    """
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)清零)，经测试for实现最快，比reduce快
    """
    T = []
    for i in range(1,len(Tm)):
        T.append(reduce(lambda x,y: y * (y + x), Tm[0:i]))
    return np.array(T)


# 经测试for最快，比reduce快
def Timeline_Integral_with_cross_before(Tm,):
    """
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)不清零，金叉(0-->1)清零)
    """
    T = [Tm[0]]
    for i in range(1,len(Tm)):
        T.append(T[i - 1] + 1) if (Tm[i] != 1) else T.append(0)
    return np.array(T)


def LIS(X):
    """
    计算最长递增子序列
    Longest increasing subsequence
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
    return S[::-1],pos[::-1]


def LDS(X):
    """
    计算最长递减子序列
    Longest decreasing subsequence
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
    return S[::-1],pos[::-1]


def kline_returns_func(data, format='pd'):
    """
    计算单个标的每 bar 跟前一bar的利润率差值
    多用途函数，可以是 QA_DataStruct.add_func 调用（可以用于多标的计算），
    也可以是函数式调用（切记单独函数式调用不能多个标的混合计算）。
    Calculating a signal Stock/price timeseries kline's returns.
    For each data[i]/data[i-1] at series value of percentage.

    Parameters
    ----------
    data : (N,) array_like or pd.DataFrame or QA_DataStruct
        传入 OHLC Kline 序列。参数类型可以为 numpy，pd.DataFrame 或者 QA_DataStruct
        The OHLC Kline.
        在传入参数中不可混入多标的数据，如果需要处理多标的价格数据，通过
        QA_DataStruct.add_func 调用。
        It can prossessing multi indices/stocks by QA_DataStruct.add_func
        called. With auto splited into single price series 
        by QA_DataStruct.add_func().
        For standalone called, It should be only pass one stock/price series. 
        If not the result will unpredictable.
    format : str, optional
        返回类型 默认值为 'pd' 将返回 pandas.DataFrame 格式的结果
        可选类型，'np' 或 etc 返回 nparray 格式的结果
        第一个 bar 会被填充为 0.
        Return data format, default is 'pd'. 
        It will return a pandas.DataFrame as result.
        If seted as string: 'np' or etc string value, 
        It will return a nparray as result.
        The first bar will be fill with zero.

    Returns
    -------
    kline returns : pandas.DataFrame or nparray
        'returns' 跟前一收盘价格变化率的百分比

    """
    from QUANTAXIS.QAData.base_datastruct import _quotation_base
    if isinstance(data, pd.DataFrame) or \
        (isinstance(data, _quotation_base)):
        data = data.close

    if (format == 'pd'):
        kline_returns = pd.DataFrame(np.nan_to_num(np.log(data / data.shift(1)), 
                                                   nan=0),
                                     columns=['returns'], 
                                     index=data.index)
        return kline_returns
    else:
        return np.nan_to_num(np.log(data / data.shift(1)), nan=0)


def price_predict_with_rolling_integral(kline, 
                                        indices, 
                                        indices_tp_min, 
                                        indices_tp_max, 
                                        offest=11):
    """
    对预算折返点的价格进行趋势计算，预测价格趋势
    """
    # pass 1
    PRICE_PREDICT = pd.DataFrame(columns=['POSITION', 'PRICE_PRED_CROSS', 'PRICE_PRED_CROSS_JX', 'PRICE_PRED_CROSS_SX', 'returns'], index=kline.index)
    PRICE_PREDICT.iloc[indices_tp_min, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS')] = indices_tp_min
    PRICE_PREDICT.iloc[indices_tp_max, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS')] = -indices_tp_max
    PRICE_PREDICT.iloc[indices_tp_min, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS_JX')] = 1
    PRICE_PREDICT.iloc[indices_tp_max, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS_SX')] = 1
    PRICE_PREDICT['PRICE_PRED_CROSS_JX'] = Timeline_Integral_with_cross_before(PRICE_PREDICT['PRICE_PRED_CROSS_JX'])
    PRICE_PREDICT['PRICE_PRED_CROSS_SX'] = Timeline_Integral_with_cross_before(PRICE_PREDICT['PRICE_PRED_CROSS_SX'])

    # 策略判断
    PRICE_PREDICT = PRICE_PREDICT.assign(POSITION_RAW=PRICE_PREDICT.apply(lambda x: 1 if (x['PRICE_PRED_CROSS_JX'] < x['PRICE_PRED_CROSS_SX']) else -1, axis=1))

    indices_s = pd.Series(indices, index=kline.index)
    PRICE_PREDICT['returns'] = np.log(indices_s / indices_s.shift(1))
    PRICE_PREDICT['returns_raw'] = PRICE_PREDICT['returns'].apply(lambda x: 1 if (x > 0) else -1)
    PRICE_PREDICT['POSITION'] = PRICE_PREDICT['POSITION_RAW'].rolling(4).apply(lambda x: x.sum(), raw=False).apply(lambda x:0 if np.isnan(x) else int(x))
    PRICE_PREDICT['POSITION_RETURNS'] = PRICE_PREDICT['returns_raw'].rolling(4).apply(lambda x: x.sum(), raw=False).apply(lambda x:0 if np.isnan(x) else int(x))
    PRICE_PREDICT['POSITION_JUNTION'] = (PRICE_PREDICT['POSITION'] + PRICE_PREDICT['POSITION_RETURNS']).apply(lambda x:0 if np.isnan(x) else int(x))

    if (len(PRICE_PREDICT.index.names) > 2):
        return PRICE_PREDICT.reset_index([1,2])
    elif (len(PRICE_PREDICT.index.names) > 1):
        return PRICE_PREDICT.reset_index([1])
    else:
        return PRICE_PREDICT


def price_predict_with_macd_trend_func(data):
    """
    价格趋势，基于巴特沃斯带通滤波器和scipy.Gaussian机器学习统计算法预测
    它包含了macd_cross_func()全部功能（没办法，重复计算2次MACD似乎很蠢）
    """
    MACD = QA.QA_indicator_MACD(data)
    
    PRICE_PREDICT = pd.DataFrame(columns=['PRICE_PRED_CROSS', 'PRICE_PRED_CROSS_JX', 'PRICE_PRED_CROSS_SX', 'MACD_CROSS', 'MACD_CROSS_JX', 'MACD_CROSS_SX'], index=data.index)
    PRICE_PREDICT = PRICE_PREDICT.assign(DIF=MACD[:,0])
    PRICE_PREDICT = PRICE_PREDICT.assign(DEA=MACD[:,1])
    PRICE_PREDICT = PRICE_PREDICT.assign(MACD=MACD[:,2])
    PRICE_PREDICT = PRICE_PREDICT.assign(DELTA=MACD[:,3])

    MACD_CROSS_JX = CROSS(PRICE_PREDICT['DIF'], PRICE_PREDICT['DEA'])
    DEA_CROSS_JX = CROSS(PRICE_PREDICT['DEA'], 0)
    MACD_CROSS_SX = CROSS(PRICE_PREDICT['DEA'], PRICE_PREDICT['DIF'])
    DEA_CROSS_SX = CROSS(0, PRICE_PREDICT['DEA'])
    PRICE_PREDICT['MACD_CROSS'] = np.where(MACD_CROSS_JX.values == 1, 1, np.where(MACD_CROSS_SX.values == 1, -1, 0))
    dea_tp_min, dea_tp_max = find_peak_vextors(PRICE_PREDICT['DEA'].values[33:], offest=33)
    PRICE_PREDICT.iloc[dea_tp_min, PRICE_PREDICT.columns.get_loc('MACD_CROSS')] = 1
    PRICE_PREDICT.iloc[dea_tp_max, PRICE_PREDICT.columns.get_loc('MACD_CROSS')] = -1
    PRICE_PREDICT['MACD_CROSS_JX'] = np.where(MACD_CROSS_JX.values == 1, 1, 0)
    PRICE_PREDICT['MACD_CROSS_SX'] = np.where(MACD_CROSS_SX.values == 1, 1, 0)
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
    #macd_up_trend_PEAKPOINT_MAX = (PRICE_PREDICT.iloc[x_tp_max,
    #PRICE_PREDICT.columns.get_loc('MACD_CROSS_JX')] <
    #PRICE_PREDICT.iloc[x_tp_max,
    #PRICE_PREDICT.columns.get_loc('MACD_CROSS_SX')])
    PRICE_PREDICT.iloc[x_tp_min, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS_JX')] = np.where(macd_up_trend_PEAKPOINT_MIN.values == True, 1, 0)
    PRICE_PREDICT.iloc[x_tp_max, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS_SX')] = 1
    PRICE_PREDICT.iloc[x_tp_min, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS')] = PRICE_PREDICT.iloc[x_tp_min].apply(lambda x: PRICE_PREDICT.index.get_level_values(level=0).get_loc(x.name[0]), axis=1)
    PRICE_PREDICT.iloc[x_tp_max, PRICE_PREDICT.columns.get_loc('PRICE_PRED_CROSS')] = PRICE_PREDICT.iloc[x_tp_max].apply(lambda x: PRICE_PREDICT.index.get_level_values(level=0).get_loc(x.name[0]) * -1, axis=1)

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
    MACD = QA.QA_indicator_MACD(data)
    
    MACD_CROSS = pd.DataFrame(columns=['MACD_CROSS', 'MACD_CROSS_JX', 'MACD_CROSS_SX'], index=data.index)
    MACD_CROSS = MACD_CROSS.assign(DIF=MACD['DIF'])
    MACD_CROSS = MACD_CROSS.assign(DEA=MACD['DEA'])
    MACD_CROSS = MACD_CROSS.assign(MACD=MACD['MACD'])
    MACD_CROSS = MACD_CROSS.assign(ZERO=0)
    # 新版考虑合并指标，将 DELTA 重命名为 MACD_DELTA
    MACD_CROSS = MACD_CROSS.assign(MACD_DELTA=MACD['MACD'].diff())
    # 为了兼容旧代码，继续保留 DELTA 字段数据一段时间
    MACD_CROSS = MACD_CROSS.assign(DELTA=MACD['MACD'].diff())

    dea_tp_min, dea_tp_max = find_peak_vextors(MACD_CROSS['DEA'].values[33:], offest=33)
    MACD_CROSS.iloc[dea_tp_min, MACD_CROSS.columns.get_loc('MACD_CROSS')] = 1
    MACD_CROSS.iloc[dea_tp_max, MACD_CROSS.columns.get_loc('MACD_CROSS')] = -1
    MACD_CROSS['MACD_CROSS_JX'] = CROSS(MACD_CROSS['DIF'], MACD_CROSS['DEA'])
    MACD_CROSS['MACD_CROSS_SX'] = CROSS(MACD_CROSS['DEA'], MACD_CROSS['DIF'])
    MACD_CROSS['MACD_CROSS'] = np.where(MACD_CROSS['MACD_CROSS_JX'] == 1, 1, np.where(MACD_CROSS['MACD_CROSS_SX'] == 1, -1, 0))
    MACD_CROSS.iloc[dea_tp_min, MACD_CROSS.columns.get_loc('MACD_CROSS_JX')] = 1
    MACD_CROSS.iloc[dea_tp_max, MACD_CROSS.columns.get_loc('MACD_CROSS_SX')] = 1

    MACD_CROSS['DEA_CROSS_JX'] = Timeline_Integral_with_cross_before(CROSS(MACD_CROSS['DEA'], MACD_CROSS['ZERO']))
    MACD_CROSS['DEA_CROSS_SX'] = Timeline_Integral_with_cross_before(CROSS(MACD_CROSS['ZERO'], MACD_CROSS['DEA']))
    MACD_CROSS['MACD_CROSS_JX'] = Timeline_Integral_with_cross_before(MACD_CROSS['MACD_CROSS_JX'])
    MACD_CROSS['MACD_CROSS_SX'] = Timeline_Integral_with_cross_before(MACD_CROSS['MACD_CROSS_SX'])
    return MACD_CROSS


def maxfactor_cross_func(data):
    """
    自创指标：MAXFACTOR
    """
    RSI = TA_RSI(data.close, timeperiod=12)
    CCI = TA_CCI(data.high, data.low, data.close)
    KDJ = TA_KDJ(data.high, data.low, data.close)    
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
    MAXFACTOR_CROSS['MAXFACTOR_CROSS'] = np.where(MAXFACTOR_CROSS_JX_JUNCTION.values == 1, 
                                             1, 
                                             np.where(MAXFACTOR_CROSS_SX_JUNCTION.values == 1,
                                                     -1, 0))
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
    DUAL_CROSS['DUAL_CROSS'] = np.where(DUAL_CROSS_JX == 1, 1, np.where(DUAL_CROSS_SX == 1, -1, 0))
    DUAL_CROSS['DUAL_CROSS_JX'] = Timeline_Integral(DUAL_CROSS_JX)
    DUAL_CROSS['DUAL_CROSS_SX'] = Timeline_Integral(DUAL_CROSS_SX)
    return DUAL_CROSS


def ma30_cross_func(data):
    """
    MA均线金叉指标
    """
    MA5 = talib.MA(data.close, 5)
    MA30 = talib.MA(data.close, 30)
        
    MA30_CROSS = pd.DataFrame(columns=['MA30_CROSS', 'MA30_CROSS_JX', 'MA30_CROSS_SX', 'MA30_TP_CROSS_JX', 'MA30_TP_CROSS_SX'], index=data.index)
    MA30_CROSS = MA30_CROSS.assign(MA5=MA5)
    MA30_CROSS = MA30_CROSS.assign(MA30=MA30)
    MA30_CROSS['MA30_CROSS_JX'] = CROSS(MA5, MA30)
    MA30_CROSS['MA30_CROSS_SX'] = CROSS(MA30, MA5)
    MA30_CROSS['MA30_CROSS'] = np.where(MA30_CROSS['MA30_CROSS_JX'].values == 1, 1, np.where(MA30_CROSS['MA30_CROSS_SX'].values == 1, -1, 0))
    MA30_CROSS['MA30_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_CROSS['MA30_CROSS_JX'])
    MA30_CROSS['MA30_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_CROSS['MA30_CROSS_SX'])
    
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

    BOLL_TP_CROSS = pd.DataFrame(columns=['BOLL_TP_CROSS_JX', 'BOLL_TP_CROSS_SX'], index=data.index)
    BOLL_TP_CROSS['BOLL_TP_CROSS_JX'] = CROSS(BOLL_CROSS['min_peak'], BBANDS[:,2])
    BOLL_TP_CROSS['BOLL_TP_CROSS_SX'] = CROSS(BBANDS[:,0], BOLL_CROSS['max_peak'])
    BOLL_CROSS['BOLL_CROSS'] = np.where(BOLL_TP_CROSS['BOLL_TP_CROSS_JX'].values == 1, 1, np.where(BOLL_TP_CROSS['BOLL_TP_CROSS_SX'].values == 1, -1, 0))

    BOLL_CROSS = BOLL_CROSS.assign(BOLL_UB=BBANDS[:,0])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_MA=BBANDS[:,1])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_LB=BBANDS[:,2])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_WIDTH=BBANDS[:,3])
    BOLL_CROSS = BOLL_CROSS.assign(BOLL_DELTA=BBANDS[:,4])
    BOLL_CROSS = BOLL_CROSS.assign(BBW_MA20=talib.MA(BBANDS[:,3], 20))
    BOLL_CROSS['BOLL_CROSS_JX'] = Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_JX'])
    BOLL_CROSS['BOLL_CROSS_SX'] = Timeline_Integral_with_cross_before(BOLL_TP_CROSS['BOLL_TP_CROSS_SX'])
    return BOLL_CROSS


def ma_power(price, range_list=range(5, 30)):
    '''
    多头排列能量强度定义
    '''
    def inv_num(series):
        '''
        计算逆序数个数
        '''
        series = np.array(series)  # 提升速度
        return np.sum([np.sum(x < series[:i]) for i, x in enumerate(series)])

    ma_pd = pd.DataFrame()
    for r in range_list:
        ma = talib.MA(price, r)
        if len(ma_pd) == 0:
            ma_pd = ma
        else:
            ma_pd = pd.concat([ma_pd, ma], axis=1)
    ma_pd.columns = range_list
    df_fixed = ma_pd.dropna()  # 前n个数据部分均线为空值，去除
    num = df_fixed.apply(lambda x: inv_num(x), axis=1)  # 每排逆序个数
    ratio = num / (len(range_list) * (len(range_list) - 1)) * 2
    return pd.DataFrame({'MAPOWER':ratio.reindex(ma_pd.index)})


def machine_learning_trend_func(data):
    """
    使用机器学习算法统计分析趋势
    """
    # 统计学习方法分析大趋势：数据准备
    highp = data.high.values
    lowp = data.low.values
    openp = self._ticks[AKA.OPEN].values
    closep = self._ticks[AKA.CLOSE].values

    # DPGMM 聚类
    X = []
    idx = []
    lag = 30
    for i in range(len(closep)):
        left = max(0,i - lag)
        right = min(len(closep) - 1,i + lag)
        l = max(0,i - 1)
        r = min(len(closep) - 1,i + 1)
        for j in range(left,right):
            minP = min(closep[left:right])
            maxP = max(closep[left:right])
            low = 1 if closep[i] <= closep[l] and closep[i] < closep[r] else 0
            high = 1 if closep[i] >= closep[l] and closep[i] > closep[r] else 0
        x = [i, closep[i], minP, maxP, low, high]
        X.append(x)
        idx.append(i)
    X = np.array(X)
    idx = np.array(idx)

    dpgmm = mixture.BayesianGaussianMixture(n_components=max(int(to_be_trimmed / 10), 16), max_iter=1000, covariance_type='spherical', weight_concentration_prior_type='dirichlet_process')
    # 训练模型不含最后一个点
    dpgmm.fit(X[:-1])
    y_t = dpgmm.predict(X)

    # 以DPGMM聚类进行分段，计算线性回归斜率
    #dif_max_fatcor = self._ind[FLD.MAX_FACTOR_CROSS_SX] - self._ind[FLD.MAX_FACTOR_CROSS_JX]

    lr = LinearRegression()       
    for c in np.unique(y_t):
        inV = []
        outV = []
        for i in range(len(closep)):
            if y_t[i] - c == 0:
                inV.append(i)
                outV.append(closep[i])

        inV = np.atleast_2d(np.array(inV)).T
        outV = np.array(outV)
        lr.fit(inV,outV)
            
        estV = lr.predict(inV)

        # 数字索引降维
        inV = np.reshape(inV, len(inV))
        self._ind.iloc[inV, self._ind.columns.get_loc(FLD.REGRESSION_PRICE)] = estV
        self._ind.iloc[inV, self._ind.columns.get_loc(FLD.REGRESSION_SLOPE)] = lr.coef_[0]
        if (lr.coef_[0] > 0):
            self._ind.iloc[inV, self._ind.columns.get_loc(FLD.REGRESSION_DIRECTION)] = estV

        # 原使用线性回归拟近，后发现合并计算MAX_FACTOR金叉/死叉时间卷积平均值，得出曲线趋势（在小斜率状态比线性回归准确）
        self._ind.iloc[inV, self._ind.columns.get_loc(FLD.REGRESSION_MAX_FACTOR)] = dif_max_fatcor.iloc[inV].mean()

    self._ind = self._ind.assign(TREND_STATUS=y_t)

        # DPGMM 聚类分析完毕
        # 下降趋势检测
        #if (self.Period_Time < timedelta(hours=1)):
        #    bV = lowp[signal.argrelextrema(lowp,np.less)]
        #    bP = signal.argrelextrema(lowp,np.less)[0]

        #    d,p = LIS(bV)

        #    idx = []
        #    for i in range(len(p)):
        #        idx.append(bP[p[i]])

        #    qV = highp[signal.argrelextrema(highp,np.greater)]
        #    qP = signal.argrelextrema(highp,np.greater)[0]

        #    qd,qp = LDS(qV)

        #    qidx = []
        #    for i in range(len(qp)):
        #        qidx.append(qP[qp[i]])

        #    self._tick_events = self._tick_events.assign(ZEN_TIDE_CROSS = None)
        #    self._tick_events.iloc[idx, self._tick_events.columns.get_loc(AKA.ZEN_TIDE_CROSS)] = ST.CROSS_JX
        #    self._tick_events.iloc[qidx, self._tick_events.columns.get_loc(AKA.ZEN_TIDE_CROSS)] = ST.CROSS_SX
        #    self._ind = self._ind.assign(ZEN_TIDE_CROSS_JX=0)
        #    self._ind.iloc[idx, self._ind.columns.get_loc(AKA.ZEN_TIDE_CROSS_JX)] = 1
        #    ZEN_TIDE_CROSS_JX_Integral = Timeline_Integral_with_cross_before(self._ind[AKA.ZEN_TIDE_CROSS_JX])
        #    self._ind[AKA.ZEN_TIDE_CROSS_JX] = ZEN_TIDE_CROSS_JX_Integral
        #    self._ind = self._ind.assign(ZEN_TIDE_CROSS_SX=0)
        #    self._ind.iloc[qidx, self._ind.columns.get_loc(AKA.ZEN_TIDE_CROSS_SX)] = 1
        #    ZEN_TIDE_CROSS_SX_Integral = Timeline_Integral_with_cross_before(self._ind[AKA.ZEN_TIDE_CROSS_SX])
        #    self._ind[AKA.ZEN_TIDE_CROSS_SX] = ZEN_TIDE_CROSS_SX_Integral



def ATR_SuperTrend_func(data):
    """
    ATR 超级趋势策略
    """
    rsi_ma, stop_line, direction = ATR_RSI_Stops(data, 27)
    ATR_SuperTrend_cross = pd.DataFrame(columns=['min_peak', 'max_peak', 'BOLL_CROSS', 'BOLL_CROSS_JX', 'BOLL_CROSS_SX'], index=data.index)

    return ATR_SuperTrend_cross


class QA_Timekline_States():
    '''
    针对不同时间序列的K线数据分析工具类 
    QA_Timeline 对象表示特定时间序列的K线蜡烛图数据分析工具
    '''
    _ind = None
    _code = ''
    _frequency = '1min'
    _period_time = timedelta(hours = 1)
    _xtick_each_hour = 0
    _states = None

    def __init__(self, baseline_kline, code, frequency,):
        self._ind = pd.DataFrame(columns=['MA5', 'MA10', 'MA30', 'DIF', 'DEA', 'MACD', 'MAX'], index=baseline_kline.index)
        self._states = pd.DataFrame(index=baseline_kline.index)
        pass


def bootstrap_trend_func(data, indices=None):
    """
    K线分型判断：逆浪，斜上坡，慢牛行情 出现MA30 长线机会，打开交易窗口成为买入点
    """
    if (indices is None):
        # Todo: Cache indices in memory.
        indices = pd.concat([ma30_cross_func(data), 
                             macd_cross_func(data),
                             boll_cross_func(data), 
                             maxfactor_cross_func(data), 
                             dual_cross_func(data)], 
                            axis=1)
        indices = indices.assign(ts_momemtum=time_series_momemtum(data.close, 5))
        indices = indices.assign(ts_mom_returns=kline_returns_func(indices['ts_momemtum'], 'np'))
        rsi_ma, stop_line, direction = ATR_RSI_Stops(data, 27)
        indices = indices.assign(stop_line=stop_line)
        indices = indices.assign(atr_direction=direction)
        tsl, atr_super_trend = ATR_SuperTrend(data)
        indices = indices.assign(atr_boll_trend=atr_super_trend)
    states = lower_settle_price_func(data, indices)

    bootstrap_trend_state = pd.DataFrame(((states['lower_settle_price'] == True) | (states['lower_settle_price'] == 1)) & (\
        ((indices['MACD_CROSS_SX'] < indices['DEA_CROSS_SX']) & (indices['MACD_CROSS_SX'] > 4)) | \
        (False & (indices['MA5'] > indices['BOLL_MA']) & (indices['atr_direction'] > 0)) | \
        (False & (indices['MA5'] > indices['BOLL_MA']) & (indices['atr_boll_trend'] > 0)) | \
        ((indices['MA5'] > indices['BOLL_MA']) & (indices['BOLL_CROSS_JX'] < indices['BOLL_CROSS_SX']) & (indices['atr_direction'] < 0)) | \
        ((indices['MACD_CROSS_SX'] > 36) & ((indices['MACD'] < 0) | (indices['atr_direction'] > 0)))) & \
        ((indices['BOLL_CROSS_SX'] > indices['MACD_CROSS_JX']) | ((indices['MACD'] > 0) & (indices['BOLL_CROSS_SX'] < indices['DUAL_CROSS_JX']))),
        columns=['bootstrap'], index=data.index)
    bootstrap_trend_state = pd.concat([bootstrap_trend_state, 
                                       states], 
                            axis=1)
    return bootstrap_trend_state


def lower_settle_price_func(data, indices=None):
    """
    K线分型判断：确定到达低价位的合适买入点。
    （金科玉律：非长（半年以上）牛行情时只有低价位股才值得买入）
    """
    if (indices is None):
        # Todo: Cache indices in memory.
        indices = pd.concat([ma30_cross_func(data), 
                             macd_cross_func(data), 
                             boll_cross_func(data), 
                             maxfactor_cross_func(data), 
                             dual_cross_func(data)], 
                            axis=1)
        indices = indices.assign(ts_momemtum=time_series_momemtum(data.close, 5))
        indices = indices.assign(ts_mom_returns=kline_returns_func(indices['ts_momemtum'], 'np'))

    lower_settle_price_state = pd.DataFrame(((indices['ts_momemtum'].rolling(4).mean().values > 0) | (indices['ts_mom_returns'].rolling(4).mean().values > 0)) & (indices['DEA'] < 0) & \
        (indices['MAXFACTOR_DELTA'].rolling(4).mean().values > 0) & \
        (indices['MACD_DELTA'].rolling(4).mean().values > 0) & (\
            (indices['MAXFACTOR_CROSS_JX'] < indices['MAXFACTOR_CROSS_SX']) | \
            ((indices['MACD'] > 0) & (indices['DUAL_CROSS_JX'] > 0) & ~(indices['DEA'] > indices['MACD']))),
        columns=['lower_settle_price'], index=data.index)

    return lower_settle_price_state