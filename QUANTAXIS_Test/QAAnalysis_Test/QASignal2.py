import QUANTAXIS as QA
from numpy import *
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *

def smooth_demo():
    data2 = QA.QA_fetch_crypto_asset_day_adv(['huobi'],
        symbol=['btcusdt'],
        start='2018-01-01',
        end='2020-06-30 23:59:59')

    xn = data2.close.values

    window_size, poly_order = 5, 1
    yy_sg = savgol_filter(xn, window_size, poly_order)

    plt.figure(figsize = (22,9))
    plt.title("The smoothing windows")
    plt.subplot(111)
    plt.plot(xn)
    plt.plot(yy_sg)
    l=['original signal', 'savgol_filter']

    plt.legend(l)
    plt.title("Smoothing a noisy signal")
    plt.show()


if __name__=='__main__':
    smooth_demo()
