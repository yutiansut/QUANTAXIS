import QUANTAXIS as QA
from numpy import *
import pandas as pd
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *
import mpl_finance as mpf
import matplotlib.dates as mdates

def smooth_demo():
    #data2 = QA.QA_fetch_crypto_asset_day_adv(['huobi'],
    #    symbol=['btcusdt'],
    #    start='2017-10-01',
    #    end='2020-06-30 23:59:59')
    data2 = QA.QA_fetch_index_day_adv('000905', '2015-01-01','2020-03-30')

    adxm, adxm_pos = TA_ADXm(data2.data)

    out = TA_HMA(data2.close.values, 10)
    plt.figure(figsize = (22,9))
    plt.rcParams['font.sans-serif'] = ['simhei']
    ax1 = plt.subplot(111)
    mpf.candlestick2_ochl(ax1, data2.data.open.values, data2.data.close.values, data2.data.high.values, data2.data.low.values, width=0.6, colorup='r', colordown='green', alpha=0.2)
    plt.plot(np.where((adxm_pos == -1), out, np.nan), color='lime', linewidth=1.5)
    plt.plot(np.where((adxm_pos == 1), out, np.nan), color='r', linewidth=1.5)
    plt.plot(np.where((adxm_pos == 0), out, np.nan), color='k', linewidth=1.5)
    l = [data2.code.values, 'ADXm(10)']

    ax1.legend(l)
    #plt.plot(out, cmap=macol, linewidth= 3)
    plt.title("Moving Average ADX line")
    plt.show()

if __name__ == '__main__':
    smooth_demo()
