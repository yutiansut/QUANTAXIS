import QUANTAXIS as QA
import numpy as np
import pandas as pd
import talib
from statsmodels import regression
import statsmodels.api as sm
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
from QUANTAXIS.QAIndicator.talib_numpy import *
from QUANTAXIS.QAAnalysis.QAAnalysis_signal import *

from scipy.optimize import leastsq
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter, savgol_filter

import mpl_finance as mpf
import matplotlib.dates as mdates

#def Fun(p,x): # 定义拟合函数形式
#    a1,a2,a3 = p
#    return a1 * x ** 2 + a2 * x + a3

#def error(p,x,y): # 拟合残差
#    return Fun(p,x) - y

#def main():
#    codelist = ['000905']
#    code = codelist[0]
#    #data_day = QA.QA_fetch_stock_day_adv(codelist, '2015-01-01','2020-03-30')
#    benchmark = QA.QA_fetch_stock_day_adv(codelist, '2015-01-01',
#    '2020-03-30')
#    benchmark = benchmark.data.loc[(slice(None), code),
#    :].reset_index([1]).close

#    p0 = [0.1,-0.01,100] # 拟合的初始参数设置
#    para = leastsq(error, p0, args=(x,y)) # 进行拟合
#    y_fitted = Fun(para[0],x) # 画出拟合后的曲线
 
#    plt.figure
#    plt.plot(x,y,'r', label = 'Original curve')
#    plt.plot(x,y_fitted,'-b', label ='Fitted curve')
#    plt.legend()
#    plt.show()
#    print(para[0])
 
#if __name__ == '__main__':
#   main()
def linereg(source, length=14, offset=0):
    """
    我试试抄Pine Script
    """
    x = np.arange(0, len(source), 1.0)
    y = source
    x_ = talib.SMA(x,length)
    y_ = talib.SMA(y,length)
    mx = pd.Series(x).rolling(length).std()
    my = pd.Series(y).rolling(length).std()

    #c = pd.DataFrame(np.c_[x,y], columns=['x', 'y']).rolling(length).corr()
    c = talib.SMA(y * x,length) - talib.SMA(y,length) * talib.SMA(x,length) / (pd.Series(length * y).rolling(length).std().values * pd.Series(length * x).rolling(length).std().values)
    slope = c * (my / mx)
    print(slope)
    # linreg = intercept + slope * (length - 1 - offset)
    intercept = y_ - slope * x_
    reg = intercept + slope * x
    return reg

def linereg_trend_func(data):
    """

    """
    lr_kline = pd.DataFrame(np.c_[TA_HMA(data.open.values, 10),
                            TA_HMA(data.high.values, 10),
                            TA_HMA(data.low.values, 10),
                            TA_HMA(data.close.values, 10)], 
                            columns=['open', 'high', 'low', 'close'], 
                            index=data_day.index.get_level_values(level=0))
    bollbands = boll_cross_func(data)
    lr_kline['ochl4'] = (lr_kline['open'] + lr_kline['close'] + lr_kline['high'] + lr_kline['low']) / 4
    lr_kline['ochl4_returns'] = kline_returns_func(lr_kline['ochl4'], 'np')
    #adxm, predict_trend_directions = ADX_MA(lr_kline[11:])
    rsi_ma, stop_line, predict_trend_directions = ATR_RSI_Stops(lr_kline[11:])
    #Tsl, predict_trend_directions = ATR_SuperTrend(lr_kline[11:])
    macd = QA.QA_indicator_MACD(data)

    deadpool = ((lr_kline['ochl4_returns'] < 0)) | \
        ((bollbands['BOLL_CROSS_SX'] < bollbands['BOLL_CROSS_JX']) & (np.r_[np.zeros(11),predict_trend_directions] < 0)) | \
        ((bollbands['BOLL_CROSS_JX'] > 6) & (macd['MACD'] < 0) & (macd['DIF'] < 0) & (lr_kline['ochl4_returns'].rolling(8).sum() < 0.0)) | \
        ((bollbands['BOLL_CROSS_SX'] < 6) & (lr_kline['ochl4_returns'].rolling(6).sum() < 0.0) & (bollbands['BBW_MA20'] > bollbands['BOLL_WIDTH']))
    bootstrap = ((lr_kline['ochl4_returns'] > 0) & (deadpool == False))
    strategy_position = pd.DataFrame(columns=['position'], index=data.index)

    return strategy_position


