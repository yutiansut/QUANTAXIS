# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
"""
QUANTAXIS  指标计算

分为7类76个指标

- 趋势指标
- 震荡指标
- 成交量指标
- 均价线指标
- 动量指标
- 通道型指标
- 大盘指标
"""


"""趋势类"""
import numpy as np
import pandas as pd
from .formula import SMA

# TODO
# 基于无状态的pd结构的指标


def QA_indicator_dma(data, f=10, s=50, N=10):
    """
    平行线差指标
    中短期指标/趋势指标
    通过计算两条基准周期不同的移动平均线的差值,来判断当前买入卖出能量的大小和未来价格走势的趋势
    """
    _dma = pd.Series(data).rolling(f).mean() - \
        pd.Series(data).rolling(s).mean()
    _ama = pd.Series(_dma).rolling(N).mean()

    return _dma, _ama


def QA_indicator_dmi(data):
    """
    趋向指标
    中长期指标
    用于判断多空力量由于受到价格波动的影响而发生的由均衡到失衡的过程

    """
    pass


def QA_indicator_dpo(data, N=20, M=6):
    """
    区间振荡
    数个短周波的组合，构成一个长周波。观察短周波的运动规律，可以估计长周波峰谷出现的时机。
    例如：
    四个短期循环底部，构成一个长期循环底部。
    因此，DPO指标刻意忽略较长周期的波动，一方面可以减少周期干扰的混淆，一方面可以凸显个别周期的波动。


    一段周期的移动平均线，其周期的二分之一处，是价格重心的聚集点。
    以20天的周期为例，第10天是整段周期的重心平衡点。
    移动平均线的形状，很像一条波浪状扭曲的绳子，股价在这条绳子的周围，上下来回穿梭。
    如果消除扭曲的波动，将这条绳子拉平，重心平衡点视为图表上的0轴。把当日价格与重心平衡点间的差距，绘制于0轴的上下方。
    如此一来，可以更清楚的显现出短周期的高、低点。
    """
    _dpo = pd.Series(data) - pd.Series(data).rolling(N / 2 + 1).mean()
    _madpo = pd.Series(_dpo).rolling(M).mean()
    return _dpo, _madpo


def QA_indicator_jlhb(high, low, close, N=7, M=5):
    """
    绝路航标
    滞后指标,灵敏性很差,容易出假信号
    N:=7;M:=5;
    VAR1:=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80;
    B:SMA(VAR1,N,1);
    VAR2:SMA(B,M,1);
    绝路航标:IF(CROSS(B,VAR2) AND B<40,38,0),COLORYELLOW,LINETHICK2;
    DRAWICON( 绝路航标>0,38,1 );

    计算公式：
    VAR1:=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80;
    B:SMA(VAR1,N,1);
    VAR2:SMA(B,M,1);
    绝路航标:IF(CROSS(B,VAR2) AND B<40,50,0);

    VAR1赋值:(收盘价-60日内最低价的最低值)/(60日内最高价的最高值-60日内最低价的最低值)*80
    输出 B:VAR1的N日[1日权重]移动平均
    输出 VAR2:B的M日[1日权重]移动平均
    输出 绝路航标:如果B上穿VAR2 AND B<40,返回50,否则返回0
    输入：
        security_list:股票列表
        check_date：要查询数据的日期
        N：统计的天数 N
        M：统计的天数 M
    输出：
        B, VAR2和绝路航标 的值。
    输出结果类型：
        字典(dict)：键(key)为股票代码，值(value)为数据。
    """
    def JLHB(security_list, check_date, N = 7, M = 5):
            '''

        '''
        import talib
        import numpy as np

        # 计算SMA(X, N, M)， 即X的N日移动平均，M为权重, 若Y=SMA(X,N,M) 则 Y = (M*X+(N-M)*Y')/N, 其中Y'表示上一周期Y值,N必须大于M。返回一个列表
        def SMA(X, N, M=1):
            ret = []
            i = 1
            length = len(X)
            # 跳过X中前面几个 nan 值
            while i < length:
                if np.isnan(X[i]):
                    i += 1
                else:
                    break
            preY = X[i] # Y'
            ret.append(preY)
            while i < length:
                Y = (M * X[i] + (N-M) * preY) / float(N)
                ret.append(Y)
                preY = Y
                i += 1
            return ret

        # VAR1:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*80;
        # 返回一个列表
        # 功能等效于talib.STOCHF返回的第一个值
        def STOCHF(high, low, close, N=60):
            VAR = []
            len_total = len(high)
            i = -len_total
            # 在N-1天之前，取不到LLV(LOW, N)和(HHV(HIGH,N)，所以VAR的值为nan
            while i < -(len_total-N + 1):
                t = np.nan
                VAR.append(t)
                i += 1
            # 终于有了LLV和HHV
            while i < -1:
                # 虽然都是+1，但意义不同，一个是弥补-N，一个是因为Python切片只能取到第二个参数所指的数的前一个
                llv = min(low[i-N+1 : i+1])
                hhv = max(high[i-N+1 : i+1])
                t = (close[i]-llv) / (hhv-llv) * 80
                VAR.append(t)
                i += 1
            # 因为low[-x: 0]取不到数值，所以low/high/close中的最后N个要单独处理
            llv = min(low[i-N+1 :])
            hhv = max(high[i-N+1 :])
            t = (close[i]-llv) / (hhv-llv) * 80
            VAR.append(t)
            return VAR

        # 计算 JLHB
        jlhb_b = {} 
        jlhb_var2 = {}
        jlhb_jlhb = {}
        # 修复传入为单只股票的情况
        if isinstance(security_list, (str,unicode)):
            security_list = [security_list]
        for stock in security_list:
            security_data = get_price(stock, end_date = check_date, frequency = '1d', fields = ['low', 'high', 'close'] , skip_paused = True, count = N * 20)
            nan_count = list(np.isnan(security_data['close'])).count(True)
            if nan_count == len(security_data['close']):
                log.info("股票 %s 输入数据全是 NaN，该股票可能已退市或刚上市，返回 NaN 值数据。" % stock)
                jlhb_b[stock] = np.nan
                jlhb_var2[stock] = np.nan
                jlhb_jlhb[stock] = np.nan
            else:
                close_JLHB = security_data['close']
                high_JLHB = security_data['high']
                low_JLHB = security_data['low']

                close = np.array(close_JLHB)
                high = np.array(high_JLHB)
                low = np.array(low_JLHB)

                # 计算VAR1值
                var1 = STOCHF(high, low, close)
                # 计算 B 值
                b = SMA(var1, N, 1)
                # 计算 var2 值
                var2 = SMA(b, M, 1)
                # 计算 绝路航标
                jlhb = 0
                cross = 0
                if b[-2] < var2[-2] and b[-1] > var2[-1]:
                    cross = 1
                if  cross == 1 and b[-1] < 40:
                    jlhb = 50

                jlhb_b[stock] = b[-1]
                jlhb_var2[stock] = var2[-1]
                jlhb_jlhb[stock] = jlhb
        return jlhb_b, jlhb_var2, jlhb_jlhb





    # _var_1 = pd.Series(low)-
        pass


