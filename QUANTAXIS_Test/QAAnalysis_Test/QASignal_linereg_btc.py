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

from QUANTAXIS.QAUtil.QADate_Adv import (
    QA_util_timestamp_to_str,
    QA_util_datetime_to_Unix_timestamp,
    QA_util_print_timestamp
)

def scale_patterns_cross_func(data, indices=None):
    """

    """
    if (indices is None):
        # Todo: Cache indices in memory.
        indices = pd.concat([ma30_cross_func(data), 
                             macd_cross_func(data),
                             boll_cross_func(data), 
                             maxfactor_cross_func(data), 
                             dual_cross_func(data), 
                             ma_power_func(data.close),
                             ATR_SuperTrend_func(data),
                             machine_learning_trend_func(data)],
                            axis=1)
        indices = indices.assign(ts_momemtum=time_series_momemtum(data.close, 5))
        indices = indices.assign(ts_mom_returns=kline_returns_func(indices['ts_momemtum'], 'np'))
        rsi_ma, stop_line, direction = ATR_RSI_Stops(data, 27)
        indices = indices.assign(stop_line=stop_line)
        indices = indices.assign(atr_direction=direction)
        indices['boll_returns'] = kline_returns_func(indices['BOLL_UB'], 'np')
        states = bootstrap_trend_func(data, indices)
        indices['lower_settle_price'] = states['lower_settle_price']
        indices['LOWER_PRICE_SETTLE_BEFORE'] = states['LOWER_PRICE_SETTLE_BEFORE']
        indices['bootstrap'] = states['bootstrap']
        indices['BOOTSTRAP_BEFORE'] = states['BOOTSTRAP_BEFORE']
        indices['REGRESSION_PRICE_RETURNS'] = kline_returns_func(indices['REGRESSION_PRICE'], 'np')

    if ('RELATIVE_BOLL_MAPOWER' not in indices.columns):
        sMAPOWER = indices['MAPOWER'].fillna(0)
        sBOLLCROSS = indices['BOLL_CROSS_SX'].fillna(0)
        indices['RELATIVE_BOLL_MAPOWER'] = sMAPOWER.rolling(3).corr(sBOLLCROSS)

    if ('RELATIVE_REGRESSION_MA30' not in indices.columns):
        sREGRESSION = indices['REGRESSION_PRICE'].fillna(0)
        indices['RELATIVE_REGRESSION_MA30'] = sREGRESSION.corr(indices['MA30'].fillna(0))
        indices['REGRESSION_RATIO'] = indices['RELATIVE_REGRESSION_MA30'] * (np.nan_to_num(np.log(indices['REGRESSION_PRICE'] / indices['MA30']), nan=0))

    if ('ATR_UB' not in indices.columns):
        scale, nATR = 1, max(14, indices['ZEN_TIDE_MEDIAN'].max())
        atr = talib.ATR(data.high, data.low, data.close, timeperiod=nATR)
        indices['ATR_UB'] = indices['REGRESSION_PRICE'] + scale * atr # 上轨
        indices['ATR_LB'] = indices['REGRESSION_PRICE'] - scale * atr # 下轨
        indices['ATR_PCT'] = np.nan_to_num(np.abs(atr / indices['REGRESSION_PRICE']), nan=0)

    if ('drawdown' not in indices.columns):
        indices['drawdown_today'] = np.nan_to_num(np.log(data.close / data.high), nan=0)
        indices['drawdown'] = np.nan_to_num(np.log(data.close / data.high.shift(1)), nan=0)
        worst_drawdown = (indices['drawdown'] <= indices['drawdown'].rolling(indices['ZEN_TIDE_MEDIAN'].max() * 2).min())
        worst_drawdown = worst_drawdown[worst_drawdown.apply(lambda x: x == True)]
      
    scale_patterns_kline = pd.DataFrame(np.c_[TA_HMA(data.open.values, 10),
                             TA_HMA(data.high.values, 10),
                             TA_HMA(data.low.values, 10),
                             TA_HMA(data.close.values, 10)], 
                            columns=['open', 'high', 'low', 'close'], 
                            index=data.index)
    indices['ochl4'] = scale_patterns_kline['ochl4'] = (scale_patterns_kline['open'] + scale_patterns_kline['close'] + scale_patterns_kline['high'] + scale_patterns_kline['low']) / 4
    indices['ochl4_returns'] = scale_patterns_kline['ochl4_returns'] = kline_returns_func(scale_patterns_kline['ochl4'], 'np')
    indices['ochl4_relative'] = np.nan_to_num(np.log(indices['BOLL_UB'] / indices['ochl4']), nan=0)
    indices['ATR_relative'] = np.nan_to_num(np.log(indices['BOLL_UB'] / indices['ATR_UB']), nan=0)

    indices['deadpool'] = deadpool = ((scale_patterns_kline['ochl4_returns'] < 0)) | \
        ((indices['DEA'] < 0) & (indices['LOWER_PRICE_SETTLE_BEFORE'] > 10))

    indices['scale_patterns'] = scale_patterns = ((scale_patterns_kline['ochl4_returns'] > 0) & (deadpool == False)) | \
        ((indices['MACD'] > 0) & (indices['ATR_SuperTrend'] > 0) & (deadpool == False))

    zen_neat_tide_minus = (((indices['ZEN_TIDE_CROSS_SX'] < indices['ZEN_TIDE_CROSS_JX'])) & (indices['REGRESSION_PRICE_RETURNS'] < 0) & (\
        (indices['ZEN_TIDE_MEDIAN'] * 2 > indices['ZEN_TIDE_CROSS_SX']) & \
        (indices['MA5'] < indices['BOLL_MA']) & (indices['bootstrap'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).sum() < 1)) & \
        ~((indices['boll_returns'] > 0) & (indices['BOLL_DELTA'] > 0) & (indices['MAPOWER_DELTA'] > 0.002)) & \
        ~((indices['MAPOWER'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).mean() > 0.618))) & \
        ~((indices['MACD'] > 0) & (indices['MACD'] > indices['DEA']) & (indices['MAPOWER'] > 0.809))

    indices['ML_FLU_TREND'] = (indices['ZEN_TIDE_DENSITY'] > min(0.512, indices['ZEN_TIDE_DENSITY'].median())) & \
        ((indices['CLUSTER_GROUP_DENSITY'] > min(0.618, indices['CLUSTER_GROUP_DENSITY'].median())) & (indices['CLUSTER_GROUP_DENSITY'] > 0.512)) | \
        ((abs(indices['BOOTSTRAP_BEFORE'] - indices['ATR_SuperTrend_CROSS_JX']) < indices['ZEN_TIDE_MEDIAN'] / 3) & \
        ((indices['CLUSTER_GROUP_DENSITY'] > 0.512) | ((indices['CLUSTER_GROUP_DENSITY'] > 0.382) & (indices['ZEN_TIDE_CROSS_SX'] > indices['ZEN_TIDE_MEDIAN']))) & \
        (indices['ATR_SuperTrend'] > 0) & (indices['bootstrap'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).sum() > 0)) | \
        ((indices['CLUSTER_GROUP_DENSITY'] > 0.382) & (indices['ZEN_TIDE_DENSITY_RETURNS'] > 0) & ((indices['MACD'] > indices['DEA']) | (indices['BOLL_CROSS_SX'] < 2)) & (indices['DUAL_CROSS_JX'] > indices['DEA_CROSS_JX']) & (indices['boll_returns'] > 0)) | \
        ((indices['MA30_SLOPE'] > 0) & (indices['DEA'] > 0) & (indices['ZEN_TIDE_DENSITY_RETURNS'] > 0) & ((indices['MACD'] > indices['DEA']) | (indices['BOLL_CROSS_SX'] < 2)) & (indices['DUAL_CROSS_JX'] > indices['DEA_CROSS_JX']) & (indices['boll_returns'] > 0)) | \
        ((indices['MA30_SLOPE'] > 0) & (indices['DEA'] > 0) & (indices['ZEN_TIDE_DENSITY_RETURNS'].rolling(4).sum() > 0.168) & ((indices['MACD'] > indices['DEA']) | (indices['BOLL_CROSS_SX'] < 2)) & (indices['boll_returns'] > 0)) | \
        ((indices['DEA_SLOPE'] > 0) & (indices['DEA_CROSS_SX'] < indices['ZEN_TIDE_MEDIAN']) & (indices['DIF'] > 0) & (indices['ZEN_TIDE_DENSITY_RETURNS'].rolling(4).sum() > 0.168) & ((indices['MACD'] > indices['DIF']) | (indices['BOLL_CROSS_SX'] < 2)) & (indices['boll_returns'] > 0))

    #indices['ML_FLU_TREND'] = (indices['ML_FLU_TREND']==True) & ~()

    zen_flu_tide = (indices['ML_FLU_TREND'] == True) & \
        (indices['MAPOWER'].rolling(2).mean() > 0.168) & \
        ((indices['ZEN_TIDE_CROSS_JX'] <= indices['ZEN_TIDE_CROSS_SX']) | (indices['REGRESSION_PRICE'] > indices['stop_line'])) & (\
        ((indices['DEA'] < 0) & (indices['bootstrap'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).sum() > 0)) | \
        ((indices['ZEN_TIDE_DENSITY_RETURNS'] > 0) & (indices['RELATIVE_BOLL_MAPOWER'] > 0.8)) | \
        ((indices['DEA'] > 0) & ((indices['BOLL_DELTA'] > 0) | (indices['ATR_LB'] > data['open']) | (indices['ATR_LB'] < indices['MA30'])) & \
        ((indices['DEA_CROSS_JX'] - indices['DEA_CROSS_SX']) > indices['ZEN_TIDE_MEDIAN'] * 2)) | \
        ((indices['BOOTSTRAP_BEFORE'] < indices['MACD_CROSS_JX']) & (indices['DEA_CROSS_JX'] < indices['MACD_CROSS_JX']) & (indices['MACD'] > 0) & (indices['DEA'] > 0) & (indices['ATR_LB'] < indices['MA30']) & (indices['DUAL_CROSS_JX'] > indices['DEA_CROSS_JX'])) | \
        ((indices['BOOTSTRAP_BEFORE'] < indices['MACD_CROSS_JX']) & (indices['DEA_CROSS_JX'] < indices['MACD_CROSS_JX']) & (indices['MACD'] > 0) & (indices['DEA'] > 0) & (indices['BOLL_DELTA'] > 0) & (indices['ATR_SuperTrend'] > 0) & (indices['ATR_SuperTrend_CROSS_JX'] > indices['DEA_CROSS_JX'])) | \
        ((indices['BOOTSTRAP_BEFORE'] < indices['MACD_CROSS_JX']) & (indices['DEA_CROSS_JX'] < indices['MACD_CROSS_JX']) & (indices['MACD'] > 0) & (indices['DEA'] > 0) & (indices['ATR_SuperTrend'] > 0) & (indices['ATR_SuperTrend_CROSS_JX'] > indices['ZEN_TIDE_MEDIAN'])) | \
        ((indices['DEA'] > 0) & ((indices['MACD'] < 0) | (indices['ATR_LB'] < indices['MA30'])) & \
        (indices['ZEN_TIDE_CROSS_JX'] < 2) & \
        ((indices['ZEN_TIDE_CROSS_SX'] - indices['ZEN_TIDE_CROSS_JX']) > indices['ZEN_TIDE_MEDIAN'] * 2) & \
        (indices['MAPOWER'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).mean() > 0.618)) | \
        ((indices['bootstrap'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).sum() > 0) & \
        ((indices['DEA'] < 0) | (indices['BOLL_DELTA'] > 0) | (indices['ATR_LB'] > data['open']) | (indices['ATR_LB'] < indices['MA30'])) & \
        ((indices['DEA_CROSS_JX'] - indices['DEA_CROSS_SX']) > indices['ZEN_TIDE_MEDIAN'] * 2)) | \
        (False)) & ~((indices['DEA'] > 0) & (indices['ATR_LB'] > indices['MA30']) & (indices['BOLL_DELTA'] < 0) & (indices['ATR_UB'] < indices['BOLL_UB'])) & \
         ~((indices['ZEN_TIDE_DENSITY_RETURNS'] < 0.001) & (indices['drawdown'] < -0.005)) & \
         ~((indices['DEA'] > 0) & (indices['drawdown'] < -0.005)) & \
         ~((indices['DEA'] > 0) & (indices['REGRESSION_SLOPE'] < 0.001)) & \
         ~((indices['DEA'] > 0) & (indices['DEA_SLOPE'] < 0.001)) & \
         ~((indices['DEA'] < 0) & (indices['DEA_SLOPE'] < indices.query('DEA_SLOPE<0')['DEA_SLOPE'].median())) & \
         ~((indices['DEA'] > 0) & (indices['ZEN_TIDE_DENSITY_RETURNS'] < 0.001)) & \
         ~((indices['MACD'] > 0) & (indices['drawdown'] < -0.005))

        #(indices['ZEN_TIDE_CROSS_JX'] <= indices['ZEN_TIDE_CROSS_SX']) & (\
        #((indices['bootstrap'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).sum()
        #> 0) & \
        #((atr_enable == True) & (indices['DEA'] > 0))) | \

    zen_neat_tide_minus = (zen_neat_tide_minus == True) & \
        ~(((indices['MACD'] > 0) | (indices['DEA'] > 0)) & (zen_flu_tide.rolling(indices['ZEN_TIDE_MEDIAN'].max()).mean() > 0) & ~(zen_flu_tide.rolling(4).mean() > 0)) & \
        ~((indices['DEA'] > 0) & (indices['ATR_SuperTrend'] == True) & (indices['ATR_SuperTrend_CROSS_JX'] > indices['ZEN_TIDE_MEDIAN'])) & \
        ~((indices['DEA'] > 0) & (indices['MA30_CROSS_JX'] < indices['MA30_CROSS_SX']) & (indices['MA30_CROSS_JX'] > indices['ZEN_TIDE_MEDIAN'] * 2) & (indices['MA5'] > indices['BOLL_MA'])) & \
        ~((indices['ML_FLU_TREND'] == True) & (indices['DEA_CROSS_JX'] > indices['ZEN_TIDE_MEDIAN']) & (indices['BOLL_CROSS_SX'] > 2) & (indices['ZEN_TIDE_DENSITY'] > 0.809) & (indices['ZEN_TIDE_DENSITY_RETURNS'] > -0.168))

    zen_neat_tide_stoploss = ((indices['drawdown'] < -0.0618) | \
        (indices['drawdown'].rolling(2).sum() < -0.0618) | \
        (indices['drawdown_today'] < -0.0512) | \
        ((indices['DEA'] > 0) & (indices['MACD'] < 0) & (indices['ZEN_TIDE_DENSITY_RETURNS'] < -0.001) & (indices['ZEN_TIDE_DENSITY_RETURNS'].rolling(2).sum() < indices['ZEN_TIDE_DENSITY_RETURNS']) & (indices['drawdown'] < 0) & (indices['drawdown'].rolling(2).sum() < indices['drawdown']) & (indices['drawdown'] <= indices['drawdown'].rolling(indices['ZEN_TIDE_MEDIAN'].max() * 2).min())) | \
        ((indices['DEA'] > 0) & (indices['MACD'] < 0) & (indices['DEA_SLOPE'].rolling(4).sum() < 0) & (indices['RELATIVE_BOLL_MAPOWER'] < -0.8) & (indices['drawdown'] < 0) & (indices['drawdown'].rolling(2).sum() < indices['drawdown']) & (indices['drawdown'] <= indices['drawdown'].rolling(indices['ZEN_TIDE_MEDIAN'].max() * 2).min())) | \
        ((indices['DEA'] > 0) & (indices['MACD'] < 0) & (indices['DEA_SLOPE'].rolling(4).sum() < 0) & (indices['RELATIVE_BOLL_MAPOWER'] < -0.8) & (indices['drawdown'] < 0) & (indices['drawdown'].rolling(2).sum() < indices['drawdown']) & (indices['drawdown'].rolling(4).mean() < indices['drawdown'])) | \
        ((indices['drawdown'] <= indices['drawdown'].rolling(indices['ZEN_TIDE_MEDIAN'].max() * 2).min()) & ((indices['drawdown'] < -0.0382) | (indices['drawdown'].rolling(2).sum() < -0.0512) | (indices['MACD'] < 0) | (indices['BOLL_CROSS_SX'] < indices['BOLL_CROSS_JX'])) & ~((indices['ML_FLU_TREND'] == True) & (indices['DEA_CROSS_JX'] > indices['ZEN_TIDE_MEDIAN']))) | \
        ((indices['MAPOWER_DELTA'] < -0.002) & (indices['RELATIVE_BOLL_MAPOWER'] < -0.8) & (indices['BOLL_CROSS_SX'] < indices['BOLL_CROSS_JX']) & (indices['drawdown'].rolling(2).sum() < -0.0512))) & \
        ~((indices['ML_FLU_TREND'] == True) & (indices['DEA_CROSS_JX'] > indices['ZEN_TIDE_MEDIAN']) & (indices['BOLL_CROSS_SX'] > 2) & (indices['ZEN_TIDE_DENSITY'] > 0.809) & (indices['ZEN_TIDE_DENSITY_RETURNS'] > -0.168)) | \
        ((indices['ZEN_TIDE_CROSS_SX'] < indices['ZEN_TIDE_CROSS_JX']) & (indices['ZEN_TIDE_CROSS_SX'] < indices['BOOTSTRAP_BEFORE']) & (indices['BOOTSTRAP_BEFORE'] < indices['MACD_CROSS_JX'])) & \
        ~((indices['ML_FLU_TREND'] == True) & (indices['DEA_CROSS_JX'] > indices['ZEN_TIDE_MEDIAN']) & (indices['BOLL_CROSS_SX'] > 2) & (indices['ZEN_TIDE_DENSITY'] > 0.809) & (indices['ZEN_TIDE_DENSITY_RETURNS'] > -0.168))

    atr_enable_debug = pd.DataFrame(columns=['atr_enable', 'debug_0', 'debug_1', 'debug_2'], index=zen_neat_tide_stoploss.index)
    atr_enable_debug['atr_enable'] = (indices['DEA_CROSS_SX'] < indices['ZEN_TIDE_MEDIAN']) & (indices['DIF'] > 0) & ((indices['MACD'] > indices['DIF']) | (indices['BOLL_CROSS_SX'] < 2))
    atr_enable_debug['debug_0'] = (indices['DEA_SLOPE'] > 0)
    atr_enable_debug['debug_1'] = (indices['ZEN_TIDE_DENSITY_RETURNS'].rolling(4).sum() > 0.168)
    atr_enable_debug['debug_2'] = (indices['boll_returns'] > 0)

    print(zen_flu_tide.loc[indices.index.get_level_values(level=0).intersection(pd.date_range('2020-03-18 10:00:00',
                                                                                         periods = 480,
                                                                                        freq = '60min')),
                                                                                        :])
    print(atr_enable_debug.loc[indices.index.get_level_values(level=0).intersection(pd.date_range('2020-03-18 10:00:00',
                                                                                         periods = 480,
                                                                                        freq = '60min')),
                                                                                        :])
    print(zen_neat_tide_stoploss.loc[indices.index.get_level_values(level=0).intersection(pd.date_range('2020-03-18 10:00:00',
                                                                                         periods = 480,
                                                                                        freq = '60min')),
                                                                                        :])

    indices = indices.assign(POSITION = np.where((zen_neat_tide_minus | zen_neat_tide_stoploss) == True, 
                                            -1, 
                                            np.where((zen_flu_tide == True), 
                                                    1, 
                                                    np.where((indices['ZEN_TIDE_CROSS_SX'] < indices['ZEN_TIDE_MEDIAN']) & (indices['drawdown'] > indices['drawdown'].median()) & (scale_patterns_kline['ochl4_returns'].values < 0), 
                                                            -1, 0))))

    # 为了处理 Position 信号抖动，使用 Rolling 过滤，无指向性的用 ATR 趋势策略填充 策略 1 加仓 0 不动， -1 减仓
    indices = indices.assign(POSITION_R5=indices['POSITION'])

    #print(indices.loc[indices.index.get_level_values(level=0).intersection(pd.date_range('2020-02-27',
    #                                                                                     periods=480,
    #                                                                                    freq='30min')),
    #                                                                                    ['bootstrap',
    #                                                                                    'POSITION_R5']])
    # 策略 Rolling合并后 1 加仓 0 不动， -1 直接清仓
    indices['POSITION_R5'] = np.where(((scale_patterns_kline['ochl4_returns'].values > 0) | (indices['ATR_LB'] < indices['MA30']) | ((indices['ATR_LB'] > data['open']) & ((indices['MACD'] < 0) | (indices['bootstrap'].rolling(indices['ZEN_TIDE_MEDIAN'].max()).sum() > 0)))) & (indices['POSITION_R5'].values > 0), 
                      1, 
                      np.where((scale_patterns_kline['ochl4_returns'].values < 0) & (indices['POSITION_R5'].values < 0), 
                               -1, 
                               0)) # 这里 0 是代表本策略中无指向性的，使用 ATR 策略填充
    indices['POSITION_R5'].ffill(inplace=True)
    indices['POSITION_R5'].fillna(0, inplace=True)

    indices = indices.assign(close = data.close)
    return indices


