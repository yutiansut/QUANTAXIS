import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QAhuobi import FIRST_PRIORITY
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *
import mpl_finance as mpf
import matplotlib.dates as mdates

if __name__ == '__main__':
    from QUANTAXIS.QAAnalysis.QAAnalysis_signal import *

    #data_day = QA.QA_fetch_index_day_adv('000905', '2015-01-01','2020-03-30')
    data_day = QA.QA_fetch_crypto_asset_day_adv(['huobi'],
        symbol=['btcusdt'],
        start='2018-01-01',
        end='2020-06-30 23:59:59')

    #codelist = ['BCHUSDT', 'BSVUSDT', 'BTCUSDT', 'EOSUSDT', 'ETHUSDT',
    #'ETCUSDT', 'DASHUSDT', 'LTCUSDT', 'XMRUSDT', 'XRPUSDT', 'ZECUSDT']
    #data_1h = QA.QA_fetch_crypto_asset_min_adv(['binance','huobi'],
    #        symbol=codelist + FIRST_PRIORITY,
    #        start='2018-01-01',
    #        end='2020-06-30 23:59:59',
    #        frequence='60min')
    #data_4h = QA.QA_DataStruct_Crypto_Asset_min(data_1h.resample('4h'))
    #massive_predict_1h = data_day.add_func(price_predict_with_macd_trend_func)
    rsi_ma, stop_line, direction = TA_ATR_Stops(data_day.data.reset_index([1,2]), 27)
    tsl, atr_super_trend = TA_ATR_SuperTrend(data_day.data.reset_index([1,2]))
    price_predict_day = data_day.add_func(price_predict_with_macd_trend_func)
    ma30_croos_day = data_day.add_func(ma30_cross_func).reset_index([1,2])
    dual_cross_day = data_day.add_func(dual_cross_func).reset_index([1,2])
    boll_bands_day = data_day.add_func(boll_cross_func).reset_index([1,2])
    maxfactor_cross_day = data_day.add_func(maxfactor_cross_func).reset_index([1,2])
    tmom_day = time_series_momemtum(data_day.data.close, 10).reset_index([1,2])

    hma5 = TA_HMA(data_day.close.values, 10)
    hma5_returns = np.nan_to_num(np.log(hma5 / pd.Series(hma5).shift(1)), nan=0)
    hma_tp_min, hma_tp_max = signal.argrelextrema(np.r_[np.zeros(11), hma5[11:]], np.less)[0], signal.argrelextrema(np.r_[np.zeros(11), hma5[11:]], np.greater)[0]
    price_predict = price_predict_with_rolling_integral(data_day.data, hma5, hma_tp_min, hma_tp_max,)

    tmom_negative = ((tmom_day['close'] < 0) & (price_predict_day['DEA'] < 0)) | \
        ((tmom_day['close'] < 0) & (price_predict_day['DELTA'] < 0)) | \
        ((tmom_day['close'] < 0) & (price_predict_day['MACD_CROSS_SX'] < price_predict_day['MACD_CROSS_JX'])) | \
        ((pd.Series(hma5_returns, index=tmom_day.index) < 0) & (pd.Series(hma5, index=tmom_day.index) > boll_bands_day['BOLL_MA']) & (boll_bands_day['BOLL_CROSS_SX'] < boll_bands_day['BOLL_CROSS_JX']))

    strategy_POSITION = pd.DataFrame(columns=['POSITION_JUNTION'], index=data_day.index.get_level_values(level=0))
    strategy_POSITION = strategy_POSITION.assign(POSITION_TMOM_NEGATIVE=tmom_negative.apply(lambda x: -1 if (x == True) else 0))

    bootstrap_exodus = (tmom_negative & (boll_bands_day['BOLL_CROSS_JX'] > 2) & (price_predict_day['PRICE_PRED_CROSS_JX'] < price_predict_day['PRICE_PRED_CROSS_SX'])) & \
        (price_predict_day['MACD_CROSS_JX'] < price_predict_day['MACD_CROSS_SX']) & (price_predict_day['DELTA'] > 0) & \
        ~((boll_bands_day['BBW_MA20'] > boll_bands_day['BOLL_WIDTH']) & (price_predict_day['MACD'] > 0))
    strategy_POSITION = strategy_POSITION.assign(POSITION_BOOTSRTAP_EXODUS=bootstrap_exodus.apply(lambda x: 1 if (x == True) else 0))

    bootstrap_maxfactor = ((hma5_returns > 0) & (maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values)) & (\
            ((maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values > 1) & (boll_bands_day['BOLL_CROSS_JX'].values > maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values) & (boll_bands_day['BOLL_CROSS_JX'].values < boll_bands_day['BOLL_CROSS_SX'].values)) | \
            ((maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values > 1) & (boll_bands_day['BBW_MA20'].values < boll_bands_day['BOLL_WIDTH'].values) & (maxfactor_cross_day['MAXFACTOR'].values > maxfactor_cross_day['REGRESSION_BASELINE'].values)) | \
            ((hma5 > boll_bands_day['BOLL_MA'].values) & (boll_bands_day['BBW_MA20'].values < boll_bands_day['BOLL_WIDTH'].values)) | \
            ((ma30_croos_day['MA30_CROSS_JX'].values < ma30_croos_day['MA30_CROSS_SX'].values)))
    strategy_POSITION = strategy_POSITION.assign(POSITION_BOOTSRTAP_MAXFACTOR=np.where(bootstrap_maxfactor == True, 1, 0))

    bootstrap_dual_cross = ((hma5_returns > 0) & (dual_cross_day['DUAL_CROSS_JX'].values > 0)) & (\
            ((maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values > 2) & (maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values)) | \
            ((hma5 > boll_bands_day['BOLL_MA'].values) & (maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values)) | \
            ((hma5 > boll_bands_day['BOLL_MA'].values) & (boll_bands_day['BBW_MA20'].values < boll_bands_day['BOLL_WIDTH'].values)) | \
            (((boll_bands_day['BOLL_CROSS_JX'].values > 18) & (ma30_croos_day['MA30_CROSS_JX'].values < ma30_croos_day['MA30_CROSS_SX'].values)) & \
            ~((boll_bands_day['BBW_MA20'].values > boll_bands_day['BOLL_WIDTH'].values) & (price_predict_day['MACD'].values > 0))) | \
            ((boll_bands_day['BOLL_CROSS_JX'].values > 2) & (price_predict_day['MACD_CROSS_JX'].values < price_predict_day['MACD_CROSS_SX'].values)) & \
            ((price_predict_day['PRICE_PRED_CROSS_JX'].values < price_predict_day['PRICE_PRED_CROSS_SX'].values)) & \
            (((boll_bands_day['BOLL_CROSS_JX'].values > 8) & (ma30_croos_day['MA30_CROSS_JX'].values < ma30_croos_day['MA30_CROSS_SX'].values)) | (boll_bands_day['BOLL_CROSS_JX'].values < 6)) & \
            ~((boll_bands_day['BBW_MA20'].values > boll_bands_day['BOLL_WIDTH'].values) & (price_predict_day['MACD'].values > 0)))
    dealpool = ((hma5_returns < 0) & (boll_bands_day['BOLL_CROSS_JX'].values > boll_bands_day['BOLL_CROSS_SX'].values)) | \
                ((hma5_returns < 0) & (maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values) & (price_predict_day['DELTA'].values < 0))
    strategy_POSITION = strategy_POSITION.assign(POSITION_BOOTSRTAP_DUAL=np.where(bootstrap_dual_cross == True, 
                                                                                  1, 
                                                                                  np.where(dealpool == True, 
                                                                                           -1, 
                                                                                           np.where((hma5_returns < 0) & (maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values), 
                                                                                                    -1, 0))))

    #adxm, adxm_pos = TA_ADXm(data_day.data)
    strategy_POSITION = strategy_POSITION.assign(POSITION_HMA5=price_predict['POSITION_JUNTION'])
    strategy_POSITION = strategy_POSITION.assign(POSITION_ATR=(direction))
    strategy_POSITION = strategy_POSITION.assign(POSITION_ATR_SUPER=(atr_super_trend))
    strategy_POSITION['POSITION_JUNTION'] = (strategy_POSITION['POSITION_TMOM_NEGATIVE'] + strategy_POSITION['POSITION_BOOTSRTAP_EXODUS'] + strategy_POSITION['POSITION_ATR_SUPER'] + strategy_POSITION['POSITION_ATR']).apply(lambda x:0 if np.isnan(x) else int(x))
    
    # 信号抖动，使用 Rolling 过滤，无指向性的用 ATR 趋势策略填充
    strategy_POSITION = strategy_POSITION.assign(POSITION_BOOTSRTAP_DUAL_R5=
                                                 strategy_POSITION['POSITION_BOOTSRTAP_DUAL'].rolling(4).apply(lambda x: 
                                                                                                               x.sum(), raw=False).apply(lambda x:
                                                                                                                                         0 if np.isnan(x) else int(x)))
    strategy_POSITION['POSITION_BOOTSRTAP_DUAL_R5'] = np.where((hma5_returns > 0) & (strategy_POSITION['POSITION_BOOTSRTAP_DUAL_R5'].values > 0), 
                      1, 
                      np.where((hma5_returns < 0) & (strategy_POSITION['POSITION_BOOTSRTAP_DUAL_R5'].values < 0), 
                               -1, 
                               strategy_POSITION['POSITION_ATR'].values))
    strategy_POSITION['returns'] = np.nan_to_num(np.log(data_day.close / data_day.close.shift(1)), nan=0)
    strategy_POSITION['strategy_R5'] = np.where(strategy_POSITION['POSITION_BOOTSRTAP_DUAL_R5'].shift(1).values > 0, 1, 0) * strategy_POSITION['returns'].shift(1)
    print(strategy_POSITION[['returns', 'POSITION_BOOTSRTAP_DUAL_R5', 'strategy_R5']].tail(60))
    strategy_POSITION[['returns', 'strategy_R5']].dropna().cumsum().apply(np.exp).plot(figsize=(10, 6))


    x_tp_min = price_predict_day[price_predict_day.apply(lambda x: x['PRICE_PRED_CROSS'] > 0, axis = 1)]['PRICE_PRED_CROSS'].values  # eqv.  Trim(x < 0)
    x_tp_max = price_predict_day[price_predict_day.apply(lambda x: x['PRICE_PRED_CROSS'] < 0, axis = 1)]['PRICE_PRED_CROSS'].values * -1  # eqv.  Trim(x > 0)
    plt.figure(figsize = (22,9))
    ax1 = plt.subplot(111)
    mpf.candlestick2_ochl(ax1, data_day.data.open.values, data_day.data.close.values, data_day.data.high.values, data_day.data.low.values, width = 0.6, colorup = 'r', colordown = 'green', alpha = 0.5)
    strategy_POSITION = strategy_POSITION.assign(DATETIME_LABEL=data_day.index.get_level_values(level=0).to_series().apply(lambda x: x.strftime("%Y-%m-%d")[2:16])) 
    ax1.set_xticks(range(0, len(strategy_POSITION['DATETIME_LABEL']), round(len(data_day.data) / 12)))
    ax1.set_xticklabels(strategy_POSITION['DATETIME_LABEL'][::round(len(data_day.data) / 12)])
    plt.plot(strategy_POSITION['DATETIME_LABEL'], data_day.close, 'c', linewidth = 0.6, alpha = 0.75)
    plt.plot(strategy_POSITION['DATETIME_LABEL'], boll_bands_day['BOLL_UB'], linewidth = 0.6, alpha = 0.75)
    plt.plot(strategy_POSITION['DATETIME_LABEL'], boll_bands_day['BOLL_LB'], linewidth = 0.6, alpha = 0.75)
    plt.plot(strategy_POSITION['DATETIME_LABEL'], boll_bands_day['BOLL_MA'], linewidth = 0.6, alpha = 0.75)
    #plt.plot(tmom_negative.index,
    #data_day.data.loc[tmom_negative.index].close, 'bx')
    #plt.plot(bootstrap_exodus.index,
    #data_day.data.close.loc[bootstrap_exodus.index], 'co')
    #plt.plot(bootstrap_exodus2.index,
    #data_day.data.close.loc[bootstrap_exodus2.index], 'yo')
    #plt.plot(bootstrap_exodus3.index,
    #data_day.data.close.loc[bootstrap_exodus3.index], 'go')
    #ax1.plot(data_day.index.get_level_values(level=0), np.where((direction <
    #0), stop_line.values, np.nan), lw=2, color='fuchsia', alpha=0.6)
    ax1.plot(strategy_POSITION['DATETIME_LABEL'],
        np.where((strategy_POSITION['POSITION_JUNTION'].values > 0), 
                 hma5, np.nan), 
        lw = 2, color = 'lime', alpha = 0.6)
    ax1.plot(strategy_POSITION['DATETIME_LABEL'],
        np.where((strategy_POSITION['POSITION_JUNTION'].values < 0), 
                 hma5, np.nan), 
        lw=2, color='red', alpha=0.6)
    ax1.plot(strategy_POSITION['DATETIME_LABEL'],
        np.where((strategy_POSITION['POSITION_JUNTION'].values == 0), 
                hma5, np.nan), 
        lw = 2, color = 'black', alpha = 0.6)
    ax1.plot(strategy_POSITION['DATETIME_LABEL'], 
             np.where((strategy_POSITION['POSITION_BOOTSRTAP_DUAL_R5'].values > 0), 
                      hma5, np.nan), 
             lw=2, color='lime', alpha=0.6)
    ax1.plot(strategy_POSITION['DATETIME_LABEL'], 
             np.where((strategy_POSITION['POSITION_BOOTSRTAP_DUAL_R5'].values > 0), 
                      hma5, np.nan), 
             'g*', alpha = 0.8)
    ax1.plot(strategy_POSITION['DATETIME_LABEL'], 
             np.where((strategy_POSITION['POSITION_BOOTSRTAP_DUAL_R5'].values < 0), 
                      hma5, np.nan), 
             'rx', alpha=0.8)
    plt.plot(strategy_POSITION.iloc[x_tp_max, 
                                    strategy_POSITION.columns.get_loc('DATETIME_LABEL')], 
             data_day.close.iloc[x_tp_max], 
        'gx', alpha = 0.3)
    plt.plot(strategy_POSITION.iloc[x_tp_min, 
                                    strategy_POSITION.columns.get_loc('DATETIME_LABEL')], 
             data_day.close.iloc[x_tp_min], 
        'ro', alpha=0.3)
    plt.show()
