# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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
    print('请安装TALIB后再调用此函数')


def AD(data):
    res = talib.AD(data.high.values, data.low.values,
                   data.close.values, data.volume.values)
    return pd.DataFrame({'AD': res}, index=data.index)


def ADOSC(data, N1=3, N2=10):
    res = talib.ADOSC(data.high.values, data.low.values,
                      data.close.values, data.volume.values, N1, N2)
    return pd.DataFrame({'ADOSC': res}, index=data.index)


def ADX(data, N=14):
    res = talib.ADX(data.high.values, data.low.values, data.close.values, N)
    return pd.DataFrame({'ADX': res}, index=data.index)


def ADXR(data, N=14):
    res = talib.ADXR(data.high.values, data.low.values, data.close.values, N)
    return pd.DataFrame({'ADXR': res}, index=data.index)


def AROON(data, N=14):
    res = talib.AROON(data.high.values, data.low.values, N)
    return pd.DataFrame({'AROON': res}, index=data.index)


def AROONOSC(data, N=14):
    res = talib.AROONOSC(data.high.values, data.low.values, N)
    return pd.DataFrame({'AROONOSC': res}, index=data.index)


def ATR(data, N=14):
    res = talib.ATR(data.high.values, data.low.values, data.close.values, N)
    return pd.DataFrame({'ATR': res}, index=data.index)


def AVGPRICE(data):
    res = talib.AVGPRICE(data.open.values, data.high.values,
                         data.low.values, data.close.values)
    return pd.DataFrame({'AVGPRICE': res}, index=data.index)


def BOP(data):
    res = talib.BOP(data.open.values, data.high.values,
                    data.low.values, data.close.values)
    return pd.DataFrame({'BOP': res}, index=data.index)


def CCI(data, N=14):
    res = talib.CCI(data.high.values, data.low.values, data.close.values, N)
    return pd.DataFrame({'CCI': res}, index=data.index)


def CDL2CROWS(data):
    res = talib.CDL2CROWS(data.open.values, data.high.values,
                          data.low.values, data.close.values)
    return pd.DataFrame({'CDL2CROWS': res}, index=data.index)


def CDL3BLACKCROWS(data):
    res = talib.CDL3BLACKCROWS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3BLACKCROWS': res}, index=data.index)


def CDL3INSIDE(data):
    res = talib.CDL3INSIDE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3INSIDE': res}, index=data.index)


def CDL3LINESTRIKE(data):
    res = talib.CDL3LINESTRIKE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3LINESTRIKE': res}, index=data.index)


def CDL3OUTSIDE(data):
    res = talib.CDL3OUTSIDE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3OUTSIDE': res}, index=data.index)


