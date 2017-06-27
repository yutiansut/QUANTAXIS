#coding:utf-8

import random
def predict(market,hold):
    """
    一个极其简单的示例策略,如果空仓则买入,如果有仓位就卖出
    """
    if hold==0:
        dat=random.random()
        if dat>0.5:
        
            return {'if_buy':1}
        else :
            return {'if_buy':0}
    else:
        dat=random.random()
        if dat>0.5:
            return {'if_buy':1}
        else :
            return {'if_buy':0}
