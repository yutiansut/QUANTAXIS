#coding:utf-8
def predict(market,hold):
    """
    一个极其简单的示例策略,如果空仓则买入,如果有仓位就卖出
    """
    if hold==0:
        return {'if_buy':1}
    else:
        return {'if_buy':0}


