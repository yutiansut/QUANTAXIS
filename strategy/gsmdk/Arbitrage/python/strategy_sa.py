#!/usr/bin/env python
# encoding: utf-8

import logging
import time
import numpy as np
from collections import deque
from gmsdk import *
from math import log

eps = 1e-6

class StatArb(StrategyBase):
    '''
        statistics arbitrage demo
    '''
    def __init__(self, *args, **kwargs):
        super(StatArb, self).__init__(*args, **kwargs)
        logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
        self.tick_size = self.config.getfloat('ss', 'tick_size') or 0.2

        self.threshold = self.config.getfloat('ss', 'sigma') or 2.345
        self.significant_diff = self.threshold * .75   ## 3/4 sigma
        self.stop_lose_threshold = self.threshold * 2.0  ## 2 * sigma

        self.trade_exchange_a = self.config.get('ss', 'trade_exchange_a') or 'CFFEX'
        self.trade_secid_a = self.config.get('ss', 'trade_secid_a') or 'IF1406'
        self.trade_unit_a = self.config.get('ss', 'trade_unit_a') or 1
        self.last_price_a = 0.0

        self.trade_exchange_b = self.config.get('ss', 'trade_exchange_b') or 'CFFEX'
        self.trade_secid_b = self.config.get('ss', 'trade_secid_b') or 'IF1407'
        self.trade_unit_b = self.config.get('ss', 'trade_unit_b') or 1
        self.last_price_b = 0.0

        self.pos_side_up = False
        self.pos_side_down = False

        self.window_size = 20

        self.close_buffer_symbol_a = deque(maxlen=self.window_size)
       	self.close_buffer_symbol_b = deque(maxlen=self.window_size)
        self.at_risk = 0
        self.bar_type = self.config.get('ss', 'bar_type')

    def on_tick(self, tick):
        if tick.sec_id == self.trade_secid_a:
            self.last_price_a = tick.last_price
        elif tick.sec_id == self.trade_secid_b:
            self.last_price_b = tick.last_price

        self.check_position()

    def on_bar(self, bar):
        if bar.bar_type == self.bar_type:
            if bar.symbol == self.trade_secid_a:
                self.close_buffer_symbol_a.append(bar.close)
            elif bar.symbol == self.trade_secid_b:
                self.close_buffer_symbol_b.append(bar.close)
            self.algo_action()

    def open_side_up(self):
        self.open_short(self.trade_exchange_a, self.trade_secid_a, self.last_price_a, self.trade_unit_a)
        self.open_long(self.trade_exchange_b, self.trade_secid_b, self.last_price_b, self.trade_unit_b)
        self.pos_side_up = True

    def close_side_up(self):
        self.close_short(self.trade_exchange_a, self.trade_secid_a, self.last_price_a, self.trade_unit_a)
        self.close_long(self.trade_exchange_b, self.trade_secid_b, self.last_price_b, self.trade_unit_b)
        self.pos_side_up = False

    def open_side_down(self):
        self.open_long(self.trade_exchange_a, self.trade_secid_a, self.last_price_a, self.trade_unit_a)
        self.open_short(self.trade_exchange_b, self.trade_secid_b, self.last_price_b, self.trade_unit_b)
        self.pos_side_down = True

    def close_side_down(self):
        self.close_long(self.trade_exchange_a, self.trade_secid_a, self.last_price_a, self.trade_unit_a)
        self.close_short(self.trade_exchange_b, self.trade_secid_b, self.last_price_b, self.trade_unit_b)
        self.pos_side_down = False

    def algo_action(self):
        latest_a = self.close_buffer_symbol_a.pop()
        lna = log(latest_a)

        latest_b = self.close_buffer_symbol_b.pop()
        lnb = log(latest_b)

        diff = lna - lnb

        if diff > self.stop_lose_threshold:
            self.close_side_up()
        elif diff > self.significant_diff and diff < self.stop_lose_threshold:
            self.open_side_up()
        elif diff < - self.stop_lose_threshold:
            self.close_side_down()
        elif diff < - self.significant_diff and diff > - self.stop_lose_threshold:
            self.open_side_down()
        elif abs(diff) < self.threshold:
            if self.pos_side_up:
                self.close_side_up()
            if self.pos_side_down:
                self.close_side_down()


    def check_position(self):
        """  TODO: check if one leg position and close it  """
        ps = self.get_positions()
        count = len(ps)
        if count % 2 != 0:
            self.at_risk += 1
            ## if more than 4 tick data passed, need to force quit
            if self.at_risk < 4:
                return

            for p in ps:
                if self.pos_side_up:
                    if p.side == OrderSide_Ask:
                        self.close_short(p.exchange, p.sec_id, self.last_price_a, p.volume)
                    elif p.side == OrderSide_Bid:
                        self.close_long(p.exchange, p.sec_id, self.last_price_b, p.volume)
                if self.pos_side_down:
                    if p.side == OrderSide_Ask:
                        self.close_short(p.exchange, p.sec_id, self.last_price_b, p.volume)
                    elif p.side == OrderSide_Bid:
                        self.close_long(p.exchange, p.sec_id, self.last_price_a, p.volume)
        else:
            self.at_risk = 0


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    dm = StatArb(config_file='strategy_sa.ini')
    ret = dm.run()
    print "Statistics Arbitrage: ", dm.get_strerror(ret)



