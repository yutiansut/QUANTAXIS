import QUANTAXIS as QA
from QAStrategy.qastockbase import QAStrategyStockBase
from QUANTAXIS import CROSS
import pprint
import talib
import datetime
import numpy as np
import pandas as pd
from qaenv import (eventmq_ip, 
                   eventmq_password, 
                   eventmq_port,
                   eventmq_username, 
                   mongo_ip)


def Timeline_Integral_with_cross_before(Tm,):
    """
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)不清零，金叉(0-->1)清零) 
	这个我一直不会写成lambda或者apply的形式，只能用for循环，谁有兴趣可以指导一下
    """
    T = [Tm[0]]
    for i in range(1,len(Tm)):
        T.append(T[i - 1] + 1) if (Tm[i] != 1) else T.append(0)
    return np.array(T)


def kline_returns_func(data, format='pd'):
    """
    计算单个标的每 bar 跟前一bar的利润率差值
    多用途函数，可以是 QA_DataStruct.add_func 调用（可以用于多标的计算），
    也可以是函数式调用（切记单独函数式调用不能多个标的混合计算）。
    Calculating a signal Stock/price timeseries kline's returns.
    For each data[i]/data[i-1] at series value of percentage.

    Parameters
    ----------
    data : (N,) array_like or pd.DataFrame or QA_DataStruct
        传入 OHLC Kline 序列。参数类型可以为 numpy，pd.DataFrame 或者 QA_DataStruct
        The OHLC Kline.
        在传入参数中不可混入多标的数据，如果需要处理多标的价格数据，通过
        QA_DataStruct.add_func 调用。
        It can prossessing multi indices/stocks by QA_DataStruct.add_func
        called. With auto splited into single price series 
        by QA_DataStruct.add_func().
        For standalone called, It should be only pass one stock/price series. 
        If not the result will unpredictable.
    format : str, optional
        返回类型 默认值为 'pd' 将返回 pandas.DataFrame 格式的结果
        可选类型，'np' 或 etc 返回 nparray 格式的结果
        第一个 bar 会被填充为 0.
        Return data format, default is 'pd'. 
        It will return a pandas.DataFrame as result.
        If seted as string: 'np' or etc string value, 
        It will return a nparray as result.
        The first bar will be fill with zero.

    Returns
    -------
    kline returns : pandas.DataFrame or nparray
        'returns' 跟前一收盘价格变化率的百分比

    """
    if isinstance(data, pd.DataFrame) or \
        (isinstance(data, QA.QAData.base_datastruct._quotation_base)):
        data = data.close

    if (format == 'pd'):
        kline_returns = pd.DataFrame(np.nan_to_num(np.log(data / data.shift(1)), 
                                                   nan=0),
                                     columns=['returns'], 
                                     index=data.index)
        return kline_returns
    else:
        np.nan_to_num(np.log(data.close / data.close.shift(1)), nan=0)


from QUANTAXIS.QAIndicator.talib_numpy import *
from QUANTAXIS.QAIndicator.base import *
from QUANTAXIS.QAAnalysis.QAAnalysis_signal import *

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
    MA30_CROSS['BOOTSRTAP_R5'] = np.where((ma30_croos_day['HMA_RETURNS'].values > 0) & (MA30_CROSS['BOOTSRTAP_R5'].values > 0), 
                      1, 
                      np.where((ma30_croos_day['HMA_RETURNS'].values < 0) & (MA30_CROSS['BOOTSRTAP_R5'].values < 0), 
                               -1, 
                               direction)) # 这里 0 是代表本策略中无指向性的，为了降低代码复杂度去掉了 ATR 策略部分
    MA30_CROSS['BOOTSRTAP_R5'].ffill(inplace=True)
    MA30_CROSS['BOOTSRTAP_R5'].fillna(0, inplace=True)
    MA30_CROSS = MA30_CROSS.assign(close=data.close)
    return MA30_CROSS


