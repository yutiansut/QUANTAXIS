import QUANTAXIS as QA
from numpy import *
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *
import mpl_finance as mpf
import matplotlib.dates as mdates

def smooth_demo():
    data2 = QA.QA_fetch_crypto_asset_day_adv(['huobi'],
        symbol=['btcusdt'],
        start='2017-10-01',
        end='2020-06-30 23:59:59')

    xn = data2.close.values
    ma5 = talib.MA(data2.close.values, 10)
    hma5 = TA_HMA(data2.close.values, 10)
    kama5 = TA_KAMA(data2.close.values, 10)

    window_size, poly_order = 5, 1
    yy_sg = savgol_filter(xn, window_size, poly_order)

    plt.figure(figsize = (22,9))
    ax1 = plt.subplot(111)
    mpf.candlestick2_ochl(ax1, data2.data.open.values, data2.data.close.values, data2.data.high.values, data2.data.low.values, width=0.6, colorup='r', colordown='green', alpha=0.5)

    #ax1.title("The smoothing windows")
    #plt.plot(xn, lw=1, alpha=0.8)
    ax1.plot(hma5, lw=2, linestyle="--", color='darkcyan', alpha=0.6)
    ax1.plot(yy_sg, lw=1, color='darkcyan', alpha=0.8)
    ax1.plot(ma5, lw=1, color='orange', alpha=0.8)
    ax1.plot(kama5, lw=1, color='lightskyblue', alpha=0.8)
    l=['Hull Moving Average', 'savgol_filter', 'talib.MA10', 'KAMA10']

    ax1.legend(l)
    plt.title("Smoothing a MA10 line")
    plt.show()

if __name__=='__main__':
    smooth_demo()
