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

def ATR_SuperTrend_demo():
    data_day = QA.QA_fetch_index_day_adv('000905', '2019-01-01','2020-06-30')
    #data_day = QA.QA_fetch_crypto_asset_day_adv(['huobi'],
    #    symbol=['btcusdt'],
    #    start='2017-10-01',
    #    end='2020-06-30 23:59:59')
    klines =  data_day.data
    bb = TA_BBANDS(data_day.data.close, 20)
    tsl, Trend = ATR_SuperTrend_cross(data_day.data)

    #################### Plot ####################
    plt.figure(figsize = (22,9))
    ax1 = plt.subplot(111)
    mpf.candlestick2_ochl(ax1, data_day.data.open.values, data_day.data.close.values, data_day.data.high.values, data_day.data.low.values, width=0.6, colorup='r', colordown='green', alpha=0.5)
    position = pd.Series(Trend, index=data_day.data.index.get_level_values(level=0))
    DATETIME_LABEL=klines.index.get_level_values(level=0).to_series().apply(lambda x: x.strftime("%Y-%m-%d")[2:13])

    ax1.set_xticks(range(0, len(DATETIME_LABEL), round(len(klines)/12)))
    ax1.set_xticklabels(DATETIME_LABEL[::round(len(klines)/12)])
    ax1.plot(DATETIME_LABEL, np.where(Trend == 1, tsl, np.NaN), lw=2, color='lime', alpha=0.6)
    ax1.plot(DATETIME_LABEL, np.where(Trend != 1, tsl, np.NaN), lw=2, color='red', alpha=0.6)
    ax1.plot(DATETIME_LABEL, np.where(Trend == 1, bb[:,1], np.NaN), lw=1, color='lime', alpha=0.6)
    ax1.plot(DATETIME_LABEL, np.where(Trend != 1, bb[:,1], np.NaN), lw=1, color='red', alpha=0.6)
    p1u = ax1.plot(DATETIME_LABEL, np.where(Trend == 1, bb[:,0], np.NaN), lw=0.75, color='darkblue', alpha=0.35)
    p1d = ax1.plot(DATETIME_LABEL, np.where(Trend != 1, bb[:,0], np.NaN), lw=0.75, color='red', alpha=0.35)
    p2u = ax1.plot(DATETIME_LABEL, np.where(Trend == 1, bb[:,2], np.NaN), lw=0.75, color='lime', alpha=0.35)
    p2d = ax1.plot(DATETIME_LABEL, np.where(Trend != 1, bb[:,2], np.NaN), lw=0.75, color='fuchsia', alpha=0.35)
    actions = (position.diff() != 0)
    ax1.plot(DATETIME_LABEL, 
             np.where((actions.values == True) & (position.values > 0), 
                      data_day.data.close.values, np.nan), 
             'g^', alpha = 0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where((actions.values == True) & (position.values < 0), 
                      data_day.data.close.values, np.nan), 
             'rv', alpha=0.8)
    l = ['Bollinger Band Upper', 'Bollinger Band Lower', 'Bollinger MA']
    #ax1.plot(data_day.close.iloc[vhma_tp_min].index.get_level_values(level=0),
    #hma5[vhma_tp_min], 'ro')
    #ax1.plot(data_day.close.iloc[vhma_tp_max].index.get_level_values(level=0),
    #hma5[vhma_tp_max], 'gx')

    ax1.legend(l)
    plt.title("ATR Super Trend")
    plt.show()
    #fill(p1, p2, color=linecolor, transp=95, title="background")


if __name__ == '__main__':
    ATR_SuperTrend_demo()