if __name__ == '__main__':
    codelist = ['000905']
    #codelist = ['600188']
    codelist = ['300263']
    code = codelist[0]
    #data_day = QA.QA_fetch_stock_day_adv(codelist,
    #                                     '2015-01-01','2020-03-30')
    #data_day = QA.QA_fetch_stock_min_adv(codelist,
    #                                      '2019-01-01','2020-03-30',end='2020-06-30
    #                                      23:59:59',
    #                                      frequence='60min')
    codelist = ['HUOBI.btcusdt']
    code = codelist[0]
    data_day = QA.QA_fetch_cryptocurrency_min_adv(code=codelist,
        start='2020-01-01',
        end='2020-06-30',
        frequence='60min')
    #data_day = QA.QA_DataStruct_CryptoCurrency_min(data_day.resample('4h'))

    scale_patterns_cross = data_day.add_func(scale_patterns_cross_func)

    actions = (scale_patterns_cross.loc[(slice(None), code), :]['POSITION_R5'] != 0)
    actions = actions[actions.apply(lambda x: x == True)]  # eqv.  Trim(x == False)
    orders = scale_patterns_cross.loc[((actions == True).index.get_level_values(level=0), code), :]

    user = QA.QA_User(username='aaaa4444', password='aaaa4444')
    portfolio = user.new_portfolio('superme44444')
    stock_account = portfolio.new_account(account_cookie='BKTST_SCL01_C{}_T{}'.format(code, QA_util_timestamp_to_str()[2:16]), 
                                          allow_t0=True,
                                          allow_margin=False,
                                          allow_sellopen=False, 
                                          market_type=QA.MARKET_TYPE.CRYPTOCURRENCY,
                                          running_environment=QA.RUNNING_ENVIRONMENT.BACKETEST)
    if (len(stock_account.history_table) > 0):
        print(stock_account.history_table)
        stock_account.reset_assets(1000000)
    for _, item in scale_patterns_cross.iterrows():
        running_time = item.name[0]
        code = item.name[1]
        print(running_time, code)
        if (item['POSITION_R5'] == 1):
            if (len(stock_account.hold_available) == 0) or \
                ((len(stock_account.hold_available) > 0) and (code not in stock_account.hold_available.index)):
                print('择时：', running_time, 'LONG', '当前标的 {}开仓！Cash:{}, amount:{:.4g}'.format(code, stock_account.cash_available, abs((stock_account.cash_available / item['close']) * 0.96)))
                stock_account.receive_simpledeal(code=code,
                                    trade_price=item['close'],
                                     trade_amount=abs((stock_account.cash_available / item['close']) * 0.96),
                                     trade_towards= item['POSITION_R5'],
                                     trade_time=running_time)
            else:
                print('LONG', '当前标的 {} 满仓！drawdown:{:.3g} DEST:{:.3g} DEA:{:.3g}'.format(code, item['drawdown'], item['ZEN_TIDE_DENSITY_RETURNS'], item['DEA_SLOPE']), '剩余资金总仓位：{:.1%}'.format(stock_account.freecash_precent))
        elif ((item['POSITION_R5'] == -1)):
            if ((len(stock_account.hold_available) > 0) and (code in stock_account.hold_available.index)) or \
                (len(stock_account.hold_available) > 0):
                stock_account.receive_simpledeal(code=code,
                                    trade_price=item['close'],
                                     trade_amount=abs(stock_account.hold_available[code]),
                                     trade_towards= item['POSITION_R5'],
                                     trade_time=running_time)
                print('择时：', running_time, 'SHORT: 当前标的 {}清仓！Cash:{}'.format(code, stock_account.cash_available))
            else:
                print('择时：', running_time, 'SHORT: 当前标的 {} 空仓！'.format(code), '剩余资金总仓位：{:.1%}'.format(stock_account.freecash_precent))
        else:
            print('无操作策略：{} drawdown:{:.3g} cond:{} CORR:{:.3g} DEA:{:.3g} foo!'.format(item['POSITION_R5'], item['drawdown'], (item['DEA'] > 0) & (item['MACD'] < 0), item['RELATIVE_BOLL_MAPOWER'], item['DEA_SLOPE']))
    print(stock_account.history_table)
    Risk = QA.QA_Risk(stock_account, benchmark_code=code, if_fq=False,
                        benchmark_type=QA.MARKET_TYPE.CRYPTOCURRENCY)
    print(Risk().T)
    Risk.plot_assets_curve()

    # 暗色主题
    plt.style.use('Solarize_Light2')

    # 正常显示中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    fig = plt.figure(figsize = (22,9))
    fig.suptitle(u'{:s} 机器学习趋势分析'.format(code), fontsize=16)
    ax1 = plt.subplot2grid((4,3),(0,0), rowspan=3, colspan=3)
    ax2 = plt.subplot2grid((4,3),(3,0), rowspan=1, colspan=3, sharex=ax1)
    ax3 = ax1.twinx()
    mpf.candlestick2_ochl(ax1,
                          data_day.data.open[11:],
                          data_day.data.close[11:],
                          data_day.data.high[11:],
                          data_day.data.low[11:],
                          width=0.6, colorup='r', colordown='green',
                          alpha=0.3)
    DATETIME_LABEL = data_day.index.get_level_values(level=0).to_series().apply(lambda x: x.strftime("%Y-%m-%d %H:%M")[2:16])[11:]
    ax1.plot(DATETIME_LABEL, scale_patterns_cross['BOLL_UB'][11:] , lw=0.75, color='cyan', alpha=0.6)
    ax1.plot(DATETIME_LABEL, scale_patterns_cross['BOLL_LB'][11:] , lw=0.75, color='fuchsia', alpha=0.6)
    ax1.plot(DATETIME_LABEL, scale_patterns_cross['MA30'][11:] , lw=0.75, color='purple', alpha=0.6)

    # 附加图，很重要！
    ax3.plot(DATETIME_LABEL, scale_patterns_cross['MA30_SLOPE'][11:], lw=0.75, color='gray', alpha=0.2)
    ax3.plot(DATETIME_LABEL, scale_patterns_cross['ZEN_TIDE_DENSITY'][11:], lw=0.75, color='lightskyblue', alpha=0.3)

    ax1.set_xticks(range(0, len(DATETIME_LABEL), round(len(data_day) / 16)))
    ax1.set_xticklabels(DATETIME_LABEL[::round(len(data_day) / 16)], rotation = 10)
    ax1.grid(True)

    ax2.plot(DATETIME_LABEL, scale_patterns_cross['DIF'][11:], color='green', lw=1, label='DIF')
    ax2.plot(DATETIME_LABEL, scale_patterns_cross['DEA'][11:], color='purple', lw=1, label='DEA')

    barlist = ax2.bar(DATETIME_LABEL, scale_patterns_cross['MACD'][11:], width=0.6, label='MACD')
    for i in range(len(DATETIME_LABEL.index)):
        if scale_patterns_cross['MACD'][i + 11] <= 0:
            barlist[i].set_color('g')
        else:
            barlist[i].set_color('r')
    ax2.set(ylabel='MACD(26,12,9)')

    ax2.set_xticks(range(0, len(DATETIME_LABEL), round(len(data_day) / 16)))
    ax2.set_xticklabels(DATETIME_LABEL[::round(len(data_day) / 16)], rotation=15)
    ax2.grid(True)

    actions = (scale_patterns_cross.loc[(slice(None), code), :]['POSITION_R5'].diff() != 0)

    scale_patterns_cross = scale_patterns_cross.assign(DATETIME_LABEL=np.r_[[np.nan for i in range(11)], DATETIME_LABEL.values])
    margin_orders_idx = pd.to_datetime(stock_account.history_table['datetime'])
    margin_orders = scale_patterns_cross.loc[(margin_orders_idx, code), :]
    scale_patterns_cross = scale_patterns_cross.assign(ORDERS=False)
    scale_patterns_cross.loc[(margin_orders_idx, code), 'ORDERS'] = 1
    #print(margin_orders.loc[:, ['ZEN_TIDE_CROSS_SX', 'POSITION_R5']])
    margin_orders.apply(lambda x:
                      ax1.text(scale_patterns_cross.loc[x.name].DATETIME_LABEL, 
                               x.BOLL_UB, 
                               u'卖:{0:.2f},DEA:{1:.2g},SLOPE{2:.3g},DWD:{3:.3g}'.format(x.close, x['DEA_SLOPE'], x['REGRESSION_SLOPE'], x['drawdown']), 
                               verticalalignment='bottom', 
                               horizontalalignment='left',
                               color='green', fontsize=11) if (x.POSITION_R5 < 0) else
                      ax1.text(scale_patterns_cross.loc[x.name].DATETIME_LABEL, 
                               x.BOLL_LB, 
                               u'买:{0:.2f},DEA:{1:.2g},SLOPE{2:.3g},DWD:{3:.3g}'.format(x.close, x['DEA_SLOPE'], x['REGRESSION_SLOPE'], x['drawdown']), 
                               verticalalignment='top', 
                               horizontalalignment='left',
                               color='red', 
                               fontsize=11)
                      , axis=1)
    p3 = ax1.plot(DATETIME_LABEL,
             np.where((scale_patterns_cross['ORDERS'].values == 1) & (scale_patterns_cross.loc[(slice(None), code),
             'POSITION_R5'].values > 0),
                      scale_patterns_cross['BOLL_LB'], np.nan)[11:],
             'r^', alpha = 0.8)
    ax2.plot(DATETIME_LABEL, 
             np.where((scale_patterns_cross['ORDERS'].values == 1) & (scale_patterns_cross.loc[(slice(None), code), 'POSITION_R5'].values > 0), 
                      scale_patterns_cross['DEA'], np.nan)[11:], 
             'r^', alpha = 0.8)
    p4 = ax1.plot(DATETIME_LABEL,
             np.where((scale_patterns_cross['ORDERS'].values == 1) & (scale_patterns_cross.loc[(slice(None), code),
             'POSITION_R5'].values < 0),
                      scale_patterns_cross['BOLL_UB'], np.nan)[11:],
             'gv', alpha = 0.8)
    #ax1.plot(DATETIME_LABEL,
    #         np.where((scale_patterns_cross['ZEN_TIDE_CROSS'].values == 1),
    #                  scale_patterns_cross['BOLL_LB'], np.nan)[11:],
    #         'yD', alpha = 0.6)

    ax1.plot(DATETIME_LABEL, 
             np.where(((scale_patterns_cross['lower_settle_price'].values == 1) & (scale_patterns_cross['MA30_SLOPE'] > 0) & (scale_patterns_cross['bootstrap'].values != 1)), 
                      scale_patterns_cross['BOLL_LB'], np.nan)[11:], 
             'gp', alpha = 0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where(((scale_patterns_cross['lower_settle_price'].values == 1) & (scale_patterns_cross['MA30_SLOPE'] < 0) & (scale_patterns_cross['bootstrap'].values != 1)), 
                      scale_patterns_cross['BOLL_LB'], np.nan)[11:], 
             'yp', alpha = 0.6)
    ax1.plot(DATETIME_LABEL, 
             np.where((scale_patterns_cross['bootstrap'].values == 1), 
                      scale_patterns_cross['BOLL_LB'], np.nan)[11:], 
             'mp', alpha = 0.8)

    ax1.plot(DATETIME_LABEL, 
             np.where((scale_patterns_cross['ML_FLU_TREND'] == True), 
                      scale_patterns_cross['MA30'], np.nan)[11:], 
             'r.', alpha = 0.2)

    #ax1.plot(DATETIME_LABEL,
    #         np.where((scale_patterns_cross['ZEN_TIDE_CROSS'].values == -1),
    #                  scale_patterns_cross['BOLL_UB'], np.nan)[11:],
    #         'mD', alpha = 0.6)
    p1 = ax1.plot(DATETIME_LABEL, 
             np.where((actions.values == True) & (scale_patterns_cross.loc[(slice(None), code), 'POSITION_R5'].values > 0), 
                      data_day.data.loc[(slice(None), code), :].close.values, np.nan)[11:], 
             'rP', alpha = 0.6)
    p2 = ax1.plot(DATETIME_LABEL, 
             np.where((actions.values == True) & (scale_patterns_cross.loc[(slice(None), code), 'POSITION_R5'].values < 0), 
                      data_day.data.loc[(slice(None), code), :].close.values, np.nan)[11:], 
             'g>', alpha=0.6)
    #ax1.legend([p3, p4], [u'建仓', u'清仓'], loc='lower right', scatterpoints=1)
#    l = ['LR']
#    ax1.legend(l)
    fig.align_xlabels()
    plt.show()