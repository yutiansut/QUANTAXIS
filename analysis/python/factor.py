#coding:utf-8

# MACD
def MACD(security_list, fastperiod=12, slowperiod=26, signalperiod=9):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 MACD
    security_data = history(slowperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    macd_DIF = {}; macd_DEA = {}; macd_HIST = {}
    for stock in security_list:
        macd_DIF[stock], macd_DEA[stock], macd = talib.MACDEXT(security_data[stock], fastperiod=fastperiod, fastmatype=1, slowperiod=slowperiod, slowmatype=1, signalperiod=signalperiod, signalmatype=1)
        macd_HIST[stock] = macd * 2
    return macd_DIF, macd_DEA, macd_HIST

# MA
def MA(security_list, timeperiod=5):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 MA
    security_data = history(timeperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    ma = {}
    for stock in security_list:
        ma[stock] = talib.MA(security_data[stock], timeperiod)
    return ma

# SMA
def SMA(security_list, timeperiod=5):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 SMA
    security_data = history(timeperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    sma = {}
    for stock in security_list:
        close = np.nan_to_num(security_data[stock])
        sma[stock] = reduce(lambda x, y: ((timeperiod - 1) * x + y) / timeperiod, close)
    return sma

# KDJ
def KDJ(security_list, fastk_period=5, slowk_period=3, fastd_period=3) :
    def SMA_CN(close, timeperiod) :
        close = np.nan_to_num(close)
        return reduce(lambda x, y: ((timeperiod - 1) * x + y) / timeperiod, close)

    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 KDJ
    n = max(fastk_period, slowk_period, fastd_period)
    k = {}; d = {}; j = {}
    for stock in security_list:

        security_data = attribute_history(stock, n*2,'1d',fields=['high', 'low', 'close'], df=False)
        high = security_data['high']
        low = security_data['low']
        close = security_data['close']
        kValue, dValue = talib.STOCHF(high, low, close, fastk_period, fastd_period, fastd_matype=0)
        kValue = np.array(map(lambda x : SMA_CN(kValue[:x], slowk_period), range(1, len(kValue) + 1)))
        dValue = np.array(map(lambda x : SMA_CN(kValue[:x], fastd_period), range(1, len(kValue) + 1)))
        jValue = 3 * kValue - 2 * dValue

        func = lambda arr : np.array([0 if x < 0 else (100 if x > 100 else x) for x in arr])

        k[stock] = func(kValue)
        d[stock] = func(dValue)
        j[stock] = func(jValue)
    return k, d, j

# RSI
def RSI(security_list, timeperiod=14):
    def SMA_CN(close, timeperiod) :
        close = np.nan_to_num(close)
        return reduce(lambda x, y: ((timeperiod - 1) * x + y) / timeperiod, close)

    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 RSI
    security_data = history(timeperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    rsi = {}
    for stock in security_list:
        close = close = security_data[stock]
        diff = map(lambda x, y : x - y, close[1:], close[:-1])
        diffGt0 = map(lambda x : 0 if x < 0 else x, diff)
        diffABS = map(lambda x : abs(x), diff)
        diff = np.array(diff)
        diffGt0 = np.array(diffGt0)
        diffABS = np.array(diffABS)
        diff = np.append(diff[0], diff)
        diffGt0 = np.append(diffGt0[0], diffGt0)
        diffABS = np.append(diffABS[0], diffABS)
        rsi[stock] = np.array(map(lambda x: SMA_CN(diffGt0[:x],timeperiod)/SMA_CN(diffABS[:x],timeperiod)*100, range(1,len(diffGt0)+1))) 
    return rsi

# CCI
def CCI(security_list, timeperiod=14):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 CCI
    cci = {}
    for stock in security_list:
        security_data = attribute_history(stock, timeperiod*2, '1d',['close','high','low'] , df=False)
        close_CCI = security_data['close']
        high_CCI = security_data['high']
        low_CCI = security_data['low']
        cci[stock] = talib.CCI(high_CCI, low_CCI, close_CCI, timeperiod)
    return cci

# ATR
def ATR(security_list, timeperiod=14):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 ATR
    atr = {}
    for stock in security_list:
        security_data = attribute_history(stock, timeperiod*2, '1d',['close','high','low'] , df=False)
        close_ATR = security_data['close']
        high_ATR = security_data['high']
        low_ATR = security_data['low']
        atr[stock] = talib.ATR(high_ATR, low_ATR, close_ATR, timeperiod)
    return atr

# 布林线
def Bollinger_Bands(security_list, timeperiod=5, nbdevup=2, nbdevdn=2):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 Bollinger Bands
    security_data = history(timeperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    upperband={}; middleband={}; lowerband={}
    for stock in security_list:
        upperband[stock], middleband[stock], lowerband[stock] = talib.BBANDS(security_data[stock], timeperiod, nbdevup, nbdevdn)
    return upperband, middleband, lowerband

# 平均成交额
def MA_MONEY(security_list, timeperiod=5):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 N 日平均成交额
    security_data = history(timeperiod*2, '1d', 'money' , security_list, df=False, skip_paused=True)
    mamoney={}
    for stock in security_list:
        x = security_data[stock]
        mamoney[stock] = talib.MA(security_data[stock], timeperiod)
    return mamoney

# 平均成交量
def MA_VOLUME(security_list, timeperiod=5):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 N 日平均成交量
    security_data = history(timeperiod*2, '1d', 'volume' , security_list, df=False, skip_paused=True)
    mavol={}
    for stock in security_list:
        x = security_data[stock]
        mavol[stock] = talib.MA(security_data[stock], timeperiod)
    return mavol

# BIAS
def BIAS(security_list, timeperiod=5):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 BIAS 
    security_data = history(timeperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    bias = {}
    for stock in security_list:
        average_price = security_data[stock][-timeperiod:].mean()
        current_price = security_data[stock][-1]
        bias[stock]=(current_price-average_price)/average_price
    return bias

# BBI
def BBI(security_list, timeperiod1=3, timeperiod2=6, timeperiod3=12, timeperiod4=24):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 BBI
    security_data = history(timeperiod4*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    bbi={}
    for stock in security_list:
        x = security_data[stock]
        d = (x[-timeperiod1:].mean()+x[-timeperiod2:].mean()+x[-timeperiod3:].mean()+x[-timeperiod4:].mean())/4.0
        bbi[stock] = d
    return bbi

# TRIX
def TRIX(security_list, timeperiod=30):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 TRIX
    security_data = history(timeperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    trix={}
    for stock in security_list:
        trix[stock] = talib.TRIX(security_data[stock], timeperiod)
    return trix

# EMA
def EMA(security_list, timeperiod=30):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 EMA
    security_data = history(timeperiod*2, '1d', 'close' , security_list, df=False, skip_paused=True)
    ema={}
    for stock in security_list:
        ema[stock] = talib.EMA(security_data[stock], timeperiod)
    return ema

# DMA
def DMA(security_list,fastperiod=5,slowperiod=60,amaperiod=20):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 DMA
    dma = {}
    for security in security_list:
        security_data = attribute_history(security, slowperiod*2, '1d', ['close'], skip_paused=True, df=False)['close']
        m1 = map(lambda i: security_data[i-fastperiod+1:i+1],range(len(security_data))[len(security_data)-slowperiod:])
        m2 = map(lambda i: security_data[i-slowperiod+1:i+1],range(len(security_data))[len(security_data)-slowperiod:])
        MA1 = map(lambda x: mean(x), m1)
        MA2 = map(lambda x: mean(x), m2)
        DMA = array(MA1) - array(MA2)
        dma[security] = DMA
    return dma

# AMA
def AMA(security_list,fastperiod=5,slowperiod=60,amaperiod=20):
    # 修复传入为单只股票的情况
    if isinstance(security_list, str):
        security_list = [security_list]
    # 计算 DMA
    ama = {}
    for security in security_list:
        security_data = attribute_history(security, slowperiod*2, '1d', ['close'], skip_paused=True, df=False)['close']
        m1 = map(lambda i: security_data[i-fastperiod+1:i+1],range(len(security_data))[len(security_data)-slowperiod:])
        m2 = map(lambda i: security_data[i-slowperiod+1:i+1],range(len(security_data))[len(security_data)-slowperiod:])
        MA1 = map(lambda x: mean(x), m1)
        MA2 = map(lambda x: mean(x), m2)
        DMA = array(MA1) - array(MA2)
        # 计算 AMA
        a1 = map(lambda i: DMA[i-amaperiod+1:i+1],range(len(DMA))[-2:])
        AMA = map(lambda x: mean(x), a1)
        ama[security] = AMA
    return ama