def CDL3STARSINSOUTH(data):
    res = talib.CDL3STARSINSOUTH(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3STARSINSOUTH': res}, index=data.index)


def CDL3WHITESOLDIERS(data):
    res = talib.CDL3WHITESOLDIERS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDL3WHITESOLDIERS': res}, index=data.index)


def CDLABANDONEDBABY(data):
    res = talib.CDLABANDONEDBABY(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLABANDONEDBABY': res}, index=data.index)


def CDLADVANCEBLOCK(data):
    res = talib.CDLADVANCEBLOCK(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLADVANCEBLOCK': res}, index=data.index)


def CDLBELTHOLD(data):
    res = talib.CDLBELTHOLD(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLBELTHOLD': res}, index=data.index)


def CDLBREAKAWAY(data):
    res = talib.CDLBREAKAWAY(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLBREAKAWAY': res}, index=data.index)


def CDLCLOSINGMARUBOZU(data):
    """
    Closing Marubozu (Pattern Recognition)

    Arguments:
        data {[type]} -- [description]
    """

    res = talib.CDLCLOSINGMARUBOZU(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLCLOSINGMARUBOZU': res}, index=data.index)


def CDLCONCEALBABYSWALL(data):
    res = talib.CDLCONCEALBABYSWALL(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLCONCEALBABYSWALL': res}, index=data.index)


def CDLCOUNTERATTACK(data):
    res = talib.CDLCOUNTERATTACK(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLCOUNTERATTACK': res}, index=data.index)


def CDLDARKCLOUDCOVER(data):
    res = talib.CDLDARKCLOUDCOVER(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLDARKCLOUDCOVER': res}, index=data.index)


def CDLDOJI(data):
    res = talib.CDLDOJI(data.open.values, data.high.values,
                        data.low.values, data.close.values)
    return pd.DataFrame({'CDLDOJI': res}, index=data.index)


def CDLDOJISTAR(data):
    res = talib.CDLDOJISTAR(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLDOJISTAR': res}, index=data.index)


def CDLDRAGONFLYDOJI(data):
    res = talib.CDLDRAGONFLYDOJI(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLDRAGONFLYDOJI': res}, index=data.index)


def CDLENGULFING(data):
    res = talib.CDLENGULFING(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLENGULFING': res}, index=data.index)


def CDLEVENINGDOJISTAR(data):
    res = talib.CDLEVENINGDOJISTAR(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLEVENINGDOJISTAR': res}, index=data.index)


def CDLEVENINGSTAR(data):
    res = talib.CDLEVENINGSTAR(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLEVENINGSTAR': res}, index=data.index)


def CDLGAPSIDESIDEWHITE(data):
    res = talib.CDLGAPSIDESIDEWHITE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLGAPSIDESIDEWHITE': res}, index=data.index)


def CDLGRAVESTONEDOJI(data):
    res = talib.CDLGRAVESTONEDOJI(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLGRAVESTONEDOJI': res}, index=data.index)


def CDLHAMMER(data):
    res = talib.CDLHAMMER(data.open.values, data.high.values,
                          data.low.values, data.close.values)
    return pd.DataFrame({'CDLHAMMER': res}, index=data.index)


def CDLHANGINGMAN(data):
    res = talib.CDLHANGINGMAN(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLHANGINGMAN': res}, index=data.index)


def CDLHARAMI(data):
    res = talib.CDLHARAMI(data.open.values, data.high.values,
                          data.low.values, data.close.values)
    return pd.DataFrame({'CDLHARAMI': res}, index=data.index)


def CDLHARAMICROSS(data):
    res = talib.CDLHARAMICROSS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLHARAMICROSS': res}, index=data.index)


def CDLHIGHWAVE(data):
    res = talib.CDLHIGHWAVE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLHIGHWAVE': res}, index=data.index)


def CDLHIKKAKE(data):
    res = talib.CDLHIKKAKE(data.open.values, data.high.values,
                           data.low.values, data.close.values)
    return pd.DataFrame({'CDLHIKKAKE': res}, index=data.index)


def CDLHIKKAKEMOD(data):
    res = talib.CDLHIKKAKEMOD(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLHIKKAKEMOD': res}, index=data.index)


def CDLHOMINGPIGEON(data):
    res = talib.CDLHOMINGPIGEON(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLHOMINGPIGEON': res}, index=data.index)


def CDLIDENTICAL3CROWS(data):
    res = talib.CDLIDENTICAL3CROWS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLIDENTICAL3CROWS': res}, index=data.index)


def CDLINNECK(data):
    res = talib.CDLINNECK(data.open.values, data.high.values,
                          data.low.values, data.close.values)
    return pd.DataFrame({'CDLINNECK': res}, index=data.index)


def CDLINVERTEDHAMMER(data):
    res = talib.CDLINVERTEDHAMMER(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLINVERTEDHAMMER': res}, index=data.index)


def CDLKICKING(data):
    res = talib.CDLKICKING(data.open.values, data.high.values,
                           data.low.values, data.close.values)
    return pd.DataFrame({'CDLKICKING': res}, index=data.index)


def CDLKICKINGBYLENGTH(data):
    res = talib.CDLKICKINGBYLENGTH(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLKICKINGBYLENGTH': res}, index=data.index)


def CDLLADDERBOTTOM(data):
    res = talib.CDLLADDERBOTTOM(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLLADDERBOTTOM': res}, index=data.index)


def CDLLONGLEGGEDDOJI(data):
    res = talib.CDLLONGLEGGEDDOJI(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLLONGLEGGEDDOJI': res}, index=data.index)


def CDLLONGLINE(data):
    res = talib.CDLLONGLINE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLLONGLINE': res}, index=data.index)


def CDLMARUBOZU(data):
    res = talib.CDLMARUBOZU(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLMARUBOZU': res}, index=data.index)


def CDLMATCHINGLOW(data):
    res = talib.CDLMATCHINGLOW(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLMATCHINGLOW': res}, index=data.index)


def CDLMATHOLD(data):
    res = talib.CDLMATHOLD(data.open.values, data.high.values,
                           data.low.values, data.close.values)
    return pd.DataFrame({'CDLMATHOLD': res}, index=data.index)


def CDLMORNINGDOJISTAR(data):
    res = talib.CDLMORNINGDOJISTAR(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLMORNINGDOJISTAR': res}, index=data.index)


def CDLMORNINGSTAR(data):
    res = talib.CDLMORNINGSTAR(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLMORNINGSTAR': res}, index=data.index)


def CDLONNECK(data):
    res = talib.CDLONNECK(data.open.values, data.high.values,
                          data.low.values, data.close.values)
    return pd.DataFrame({'CDLONNECK': res}, index=data.index)


def CDLPIERCING(data):
    res = talib.CDLPIERCING(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLPIERCING': res}, index=data.index)


def CDLRICKSHAWMAN(data):
    res = talib.CDLRICKSHAWMAN(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLRICKSHAWMAN': res}, index=data.index)


def CDLRISEFALL3METHODS(data):
    res = talib.CDLRISEFALL3METHODS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLRISEFALL3METHODS': res}, index=data.index)


def CDLSEPARATINGLINES(data):
    res = talib.CDLSEPARATINGLINES(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLSEPARATINGLINES': res}, index=data.index)


def CDLSHOOTINGSTAR(data):
    res = talib.CDLSHOOTINGSTAR(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLSHOOTINGSTAR': res}, index=data.index)


def CDLSHORTLINE(data):
    res = talib.CDLSHORTLINE(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLSHORTLINE': res}, index=data.index)


def CDLSPINNINGTOP(data):
    res = talib.CDLSPINNINGTOP(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLSPINNINGTOP': res}, index=data.index)


def CDLSTALLEDPATTERN(data):
    res = talib.CDLSTALLEDPATTERN(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLSTALLEDPATTERN': res}, index=data.index)


def CDLSTICKSANDWICH(data):
    res = talib.CDLSTICKSANDWICH(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLSTICKSANDWICH': res}, index=data.index)


def CDLTAKURI(data):
    res = talib.CDLTAKURI(data.open.values, data.high.values,
                          data.low.values, data.close.values)
    return pd.DataFrame({'CDLTAKURI': res}, index=data.index)


def CDLTASUKIGAP(data):
    res = talib.CDLTASUKIGAP(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLTASUKIGAP': res}, index=data.index)


def CDLTHRUSTING(data):
    res = talib.CDLTHRUSTING(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLTHRUSTING': res}, index=data.index)


def CDLTRISTAR(data):
    res = talib.CDLTRISTAR(data.open.values, data.high.values,
                           data.low.values, data.close.values)
    return pd.DataFrame({'CDLTRISTAR': res}, index=data.index)


def CDLUNIQUE3RIVER(data):
    res = talib.CDLUNIQUE3RIVER(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLUNIQUE3RIVER': res}, index=data.index)


def CDLUPSIDEGAP2CROWS(data):
    res = talib.CDLUPSIDEGAP2CROWS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLUPSIDEGAP2CROWS': res}, index=data.index)


def CDLXSIDEGAP3METHODS(data):
    res = talib.CDLXSIDEGAP3METHODS(
        data.open.values, data.high.values, data.low.values, data.close.values)
    return pd.DataFrame({'CDLXSIDEGAP3METHODS': res}, index=data.index)


def DX(data, N=14):
    res = talib.DX(data.high.values, data.low.values, data.close.values, N)
    return pd.DataFrame({'DX': res}, index=data.index)
