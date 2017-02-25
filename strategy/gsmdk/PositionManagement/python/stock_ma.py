#!/usr/bin/env python
# encoding: utf-8

import sys
import logging
import logging.config
import time
from talib.abstract import SMA
import numpy as np
from collections import deque
#from gmsdk import StrategyBase, OrderSide_Ask, OrderSide_Bid, PositionEffect_Open, PositionEffect_Close
from gmsdk import *

import threading

eps = 1e-6

class DualMA(StrategyBase):

    ''' strategy example: dual MA decision
        short MA cross long MA, when get significant trends, place orders with volume decades
    '''

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)

        #import pdb; pdb.set_trace()
        super(DualMA, self).__init__(*args, **kwargs)
        self.tick_size = self.config.getfloat('para', 'tick_size') or 0.2
        self.half_tick_size = self.tick_size / 2.0

        self.threshold_factor = self.config.getfloat('para', 'threshold_factor') or 1.3
        self.significant_diff_factor = self.config.getfloat('para', 'significant_diff_factor') or 4.5
        self.stop_lose_threshold_factor = self.config.getfloat('para', 'stop_lose_threshold_factor') or 1.5
        self.stop_profit_threshold_factor = self.config.getfloat('para', 'stop_profit_threshold_factor') or 5.5
        self.drawdown = self.config.getfloat('para', 'stop_profit_drawdown') or 0.3

        self.threshold = self.tick_size * self.threshold_factor
        self.significant_diff = self.tick_size * self.significant_diff_factor
        self.stop_lose_threshold = self.tick_size * self.stop_lose_threshold_factor
        self.stop_profit_threshold = self.tick_size * self.stop_profit_threshold_factor
        self.exchange = self.config.get('para', 'trade_exchange')
        self.sec_id = self.config.get('para', 'trade_ticker')
        self.symbol = ".".join([self.exchange, self.sec_id])
        ## trade unit list, eg. fib numbers [1,2,3,5,8] or [8, 4.0, 2.0, 1.0]
        self.trade_unit = [int(x) for x in self.config.get('para', 'trade_unit_list').split(',')]

        self.cancel_ticks = self.config.getint('para', 'cancel_ticks') or 10
        self.trade_limit = self.config.getint('para', 'trade_limit')
        self.trade_limit = min(self.trade_limit, len(self.trade_unit))
        self.positive_stop = self.config.getboolean('para', 'positive_stop') or 0
        self.hops = self.config.getint('para', 'hops') or 1
        self.momentum_factor = self.config.getfloat('para', 'momentum_factor') or 1.1
        self.window_size = self.config.getint('para', 'window_size') or 20
        self.short_timeperiod = self.config.getint('para', 'short_timeperiod') or 5
        self.long_timeperiod = self.config.getint('para', 'long_timeperiod') or 10
        self.life_timeperiod = self.config.getint('para', 'life_timeperiod') or 30
        self.bar_type = self.config.getint('para', 'bar_type') or 15
        self.close_buffer = deque(maxlen=self.window_size)
        # prepare historical bars for MA calculating
        last_closes = [bar.close for bar in self.get_last_n_bars(self.symbol, self.bar_type, self.window_size)]
        last_closes.reverse()
        self.close_buffer.extend(last_closes)
        self.orders = []
        self.tick_counter = 0
        ##get positions
        # long position
        #self.b_p = self.get_position(self.exchange, self.sec_id, OrderSide_Bid) or Position()

        self.positions = dict()
        ps = self.get_positions()
        for p in ps:
            #import pdb; pdb.set_trace();
            sym = "{0}.{1}_{2}".format(p.exchange, p.sec_id, p.side)
            self.positions[sym] = p

        self.b_p = self.positions.get("{0}.{1}_{2}".format(self.exchange, self.sec_id, OrderSide_Bid))

        self.last_price = last_closes[-1] if len(last_closes) else 0 ## for backtest, make last price is last close
        self.trade_count = 0
        self.momentum = 0.0
        self.long_trends = False
        self.short_trends = False
        self.moving = False
        self.moving_long = False
        self.moving_short = False
        self.highest_pnl = 0.0
        self.analyse_only = self.config.getboolean('para', 'analyse_only') or False

    ## 以下是行情订阅，包括实时行情或者是回放行情
    ## 分时数据处理
    def on_bar(self, bar):
        #self.logger.info( "received bar: %s" % bar.__dict__)
        if bar.bar_type == self.bar_type:
            # go to handle new bar data
            self.close_buffer.append(bar.close)
            self.logger.info("received bar: {0}, close: {1} ".format(bar.strtime, round(bar.close,1)))
            self.algo_action()

            self.tick_counter = 0

    ## tick数据处理
    def on_tick(self, tick):
        ## filter none own sec_id
        if tick.sec_id != self.sec_id:
            return

        # self.logger.info( "received tick: %s" % to_dict(tick))

        self.tick_counter += 1
        if self.tick_counter >= self.cancel_ticks:
            # cancel unfinished orders
            self.cancel_unfinished_orders()

        if (len(tick.bids)*len(tick.asks) == 0):
            return

        if (not tick.last_price > 0):
            return

        self.last_price = tick.last_price

    ## 所有成交回报, 包括订单状态变化，撤单拒绝等，可以忽略，只处理如下面关心的订单状态变更信息
    def on_execrpt(self, execution):
        ## filter none own sec_id
        if execution.sec_id != self.sec_id:
            return
        self.logger.info("received execution: exec_type = {0}, rej_reason = {1} ".format(execution.exec_type, execution.ord_rej_reason_detail))
        if execution.exec_type == 15:
          self.logger.info('''
            received execution filled: sec_id: {0}, side: {1}, filled volume: {2}, filled price: {3}
            '''.format(execution.sec_id, execution.side, execution.volume, execution.price))

    ## 订单被接受
    def on_order_new(self, order):
        ## filter none own sec_id
        if order.sec_id != self.sec_id:
            return
        self.orders.append(order)

    ## 订单部分成交
    def on_order_partially_filled(self, order):
        ## filter none own sec_id
        if order.sec_id != self.sec_id:
            return
        self.logger.info('''
          received order partially filled: sec_id: {0}, side: {1}, pe: {2}, volume: {3}, filled price: {4}, filled: {5}
          '''.format(order.sec_id, order.side, order.position_effect, order.volume, order.filled_vwap, order.filled_volume))

    ## 订单完全成交
    def on_order_filled(self, order):
        ## filter none own sec_id
        if order.sec_id != self.sec_id:
            return
        self.logger.info('''
        received order filled: sec_id: {0}, side: {1}, volume: {2}, filled price: {3}, filled: {4}
        '''.format(order.sec_id, order.side, order.volume, order.filled_vwap, order.filled_volume))
        self.clean_final_orders(order)

    def on_order_cancelled(self, order):
        ## filter none own sec_id
        if order.sec_id != self.sec_id:
            return
        self.logger.info('''
        received order cancelled {0}: sec_id: {1}, side: {2}, volume: {3}, price: {4}, filled: {5}
        '''.format(order.cl_ord_id, order.sec_id, order.side, order.volume, order.price, order.filled_volume))
        self.clean_final_orders(order)

    ## 订单被拒绝
    def on_order_rejected(self, order):
        ## filter none own sec_id
        if order.sec_id != self.sec_id:
            return
        self.logger.info('''
        received order rejected {0}, sec_id: {1}, side: {2}, volume: {3}, price: {4}, filled: {5}, reason: {6}
        '''.format(order.cl_ord_id, order.sec_id, order.side, order.volume, order.price, order.filled_volume, order.ord_rej_reason_detail))
        self.clean_final_orders(order)

    def close_long_positions(self, b_p, ord_price=None):
        self.print_positions()
        price = ord_price if ord_price else self.last_price - self.hops*self.tick_size
        self.logger.info("try to close long ... {0} @ {1}, today's position first".format(b_p.volume, price))

        if b_p.exchange in ('SHSE', 'SZSE'):  ## stocks
            if b_p.available_yesterday:
                self.close_long(b_p.exchange, b_p.sec_id, price, b_p.available_yesterday)

    def print_positions(self):
        if self.b_p:
            b_p = self.b_p
            self.logger.debug(
                'long volume today = {0}/{1}, volume = {2}/{3}'.format(b_p.volume_today, b_p.available_today,
                                                                       b_p.volume, b_p.available))

    ## 移除本地管理的已进入完成状态的订单
    def clean_final_orders(self, order):
        self.logger.info("try to remove finished order {0}, sec_id {1} volume {2} price {3} ".format(order.cl_ord_id, order.sec_id, order.volume, order.price))
        for o in self.orders:
            if o.cl_ord_id == order.cl_ord_id:
                self.orders.remove(o)

    ## 撤销未完成状态的订单
    def cancel_unfinished_orders(self):
        if len(self.orders) > 0:
            for o in self.orders:
                self.logger.info("try to cancel order {0}, sec_id {1} volume {2} price {3} ".format(o.cl_ord_id, o.sec_id, o.volume, o.price))
                #self.trade_count -= 1
                self.cancel_order(o.cl_ord_id)

    ## 仓位管理，关注持仓的最高收益，用价差表示
    def care_positions(self):
        if self.analyse_only:
            return

        b_p = self.b_p = self.get_position(self.exchange, self.sec_id, OrderSide_Bid)
        self.logger.info('pos long: {0} vwap: {1}'.format(b_p.volume if b_p else 0.0,
                round(b_p.vwap, 2) if b_p else 0.0))

        if b_p:
            self.highest_pnl = max(self.last_price - b_p.vwap, self.highest_pnl)
        else:
            self.highest_pnl = 0.0

    ## 出场信号逻辑，停止持仓
    def try_stop_action(self):
        b_p = self.b_p
        short_trends = self.short_trends
        long_trends = self.long_trends
        stop_profit_threshold = self.stop_profit_threshold
        stop_lose_threshold = self.stop_lose_threshold
        significant_diff = self.significant_diff
        momentum = self.momentum
        moving = self.moving
        moving_long = self.moving_long
        moving_short = self.moving_short

        ## 多仓
        if b_p and b_p.volume > eps:
            b_pnl = self.last_price - b_p.vwap
            ## 触发止损阈值，或趋势不再继续
            if (b_pnl < - stop_lose_threshold ):
                self.logger.info("stop lose, close long...")
                self.close_long_positions(b_p)
                self.trade_count = 0
            elif (not long_trends or (moving_short and momentum < - significant_diff)):
                self.logger.info("long trends stopped, close long...")
                self.close_long_positions(b_p)
                self.trade_count = 0
            ## 触发最大回撤阈值
            elif self.threshold < b_pnl <= (1 - self.drawdown) * self.highest_pnl:
                self.logger.info("pnl drawdown, stop profit, close long...")
                self.close_long_positions(b_p)
                self.trade_count = 0
            ## 触发固定止赢
            elif self.positive_stop and b_pnl >= stop_profit_threshold:
                self.logger.info("take fixed earning, stop profit, close long...")
                self.close_long_positions(b_p)
                self.trade_count = 0

    ## 趋势信号的进出场判断，只在分时数据到来时计算
    def algo_action(self):
        close = np.asarray(self.close_buffer)
        if len(close) < self.life_timeperiod:
          self.logger.info('data not enough! len = {0}'.format(len(close)))
          return

        sma = SMA({'close':close}, timeperiod=self.short_timeperiod)
        lma = SMA({'close':close}, timeperiod=self.long_timeperiod)   ## make sure last lma is a number
        life = SMA({'close':close}, timeperiod=self.life_timeperiod)

        s_l_ma_delta = sma[-1] - lma[-1]  ## 最新的短长MA差值
        last_ma = sma[-1]          ## 最新的短MA

        #momentum = self.momentum = sma[-1] - sma[-2]  ## MA冲量
        momentum = self.momentum = self.last_price - sma[-1]  ## 当前价格相对MA冲量

        ## 短MA变动趋势，true表示进入趋势，false表示震荡
        moving_long = self.moving_long = moving_short = self.moving_short = False

        sma_diff = sma[-1] - sma[-2]
        sma_diff_1 = sma[-2] - sma[-3]
        moving = self.moving = sma_diff * sma_diff_1 > 0
        if moving and (sma_diff * momentum > 0 or momentum >= self.momentum_factor* s_l_ma_delta):
            moving_long = self.moving_long = True
        elif moving and (sma_diff * momentum > 0 or momentum <= self.momentum_factor* s_l_ma_delta):
            moving_short = self.moving_short = True

        ## 均线是多头还是空头排列
        long_trends = self.long_trends = (sma[-1] > lma[-1] > life[-1])
        short_trends = self.short_trends = (sma[-1] < lma[-1] < life[-1])
        self.logger.info('short ma: {0}, long ma: {1}, life line: {2}'.format(round(sma[-1],4), round(lma[-1],4), round(life[-1],4)))
        self.logger.info('short long ma delta: {0}, last_ma: {1}, momentum: {2}'.format(round(s_l_ma_delta,4), round(last_ma,4), round(momentum,4)))
        self.logger.info('## short ma moving long: {0}, moving short: {1}; Trends is long: {2}, is short: {3}.'.format(moving_long, moving_short, long_trends, short_trends))

        if self.analyse_only:
            return

        ## 下单基准价，为了能够成交，所有开平仓都会根据配置的跳数追价，这里先计算基准价格
        price_base = max(self.last_price, close[-1]) if long_trends else (min(self.last_price, close[-1]) if short_trends else self.last_price)

        self.logger.info("current trade count = {0}, price base = {1} ".format(self.trade_count, round(price_base, 1)))

        self.care_positions()
        b_p = self.b_p

        # cancel unfinished orders
        #self.cancel_unfinished_orders()

        threshold = self.threshold
        significant_diff = self.significant_diff
        stop_lose_threshold = self.stop_lose_threshold
        stop_profit_threshold = self.stop_profit_threshold

        ## 多信号
        if long_trends:        ## short ma cross up long ma
            ## 没有多仓
            if (b_p is None or b_p.volume < eps):
                signal_filter = (moving_long or momentum >= significant_diff) and s_l_ma_delta > threshold and self.trade_count < self.trade_limit
                vol = self.trade_unit[self.trade_count]  ## get order volume from configured list
                if signal_filter and vol > eps:
                    self.trade_count += 1
                    ord_price = price_base + self.hops*self.tick_size
                    self.logger.info("open long ... count {0}, {1} @ {2}".format(self.trade_count, vol, ord_price))
                    self.open_long(self.exchange, self.sec_id, ord_price, vol)
            ## 有多仓，且有止赢要求
            elif b_p and b_p.volume > eps:
                checking_limit = self.trade_count == self.trade_limit ## 最大交易次数限制止赢
                b_pnl = self.last_price - b_p.vwap                    ## 多仓浮赢
                if self.positive_stop and (checking_limit or b_pnl >= stop_profit_threshold):
                    ord_price = price_base - self.hops*self.tick_size
                    self.logger.info("trade count {0} to limit time[{1}], stop profit, close long @ {2}".format(self.trade_count, self.trade_limit, ord_price))
                    self.close_long_positions(b_p, ord_price)
                    self.trade_count = 0
                elif moving_short:  ## 短线趋势反转，检查是否要riskoff
                    self.try_stop_action()
            else:
                pass

        ## 空信号
        elif short_trends :     ## short ma cross down long ma
            ## 有多仓
            if b_p and b_p.volume > eps:
                self.logger.info("trend changed, stop lose, close long")
                self.close_long_positions(b_p)
                self.trade_count = 0
            else:
                pass

        else:  ##  check if need to stop trading,  close all positions
            self.logger.info("no trends, here check if need to stop ...")
            self.try_stop_action()


if __name__ == '__main__':
    ini_file = sys.argv[1] if len(sys.argv) > 1 else 'stock_ma.ini'
    logging.config.fileConfig(ini_file)
    dm = DualMA(config_file=ini_file)
    dm.logger.info("Strategy info : %s" % (dm.__dict__))
    dm.logger.info("Strategy dual ma ready, waiting for data ...")
    ret = dm.run()
    dm.logger.info("DualMA message %s" % (dm.get_strerror(ret)))
