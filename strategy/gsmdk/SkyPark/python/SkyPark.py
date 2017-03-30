# encoding: utf-8
from gmsdk.api import StrategyBase
from gmsdk import md
from gmsdk.enums import *
import arrow
import time

#每次开仓量
OPEN_VOL = 5

class SkyPark(StrategyBase) :
    def __init__(self, *args, **kwargs):
        super(SkyPark, self).__init__(*args, **kwargs)
        #上、下轨
        self.upr = None
        self.dwn = None
       
        #开仓标识
        self.open_long_flag = False
        self.open_short_flag = False
        
        #持仓量
        self.hoding = 0;

        self.__get_param()
        self.__init_data()

    def __get_param( self ):
        '''
        获取配置参数
        '''
        #交易证券代码
        self.trade_symbol = self.config.get('para', 'trade_symbol')
        pos = self.trade_symbol.find('.')
        self.exchange = self.trade_symbol[:pos]
        self.sec_id = self.trade_symbol[pos+1:]

        FMT = '%s %s'
        today = arrow.now().date()

        #第一根K线时间
        first_kline_time = self.config.get('para', 'first_kline_time') 
        et = FMT % (today.isoformat(), first_kline_time)
        self.first_kline_time_str = et

        #平仓时间
        end_time = self.config.get('para', 'end_time')
        et = FMT % (today.isoformat(), end_time)
        self.end_trading = arrow.get(et).replace(tzinfo='local').timestamp
        print "end time %s" % (et)

        #开多阀值
        self.open_long_size = self.config.getfloat('para', 'open_long_size')
        #开空阀值
        self.open_short_size = self.config.getfloat('para', 'open_short_size')

    def __init_data( self ):
        dailybars = self.get_last_dailybars( self.trade_symbol )
        if len(dailybars) > 0 :
            self.pre_close = dailybars[0].close;

        #第一根K线数据
        while self.upr is None or self.dwn is None:
            print 'waiting for get the first K line...'
            bars = self.get_bars( self.trade_symbol, 60, self.first_kline_time_str, self.first_kline_time_str )
            if  len(bars) > 0 :
                self.upr = bars[0].high   #上轨
                self.dwn = bars[0].low   #下轨
                print 'upr:%s, dwn: %s'%(self.upr, self.dwn)

                if bars[0].open > self.pre_close * (1 + self.open_long_size) :
                    self.open_long_flag = True #开多仓标识
                elif bars[0].open > self.pre_close * ( 1 - self.open_short_size):
                    self.open_short_flag = True#开空仓标识
                else:
                    print 'Do not meet the trading condition, today do not trading.'
                break

            time.sleep( 1 )
            

    def on_tick(self, tick):
        #最新报价
        self.close = tick.last_price

    def on_bar(self, bar):
        '''
        bar周期数据事件
        '''    
        if self.open_long_flag and self.close > self.upr and 0 == self.hoding :
            self.open_long(self.exchange, self.sec_id, 0, OPEN_VOL )
            self.hoding += OPEN_VOL
            print 'open long: last price %s, vol %s'%(self.close, OPEN_VOL)
        elif self.open_short_flag and self.close < self.dwn and 0 == self.hoding :
            self.open_short( self.exchange, self.sec_id, 0, OPEN_VOL ) 
            self.hoding += OPEN_VOL
            print 'open short: last price %s, vol %s'%(self.close, OPEN_VOL)

        #日内平仓
        if bar.utc_time > self.end_trading :
            if self.open_long_flag and self.hoding > 0 :
                self.close_long( self.exchange, self.sec_id, 0, self.hoding )
                print 'end trading time close long, vol: %s'%self.hoding
            elif self.open_short_flag and self.hoding > 0 :
                self.close_short( self.exchange, self.sec_id, 0, self.hoding ) 
                print 'end trading time close short, vol: %s'%self.hoding

if __name__ == '__main__':
    sky_park = SkyPark(config_file='SkyPark.ini')
    ret = sky_park.run()
    print sky_park.get_strerror(ret)


