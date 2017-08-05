# coding:utf-8

# strategy warpper


class QA_Strategy():
    def __init__(self):
        self.strategy_list = {}

    def before_strategy_exec(self):
        print('before')
        pass

    def after_strategy_exec(self):
        print('after')
        pass



    @classmethod
    def strategy_init(clcs, func, *arg, **kwargs):

        


        def __init( *arg, **kwargs):
            clcs.strategy_type='0x01'


    @classmethod
    def strategy_loader(clcs, func, *arg, **kwargs):
        def __load(*arg, **kwargs):
            clcs.before_strategy_exec(clcs)
            func(*arg, **kwargs)
            clcs.after_strategy_exec(clcs)

        return __load

    def exec_strategy(self):
        pass


if __name__ == '__main__':




    class strategy():

        @QA_Strategy.strategy_init
        def strategy_init(self):
            pass
        @QA_Strategy.strategy_loader
        def data_handle(self,a,v):
            print(a)

    strategy(1,2)