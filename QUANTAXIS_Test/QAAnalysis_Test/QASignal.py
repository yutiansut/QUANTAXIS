import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QAhuobi import FIRST_PRIORITY
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *

if __name__ == '__main__':
    codelist = ['BCHUSDT', 'BSVUSDT', 'BTCUSDT', 'EOSUSDT', 'ETHUSDT', 'ETCUSDT', 'DASHUSDT', 'LTCUSDT', 'XMRUSDT', 'XRPUSDT', 'ZECUSDT']
    data_1h = QA.QA_fetch_crypto_asset_min_adv(['binance','huobi'],
            symbol=codelist + FIRST_PRIORITY,
            start='2018-01-01',
            end='2020-06-30 23:59:59',
            frequence='60min')
    #data_4h = QA.QA_DataStruct_Crypto_Asset_min(data_1h.resample('4h'))
    #massive_predict_1h = data_day.add_func(price_predict_with_macd_trend_func)

    from QUANTAXIS.QAAnalysis.QAAnalysis_signal import *

    def ADXm(price, p=14, Level=25):
        """
        和传统的ADX指标不同，ADX本身是使用绝对单位绘制的并阻止了趋势方向的侦测，而本指标清晰地显示了ADX的正向和反向半波(在图表上使用彩色显示)，而 DI+/- 信号显示了它们的差距 (灰色)。
        使用这个指标的方法与传统指标一样，
        另外，它还显示了水平(虚线), 在虚线水平之上时就认为市场在有趋势的状态。这个水平通常设在百分之20-25的水平，依赖于它所应用的时段。

        在设置中:
        p - ADX 周期数.
        Level - 重要水平. 
        """
        Bars = len(price)
        IndicatorCounted()
        Open = price.open.values
        High = price.high.values
        Low = price.low.values
        Close = price.close.values
        Time = price.index.get_level_values(Level=0)
        return False

    data_day = QA.QA_fetch_crypto_asset_day_adv(['huobi'],
        symbol=['btcusdt'],
        start='2018-01-01',
        end='2020-06-30 23:59:59')

    price_predict_day = data_day.add_func(price_predict_with_macd_trend_func)
    ma30_croos_day = data_day.add_func(ma30_cross_func).reset_index([1,2])
    dual_cross_day = data_day.add_func(dual_cross_func).reset_index([1,2])
    boll_bands_day = data_day.add_func(boll_cross_func).reset_index([1,2])
    tmom_day = time_series_momemtum(data_day.data.close, 10).reset_index([1,2])

    tmom_negative = ((tmom_day['close'] < 0) & (price_predict_day['DEA'] < 0)) | \
        ((tmom_day['close'] < 0) & (price_predict_day['DELTA'] < 0)) | \
        ((tmom_day['close'] < 0) & (price_predict_day['MACD_CROSS_SX'] < price_predict_day['MACD_CROSS_JX']))

    tmom_negative = tmom_negative[tmom_negative.apply(lambda x: x == True)]  # eqv.  Trim(x == False)
    x_tp_min = price_predict_day[price_predict_day.apply(lambda x: x['PRICE_PRED_CROSS'] > 0, axis = 1)]['PRICE_PRED_CROSS'].values  # eqv.  Trim(x < 0)
    x_tp_max = price_predict_day[price_predict_day.apply(lambda x: x['PRICE_PRED_CROSS'] < 0, axis = 1)]['PRICE_PRED_CROSS'].values * -1  # eqv.  Trim(x > 0)

    bootstrap_exodus = (tmom_negative & (boll_bands_day['BOLL_CROSS_JX'] > 2) & (price_predict_day['PRICE_PRED_CROSS_JX'] < price_predict_day['PRICE_PRED_CROSS_SX'])) & \
        (price_predict_day['MACD_CROSS_JX'] < price_predict_day['MACD_CROSS_SX']) & (price_predict_day['DELTA'] > 0) & \
        ~((boll_bands_day['BBW_MA20'] > boll_bands_day['BOLL_WIDTH']) & (price_predict_day['MACD'] > 0))
    bootstrap_exodus = bootstrap_exodus[bootstrap_exodus.apply(lambda x: x == True)]  # eqv.  Trim(x == False)

    bootstrap_exodus2 = ((dual_cross_day['DUAL_CROSS_JX'] > 0) & (boll_bands_day['BOLL_CROSS_JX'] > 18) & (ma30_croos_day['MA30_CROSS_JX'] < ma30_croos_day['MA30_CROSS_SX'])) & \
        ((price_predict_day['PRICE_PRED_CROSS_JX'] < price_predict_day['PRICE_PRED_CROSS_SX'])) & \
        ~((boll_bands_day['BBW_MA20'] > boll_bands_day['BOLL_WIDTH']) & (price_predict_day['MACD'] > 0))
    bootstrap_exodus2 = bootstrap_exodus2[bootstrap_exodus2.apply(lambda x: x == True)]  # eqv.  Trim(x == False)

    bootstrap_exodus3 = ((dual_cross_day['DUAL_CROSS_JX'] > 0) & (boll_bands_day['BOLL_CROSS_JX'] > 2) & (price_predict_day['MACD_CROSS_JX'] < price_predict_day['MACD_CROSS_SX'])) & \
        ((price_predict_day['PRICE_PRED_CROSS_JX'] < price_predict_day['PRICE_PRED_CROSS_SX'])) & \
        (((boll_bands_day['BOLL_CROSS_JX'] > 8) & (ma30_croos_day['MA30_CROSS_JX'] < ma30_croos_day['MA30_CROSS_SX'])) | (boll_bands_day['BOLL_CROSS_JX'] < 6)) & \
        ~((boll_bands_day['BBW_MA20'] > boll_bands_day['BOLL_WIDTH']) & (price_predict_day['MACD'] > 0))
    bootstrap_exodus3 = bootstrap_exodus3[bootstrap_exodus3.apply(lambda x: x == True)]  # eqv.  Trim(x == False)

    plt.figure(figsize = (22,9))
    plt.plot(data_day.index.get_level_values(level=0), data_day.close, 'c', linewidth=0.6, alpha=0.75)
    plt.plot(data_day.index.get_level_values(level=0), boll_bands_day['BOLL_UB'], linewidth = 0.6, alpha = 0.75)
    plt.plot(data_day.index.get_level_values(level=0), boll_bands_day['BOLL_LB'], linewidth=0.6, alpha=0.75)
    plt.plot(data_day.index.get_level_values(level=0), boll_bands_day['BOLL_MA'], linewidth = 0.6, alpha = 0.75)
    plt.plot(tmom_negative.index, data_day.data.loc[tmom_negative.index].close, 'bx')
    plt.plot(bootstrap_exodus.index, data_day.data.close.loc[bootstrap_exodus.index], 'co')
    plt.plot(bootstrap_exodus2.index, data_day.data.close.loc[bootstrap_exodus2.index], 'yo')
    plt.plot(bootstrap_exodus3.index, data_day.data.close.loc[bootstrap_exodus3.index], 'go')
    plt.plot(data_day.close.iloc[x_tp_max].index.get_level_values(level=0), data_day.close.iloc[x_tp_max], 'gx')
    plt.plot(data_day.close.iloc[x_tp_min].index.get_level_values(level=0), data_day.close.iloc[x_tp_min], 'ro')
    plt.show()
