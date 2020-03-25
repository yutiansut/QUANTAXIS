import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QAhuobi import FIRST_PRIORITY
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *
from QUANTAXIS.QAIndicator.base import *
import mpl_finance as mpf
import matplotlib.dates as mdates


def hma_cross_func(data):
    """
    HMA均线金叉指标
    """
    HMA10 = talib.WMA(2 * talib.WMA(data.close, 
                                    int(10 / 2)) - talib.WMA(data.close, 
                                                             10), 
                      int(np.sqrt(10)))
    MA30 = talib.MA(data.close, 30)
    
    MA30_CROSS = pd.DataFrame(columns=['MA30_CROSS', 
                                       'MA30_CROSS_JX', 
                                       'MA30_CROSS_SX'], 
                              index=data.index)
    MA30_CROSS_JX = CROSS(HMA10, MA30)
    MA30_CROSS_SX = CROSS(MA30, HMA10)
    MA30_CROSS['MA30_CROSS'] = np.where(MA30_CROSS_JX.values == 1, 
                                        1, np.where(MA30_CROSS_SX.values == 1, 
                                                    -1, 0))
    MA30_CROSS['MA30_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_CROSS_JX)
    MA30_CROSS['MA30_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_CROSS_SX)
    MA30_CROSS['HMA_RETURNS'] = kline_returns_func(HMA10)
    MA30_CROSS['RETURNS'] = kline_returns_func(data.close)
    MA30_CROSS = MA30_CROSS.assign(HMA10=HMA10)

    rsi_ma, stop_line, direction = ATR_RSI_Stops(data, 27)
    tsl, atr_super_trend = ATR_SuperTrend_cross(data)
    price_predict_day = price_predict_with_macd_trend_func(data)
    dual_cross_day = dual_cross_func(data)
    boll_bands_day = boll_cross_func(data)
    maxfactor_cross_day = maxfactor_cross_func(data)
    machine_learning_trend = machine_learning_trend_func(data)
    settle_state = bootstrap_trend_func(data)

    ma30_croos_day = MA30_CROSS
    hma5_returns = ma30_croos_day['HMA_RETURNS'].values
    dealpool = ((hma5_returns < 0) & \
        (ma30_croos_day['MA30_CROSS_JX'].values > ma30_croos_day['MA30_CROSS_SX'].values)) | \
        ((ma30_croos_day['HMA_RETURNS'].values < 0) & (boll_bands_day['BOLL_CROSS_JX'].values > boll_bands_day['BOLL_CROSS_SX'].values)) | \
        ((ma30_croos_day['HMA_RETURNS'].values < 0) & (maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values) & (price_predict_day['DELTA'].values < 0))
    bootstrap = ((hma5_returns > 0) & (machine_learning_trend['ZEN_TIDE_CROSS_JX'] <= machine_learning_trend['ZEN_TIDE_CROSS_SX']) & (dual_cross_day['DUAL_CROSS_JX'].values > 0)) & (\
            ((maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values > 2) & (maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values)) | \
            ((maxfactor_cross_day['MAXFACTOR_DELTA'].rolling(4).mean().values > 0) & (maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values) & (price_predict_day['DELTA'].values > 0)) | \
            ((maxfactor_cross_day['MAXFACTOR_DELTA'].rolling(4).mean().values > 0) & (maxfactor_cross_day['MAXFACTOR_DELTA'].values > -61.8) & (price_predict_day['MACD_CROSS_JX'].values < price_predict_day['MACD_CROSS_SX'].values) & (price_predict_day['DELTA'].values > 0)) | \
            ((maxfactor_cross_day['MAXFACTOR_DELTA'].rolling(4).mean().values > 0) & (maxfactor_cross_day['MAXFACTOR_DELTA'].values > -61.8) & (price_predict_day['DELTA'].rolling(4).mean().values > 0) & (price_predict_day['DELTA'].values > 0)) | \
            ((HMA10 > boll_bands_day['BOLL_MA'].values) & (maxfactor_cross_day['MAXFACTOR_CROSS_JX'].values < maxfactor_cross_day['MAXFACTOR_CROSS_SX'].values)) | \
            ((HMA10 > boll_bands_day['BOLL_MA'].values) & (boll_bands_day['BBW_MA20'].values < boll_bands_day['BOLL_WIDTH'].values)) | \
            (((boll_bands_day['BOLL_CROSS_JX'].values > 18) & (ma30_croos_day['MA30_CROSS_JX'].values < ma30_croos_day['MA30_CROSS_SX'].values)) & \
            ~((boll_bands_day['BBW_MA20'].values > boll_bands_day['BOLL_WIDTH'].values) & (price_predict_day['MACD'].values > 0))) | \
            ((boll_bands_day['BOLL_CROSS_JX'].values > 2) & (price_predict_day['MACD_CROSS_JX'].values < price_predict_day['MACD_CROSS_SX'].values)) & \
            ((price_predict_day['PRICE_PRED_CROSS_JX'].values < price_predict_day['PRICE_PRED_CROSS_SX'].values)) & \
            (((boll_bands_day['BOLL_CROSS_JX'].values > 8) & (ma30_croos_day['MA30_CROSS_JX'].values < ma30_croos_day['MA30_CROSS_SX'].values)) | (boll_bands_day['BOLL_CROSS_JX'].values < 6)) & \
            ~((boll_bands_day['BBW_MA20'].values > boll_bands_day['BOLL_WIDTH'].values) & (price_predict_day['MACD'].values > 0)))
    MA30_CROSS = MA30_CROSS.assign(POSITION=np.where(dealpool == True, 
                                            -1, 
                                            np.where(bootstrap == True, 
                                                    1, 
                                                    np.where((ma30_croos_day['HMA_RETURNS'].values < 0), 
                                                            -1, 0))))

    # 为了处理 Position 信号抖动，使用 Rolling 过滤，无指向性的用 ATR 趋势策略填充 策略 1 加仓 0 不动， -1 减仓
    MA30_CROSS = MA30_CROSS.assign(BOOTSRTAP_R5=
                                                 MA30_CROSS['POSITION'].rolling(4).apply(lambda x: 
                                                                                    x.sum(), raw=False).apply(lambda x:
                                                                                                                0 if np.isnan(x) else int(x)))
    # 策略 Rolling合并后 1 加仓 0 不动， -1 直接清仓
    MA30_CROSS['BOOTSRTAP_R5'] = np.where((ma30_croos_day['HMA_RETURNS'].values > 0) & (machine_learning_trend['ZEN_TIDE_CROSS_SX'] > machine_learning_trend['ZEN_TIDE_CROSS_SX'].median() * 0.382) & (MA30_CROSS['BOOTSRTAP_R5'].values > 0), 
                      1, 
                      np.where((ma30_croos_day['HMA_RETURNS'].values < 0) & (MA30_CROSS['BOOTSRTAP_R5'].values < 0), 
                               -1, 
                               np.where((direction==True) & (machine_learning_trend['ZEN_TIDE_CROSS_SX'] > machine_learning_trend['ZEN_TIDE_CROSS_SX'].median() * 0.382), 1, 0))) # 这里 0 是代表本策略中无指向性的，为了降低代码复杂度去掉了 ATR 策略部分
    MA30_CROSS['BOOTSRTAP_R5'].ffill(inplace=True)
    MA30_CROSS['BOOTSRTAP_R5'].fillna(0, inplace=True)
    MA30_CROSS = MA30_CROSS.assign(close=data.close)
    return MA30_CROSS

if __name__ == '__main__':
    from QUANTAXIS.QAAnalysis.QAAnalysis_signal import *
    codelist = ['000905']
    #data_day = QA.QA_fetch_stock_day_adv(codelist, '2015-01-01','2020-03-30')
    data_day = QA.QA.QA_fetch_stock_min_adv(codelist,
                                          '2015-01-01','2020-03-30',
                                          frequence='60min')

    hma_cross_day = data_day.add_func(hma_cross_func)

    # 这四行是我自己用来看收益率，因为我不会做到QABacktest和QAStrategy来评估策略好坏。只能自己写个简单版的。
    code = codelist[0]
    #strategy_POSITION = data_day.add_func(kline_returns_func)
    #strategy_POSITION['strategy_R5'] =
    #    np.where(strategy_POSITION['BOOTSRTAP_R5'].shift(1).values > 0, 1, 0)
    #    *
    #strategy_POSITION['returns'].shift(1)
    #print(strategy_POSITION.tail(60))
    #print(hma_croos_day.tail(60))
    #strategy_POSITION[['returns',
    #'strategy_R5']].dropna().cumsum().apply(np.exp).plot(figsize=(10, 6))

    code = codelist[0]
    actions = (hma_cross_day.loc[(slice(None), code), :]['BOOTSRTAP_R5'].diff() != 0)
    actions = actions[actions.apply(lambda x: x == True)]  # eqv.  Trim(x == False)
    #print(actions)
    orders = hma_cross_day.loc[((actions == True).index.get_level_values(level=0), code), :]
    print(orders)

    user = QA.QA_User(username='aaaa22', password='aaaa22')
    portfolio = user.new_portfolio('superme22')
    stock_account = portfolio.new_account(account_cookie='BKTST_HMA01_C{}_T{}'.format(codes[0], QA_util_timestamp_to_str()[2:16]),allow_t0=False,allow_margin=False,allow_sellopen=False,running_environment=QA.MARKET_TYPE.STOCK_CN)
    for _, item in orders.iterrows():
        running_time = item.name[0]
        code = item.name[1]
        if (item['BOOTSRTAP_R5'] == 1):
            if (len(stock_account.hold_available) == 0) or \
                ((len(stock_account.hold_available) > 0) and (code not in stock_account.hold_available.index)):
                print('择时：', running_time, 'LONG', '当前标的 {}开仓！Cash:{}'.format(code, stock_account.cash_available))
                stock_account.receive_simpledeal(code=code,
                trade_price=item['close'],
                                     trade_amount=abs(100 * int((stock_account.cash_available / item['close']) * 0.009)),
                                     trade_towards= item['BOOTSRTAP_R5'],
                                     trade_time=running_time)
            else:
                print('LONG', '当前标的 {} 满仓！'.format(code), '剩余资金总仓位：{:.1%}'.format(stock_account.freecash_precent))
        elif ((item['BOOTSRTAP_R5'] == -1)):
            if (len(stock_account.hold_available) > 0) and (code in stock_account.hold_available.index):
                stock_account.receive_simpledeal(code=code,
                trade_price=item['close'],
                                     trade_amount=abs(stock_account.hold_available[code]),
                                     trade_towards= item['BOOTSRTAP_R5'],
                                     trade_time=running_time)
                print('择时：', running_time, 'SHORT: 当前标的 {}清仓！Cash:{}'.format(code, stock_account.cash_available))
            else:
                print('择时：', running_time, 'SHORT: 当前标的 {} 空仓！'.format(code), '剩余资金总仓位：{:.1%}'.format(stock_account.freecash_precent))

    print(stock_account.history_table)
    Risk = QA.QA_Risk(stock_account, benchmark_code=code,
                        benchmark_type=QA.MARKET_TYPE.STOCK_CN)
    print(Risk().T)
    Risk.plot_assets_curve()
    #Risk.save()
    #stock_account.save()

    #print(action[-60:])
    #print(hma_croos_day.loc[(slice(None), code),
    #:]['BOOTSRTAP_R5'].values[-60:])
    #foo = np.c_[hma_croos_day.loc[(slice(None), code),
    #:]['BOOTSRTAP_R5'].index.values.T, hma_croos_day.loc[(slice(None), code),
    #:]['BOOTSRTAP_R5'].values.T]
    #print(foo)
    #towards = np.where(action == 1, hma_croos_day.loc[(slice(None), code),
    #:]['BOOTSRTAP_R5'].index.values, np.NaN)
    #print(towards[-60:])
    #orders = towards
    plt.figure(figsize = (22,9))
    ax1 = plt.subplot(111)
    mpf.candlestick2_ochl(ax1, 
                          data_day.data.loc[(slice(None), code), :].open.values, 
                          data_day.data.loc[(slice(None), code), :].close.values, 
                          data_day.data.loc[(slice(None), code), :].high.values, 
                          data_day.data.loc[(slice(None), code), :].low.values, 
                          width = 0.6, colorup = 'r', colordown = 'green', alpha = 0.5)
    DATETIME_LABEL = data_day.data.loc[(slice(None), code), :].index.get_level_values(level=0).to_series().apply(lambda x: x.strftime("%Y-%m-%d")[2:13])

    ax1.set_xticks(range(0, len(DATETIME_LABEL), round(len(data_day) / 12)))
    ax1.set_xticklabels(DATETIME_LABEL[::round(len(data_day) / 12)])

    plt.plot(DATETIME_LABEL, hma_cross_day.loc[(slice(None), code), 'HMA10'].values, 'c', linewidth = 0.6, alpha = 0.75)
    actions = (hma_cross_day.loc[(slice(None), code), :]['BOOTSRTAP_R5'].diff() != 0)
    ax1.plot(DATETIME_LABEL, 
             np.where((actions.values == True) & (hma_cross_day.loc[(slice(None), code), 'BOOTSRTAP_R5'].values > 0), 
                      data_day.data.loc[(slice(None), code), :].close.values, np.nan), 
             'g^', alpha = 0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where((actions.values == True) & (hma_cross_day.loc[(slice(None), code), 'BOOTSRTAP_R5'].values < 0), 
                      data_day.data.loc[(slice(None), code), :].close.values, np.nan), 
             'rv', alpha=0.8)
    plt.show()