class HMA_Strategy(QAStrategyStockBase):
    def __init__(self, 
                code=['000001'], frequence='day', strategy_id='QA_STRATEGY_DEMO', risk_check_gap=1,
                portfolio='default',
                start='2019-01-01', end='2019-10-21', send_wx=False, market_type='stock_cn',
                data_host=eventmq_ip, data_port=eventmq_port, data_user=eventmq_username,
                data_password=eventmq_password,
                trade_host=eventmq_ip, trade_port=eventmq_port, trade_user=eventmq_username,
                trade_password=eventmq_password,
                taskid=None, 
                mongo_ip=mongo_ip):
        """
        code 可以传入单个标的 也可以传入一组标的(list)
        会自动基于code来判断是什么市场
        """

        super().__init__(code=code, frequence=frequence, strategy_id=strategy_id, risk_check_gap=risk_check_gap,
                        portfolio=portfolio,
                        start=start, end=end, send_wx=send_wx, market_type=market_type,
                        data_host=eventmq_ip, data_port=eventmq_port, data_user=eventmq_username,
                        data_password=eventmq_password,
                        trade_host=eventmq_ip, trade_port=eventmq_port, trade_user=eventmq_username,
                        trade_password=eventmq_password,
                        taskid=taskid, mongo_ip=mongo_ip)
        print(code)
        klines = QA.QA_fetch_stock_day_adv(code, start, end)
        self._hma = klines.add_func(hma_cross_func)

    def on_bar(self, bar):
        indices = self.hma(bar)
        code = bar.name[1]
        if (indices['BOOTSRTAP_R5'][-1] == 1):
            if self.acc.get_position(code).volume_long == 0:
                print('择时：', self.running_time, 'LONG', '当前标的 {} 开仓！Cash:{}'.format(code, self.acc.cash_available))
                self.send_order('BUY', 'OPEN', 
                                code=code, price=bar['close'], 
                                volume=100 * int((self.acc.cash_available / bar['close']) * 0.009))
            else:
                print('LONG', '当前标的 {} 满仓！'.format(code), '剩余资金总仓位：{:.1%}'.format(self.acc.freecash_precent) )
        elif ((indices['BOOTSRTAP_R5'][-1] == -1)):
            if self.acc.get_position(code).volume_long > 0:
                self.send_order('SELL', 'CLOSE',
                                code=code, price=bar['close'], 
                                volume=self.acc.get_position(code).volume_long)
                print('择时：', self.running_time, 'SHORT: 当前标的 {} 清仓！Cash:{}'.format(code, self.acc.cash_available))
            else:
                print('择时：', self.running_time, 'SHORT: 当前标的 {} 空仓！'.format(code), '剩余资金总仓位：{:.1%}'.format(self.acc.freecash_precent) )
        else:
            if (indices['BOOTSRTAP_R5'][-1] == 1) or \
                ((indices['BOOTSRTAP_R5'][-1] == -1)):
                print(self.running_time)
                print('bar DATA:', bar)
                print('INDICES:', indices.iloc[-1])
                print()

    def hma(self, data):
        """
        每bar数据的预处理，这个函数自定义，由on_bar调用。
        功能包括指标计算、bar的时间和标的code提取
        """
        day = data.name[0]
        # code为多标的处理，每次 on_bar 传来的是单一标的，标的品种就在 code 中
        code = data.name[1]
        if self.running_mode == 'sim':
            # 实盘模拟需要每bar重新计算指标，因为data数据更新了
            pass
        elif self.running_mode == 'backtest':
            # 回测模式为了加快运行速度，不进行指标的重复计算，直接读取策略类
            # __init__时计算好的DataFrame缓存值。
            return self._hma.loc[(slice(pd.Timestamp(day - datetime.timedelta(60)), pd.Timestamp(day)), code), :]

    def risk_check(self):
        pass
        # pprint.pprint(self.qifiacc.message)


if __name__ == '__main__':
    from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
    from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk
    from QUANTAXIS.QAUtil.QADate_Adv import (
        QA_util_timestamp_to_str,
        QA_util_datetime_to_Unix_timestamp,
        QA_util_print_timestamp
    )

    user = QA.QA_User(username ='quantaxis', password = 'quantaxis')
    portfolio=user.new_portfolio('hma_super_trend')
    stock_account= portfolio.new_account(account_cookie ='stock',allow_t0=False,allow_margin=False,allow_sellopen=False,running_environment=QA.MARKET_TYPE.STOCK_CN)

    codes = ['000905']
    strategy = HMA_Strategy(code=codes,
        frequence='day',
        strategy_id='BKTST_HMA01_C{}_T{}'.format(codes[0], QA_util_timestamp_to_str()[2:16]), 
        risk_check_gap=1,
        portfolio='hma_super_trend',
        start='2015-01-01',
        end='2020-03-30',)
    
    #strategy.debug()
    strategy.run_backtest()
    QA_util_log_info(strategy.acc.history_table)
    # check if the history_table is empty list
    if len(strategy.acc.history_table) == 0:
        # 没有交易历史记录，直接返回
        pass
    else:
        risk = QA_Risk(strategy.acc, benchmark_code=codes[0],
                        benchmark_type=QA.MARKET_TYPE.STOCK_CN)
        print(risk().T)
        risk.plot_assets_curve()
        risk.plot_dailyhold()
        risk.plot_signal()
        performance = QA_Performance(strategy.acc)
        performance.plot_pnlmoney()
        performance.plot_pnlratio()
        #risk.save()

        # 回测之后，清除历史订单数据
        strategy.acc.reset_assets(1000000)
        strategy.acc.save()

    print(strategy.acc.reset_assets(1000000))
    print(strategy.acc.save())