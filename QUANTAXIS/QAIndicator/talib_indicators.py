# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import pandas as pd
try:
    import talib
except:
    pass
    #print('PLEASE install TALIB to call these methods')


def AD(DataFrame):
    res = talib.AD(DataFrame.high.values, DataFrame.low.values,
                   DataFrame.close.values, DataFrame.volume.values)
    return pd.DataFrame({'AD': res}, index=DataFrame.index)


def ADOSC(DataFrame, N1=3, N2=10):
    res = talib.ADOSC(DataFrame.high.values, DataFrame.low.values,
                      DataFrame.close.values, DataFrame.volume.values, N1, N2)
    return pd.DataFrame({'ADOSC': res}, index=DataFrame.index)


def ADX(DataFrame, N=14):
    res = talib.ADX(DataFrame.high.values, DataFrame.low.values, DataFrame.close.values, N)
    return pd.DataFrame({'ADX': res}, index=DataFrame.index)


def ADXR(DataFrame, N=14):
    res = talib.ADXR(DataFrame.high.values, DataFrame.low.values, DataFrame.close.values, N)
    return pd.DataFrame({'ADXR': res}, index=DataFrame.index)


def AROON(DataFrame, N=14):
    """阿隆指标
    
    Arguments:
        DataFrame {[type]} -- [description]
    
    Keyword Arguments:
        N {int} -- [description] (default: {14})
    
    Returns:
        [type] -- [description]
    """

    ar_up, ar_down = talib.AROON(DataFrame.high.values, DataFrame.low.values, N)
    return pd.DataFrame({'AROON_UP': ar_up,'AROON_DOWN': ar_down}, index=DataFrame.index)

def AROONOSC(DataFrame, N=14):
    res = talib.AROONOSC(DataFrame.high.values, DataFrame.low.values, N)
    return pd.DataFrame({'AROONOSC': res}, index=DataFrame.index)


def ATR(DataFrame, N=14):
    res = talib.ATR(DataFrame.high.values, DataFrame.low.values, DataFrame.close.values, N)
    return pd.DataFrame({'ATR': res}, index=DataFrame.index)


def AVGPRICE(DataFrame):
    res = talib.AVGPRICE(DataFrame.open.values, DataFrame.high.values,
                         DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'AVGPRICE': res}, index=DataFrame.index)


def BOP(DataFrame):
    res = talib.BOP(DataFrame.open.values, DataFrame.high.values,
                    DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'BOP': res}, index=DataFrame.index)


def CCI(DataFrame, N=14):
    res = talib.CCI(DataFrame.high.values, DataFrame.low.values, DataFrame.close.values, N)
    return pd.DataFrame({'CCI': res}, index=DataFrame.index)


