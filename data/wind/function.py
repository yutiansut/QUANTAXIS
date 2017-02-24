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



    data=w.wsd("IC1508.CFE", "lasttrade_date,lastdelivery_date,dlmonth,lprice,sccode,margin,changelt,punit,mfprice,contractmultiplier,cdmonths,thours,ltdated,ftmargins,trade_hiscode", "2017-01-25", "2017-01-26", "Fill=Previous")
print data.Data