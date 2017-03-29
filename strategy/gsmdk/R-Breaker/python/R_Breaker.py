# encoding: utf-8

from gmsdk.api import StrategyBase
from gmsdk import md
from gmsdk.enums import *
import arrow

'''
R-Breaker是个经典的具有长生命周期的日内模型
类型：日内趋势追踪+反转策略
周期：1分钟、5分钟
根据前一个交易日的收盘价、最高价和最低价数据通过一定方式计算出六个价位，
从大到小依次为：
突破买入价（buy_break)、观察卖出价(sell_setup)、
反转卖出价(sell_enter)、反转买入价(buy_enter)、
观察买入价(buy_setup)、突破卖出价(sell_break)
以此来形成当前交易日盘中交易的触发条件。
 
交易规则：
反转:
持多单，当日内最高价超过观察卖出价后，盘中价格出现回落，且进一步跌破反转卖出价构成的支撑线时，采取反转策略，即在该点位反手做空；
持空单，当日内最低价低于观察买入价后，盘中价格出现反弹，且进一步超过反转买入价构成的阻力线时，采取反转策略，即在该点位反手做多；
突破:
在空仓的情况下，如果盘中价格超过突破买入价，则采取趋势策略，即在该点位开仓做多；
在空仓的情况下，如果盘中价格跌破突破卖出价，则采取趋势策略，即在该点位开仓做空；
'''

#每次开仓量
OPEN_VOL = 5

class R_Breaker(StrategyBase) :
    def __init__(self, *args, **kwargs):
        super(R_Breaker, self).__init__(*args, **kwargs)
        self.__get_param()
        self.__init_data()


    def __get_param( self ):
        '''
        获取配置参数
        '''

        self.trade_symbol = self.config.get('para', 'trade_symbol')
        pos = self.trade_symbol.find('.')
        
        #策略的一些阀值
        self.exchange = self.trade_symbol[:pos]
        self.sec_id = self.trade_symbol[pos+1:]
        self.observe_size = self.config.getfloat('para', 'observe_size')
        self.reversal_size = self.config.getfloat('para', 'reversal_size')
        self.break_size = self.config.getfloat('para', 'break_size' )
        
        #交易开始和结束时间
        FMT = '%sT%s'
        today = arrow.now().date()
        begin_time = self.config.get('para', 'begin_time')
        et = FMT % (today.isoformat(), begin_time)
        self.begin_trading = arrow.get(et).replace(tzinfo='local').timestamp
        end_time = self.config.get('para', 'end_time')
        et = FMT % (today.isoformat(), end_time)
        self.end_trading = arrow.get(et).replace(tzinfo='local').timestamp
        print "start time %s, end time %s" % (self.begin_trading, self.end_trading)

    def __init_data( self ):
        '''
        提取数据，计算价位
        '''

        prev_dailybar = self.get_last_dailybars(self.trade_symbol)
        
        if len(prev_dailybar) < 1 :
            return 

        self.prev_high = prev_dailybar[0].high
        self.prev_low = prev_dailybar[0].low
        self.prev_close = prev_dailybar[0].close

        self.high = self.prev_close
        self.low = self.prev_close
        self.close = self.prev_close

        #观察卖出价
        self.sell_setup= self.prev_high + self.observe_size * ( self.prev_close - self.prev_low )
        print 'sell_setup price: %s'%self.sell_setup

        #反转卖出价
        self.sell_enter = (1 + self.reversal_size)/2 * (self.prev_high + self.prev_low ) - self.reversal_size * self.prev_low
        print 'sell_enter price:%s'%self.sell_enter

        #反转买入价
        self.buy_enter = (1 + self.reversal_size)/2 * (self.prev_high + self.prev_low ) - self.reversal_size * self.prev_high
        print 'buy_enter price:%s'%self.buy_enter

        #观察买入价
        self.buy_setup = self.prev_low - self.observe_size * ( self.prev_high - self.prev_close )
        print 'buy_setup:%s'%self.buy_setup

        #突破买入价
        self.buy_break = self.sell_setup + self.break_size * ( self.sell_setup - self.buy_setup )
        print 'buy_break:%s'%self.buy_break

        #突破卖出价
        self.sell_break = self.buy_setup + self.break_size * ( self.sell_setup - self.buy_setup)
        print 'sell_break:%s'%self.sell_break

        self.bid_holding = 0.0
        position = self.get_position( self.exchange, self.sec_id, OrderSide_Bid);
        if position is not None:
            self.bid_holding = position.volume

        self.ask_holding = 0.0
        position = self.get_position( self.exchange, self.sec_id, OrderSide_Ask)
        if position is not None:
            self.ask_holding = position.volume


    def on_tick(self, tick):
        '''
        tick行情事件
        '''

        #即时获取当天高、低、现价 
        self.high = tick.high
        self.low = tick.low
        self.close = tick.last_price

    def on_bar(self, bar):
        '''
        bar周期数据事件
        '''    
        if bar.utc_time  > self.begin_trading and  bar.utc_time < self.end_trading :
            if self.close > self.buy_break and self.bid_holding < 1:
                #空仓做多
                self.open_long( self.exchange, self.sec_id, self.close, OPEN_VOL )
                print 'open long: price %s, vol %s'%(self.close, OPEN_VOL)
            elif self.close < self.sell_break and self.ask_holding < 1:
                #空仓做空
                self.open_short( self.exchange, self.sec_id, self.close, OPEN_VOL )
                print 'open short: price %s, vol %s'%(self.close, OPEN_VOL)
            elif self.bid_holding > 0 and self.high > self.sell_setup and self.close < self.sell_enter:
                #多单反转
                self.close_long(self.exchange, self.sec_id, self.close, self.bid_holding )
                print 'close long: price %s, vol %s'%(self.close, self.bid_holding)

                self.open_short( self.exchange, self.sec_id, self.close, OPEN_VOL )
                print 'Reverse open short: price %s, vol %s'%(self.close, OPEN_VOL)

            elif self.ask_holding > 0 and self.low < self.buy_setup and self.close > self.buy_enter:
                #空单反转
                self.close_short( self.exchange, self.sec_id, self.close, self.ask_holding )
                print 'close short: price %s, vol %s'%(self.close, self.ask_holding )
                
                self.open_long( self.exchange, self.sec_id, self.close, OPEN_VOL )
                print 'Reverse open long: price %s, vol %s'%(self.close, OPEN_VOL)

        if bar.utc_time > self.end_trading :
            #日内平仓
            if self.bid_holding > 0 :
                self.close_long( self.exchange, self.sec_id, 0, self.bid_holding )
            elif self.ask_holding > 0:
                self.close_short( self.exchange, self.sec_id, 0, self.ask_holding )
   
                
def on_execrpt(self, rpt):
    '''
    委托回报事件回调
    '''    

    if rpt.exec_type != ExecType_Trade :
        return

    #从成交回报累计持仓量
    if PositionEffect_Open == rpt.position_effect and OrderSide_Bid == rpt.side :
        self.bid_holding += rpt.volume
    elif PositionEffect_Open == rpt.position_effect and OrderSide_Ask == rpt.side:
        self.ask_holding += rpt.volume
    elif PositionEffect_Close == rpt.position_effect and OrderSide_Bid == rpt.side:
        self.bid_holding -= rpt.volume
    elif PositionEffect_Close == rpt.position_effect and OrderSide_Ask == rpt.side:
        self.ask_holding -= rpt.volume
            

if __name__ == '__main__':
    r_breaker = R_Breaker(config_file='R_Breaker.ini')
    ret = r_breaker.run()
    print r_breaker.get_strerror(ret)