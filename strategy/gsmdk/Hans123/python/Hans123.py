# encoding: utf-8
from gmsdk.api import StrategyBase
from gmsdk import md
from gmsdk.enums import *
import arrow
import time


#每次开仓量
OPEN_VOL = 5

#最大开仓次数
MAX_TRADING_TIMES = 3

class Hans123(StrategyBase) :
    def __init__(self, *args, **kwargs):
        super(Hans123, self).__init__(*args, **kwargs)

        #是否已获取当天时间标识
        self.time_flag = False

        #是否已获取当天上、下轨数据
        self.data_flag = False 
        
        #持仓量
        self.long_hoding = 0;
        self.short_hoding = 0;

        #当天交易次数
        self.trading_times = 0;

        self.__get_param()

    
    def __get_param( self ):
        '''
        获取配置参数
        '''
        #交易证券代码
        self.trade_symbol = self.config.get('para', 'trade_symbol')
        pos = self.trade_symbol.find('.')
        self.exchange = self.trade_symbol[:pos]
        self.sec_id = self.trade_symbol[pos+1:]
        
        #开盘时间
        self.open_time = self.config.get( 'para', 'open_time')
        
        #hans时间
        self.hans_time = self.config.get('para', 'hans_time') 
        
        #强制平仓时间
        self.ex_time = self.config.get('para', 'ex_time')

    def __get_time( self, cur_utc ):
        '''
        获取当天的重要时间参数
        '''
        utc = arrow.get( cur_utc ).replace(tzinfo='local')
        cur_date = utc.format('YYYY-MM-DD')
        FMT = '%s %s'
        self.today_open_time = FMT%(cur_date, self.open_time)
        print 'today open time: %s'%self.today_open_time
        
        self.today_hans_time = FMT%(cur_date, self.hans_time)
        print 'today hans time: %s'%self.today_hans_time

        today_ex_time = FMT%(cur_date, self.ex_time )
        print 'today exit time:%s'%today_ex_time

        self.ex_time_utc = arrow.get(today_ex_time).replace(tzinfo='local').timestamp
        self.hans_time_utc = arrow.get(self.today_hans_time).replace(tzinfo='local').timestamp

    def __init_band_data( self, bar_type ):
         '''
         获取上、下轨数据
         '''
         bars = self.get_bars( self.trade_symbol, bar_type, self.today_open_time, self.today_hans_time )
         close_list =[bar.close for bar in bars ]

         #上轨
         self.upr_band = max(close_list)
         print 'upper band:%s'%self.upr_band

         #下轨
         self.dwn_band = min(close_list)
         print 'down band: %s'%self.dwn_band

    def on_tick(self, tick):
         '''
         tick行情事件
         '''
         #获取最新价
         self.last_price = tick.last_price

    def on_bar(self, bar):
        '''
        bar周期数据事件
        ''' 
        #获取当天的时间参数
        if  self.time_flag is False :
            self.__get_time( bar.utc_time )
            self.time_flag = True

        #计算上、下轨
        if bar.utc_time < self.ex_time_utc and bar.utc_time > self.hans_time_utc :
            if self.time_flag is True and self.data_flag is False:
                self.__init_band_data( bar.bar_type )
                self.data_flag = True

        #休市前强平当天仓位
        if bar.utc_time > self.ex_time_utc :
            if self.long_hoding > 0 :
                self.close_long( self.exchange, self.sec_id, 0, self.long_hoding )
                print 'exit time close long: %s, vol: %s'%( self.trade_symbol, self.long_hoding )
                self.long_hoding = 0
                
            elif self.short_hoding > 0:
                self.close_short( self.exchange, self.sec_id, 0, self.short_hoding )
                print 'exit time close long: %s, vol: %s'%( self.trade_symbol, self.short_hoding )
                self.short_hoding = 0
            return 

        if self.trading_times > MAX_TRADING_TIMES :
            print 'trading times more than max trading times, stop trading'
            return

        #交易时间段
        if bar.utc_time > self.hans_time_utc and bar.utc_time < self.ex_time_utc :
            if bar.close > self.upr_band :
                if self.short_hoding > 0 :
                    #有空仓，先平空仓
                    self.close_short( self.exchange, self.sec_id, 0, self.short_hoding )
                    print 'close short: %s, vol:%s'%(self.trade_symbol, self.short_hoding)
                    self.short_hoding = 0
                
                #开多仓
                self.open_long( self.exchange, self.sec_id, 0, OPEN_VOL )  
                print 'open long: %s, vol:%s'%(self.trade_symbol, OPEN_VOL)  
                self.long_hoding += OPEN_VOL

                #开仓次数+1
                self.trading_times += 1
            elif bar.close < self.dwn_band :
                if self.long_hoding > 0 :
                    #有多仓，先平多仓
                    self.close_long( self.exchange, self.sec_id, 0, self.long_hoding )
                    print 'close long: %s, vol:%s'%(self.trade_symbol, self.long_hoding)
                    self.long_hoding = 0

                #开空仓
                self.open_short( self.exchange, self.sec_id, 0,  OPEN_VOL )
                print 'open short: %s, vol:%s'%(self.trade_symbol, OPEN_VOL)
                self.short_hoding += OPEN_VOL

               #开仓次数+1
                self.trading_times += 1


            
if __name__ == '__main__':
    hans123 = Hans123(config_file='Hans123.ini')
    ret = hans123.run()
    print hans123.get_strerror(ret)