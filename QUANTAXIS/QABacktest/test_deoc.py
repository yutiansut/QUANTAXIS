# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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