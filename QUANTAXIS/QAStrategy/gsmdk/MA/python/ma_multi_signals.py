#!/usr/bin/env python
# encoding: utf-8


import time
from talib import SMA
import numpy as np
from collections import deque
from gmsdk import *

# 算法用到的一些常量，阀值，主要用于信号过滤
eps = 1e-6
threshold = 0.235
tick_size = 0.2
half_tick_size = tick_size / 2
significant_diff = tick_size * 2.6

class MA(StrategyBase):

    ''' strategy example1: MA decision price cross long MA, then place a order, temporary reverse trends place more orders '''

    def __init__(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        super(MA, self).__init__(*args, **kwargs)
        # 策略初始化工作在这里写，从外部读取静态数据，读取策略配置参数等工作，只在策略启动初始化时执行一次。

        # 从配置文件中读取配置参数
        self.exchange = self.config.get('para', 'trade_exchange')
        self.sec_id = self.config.get('para', 'trade_symbol')
        self.symbol = ".".join([self.exchange, self.sec_id])
        self.last_price = 0.0
        self.trade_unit = [3, 1, 2, 0]
        self.trade_count = 0
        self.trade_limit = len(self.trade_unit)
        self.window_size = self.config.getint('para', 'window_size') or 60
        self.timeperiod = self.config.getint('para', 'timeperiod') or 60
        self.bar_type = self.config.getint('para', 'bar_type') or 15
        self.close_buffer = deque(maxlen=self.window_size)
        self.significant_diff = self.config.getfloat('para', 'significant_diff') or significant_diff

        # prepare historical bars for MA calculating
        # 从数据服务中准备一段历史数据，使得收到第一个bar后就可以按需要计算ma
        last_closes = [bar.close for bar in self.get_last_n_bars(self.symbol, self.bar_type, self.window_size)]
        last_closes.reverse()     #因为查询出来的时间是倒序排列，需要倒一下顺序
        self.close_buffer.extend(last_closes)

    # 响应bar数据到达事件
    def on_bar(self, bar):
        # 确认下bar数据是订阅的分时
        if bar.bar_type == self.bar_type:
            # 把数据加入缓存
            self.close_buffer.append(bar.close)
            # 调用策略计算
            self.algo_action()

    # 响应tick数据到达事件
    def on_tick(self, tick):
        # 更新市场最新成交价
        self.last_price = tick.last_price

    def on_execution(self, execution):
        #打印订单成交回报信息
        print("received execution: %s" % execution.exec_type)

    #策略的算法函数，策略的交易逻辑实现部分
    def algo_action(self):
        #数据转换，方便调用ta-lib函数进行技术指标的计算，这里用SMA指标
        close = np.asarray(self.close_buffer)
        ma = SMA(close, timeperiod=self.timeperiod)
        delta = round(close[-1] - ma[-1],4)     # 最新数据点，bar的收盘价跟ma的差
        cross = (close[-1] - ma[-1]) * (close[-3] - ma[-3]) < 0  ## 判断有否交叉
        last_ma = round(ma[-1], 4)  #  均线ma的最新值
        momentum = round(self.last_price - last_ma,4)  # 当前最新价格跟ma之间的差，成交价相对ma偏离
        #print 'close: ', close
        print(('close ma delta: {0}, last_ma: {1}, momentum: {2}'.format(delta, last_ma, momentum)))

        a_p = self.get_position(self.exchange, self.sec_id, OrderSide_Ask)    #查询策略所持有的空仓
        b_p = self.get_position(self.exchange, self.sec_id, OrderSide_Bid)    #查询策略所持有的多仓
        # 打印持仓信息
        print(('pos long: {0} vwap: {1}, pos short: {2}, vwap: {3}'.format(b_p.volume if b_p else 0.0,
                round(b_p.vwap,2) if b_p else 0.0,
                a_p.volume if a_p else 0.0,
                round(a_p.vwap,2) if a_p else 0.0)))

        if cross < 0 and delta > threshold and momentum >= significant_diff:        ## 收盘价上穿均线，且当前价格偏离满足门限过滤条件，多信号
            # 没有空仓，开多，或者是有多仓且没有超出下单次数限制，继续加多
            if (a_p is None or a_p.volume < eps) or (b_p and self.trade_count < self.trade_limit):
                # 依次获取下单的交易量，下单量是配置的一个整数数列，用于仓位管理，可用配置文件中设置
                vol = self.trade_unit[self.trade_count]
                # 如果本次下单量大于0,  发出买入委托交易指令
                if vol > eps:
                    self.open_long(self.exchange, self.sec_id, self.last_price, vol)
                self.trade_count += 1    #增加计数
            else:
                #  如果有空仓，平掉空仓
                if a_p and a_p.volume > eps:
                    self.close_short(self.exchange, self.sec_id, self.last_price, a_p.volume)
                    self.trade_count = 0
        elif cross < 0 and delta < -threshold and momentum <= - significant_diff:     ## bar 收盘价下穿ma均线，且偏离满足信号过滤条件
            # 没有多仓时，开空, 或者是有空仓时，且没超出交易次数限制，继续加空
            if (b_p is None or b_p.volume < eps) or (a_p and self.trade_count < self.trade_limit):
                vol = self.trade_unit[self.trade_count]
                self.trade_count += 1
                if vol > eps:
                    self.open_short(self.exchange, self.sec_id, self.last_price, vol)
            else:
                # 已有多仓，平掉多仓
                if b_p and b_p.volume > eps:
                    self.close_long(self.exchange, self.sec_id, self.last_price, b_p.volume)
                    self.trade_count = 0
        else:       ##  其他情况，忽略不处理
            ## get positions and close if any
            #self.trade_count = 0   ## reset trade count
            pass

# 策略启动入口
if __name__ == '__main__':
    #  初始化策略
    ma = MA(config_file='ma.ini')
    #import pdb; pdb.set_trace()   # python调试开关
    print('strategy ready, waiting for market data ......')
    # 策略进入运行，等待数据事件
    ret = ma.run()
    # 打印策略退出状态
    print("MA :", ma.get_strerror(ret))

