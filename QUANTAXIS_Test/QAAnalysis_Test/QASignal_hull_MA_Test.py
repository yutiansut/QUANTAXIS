import QUANTAXIS as QA
from numpy import *
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *
import mpl_finance as mpf
import matplotlib.dates as mdates
import scipy.signal as signal
from QUANTAXIS.QAAnalysis.QAAnalysis_signal import *

def smooth_demo():
    data_day = QA.QA_fetch_crypto_asset_day_adv(['huobi'],
        symbol=['btcusdt'],
        start='2017-10-01',
        end='2020-06-30 23:59:59')

    ma5 = talib.MA(data_day.close.values, 10)
    hma5 = TA_HMA(data_day.close.values, 10)
    hma_tp_min, hma_tp_max = signal.argrelextrema(np.r_[np.zeros(11), hma5[11:]], np.less)[0], signal.argrelextrema(np.r_[np.zeros(11), hma5[11:]], np.greater)[0]
    price_predict = price_predict_with_rolling_integral(data_day.data, hma5, hma_tp_min, hma_tp_max,)

    kama5 = TA_KAMA(data_day.close.values, 10)
    vhma = VHMA(data_day.data)
    
    vhma_tp_min, vhma_tp_max = find_peak_vextors_eagerly(np.r_[np.zeros(7), vhma[7:]], smooth_ma5=np.r_[np.zeros(7), vhma[7:]])

    window_size, poly_order = 5, 1
    #yy_sg = savgol_filter(xn, window_size, poly_order)

    plt.figure(figsize = (22,9))
    ax1 = plt.subplot(111)
    #mpf.candlestick2_ochl(ax1, data2.data.open.values,
    #data2.data.close.values, data2.data.high.values, data2.data.low.values,
    #width=0.6, colorup='r', colordown='green', alpha=0.5)

    #ax1.title("The smoothing windows")
    #plt.plot(xn, lw=1, alpha=0.8)
    ax1.plot(data_day.index.get_level_values(level=0), np.where((price_predict['POSITION_JUNTION'].values > 0), hma5, np.nan), lw=2, color='lime', alpha=0.6)
    ax1.plot(data_day.index.get_level_values(level=0), np.where((price_predict['POSITION_JUNTION'].values < 0), hma5, np.nan), lw=2, color='red', alpha=0.6)
    ax1.plot(data_day.index.get_level_values(level=0), np.where((price_predict['POSITION_JUNTION'].values == 0), hma5, np.nan), lw=2, color='black', alpha=0.6)
    #ax1.plot(yy_sg, lw=1, color='darkcyan', alpha=0.2)
    #ax1.plot(data_day.index.get_level_values(level=0), ma5, lw=1,
    #color='orange', alpha=0.2)
    #ax1.plot(data_day.index.get_level_values(level=0), vhma, lw=1.5,
    #color='lightskyblue', alpha=0.8)
    l = ['Hull Moving Average', 'talib.MA10', 'vhma']
    ax1.plot(data_day.close.iloc[vhma_tp_min].index.get_level_values(level=0), hma5[vhma_tp_min], 'ro')
    ax1.plot(data_day.close.iloc[vhma_tp_max].index.get_level_values(level=0), hma5[vhma_tp_max], 'gx')

    ax1.legend(l)
    plt.title("Smoothing a MA10 line")
    plt.show()

if __name__ == '__main__':
    smooth_demo()
