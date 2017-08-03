# coding:utf-8

from functools import wraps

class backtest():
    cash=10000
    def __init__(self,):
        self.account=1000000
    

    @classmethod
    def backtest_init(backtest,func,*a,**b):
        backtest.account=199
        return func(backtest,*a,**b)

    @classmethod
    def before_backtest(backtest,func,*a,**b):
        #yield backtest.cash
        return func(backtest,*a,**b)

    
   # @staticmethod
    def before_trading(self,func,*a,**b):
        @wraps(func)
        def before(*a,**b):
        #yield backtest.cash
            return func(*a,**b)
        return before



    @classmethod
    def strategy(backtest,func,*a,**b):
        print(dir(backtest))
        return func(backtest,*a,**b)
    @classmethod
    def end_trading(backtest,func,*a,**b):
        #yield backtest.cash
        return func(backtest,*a,**b)
    
    def exec_bid(self,bid):
        print(bid)
        self.cash+=bid
        

x=backtest()
@x.before_trading
def before_trading(backtest):
    print(backtest.cash)
    #backtest.test_mod='xxx'  如果在外部向框架注入变量 则不被允许
@backtest.backtest_init
def init_backtest(backtest):
    print(backtest.account)

@backtest.strategy
def handle_bar(backtest):
    print('x')
    print(backtest.cash)
    backtest.exec_bid(backtest,1000)
    print(backtest.account)
    #print(backtest.test_mod)   type object 'backtest' has no attribute 'test_mod'

"""
相当于是策略在外部 替换掉了框架内部的变量/函数

获取/改变

==> 策略获取回测时的状态
==> 策略改变回测时的状态


"""



if __name__=='__main__':
    before_trading
    handle_bar