def CDL2CROWS(DataFrame):
    res = talib.CDL2CROWS(DataFrame.open.values, DataFrame.high.values,
                          DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDL2CROWS': res}, index=DataFrame.index)


def CDL3BLACKCROWS(DataFrame):
    res = talib.CDL3BLACKCROWS(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDL3BLACKCROWS': res}, index=DataFrame.index)


def CDL3INSIDE(DataFrame):
    res = talib.CDL3INSIDE(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDL3INSIDE': res}, index=DataFrame.index)


def CDL3LINESTRIKE(DataFrame):
    res = talib.CDL3LINESTRIKE(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDL3LINESTRIKE': res}, index=DataFrame.index)


def CDL3OUTSIDE(DataFrame):
    res = talib.CDL3OUTSIDE(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDL3OUTSIDE': res}, index=DataFrame.index)


def CDL3STARSINSOUTH(DataFrame):
    res = talib.CDL3STARSINSOUTH(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDL3STARSINSOUTH': res}, index=DataFrame.index)


def CDL3WHITESOLDIERS(DataFrame):
    res = talib.CDL3WHITESOLDIERS(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDL3WHITESOLDIERS': res}, index=DataFrame.index)


def CDLABANDONEDBABY(DataFrame):
    res = talib.CDLABANDONEDBABY(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLABANDONEDBABY': res}, index=DataFrame.index)


def CDLADVANCEBLOCK(DataFrame):
    res = talib.CDLADVANCEBLOCK(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLADVANCEBLOCK': res}, index=DataFrame.index)


def CDLBELTHOLD(DataFrame):
    res = talib.CDLBELTHOLD(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLBELTHOLD': res}, index=DataFrame.index)


def CDLBREAKAWAY(DataFrame):
    res = talib.CDLBREAKAWAY(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLBREAKAWAY': res}, index=DataFrame.index)


def CDLCLOSINGMARUBOZU(DataFrame):
    """
    Closing Marubozu (Pattern Recognition)

    Arguments:
        DataFrame {[type]} -- [description]
    """

    res = talib.CDLCLOSINGMARUBOZU(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLCLOSINGMARUBOZU': res}, index=DataFrame.index)


def CDLCONCEALBABYSWALL(DataFrame):
    res = talib.CDLCONCEALBABYSWALL(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLCONCEALBABYSWALL': res}, index=DataFrame.index)


def CDLCOUNTERATTACK(DataFrame):
    res = talib.CDLCOUNTERATTACK(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLCOUNTERATTACK': res}, index=DataFrame.index)


def CDLDARKCLOUDCOVER(DataFrame):
    res = talib.CDLDARKCLOUDCOVER(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLDARKCLOUDCOVER': res}, index=DataFrame.index)


def CDLDOJI(DataFrame):
    res = talib.CDLDOJI(DataFrame.open.values, DataFrame.high.values,
                        DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLDOJI': res}, index=DataFrame.index)


def CDLDOJISTAR(DataFrame):
    res = talib.CDLDOJISTAR(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLDOJISTAR': res}, index=DataFrame.index)


def CDLDRAGONFLYDOJI(DataFrame):
    res = talib.CDLDRAGONFLYDOJI(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLDRAGONFLYDOJI': res}, index=DataFrame.index)


def CDLENGULFING(DataFrame):
    res = talib.CDLENGULFING(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLENGULFING': res}, index=DataFrame.index)


def CDLEVENINGDOJISTAR(DataFrame):
    res = talib.CDLEVENINGDOJISTAR(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLEVENINGDOJISTAR': res}, index=DataFrame.index)


def CDLEVENINGSTAR(DataFrame):
    res = talib.CDLEVENINGSTAR(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLEVENINGSTAR': res}, index=DataFrame.index)


def CDLGAPSIDESIDEWHITE(DataFrame):
    res = talib.CDLGAPSIDESIDEWHITE(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLGAPSIDESIDEWHITE': res}, index=DataFrame.index)


def CDLGRAVESTONEDOJI(DataFrame):
    res = talib.CDLGRAVESTONEDOJI(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLGRAVESTONEDOJI': res}, index=DataFrame.index)


def CDLHAMMER(DataFrame):
    res = talib.CDLHAMMER(DataFrame.open.values, DataFrame.high.values,
                          DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHAMMER': res}, index=DataFrame.index)


def CDLHANGINGMAN(DataFrame):
    res = talib.CDLHANGINGMAN(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHANGINGMAN': res}, index=DataFrame.index)


def CDLHARAMI(DataFrame):
    res = talib.CDLHARAMI(DataFrame.open.values, DataFrame.high.values,
                          DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHARAMI': res}, index=DataFrame.index)


def CDLHARAMICROSS(DataFrame):
    res = talib.CDLHARAMICROSS(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHARAMICROSS': res}, index=DataFrame.index)


def CDLHIGHWAVE(DataFrame):
    res = talib.CDLHIGHWAVE(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHIGHWAVE': res}, index=DataFrame.index)


def CDLHIKKAKE(DataFrame):
    res = talib.CDLHIKKAKE(DataFrame.open.values, DataFrame.high.values,
                           DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHIKKAKE': res}, index=DataFrame.index)


def CDLHIKKAKEMOD(DataFrame):
    res = talib.CDLHIKKAKEMOD(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHIKKAKEMOD': res}, index=DataFrame.index)


def CDLHOMINGPIGEON(DataFrame):
    res = talib.CDLHOMINGPIGEON(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLHOMINGPIGEON': res}, index=DataFrame.index)


def CDLIDENTICAL3CROWS(DataFrame):
    res = talib.CDLIDENTICAL3CROWS(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLIDENTICAL3CROWS': res}, index=DataFrame.index)


def CDLINNECK(DataFrame):
    res = talib.CDLINNECK(DataFrame.open.values, DataFrame.high.values,
                          DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLINNECK': res}, index=DataFrame.index)


def CDLINVERTEDHAMMER(DataFrame):
    res = talib.CDLINVERTEDHAMMER(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLINVERTEDHAMMER': res}, index=DataFrame.index)


def CDLKICKING(DataFrame):
    res = talib.CDLKICKING(DataFrame.open.values, DataFrame.high.values,
                           DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLKICKING': res}, index=DataFrame.index)


def CDLKICKINGBYLENGTH(DataFrame):
    res = talib.CDLKICKINGBYLENGTH(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLKICKINGBYLENGTH': res}, index=DataFrame.index)


def CDLLADDERBOTTOM(DataFrame):
    res = talib.CDLLADDERBOTTOM(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLLADDERBOTTOM': res}, index=DataFrame.index)


def CDLLONGLEGGEDDOJI(DataFrame):
    res = talib.CDLLONGLEGGEDDOJI(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLLONGLEGGEDDOJI': res}, index=DataFrame.index)


def CDLLONGLINE(DataFrame):
    res = talib.CDLLONGLINE(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLLONGLINE': res}, index=DataFrame.index)


def CDLMARUBOZU(DataFrame):
    res = talib.CDLMARUBOZU(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLMARUBOZU': res}, index=DataFrame.index)


def CDLMATCHINGLOW(DataFrame):
    res = talib.CDLMATCHINGLOW(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLMATCHINGLOW': res}, index=DataFrame.index)


def CDLMATHOLD(DataFrame):
    res = talib.CDLMATHOLD(DataFrame.open.values, DataFrame.high.values,
                           DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLMATHOLD': res}, index=DataFrame.index)


def CDLMORNINGDOJISTAR(DataFrame):
    res = talib.CDLMORNINGDOJISTAR(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLMORNINGDOJISTAR': res}, index=DataFrame.index)


def CDLMORNINGSTAR(DataFrame):
    res = talib.CDLMORNINGSTAR(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLMORNINGSTAR': res}, index=DataFrame.index)


def CDLONNECK(DataFrame):
    res = talib.CDLONNECK(DataFrame.open.values, DataFrame.high.values,
                          DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLONNECK': res}, index=DataFrame.index)


def CDLPIERCING(DataFrame):
    res = talib.CDLPIERCING(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLPIERCING': res}, index=DataFrame.index)


def CDLRICKSHAWMAN(DataFrame):
    res = talib.CDLRICKSHAWMAN(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLRICKSHAWMAN': res}, index=DataFrame.index)


def CDLRISEFALL3METHODS(DataFrame):
    res = talib.CDLRISEFALL3METHODS(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLRISEFALL3METHODS': res}, index=DataFrame.index)


def CDLSEPARATINGLINES(DataFrame):
    res = talib.CDLSEPARATINGLINES(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLSEPARATINGLINES': res}, index=DataFrame.index)


def CDLSHOOTINGSTAR(DataFrame):
    res = talib.CDLSHOOTINGSTAR(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLSHOOTINGSTAR': res}, index=DataFrame.index)


def CDLSHORTLINE(DataFrame):
    res = talib.CDLSHORTLINE(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLSHORTLINE': res}, index=DataFrame.index)


def CDLSPINNINGTOP(DataFrame):
    res = talib.CDLSPINNINGTOP(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLSPINNINGTOP': res}, index=DataFrame.index)


def CDLSTALLEDPATTERN(DataFrame):
    res = talib.CDLSTALLEDPATTERN(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLSTALLEDPATTERN': res}, index=DataFrame.index)


def CDLSTICKSANDWICH(DataFrame):
    res = talib.CDLSTICKSANDWICH(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLSTICKSANDWICH': res}, index=DataFrame.index)


def CDLTAKURI(DataFrame):
    res = talib.CDLTAKURI(DataFrame.open.values, DataFrame.high.values,
                          DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLTAKURI': res}, index=DataFrame.index)


def CDLTASUKIGAP(DataFrame):
    res = talib.CDLTASUKIGAP(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLTASUKIGAP': res}, index=DataFrame.index)


def CDLTHRUSTING(DataFrame):
    res = talib.CDLTHRUSTING(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLTHRUSTING': res}, index=DataFrame.index)


def CDLTRISTAR(DataFrame):
    res = talib.CDLTRISTAR(DataFrame.open.values, DataFrame.high.values,
                           DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLTRISTAR': res}, index=DataFrame.index)


def CDLUNIQUE3RIVER(DataFrame):
    res = talib.CDLUNIQUE3RIVER(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLUNIQUE3RIVER': res}, index=DataFrame.index)


def CDLUPSIDEGAP2CROWS(DataFrame):
    res = talib.CDLUPSIDEGAP2CROWS(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLUPSIDEGAP2CROWS': res}, index=DataFrame.index)


def CDLXSIDEGAP3METHODS(DataFrame):
    res = talib.CDLXSIDEGAP3METHODS(
        DataFrame.open.values, DataFrame.high.values, DataFrame.low.values, DataFrame.close.values)
    return pd.DataFrame({'CDLXSIDEGAP3METHODS': res}, index=DataFrame.index)


def DX(DataFrame, N=14):
    res = talib.DX(DataFrame.high.values, DataFrame.low.values, DataFrame.close.values, N)
    return pd.DataFrame({'DX': res}, index=DataFrame.index)


# SAR - Parabolic SAR
def SAR(DataFrame, acceleration=0, maximum=0):
    res = talib.SAR(DataFrame.high.values, DataFrame.low.values, acceleration, maximum)
    return pd.DataFrame({'SAR': res}, index=DataFrame.index)


def SAREXT(DataFrame, startvalue=0, offsetonreverse=0, accelerationinitlong=0,
           accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0):
    res = talib.SAREXT(DataFrame.high.values, DataFrame.low.values,
                       startvalue, offsetonreverse, accelerationinitlong, accelerationlong, accelerationmaxlong,
                       accelerationinitshort, accelerationshort, accelerationmaxshort)
    return pd.DataFrame({'SAREXT': res}, index=DataFrame.index)


def STOCH(DataFrame, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0):
    slowk, slowd = talib.STOCH(DataFrame.high.values, DataFrame.low.values, DataFrame.close.values,
                               fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype)
    return pd.DataFrame({'STOCH_SLOWK': slowk, 'STOCH_SLOWD': slowd}, index=DataFrame.index)


def STOCHF(DataFrame, fastk_period=5, fastd_period=3, fastd_matype=0):
    fastk, fastd = talib.STOCHF(DataFrame.high.values, DataFrame.low.values, DataFrame.close.values,
                               fastk_period, fastd_period, fastd_matype)
    return pd.DataFrame({'STOCHF_FASTK': fastk, 'STOCHF_FASTD': fastd}, index=DataFrame.index)
