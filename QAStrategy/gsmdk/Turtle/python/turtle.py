# encoding: utf8

import logging
import logging.config
import pandas as pd
import numpy as np
from gmsdk import *


class TurtleStrategy(StrategyBase):
    def __init__(self, *args, **kwargs):
        super(TurtleStrategy, self).__init__(*args, **kwargs)
        self.__get_param__()
        self.__init_data__()

    def __get_param__(self):
        self.csv_file = self.config.get('para', 'csv_file')
        self.period = self.config.getint('para', 'period')
        self.hop = self.config.get('para', 'hop') or 0

    def __init_data__(self):
        '''
        read stocks from csv file
        :return:
        '''
        self.sec_ids = []
        self.hist_data = dict()
        self.positions = dict()

        subscribe_symbols = []

        stocks = pd.read_csv(self.csv_file, sep=',')
        for r in stocks.iterrows():
            exchange = r[1][0]
            sec_id = r[1][1]
            buy_amount = r[1][2]
            t = "{0}.{1}".format(exchange, sec_id)

            hl = self.get_highest_lowest_price(t)
            self.hist_data[t] = hl + (buy_amount,)   ## high, low, buy_amount

            self.sec_ids.append("{0}".format(sec_id))
            subscribe_symbols.append(t + ".tick")

        ## subscribe
        self.subscribe(",".join(subscribe_symbols))

        ps = self.get_positions()
        for p in ps:
            sym = ".".join([p.exchange, p.sec_id])
            self.positions[sym] = p

            ## if not in stock list, close long position
            if p.sec_id not in self.sec_ids:
                self.close_long(p.exchange, p.sec_id, 0, p.volume)


    def get_highest_lowest_price(self, symbol):
        print(symbol)
        ## get last N dailybars
        hd = self.get_last_n_dailybars(symbol, self.period)

        high_prices = [b.high for b in hd]
        #high_prices.reverse()

        low_prices = [b.low for b in hd]
        #low_prices.reverse()

        return np.max(high_prices), np.min(low_prices)


    def on_tick(self, tick):
        if not tick.sec_id in self.sec_ids:
            self.logger.info( "received tick: %s %s %s %s" % (tick.exchange, tick.sec_id, round(tick.last_price,2), tick.last_volume))
        else:
            self.logger.info( "received tick: %s %s, A: %s B: %s" % (tick.sec_id, round(tick.last_price,2), round(tick.asks[0][0],2), round(tick.bids[0][0],2)))
            symbol = ".".join([tick.exchange, tick.sec_id])
            data = self.hist_data.get(symbol)

            if data and tick.last_price > data[0]:  ## check high
                volume = int(data[2]/(tick.last_price+self.hop)/100)*100  ## get slots, then shares
                self.open_long(tick.exchange, tick.sec_id, tick.last_price + self.hop, volume)
            if data and tick.last_price < data[1]:  ## check low
                #p = self.get_position(tick.exchange, tick.sec_id, OrderSide_Bid)
                p = self.positions.get(symbol)
                if p:
                    self.close_long(tick.exchange, tick.sec_id, tick.last_price - self.hop, p.volume - p.volume_today)


if __name__ == '__main__':
    ini_file = sys.argv[1] if len(sys.argv) > 1 else 'stocks_ind.ini'
    logging.config.fileConfig(ini_file)
    st = TurtleStrategy(config_file=ini_file)
    st.logger.info("Strategy turtle ready, waiting for data ...")
    ret = st.run()
    st.logger.info("Strategy turtle message %s" % st.get_strerror(ret))
