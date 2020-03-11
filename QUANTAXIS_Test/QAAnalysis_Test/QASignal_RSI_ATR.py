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

def ATR_Stops_demo():
    data_day = QA.QA_fetch_index_day_adv('000905', '2019-01-01','2020-06-30')
    #QA.QA_fetch_crypto_asset_day_adv(['huobi'],
    #    symbol=['btcusdt'],
    #    start='2017-10-01',
    #    end='2020-06-30 23:59:59')

    xn = data_day.close.values
    rsi_ma, stop_line, direction = ATR_RSI_Stops(data_day.data.reset_index([1]), 27)

    plt.figure(figsize = (22,9))
    ax1 = plt.subplot(111)
    mpf.candlestick2_ochl(ax1, data_day.data.open.values, data_day.data.close.values, data_day.data.high.values, data_day.data.low.values, width=0.6, colorup='r', colordown='green', alpha=0.5)
    position = pd.Series(direction, index=data_day.data.index.get_level_values(level=0))
    DATETIME_LABEL=data_day.data.index.get_level_values(level=0).to_series().apply(lambda x: x.strftime("%Y-%m-%d")[2:13])

    ax1.set_xticks(range(0, len(DATETIME_LABEL), round(len(DATETIME_LABEL)/12)))
    ax1.set_xticklabels(DATETIME_LABEL[::round(len(DATETIME_LABEL)/12)])

    #ax1.title("The smoothing windows")
    #plt.plot(xn, lw=1, alpha=0.8)
    ax1.plot(DATETIME_LABEL, np.where((direction > 0), stop_line.values, np.nan), lw=2, color='lime', alpha=0.6)
    ax1.plot(DATETIME_LABEL, np.where((direction < 0), stop_line.values, np.nan), lw=2, color='red', alpha=0.6)
    #ax1.plot(data_day.index.get_level_values(level=0), np.where((price_predict['POSITION_JUNTION'].values < 0), hma5, np.nan), lw=2, color='red', alpha=0.6)
    #ax1.plot(data_day.index.get_level_values(level=0), np.where((price_predict['POSITION_JUNTION'].values == 0), hma5, np.nan), lw=2, color='black', alpha=0.6)
    ax1.plot(DATETIME_LABEL, rsi_ma.values, lw=1, color='darkcyan', alpha=0.2)
    #ax1.plot(stop_line.values, lw=1, color='orange', alpha=0.2)
    #ax1.plot(data_day.index.get_level_values(level=0), vhma, lw=1.5,
    #color='lightskyblue', alpha=0.8)
    l = ['Rsi Stops bearish', 'Rsi Stops bullish', 'RSI_MA']
    #ax1.plot(data_day.close.iloc[vhma_tp_min].index.get_level_values(level=0), hma5[vhma_tp_min], 'ro')
    #ax1.plot(data_day.close.iloc[vhma_tp_max].index.get_level_values(level=0), hma5[vhma_tp_max], 'gx')

    ax1.legend(l)
    plt.title("RSI_MA with ATR Trend direction")
    plt.show()

if __name__ == '__main__':
    ATR_Stops_demo()
