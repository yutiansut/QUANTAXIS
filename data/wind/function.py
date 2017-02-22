import talib

def MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    参数设置:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    返回: macd - signal
    '''
    macd, signal, hist = talib.MACD(prices, 
                                    fastperiod=fastperiod, 
                                    slowperiod=slowperiod, 
                                    signalperiod=signalperiod)
    return macd[-1] - signal[-1]