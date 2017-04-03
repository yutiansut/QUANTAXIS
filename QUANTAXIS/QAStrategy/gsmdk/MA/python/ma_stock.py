#!/usr/bin/env python
# encoding: utf-8

from talib.abstract import SMA
import numpy as np
from collections import deque
from gmsdk import *

# 算法用到的一些常量，阀值，主要用于信号过滤
eps = 1e-6
threshold = 0.235
tick_size = 1
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
        self.trade_unit = [1, 2, 0] ##  [5, 1, 3, 0]
        self.trade_count = 0
        self.trade_limit = len(self.trade_unit)
        self.window_size = self.config.getint('para', 'window_size') or 20
        self.timeperiod = self.config.getint('para', 'timeperiod') or 20
        self.bar_type = self.config.getint('para', 'bar_type') or 60
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
        ma = SMA({'close':close}, timeperiod=self.timeperiod)
        delta = round(close[-1] - ma[-1],4)     # 最新数据点，bar的收盘价跟ma的差
        last_ma = round(ma[-1], 4)  #  均线ma的最新值
        momentum = round(self.last_price - last_ma,4)  # 当前最新价格跟ma之间的差，成交价相对ma偏离
        cross = (close[-1] - ma[-1]) * (close[-3] - ma[-3]) < 0  ## 判断有否交叉
        #print 'close: ', close
        print(('close ma delta: {0}, last_ma: {1}, momentum: {2}'.format(delta, last_ma, momentum)))

        b_p = self.get_position(self.exchange, self.sec_id, OrderSide_Bid)    #查询策略所持有的多仓
        # 打印持仓信息
        print(('pos long: {0} vwap: {1:.2f}'.format(b_p.volume if b_p else 0.0, b_p.vwap if b_p else 0.0)))
        if cross < 0 and delta > threshold and momentum >= significant_diff:        ## 收盘价上穿均线，且当前价格偏离满足门限过滤条件，多信号
            # 没有超出下单次数限制
            if self.trade_count < self.trade_limit:
                # 依次获取下单的交易量，下单量是配置的一个整数数列，用于仓位管理，可用配置文件中设置
                vol = self.trade_unit[self.trade_count]
                # 如果本次下单量大于0,  发出买入委托交易指令
                if vol > eps:
                    self.open_long(self.exchange, self.sec_id, self.last_price, vol)
                self.trade_count += 1    #增加计数
        elif cross < 0 and delta < -threshold and momentum <= - significant_diff:     ## bar 收盘价下穿ma均线，且偏离满足信号过滤条件
            # 超出下单次数限制
            if b_p and b_p.available_yesterday > eps:
                self.close_long(self.exchange, self.sec_id, self.last_price, b_p.available_yesterday)
                self.trade_count = 0
        else:       ##  其他情况，忽略不处理
            pass

# 策略启动入口
if __name__ == '__main__':
    #  初始化策略
    ma = MA(config_file='ma_stock.ini')
    #import pdb; pdb.set_trace()   # python调试开关
    print('strategy ready, waiting for market data ......')
    # 策略进入运行，等待数据事件
    ret = ma.run()
    # 打印策略退出状态
    print("MA :", ma.get_strerror(ret))

