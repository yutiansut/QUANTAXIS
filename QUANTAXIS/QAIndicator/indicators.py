# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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

from functools import reduce

import numpy as np
import pandas as pd

from QUANTAXIS.QAIndicator.base import *


"""
DataFrame 类

以下的函数都可以被直接add_func


"""


"""
1.	趋向指标 
又叫趋势跟踪类指标,主要用于跟踪并预测股价的发展趋势

包含的主要指标
1. 移动平均线 MA
2. 指数平滑移动平均线 MACD
3. 趋向指标 DMI
4. 瀑布线 PBX
5. 平均线差 DMA
6. 动力指标(动量线)  MTM
7. 指数平均线 EXPMA
8. 佳庆指标 CHO
"""


def QA_indicator_MA(DataFrame,*args,**kwargs):
    """MA
    
    Arguments:
        DataFrame {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    CLOSE = DataFrame['close']
    return pd.DataFrame({'MA{}'.format(N): MA(CLOSE, N)  for N in list(args)})


def QA_indicator_EMA(DataFrame, N):
    CLOSE = DataFrame['close']
    return pd.DataFrame({'EMA': EMA(CLOSE, N)})


def QA_indicator_SMA(DataFrame, N):
    CLOSE = DataFrame['close']
    return pd.DataFrame({'SMA': SMA(CLOSE, N)})


def QA_indicator_MACD(DataFrame, short=12, long=26, mid=9):
    """
    MACD CALC
    """
    CLOSE = DataFrame['close']

    DIF = EMA(CLOSE, short)-EMA(CLOSE, long)
    DEA = EMA(DIF, mid)
    MACD = (DIF-DEA)*2

    return pd.DataFrame({'DIF': DIF, 'DEA': DEA, 'MACD': MACD})


def QA_indicator_DMI(DataFrame, M1=14, M2=6):
    """
    趋向指标 DMI
    """
    HIGH = DataFrame.high
    LOW = DataFrame.low
    CLOSE = DataFrame.close
    OPEN = DataFrame.open

    TR = SUM(MAX(MAX(HIGH-LOW, ABS(HIGH-REF(CLOSE, 1))),
                 ABS(LOW-REF(CLOSE, 1))), M1)
    HD = HIGH-REF(HIGH, 1)
    LD = REF(LOW, 1)-LOW
    DMP = SUM(IFAND(HD>0,HD>LD,HD,0), M1)
    DMM = SUM(IFAND(LD>0,LD>HD,LD,0), M1)
    DI1 = DMP*100/TR
    DI2 = DMM*100/TR
    ADX = MA(ABS(DI2-DI1)/(DI1+DI2)*100, M2)
    ADXR = (ADX+REF(ADX, M2))/2

    return pd.DataFrame({
        'DI1': DI1, 'DI2': DI2,
        'ADX': ADX, 'ADXR': ADXR
    })


def QA_indicator_PBX(DataFrame, N1=3, N2=5, N3=8, N4=13, N5=18, N6=24):
    '瀑布线'
    C = DataFrame['close']
    PBX1 = (EMA(C, N1) + EMA(C, 2 * N1) + EMA(C, 4 * N1)) / 3
    PBX2 = (EMA(C, N2) + EMA(C, 2 * N2) + EMA(C, 4 * N2)) / 3
    PBX3 = (EMA(C, N3) + EMA(C, 2 * N3) + EMA(C, 4 * N3)) / 3
    PBX4 = (EMA(C, N4) + EMA(C, 2 * N4) + EMA(C, 4 * N4)) / 3
    PBX5 = (EMA(C, N5) + EMA(C, 2 * N5) + EMA(C, 4 * N5)) / 3
    PBX6 = (EMA(C, N6) + EMA(C, 2 * N6) + EMA(C, 4 * N6)) / 3
    DICT = {'PBX1': PBX1, 'PBX2': PBX2, 'PBX3': PBX3,
            'PBX4': PBX4, 'PBX5': PBX5, 'PBX6': PBX6}

    return pd.DataFrame(DICT)


def QA_indicator_DMA(DataFrame, M1=10, M2=50, M3=10):
    """
    平均线差 DMA
    """
    CLOSE = DataFrame.close
    DDD = MA(CLOSE, M1) - MA(CLOSE, M2)
    AMA = MA(DDD, M3)
    return pd.DataFrame({
        'DDD': DDD, 'AMA': AMA
    })


def QA_indicator_MTM(DataFrame, N=12, M=6):
    '动量线'
    C = DataFrame.close
    mtm = C - REF(C, N)
    MTMMA = MA(mtm, M)
    DICT = {'MTM': mtm, 'MTMMA': MTMMA}

    return pd.DataFrame(DICT)


def QA_indicator_EXPMA(DataFrame, P1=5, P2=10, P3=20, P4=60):
    """ 指数平均线 EXPMA"""
    CLOSE = DataFrame.close
    MA1 = EMA(CLOSE, P1)
    MA2 = EMA(CLOSE, P2)
    MA3 = EMA(CLOSE, P3)
    MA4 = EMA(CLOSE, P4)
    return pd.DataFrame({
        'MA1': MA1, 'MA2': MA2, 'MA3': MA3, 'MA4': MA4
    })


def QA_indicator_CHO(DataFrame, N1=10, N2=20, M=6):
    """
    佳庆指标 CHO
    """
    HIGH = DataFrame.high
    LOW = DataFrame.low
    CLOSE = DataFrame.close
    VOL = DataFrame.volume
    MID = SUM(VOL*(2*CLOSE-HIGH-LOW)/(HIGH+LOW), 0)
    CHO = MA(MID, N1)-MA(MID, N2)
    MACHO = MA(CHO, M)
    return pd.DataFrame({
        'CHO': CHO, 'MACHO': MACHO
    })


"""

