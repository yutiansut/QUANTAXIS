# coding:utf-8



class backtest():
    cash=10000
    def __init__(self,):
        pass
    
    @classmethod
    def before_backtest(backtest,func,*a,**b):
        #yield backtest.cash
        return func(backtest,*a,**b)

    
    @classmethod
    def before_trading(backtest,func,*a,**b):
        #yield backtest.cash
        return func(backtest,*a,**b)



    @classmethod
    def strategy(backtest,func,*a,**b):
        
        return func(backtest,*a,**b)
    @classmethod
    def end_trading(backtest,func,*a,**b):
        #yield backtest.cash
        return func(backtest,*a,**b)
    
    def exec_bid(self,bid):
        print(bid)
        self.cash+=bid
        


        
@backtest.before_trading
def before_trading(backtest):
    print(backtest.cash)


@backtest.strategy
def handle_bar(backtest):
    print('x')
    print(backtest.cash)
    backtest.exec_bid(backtest,1000)
    print(backtest.cash)


if __name__=='__main__':
    before_trading
    handle_bar