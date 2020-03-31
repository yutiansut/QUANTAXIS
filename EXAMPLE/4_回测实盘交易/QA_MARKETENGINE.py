#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'EXAMPLE\QAMARKET 相关'))
	print(os.getcwd())
except:
	pass

#%%
import QUANTAXIS as QA
import threading
import pandas as pd


#%%
user = QA.QA_User(username='admin',password='940809x')
portfolio = user.new_portfolio('example')
# 创建两个account
#这里是创建一个资产组合,然后在组合里面创建两个account  你可以想象成股票里面的两个策略账户
#然后返回的是这个账户的id
a_1 = portfolio.new_account(account_cookie='a1')
a_2 = portfolio.new_account(account_cookie='a2')


#%%
a_1


#%%
"""
然后这里 是创建一个交易前置  你可以理解成 创建了一个无界面的通达信客户端
然后start()开启这个客户端
连接到backtest的broker上 这个broker可以更换
"""
# 创建一个交易前置
market = QA.QA_Market()
# 交易前置连接broker 
market.start()
market.connect(QA.RUNNING_ENVIRONMENT.BACKETEST)

# 打印market
print(market)


#%%

"""
登陆到这个交易前置上 把你刚才的两个账户
"""
# 登陆交易
market.login(QA.BROKER_TYPE.BACKETEST,a_1.account_cookie, a_1)
market.login(QA.BROKER_TYPE.BACKETEST,a_2.account_cookie, a_2)
# 打印市场中的交易账户
print(market.get_account_cookie())


#%%
#然后这里 往交易前置里面添加订单 这个操作是异步的


#%%
market.insert_order(account_cookie=a_1.account_cookie, money=100000, amount=None,price=None, amount_model=QA.AMOUNT_MODEL.BY_MONEY,time='2017-12-01', code='600010', 
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY,market_type=QA.MARKET_TYPE.STOCK_CN,
                   frequence=QA.FREQUENCE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)


#%%
market.insert_order(account_cookie=a_1.account_cookie, amount=100,price=None, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT,time='2017-12-01', code='000001', 
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY,market_type=QA.MARKET_TYPE.STOCK_CN,
                   frequence=QA.FREQUENCE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)


#%%
#
"""
下单以后 现金不会减少 但是可用现金会被扣除
因为如果是市价单 你的成交价未定
没法直接减少现金
可用现金减少 cash不减少 等到settle 等到成功交易的时候 才会扣cash

"""


#%%
market.session[a_1.account_cookie].cash_available


#%%
market.session[a_1.account_cookie].cash


#%%
"""
这里是交易前置内部的订单队列
"""


#%%
market.order_handler.order_queue()




#%%
market.order_handler.order_queue.order_list


#%%
#pending 是指的待成交列表


#%%
market.order_handler.order_queue.pending


#%%
"""
这个_trade是一个私有方法 只有模拟盘和回测才会有 实盘就是真的交易了 
这个_trade是backtest类去调用的

"""
#market._trade(QA.QA_Event(broker_name=QA.BROKER_TYPE.BACKETEST,after_success=None))


#%%
"""下面这两个是 查询  一个是异步查询 一个是同步的(no_wait)
异步不会阻塞当前线程 同步会阻塞"""


#%%
market.query_data(broker_name=QA.BROKER_TYPE.BACKETEST,frequence=QA.FREQUENCE.DAY,market_type=QA.MARKET_TYPE.STOCK_CN,
                 code='600010',start='2017-12-01')


#%%
market.query_data_no_wait(broker_name=QA.BROKER_TYPE.BACKETEST,frequence=QA.FREQUENCE.DAY,market_type=QA.MARKET_TYPE.STOCK_CN,
                 code='000001',start='2017-12-14')


#%%
"""成交了以后 你可以看到账户的资产变化了"""
market.session[a_1.account_cookie]


#%%
"""待成交列表被清空"""


#%%
market.order_handler.order_queue.pending


#%%
"""待成交队列清空"""


#%%
market.order_handler.order_queue.order_list


#%%
market.order_handler.order_queue()


#%%
"""
cash 现金减少
"""
market.session[a_1.account_cookie].cash


#%%
"""
因为没有触发每日结算时间 在T+1的市场 即使买入了也没有可卖的
"""
market.session[a_1.account_cookie].sell_available


#%%
sa=market.session[a_1.account_cookie].sell_available


#%%
ac=market.session[a_1.account_cookie]


#%%
ac.hold


#%%
sa


#%%
market.session[a_1.account_cookie].history


#%%
"""
持仓表增加
"""
market.session[a_1.account_cookie].hold


#%%
"""
账户信息

可以看到 减少的资产 主要是因为收了手续费
"""
market.session[a_1.account_cookie].message


#%%
"""结算事件"""
market._settle(QA.BROKER_TYPE.BACKETEST)


#%%
"""
结算完以后 可卖数量就会变成和持仓数一样
"""


#%%
market.session[a_1.account_cookie].hold


#%%
market.session[a_1.account_cookie].sell_available


#%%
"""
结算完以后 待成交队列也被清空
"""


#%%
market.order_handler.order_queue()


#%%
market.insert_order(account_cookie=a_1.account_cookie, amount=market.session[a_1.account_cookie].sell_available.get('600010',0),price=None, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT,time='2017-12-05', code='600010', 
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.SELL,market_type=QA.MARKET_TYPE.STOCK_CN,
                   frequence=QA.FREQUENCE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)


#%%
market.order_handler.order_queue.order_list


#%%
market.order_handler.order_queue()


#%%
market.session[a_1.account_cookie].sell_available


#%%
#market._trade(QA.QA_Event(broker_name=QA.BROKER_TYPE.BACKETEST,after_success=None))


#%%
market.session[a_1.account_cookie].cash


#%%
market.session[a_1.account_cookie].history


#%%
ac.save()