2.	反趋向指标
主要捕捉趋势的转折点

随机指标KDJ
乖离率 BIAS
变动速率 ROC
顺势指标 CCI
威廉指标 W&R
震荡量(变动速率) OSC
相对强弱指标 RSI
动态买卖指标 ADTM

"""


def QA_indicator_KDJ(DataFrame, N=9, M1=3, M2=3):
    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']

    RSV = (C - LLV(L, N)) / (HHV(H, N) - LLV(L, N)) * 100
    K = SMA(RSV, M1)
    D = SMA(K, M2)
    J = 3 * K - 2 * D
    DICT = {'KDJ_K': K, 'KDJ_D': D, 'KDJ_J': J}
    return pd.DataFrame(DICT)


def QA_indicator_BIAS(DataFrame, N1, N2, N3):
    '乖离率'
    CLOSE = DataFrame['close']
    BIAS1 = (CLOSE - MA(CLOSE, N1)) / MA(CLOSE, N1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, N2)) / MA(CLOSE, N2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, N3)) / MA(CLOSE, N3) * 100
    DICT = {'BIAS1': BIAS1, 'BIAS2': BIAS2, 'BIAS3': BIAS3}

    return pd.DataFrame(DICT)


def QA_indicator_ROC(DataFrame, N=12, M=6):
    '变动率指标'
    C = DataFrame['close']
    roc = 100 * (C - REF(C, N)) / REF(C, N)
    ROCMA = MA(roc, M)
    DICT = {'ROC': roc, 'ROCMA': ROCMA}

    return pd.DataFrame(DICT)


def QA_indicator_CCI(DataFrame, N=14):
    """
    TYP:=(HIGH+LOW+CLOSE)/3;
    CCI:(TYP-MA(TYP,N))/(0.015*AVEDEV(TYP,N));
    """
    typ = (DataFrame['high'] + DataFrame['low'] + DataFrame['close']) / 3
    cci = ((typ - MA(typ, N)) / (0.015 * AVEDEV(typ, N)))
    a = 100
    b = -100

    return pd.DataFrame({
        'CCI': cci, 'a': a, 'b': b
    })


def QA_indicator_WR(DataFrame, N, N1):
    '威廉指标'
    HIGH = DataFrame['high']
    LOW = DataFrame['low']
    CLOSE = DataFrame['close']
    WR1 = 100 * (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N))
    WR2 = 100 * (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1))
    DICT = {'WR1': WR1, 'WR2': WR2}

    return pd.DataFrame(DICT)


def QA_indicator_OSC(DataFrame, N=20, M=6):
    """变动速率线

    震荡量指标OSC，也叫变动速率线。属于超买超卖类指标,是从移动平均线原理派生出来的一种分析指标。

    它反应当日收盘价与一段时间内平均收盘价的差离值,从而测出股价的震荡幅度。

    按照移动平均线原理，根据OSC的值可推断价格的趋势，如果远离平均线，就很可能向平均线回归。
    """
    C = DataFrame['close']
    OS = (C - MA(C, N)) * 100
    MAOSC = EMA(OS, M)
    DICT = {'OSC': OS, 'MAOSC': MAOSC}

    return pd.DataFrame(DICT)


def QA_indicator_RSI(DataFrame, N1=12, N2=26, N3=9):
    '相对强弱指标RSI1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100;'
    CLOSE = DataFrame['close']
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1) / SMA(ABS(CLOSE - LC), N1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2) / SMA(ABS(CLOSE - LC), N2) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3) / SMA(ABS(CLOSE - LC), N3) * 100
    DICT = {'RSI1': RSI1, 'RSI2': RSI2, 'RSI3': RSI3}

    return pd.DataFrame(DICT)


def QA_indicator_ADTM(DataFrame, N=23, M=8):
    '动态买卖气指标'
    HIGH = DataFrame.high
    LOW = DataFrame.low
    OPEN = DataFrame.open
    DTM = IF(OPEN > REF(OPEN, 1), MAX((HIGH - OPEN), (OPEN - REF(OPEN, 1))), 0)
    DBM = IF(OPEN < REF(OPEN, 1), MAX((OPEN - LOW), (OPEN - REF(OPEN, 1))), 0)
    STM = SUM(DTM, N)
    SBM = SUM(DBM, N)
    ADTM1 = IF(STM > SBM, (STM - SBM) / STM,
               IF(STM != SBM, (STM - SBM) / SBM, 0))
    MAADTM = MA(ADTM1, M)
    DICT = {'ADTM': ADTM1, 'MAADTM': MAADTM}

    return pd.DataFrame(DICT)


"""
3.	量能指标
通过成交量的大小和变化研判趋势变化
容量指标 VR
量相对强弱 VRSI
能量指标 CR
人气意愿指标 ARBR
成交量标准差 VSTD"""


def QA_indicator_VR(DataFrame, M1=26, M2=100, M3=200):
    VOL = DataFrame.volume
    CLOSE = DataFrame.close
    LC = REF(CLOSE, 1)
    VR = SUM(IF(CLOSE > LC, VOL, 0), M1)/SUM(IF(CLOSE <= LC, VOL, 0), M1)*100
    a = M2
    b = M3
    return pd.DataFrame({
        'VR': VR, 'a': a, 'b': b
    })


def QA_indicator_VRSI(DataFrame, N=6):

    VOL = DataFrame.volume
    vrsi = SMA(MAX(VOL-REF(VOL, 1), 0), N, 1) / \
        SMA(ABS(VOL-REF(VOL, 1)), N, 1)*100

    return pd.DataFrame({'VRSI': vrsi})


def QA_indicator_CR(DataFrame, N=26, M1=5, M2=10, M3=20):
    HIGH = DataFrame.high
    LOW = DataFrame.low
    CLOSE = DataFrame.close
    VOL = DataFrame.volume
    MID = (HIGH+LOW+CLOSE)/3

    CR = SUM(MAX(0, HIGH-REF(MID, 1)), N)/SUM(MAX(0, REF(MID, 1)-LOW), N)*100
    MA1 = REF(MA(CR, M1), M1/2.5+1)
    MA2 = REF(MA(CR, M2), M2/2.5+1)
    MA3 = REF(MA(CR, M3), M3/2.5+1)
    return pd.DataFrame({
        'CR': CR, 'MA1': MA1, 'MA2': MA2, 'MA3': MA3
    })


def QA_indicator_ARBR(DataFrame, M1=26, M2=70, M3=150):
    HIGH = DataFrame.high
    LOW = DataFrame.low
    CLOSE = DataFrame.close
    OPEN = DataFrame.open
    AR = SUM(HIGH-OPEN, M1)/SUM(OPEN-LOW, M1)*100
    BR = SUM(MAX(0, HIGH-REF(CLOSE, 1)), M1) / \
        SUM(MAX(0, REF(CLOSE, 1)-LOW), M1)*100
    a = M2
    b = M3
    return pd.DataFrame({
        'AR': AR, 'BR': BR, 'a': a, 'b': b
    })


def QA_indicator_VSTD(DataFrame, N=10):
    VOL = DataFrame.volume
    vstd = STD(VOL, N)
    return pd.DataFrame({'VSTD': vstd})


"""
4.	量价指标
通过成交量和股价变动关系分析未来趋势
震荡升降指标ASI
价量趋势PVT
能量潮OBV
量价趋势VPT
"""


def QA_indicator_ASI(DataFrame, M1=26, M2=10):
    """
    LC=REF(CLOSE,1);
    AA=ABS(HIGH-LC);
    BB=ABS(LOW-LC);
    CC=ABS(HIGH-REF(LOW,1));
    DD=ABS(LC-REF(OPEN,1));
    R=IF(AA>BB AND AA>CC,AA+BB/2+DD/4,IF(BB>CC AND BB>AA,BB+AA/2+DD/4,CC+DD/4));
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1));
    SI=16*X/R*MAX(AA,BB);
    ASI:SUM(SI,M1);
    ASIT:MA(ASI,M2);
    """
    CLOSE = DataFrame['close']
    HIGH = DataFrame['high']
    LOW = DataFrame['low']
    OPEN = DataFrame['open']
    LC = REF(CLOSE, 1)
    AA = ABS(HIGH - LC)
    BB = ABS(LOW-LC)
    CC = ABS(HIGH - REF(LOW, 1))
    DD = ABS(LC - REF(OPEN, 1))

    R = IFAND(AA > BB, AA > CC, AA+BB/2+DD/4,
           IFAND(BB > CC, BB > AA, BB+AA/2+DD/4, CC+DD/4))
    X = (CLOSE - LC + (CLOSE - OPEN) / 2 + LC - REF(OPEN, 1))
    SI = 16*X/R*MAX(AA, BB)
    ASI = SUM(SI, M1)
    ASIT = MA(ASI, M2)
    return pd.DataFrame({
        'ASI': ASI, 'ASIT': ASIT
    })


def QA_indicator_PVT(DataFrame):
    CLOSE = DataFrame.close
    VOL = DataFrame.volume
    PVT = SUM((CLOSE-REF(CLOSE, 1))/REF(CLOSE, 1)*VOL, 0)
    return pd.DataFrame({'PVT': PVT})


def QA_indicator_OBV(DataFrame):
    """能量潮"""
    VOL = DataFrame.volume
    CLOSE = DataFrame.close
    return pd.DataFrame({
        'OBV': np.cumsum(IF(CLOSE > REF(CLOSE, 1), VOL, IF(CLOSE < REF(CLOSE, 1), -VOL, 0)))/10000
    })


def QA_indicator_VPT(DataFrame, N=51, M=6):
    VOL = DataFrame.volume
    CLOSE = DataFrame.close
    VPT = SUM(VOL*(CLOSE-REF(CLOSE, 1))/REF(CLOSE, 1), 0)
    MAVPT = MA(VPT, M)
    return pd.DataFrame({
        'VPT': VPT, 'MAVPT': MAVPT
    })


"""
5.	压力支撑指标
主要用于分析股价目前收到的压力和支撑
布林带 BOLL
麦克指标 MIKE
"""


def QA_indicator_BOLL(DataFrame, N=20, P=2):
    '布林线'
    C = DataFrame['close']
    boll = MA(C, N)
    UB = boll + P * STD(C, N)
    LB = boll - P * STD(C, N)
    DICT = {'BOLL': boll, 'UB': UB, 'LB': LB}

    return pd.DataFrame(DICT)


def QA_indicator_MIKE(DataFrame, N=12):
    """
    MIKE指标
    指标说明
    MIKE是另外一种形式的路径指标。
    买卖原则
    1  WEAK-S，MEDIUM-S，STRONG-S三条线代表初级、中级、强力支撑。
    2  WEAK-R，MEDIUM-R，STRONG-R三条线代表初级、中级、强力压力。
    """
    HIGH = DataFrame.high
    LOW = DataFrame.low
    CLOSE = DataFrame.close

    TYP = (HIGH+LOW+CLOSE)/3
    LL = LLV(LOW, N)
    HH = HHV(HIGH, N)

    WR = TYP+(TYP-LL)
    MR = TYP+(HH-LL)
    SR = 2*HH-LL
    WS = TYP-(HH-TYP)
    MS = TYP-(HH-LL)
    SS = 2*LL-HH
    return pd.DataFrame({
        'WR': WR, 'MR': MR, 'SR': SR,
        'WS': WS, 'MS': MS, 'SS': SS
    })


def QA_indicator_BBI(DataFrame, N1=3, N2=6, N3=12, N4=24):
    '多空指标'
    C = DataFrame['close']
    bbi = (MA(C, N1) + MA(C, N2) + MA(C, N3) + MA(C, N4)) / 4
    DICT = {'BBI': bbi}

    return pd.DataFrame(DICT)


def QA_indicator_MFI(DataFrame, N=14):
    """
    资金指标
    TYP := (HIGH + LOW + CLOSE)/3;
    V1:=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N);
    MFI:100-(100/(1+V1));
    赋值: (最高价 + 最低价 + 收盘价)/3
    V1赋值:如果TYP>1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和/如果TYP<1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和
    输出资金流量指标:100-(100/(1+V1))
    """
    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']
    VOL = DataFrame['volume']
    TYP = (C + H + L) / 3
    V1 = SUM(IF(TYP > REF(TYP, 1), TYP * VOL, 0), N) / \
        SUM(IF(TYP < REF(TYP, 1), TYP * VOL, 0), N)
    mfi = 100 - (100 / (1 + V1))
    DICT = {'MFI': mfi}

    return pd.DataFrame(DICT)


def QA_indicator_ATR(DataFrame, N=14):
    """
    输出TR:(最高价-最低价)和昨收-最高价的绝对值的较大值和昨收-最低价的绝对值的较大值
    输出真实波幅:TR的N日简单移动平均
    算法：今日振幅、今日最高与昨收差价、今日最低与昨收差价中的最大值，为真实波幅，求真实波幅的N日移动平均

    参数：N　天数，一般取14

    """
    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']
    TR = MAX(MAX((H - L), ABS(REF(C, 1) - H)), ABS(REF(C, 1) - L))
    atr = MA(TR, N)
    return pd.DataFrame({'TR': TR, 'ATR': atr})


def QA_indicator_SKDJ(DataFrame, N=9, M=3):
    """
    1.指标>80 时，回档机率大；指标<20 时，反弹机率大；
    2.K在20左右向上交叉D时，视为买进信号参考； 
    3.K在80左右向下交叉D时，视为卖出信号参考；
    4.SKDJ波动于50左右的任何讯号，其作用不大。

    """
    CLOSE = DataFrame['close']
    LOWV = LLV(DataFrame['low'], N)
    HIGHV = HHV(DataFrame['high'], N)
    RSV = EMA((CLOSE - LOWV) / (HIGHV - LOWV) * 100, M)
    K = EMA(RSV, M)
    D = MA(K, M)
    DICT = {'RSV': RSV, 'SKDJ_K': K, 'SKDJ_D': D}

    return pd.DataFrame(DICT)


def QA_indicator_DDI(DataFrame, N=13, N1=26, M=1, M1=5):
    """
    '方向标准离差指数'
    分析DDI柱状线，由红变绿(正变负)，卖出信号参考；由绿变红，买入信号参考。
    """

    H = DataFrame['high']
    L = DataFrame['low']
    DMZ = IF((H + L) > (REF(H, 1) + REF(L, 1)), 
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))), 0)
    DMF = IF((H + L) < (REF(H, 1) + REF(L, 1)),
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))), 0)
    DIZ = SUM(DMZ, N) / (SUM(DMZ, N) + SUM(DMF, N))
    DIF = SUM(DMF, N) / (SUM(DMF, N) + SUM(DMZ, N))
    ddi = DIZ - DIF
    ADDI = SMA(ddi, N1, M)
    AD = MA(ADDI, M1)
    DICT = {'DDI': ddi, 'ADDI': ADDI, 'AD': AD}

    return pd.DataFrame(DICT)


def QA_indicator_shadow(DataFrame):
    """
    上下影线指标
    """
    return {
        'LOW': lower_shadow(DataFrame), 'UP': upper_shadow(DataFrame),
        'BODY': body(DataFrame), 'BODY_ABS': body_abs(DataFrame), 'PRICE_PCG': price_pcg(DataFrame)
    }


def lower_shadow(DataFrame):  # 下影线
    return abs(DataFrame.low - MIN(DataFrame.open, DataFrame.close))


def upper_shadow(DataFrame):  # 上影线
    return abs(DataFrame.high - MAX(DataFrame.open, DataFrame.close))


def body_abs(DataFrame):
    return abs(DataFrame.open - DataFrame.close)


def body(DataFrame):
    return DataFrame.close - DataFrame.open


def price_pcg(DataFrame):
    return body(DataFrame) / DataFrame.open


def amplitude(DataFrame):
    return (DataFrame.high - DataFrame.low) / DataFrame.low


"""

6.	大盘指标
通过涨跌家数研究大盘指数的走势
涨跌比率 ADR
绝对幅度指标 ABI
新三价率 TBR
腾落指数 ADL
广量冲力指标
指数平滑广量 STIX
"""