if __name__ == '__main__':
    codelist = ['600188']
    code = codelist[0]
    data_day = QA.QA_fetch_stock_day_adv(codelist, 
                                         '2015-01-01','2020-03-30')
    #data_day = QA.QA_fetch_stock_min_adv(codelist,
    #                                      '2019-01-01','2020-03-30',
    #                                      frequence='60min')
    #lr = linereg(data_day.data.loc[(slice(None), code),
    #:].reset_index([1]).close.values)
    window_size, poly_order = 5, 1
    #lr_open = savgol_filter(data_day.data.loc[(slice(None), code),
    #:].reset_index([1]).open.values, window_size, poly_order)
    #lr_high = savgol_filter(data_day.data.loc[(slice(None), code),
    #:].reset_index([1]).high.values, window_size, poly_order)
    #lr_low = savgol_filter(data_day.data.loc[(slice(None), code),
    #:].reset_index([1]).low.values, window_size, poly_order)
    #lr_close = savgol_filter(data_day.data.loc[(slice(None), code),
    #:].reset_index([1]).close.values, window_size, poly_order)
    lr_kline = pd.DataFrame(np.c_[TA_HMA(data_day.data.loc[(slice(None), code), :].reset_index([1]).open.values, 10),
                             TA_HMA(data_day.data.loc[(slice(None), code), :].reset_index([1]).high.values, 10),
                             TA_HMA(data_day.data.loc[(slice(None), code), :].reset_index([1]).low.values, 10),
                             TA_HMA(data_day.data.loc[(slice(None), code), :].reset_index([1]).close.values, 10)], columns=['open', 'high', 'low', 'close'], index=data_day.index.get_level_values(level=0))
    bollbands = data_day.add_func(boll_cross_func)
    ma30_cross = data_day.add_func(ma30_cross_func)
    dual_cross = data_day.add_func(dual_cross_func)
    settle_state = data_day.add_func(bootstrap_trend_func)
    #settle_state = data_day.add_func(lower_settle_price_func)
    #bootstrap_trend = data_day.add_func(bootstrap_trend_func)

    lr_kline['ochl4'] = (lr_kline['open'] + lr_kline['close'] + lr_kline['high'] + lr_kline['low']) / 4
    lr_kline['ochl4_returns'] = kline_returns_func(lr_kline['ochl4'], 'np')
    bollbands['boll_returns'] = kline_returns_func(bollbands['BOLL_UB'], 'np')
    #adxm, predict_trend_directions = ADX_MA(lr_kline[11:])
    rsi_ma, stop_line, predict_trend_directions = ATR_RSI_Stops(lr_kline[11:])
    #Tsl, predict_trend_directions = ATR_SuperTrend(lr_kline[11:])
    macd = data_day.add_func(macd_cross_func)

    deadpool = ((lr_kline['ochl4_returns'] < 0)) | \
        ((macd['DEA'] < 0) & (settle_state['lower_settle_price'].values == False))
        ##((macd['DEA'] > 0) & (np.r_[np.zeros(11),predict_trend_directions] <
        ##0) & (macd['MACD'] < 0) & (macd['MACD_CROSS_SX'] > 8)) | \
        ##((bollbands['boll_returns'] < 0) & (bollbands['BOLL_CROSS_JX'] > 8) &
        ##(bollbands['BOLL_CROSS_SX'] > 1) & ~((bollbands['BOLL_CROSS_JX'] -
        ##dualcross['DUAL_CROSS_JX']) < 6)) | \
        ##((bollbands['boll_returns'] < 0) & (bollbands['BOLL_CROSS_SX'] <
        ##bollbands['BOLL_CROSS_JX']) & (macd['MACD'] < 0) & (macd['DEA'] > 0))
        ##| \
        ##((bollbands['BOLL_CROSS_SX'] < bollbands['BOLL_CROSS_JX']) &
        ##(macd['DELTA'] < 0) & (macd['DEA'] > 0)) | \
        ##((bollbands['BOLL_CROSS_SX'] > macd['MACD_CROSS_SX']) & (macd['MACD']
        ##< 0) & (macd['MACD_CROSS_SX'] > 10) &
        ##(np.r_[np.zeros(11),predict_trend_directions] < 0)) | \
        ##((bollbands['BOLL_CROSS_SX'] < bollbands['BOLL_CROSS_JX']) &
        ##(np.r_[np.zeros(11),predict_trend_directions] < 0)) | \
        #((bollbands['BOLL_CROSS_JX'] > 6) & (macd['MACD'] < 0) & (macd['DIF']
        #< 0) & (lr_kline['ochl4_returns'].rolling(8).sum() < 0.0)) | \
        #((bollbands['BOLL_CROSS_SX'] < 6) &
        #(lr_kline['ochl4_returns'].rolling(6).sum() < 0.0) &
        #(bollbands['BBW_MA20'] > bollbands['BOLL_WIDTH']))
    bootstrap = ((lr_kline['ochl4_returns'] > 0) & (deadpool == False)) | \
        ((macd['MACD'] > 0) & (np.r_[np.zeros(11),predict_trend_directions] > 0) & (deadpool == False))

    fig = plt.figure(figsize = (22,9))
    ax1 = plt.subplot2grid((4,3),(0,0), rowspan=3, colspan=3)
    ax2 = plt.subplot2grid((4,3),(3,0), rowspan=1, colspan=3, sharex=ax1)
    #mpf.candlestick2_ochl(ax1,
    #                      lr_kline['open'][11:],
    #                      lr_kline['close'][11:],
    #                      lr_kline['high'][11:],
    #                      lr_kline['low'][11:],
    #                      width=0.6, colorup='r', colordown='green',
    #                      alpha=0.75)
    mpf.candlestick2_ochl(ax1,
                          data_day.data.open[11:],
                          data_day.data.close[11:],
                          data_day.data.high[11:],
                          data_day.data.low[11:],
                          width=0.6, colorup='r', colordown='green',
                          alpha=0.3)
    DATETIME_LABEL = data_day.index.get_level_values(level=0).to_series().apply(lambda x: x.strftime("%Y-%m-%d %H:%M")[2:16])[11:]
    ax1.plot(DATETIME_LABEL, bollbands['BOLL_UB'][11:] , lw=0.75, color='cyan', alpha=0.6)
    ax1.plot(DATETIME_LABEL, bollbands['BOLL_LB'][11:] , lw=0.75, color='fuchsia', alpha=0.6)
    ax1.plot(DATETIME_LABEL, ma30_cross['MA30'][11:] , lw=0.75, color='purple', alpha=0.6)

    ax1.plot(DATETIME_LABEL, 
             np.where(((lr_kline['ochl4_returns'] > 0) & (deadpool == False))[11:],
                      lr_kline['ochl4'][11:], np.nan), lw=2, color='lime', alpha=0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where((deadpool[11:] == True),
                      lr_kline['ochl4'][11:], np.nan), lw=2, color='red', alpha=0.8)

    ax1.plot(DATETIME_LABEL, 
             np.where((predict_trend_directions > 0), 
                      stop_line.values, np.nan), lw=1, color='lime', alpha=0.2)
    ax1.plot(DATETIME_LABEL, 
             np.where((predict_trend_directions < 0), 
                      stop_line.values, np.nan), lw=1, color='red', alpha=0.2)

    ax1.set_xticks(range(0, len(DATETIME_LABEL), round(len(data_day) / 16)))
    ax1.set_xticklabels(DATETIME_LABEL[::round(len(data_day) / 16)])
    ax1.grid(True)

    ax2.plot(DATETIME_LABEL, macd['DIF'][11:], color='green', lw=1, label='DIF')
    ax2.plot(DATETIME_LABEL, macd['DEA'][11:], color='purple', lw=1, label='DEA')

    ax1.plot(DATETIME_LABEL, 
             np.where(((settle_state['bootstrap'].values == True) & (lr_kline['ochl4_returns'] > 0))[11:], 
                      lr_kline['ochl4'][11:], np.nan), 'g^', alpha=0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where(((settle_state['bootstrap'].values == True) & (lr_kline['ochl4_returns'] < 0))[11:], 
                      lr_kline['ochl4'][11:], np.nan), 'r^', alpha=0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where(((settle_state['bootstrap'].values == False) & (bollbands['BOLL_CROSS_SX'] < macd['MACD_CROSS_SX']) & (settle_state['lower_settle_price'].values == True))[11:], 
                      lr_kline['ochl4'][11:], np.nan), 'bo', alpha=0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where(((settle_state['bootstrap'].values == False) & (ma30_cross['MA30_CROSS_SX'] < 10) & (settle_state['lower_settle_price'].values == True))[11:], 
                      lr_kline['ochl4'][11:], np.nan), 'c*', alpha=0.6)
    ax1.plot(DATETIME_LABEL, 
             np.where(((settle_state['bootstrap'].values == False) & (bollbands['BOLL_CROSS_SX'] > macd['MACD_CROSS_SX']) & (ma30_cross['MA30_CROSS_SX'] >= 10) & (settle_state['lower_settle_price'].values == True))[11:], 
                      lr_kline['ochl4'][11:], np.nan), 'ko', alpha=0.6)

##    ax2.plot(DATETIME_LABEL, output_ind.iloc[tp_dea].DEA, 'g--', label='DEA
##    simplified trajectory')
##    ax2.plot(DATETIME_LABEL, output_ind.iloc[tp_dea].DEA, 'ro', markersize =
##    7, label=u'DEA turning point')

    barlist = ax2.bar(DATETIME_LABEL, macd['MACD'][11:], width=0.6, label='MACD')
    for i in range(len(DATETIME_LABEL.index)):
        if macd['MACD'][i + 11] <= 0:
            barlist[i].set_color('g')
        else:
            barlist[i].set_color('r')
    ax2.set(ylabel='MACD(26,12,9)')

    ax2.set_xticks(range(0, len(DATETIME_LABEL), round(len(data_day) / 16)))
    ax2.set_xticklabels(DATETIME_LABEL[::round(len(data_day) / 16)])
    ax2.grid(True)

#    l = ['LR']
#    ax1.legend(l)
    fig.align_xlabels()
    plt.show()