def QA_indicator_cho(data):
    pass


def QA_indicator_macd(data):
    pass


def QA_indicator_emv(data):
    pass


def QA_indicator_trix(data):
    pass


def QA_indicator_gdx(data):
    pass


def QA_indicator_qacd(data):
    pass


def QA_indicator_uos(data):
    pass


def QA_indicator_vpt(data):
    pass


def QA_indicator_qr(data):
    pass


def QA_indicator_cye(data):
    pass


def QA_indicator_js(data):
    pass


def QA_indicator_wvad(deta):
    pass


"""震荡指标"""


def QA_indicator_rsi(data):
    pass


def QA_indicator_marsi(data):
    pass


def QA_indicator_cci(data):
    pass


def QA_indicator_mfi(deta):
    pass


def QA_indicator_mtm(data):
    pass


def QA_indicator_osc(data):
    pass


def QA_indicator_roc(data):
    pass


def QA_indicator_kd(data):
    pass


def QA_indicator_kdj(data):
    pass


def QA_indicator_skdj(data):
    pass


def QA_indicator_udl(data):
    pass


def QA_indicator_wr(data):
    pass


def QA_indicator_lwr(data):
    pass


def QA_indicator_bias(data):
    pass


def QA_indicator_accer(data):
    pass


def QA_indicator_cyd(data):
    pass


def QA_indicator_cyf(data):
    pass


def QA_indicator_fsl(data):
    pass


def QA_indicator_tapi(data):
    pass


def QA_indicator_dkx(data):
    pass


def QA_indicator_atr(data):
    pass


def QA_indicator_adtm(data):
    pass


"""成交量指标"""


def QA_indicator_vol(data):
    pass


def QA_indicator_vrsi(data):
    pass


def QA_indicator_obv(data):
    pass


def QA_indicator_dblb(data):
    pass


def QA_indicator_dbqrv(data):
    pass


def QA_indicator_amo(data):
    pass


def QA_indicator_hsl(data):
    pass


def QA_indicator_hscol(data):
    pass


"""均价线指标"""


def QA_indicator_ma(data):
    pass


def QA_indicator_expma(data):
    pass


def QA_indicator_hma(data):
    pass


def QA_indicator_lma(data):
    pass


def QA_indicator_vma(data):
    pass


def QA_indicator_amv(data):
    pass


def QA_indicator_acd(data):
    pass


def QA_indicator_bbi(data):
    pass


"""动量指标"""


def QA_indicator_psy(data):
    pass


def QA_indicator_vr(data):
    pass


def QA_indicator_brar(data):
    pass


def QA_indicator_cr(data):
    pass


def QA_indicator_mass(data):
    pass


def QA_indicator_wad(data):
    pass


def QA_indicator_pcnt(data):
    pass


def QA_indicator_cyr(data):
    pass


"""通道型指标"""


def QA_indicator_boll(data):
    pass


def QA_indicator_pbx(data):
    pass


def QA_indicator_ene(data):
    pass


def QA_indicator_mike(data):
    pass


def QA_indicator_xs(data):
    pass


def QA_indicator_xt(data):
    pass


"""大盘指标"""


def QA_indicator_adl(data):
    pass


def QA_indicator_adr(data):
    pass


def QA_indicator_arms(data):
    pass


def QA_indicator_abi(data):
    pass


def QA_indicator_bti(data):
    pass


def QA_indicator_mcl(data):
    pass


def QA_indicator_obos(data):
    pass


def QA_indicator_stix(data):
    pass


if __name__ == '__main__':
    import QUANTAXIS as QA
    import pymongo
    data = QA.QA_fetch_stock_day(
        '600016', '2017-01-01', '2017-07-01').T[1].astype(float)
    print(QA_indicator_dma(data))
