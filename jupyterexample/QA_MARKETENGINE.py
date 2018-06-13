
# coding: utf-8

import QUANTAXIS as QA
import threading
import pandas as pd


user = QA.QA_Portfolio()
# 创建两个account
#这里是创建一个资产组合,然后在组合里面创建两个account  你可以想象成股票里面的两个策略账户
#然后返回的是这个账户的id
a_1 = user.new_account()
a_2 = user.new_account()


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



"""
登陆到这个交易前置上 把你刚才的两个账户
"""
# 登陆交易
market.login(QA.BROKER_TYPE.BACKETEST,a_1)
market.login(QA.BROKER_TYPE.BACKETEST,a_2)
# 打印市场中的交易账户
print(market.get_account_id())




market.insert_order(account_id=a_1, amount=100000,price=None, amount_model=QA.AMOUNT_MODEL.BY_MONEY,time='2017-12-01', code='600010', 
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY,market_type=QA.MARKET_TYPE.STOCK_CN,
                   data_type=QA.FREQUENCE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)


market.insert_order(account_id=a_1, amount=100000,price=None, amount_model=QA.AMOUNT_MODEL.BY_MONEY,time='2017-12-01', code='000001', 
                    order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY,market_type=QA.MARKET_TYPE.STOCK_CN,
                   data_type=QA.FREQUENCE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)



# market.insert_order(account_id=a_2, amount=100000,price=None, amount_model=QA.AMOUNT_MODEL.BY_MONEY,time='2017-12-14', code='000001', 
#                     order_model=QA.ORDER_MODEL.CLOSE, towards=QA.ORDER_DIRECTION.BUY,market_type=QA.MARKET_TYPE.STOCK_CN,
#                    data_type=QA.FREQUENCE.DAY,broker_name=QA.BROKER_TYPE.BACKETEST)



print(market.session[a_1].cash_available)


# In[67]:


market.session[a_1].cash


# In[13]:


"""
这里是交易前置内部的订单队列
"""


# In[71]:


print(market.broker[QA.BROKER_TYPE.BACKETEST].order_handler.order_queue())


# In[15]:


market.broker[QA.BROKER_TYPE.BACKETEST].order_handler.order_queue.trade_list


# In[16]:


#pending 是指的待成交列表


# In[17]:


market.broker[QA.BROKER_TYPE.BACKETEST].order_handler.order_queue.pending


# In[49]:


"""
这个_trade是一个私有方法 只有模拟盘和回测才会有 实盘就是真的交易了 
这个_trade是backtest类去调用的

"""
market._trade(QA.QA_Event(broker_name=QA.BROKER_TYPE.BACKETEST,after_success=None))


# In[19]:


"""下面这两个是 查询  一个是异步查询 一个是同步的(no_wait)
异步不会阻塞当前线程 同步会阻塞"""


# In[20]:


market.query_data(broker_name=QA.BROKER_TYPE.BACKETEST,data_type=QA.FREQUENCE.DAY,market_type=QA.MARKET_TYPE.STOCK_CN,
                 code='600010',start='2017-12-01')


# In[21]:


#market.query_data_no_wait(broker_name=QA.BROKER_TYPE.BACKETEST,data_type=QA.FREQUENCE.DAY,market_type=QA.MARKET_TYPE.STOCK_CN,
                 #code='000001',start='2017-12-14')


# In[22]:


"""成交了以后 你可以看到账户的资产变化了"""
market.session[a_1]


# In[23]:


"""待成交列表被清空"""


# In[50]:


market.broker[QA.BROKER_TYPE.BACKETEST].order_handler.order_queue.pending


# In[25]:


"""待成交队列清空"""


# In[51]:


market.broker[QA.BROKER_TYPE.BACKETEST].order_handler.order_queue.trade_list


# In[27]:


market.broker[QA.BROKER_TYPE.BACKETEST].order_handler.order_queue()


# In[52]:


"""
cash 现金减少
"""
market.session[a_1].cash


# In[53]:


"""
因为没有触发每日结算时间 在T+1的市场 即使买入了也没有可卖的
"""
market.session[a_1].sell_available


# In[54]:


sa=market.session[a_1].sell_available


# In[40]:


ac=market.session[a_1]


# In[41]:


ac.hold


# In[42]:


sa


# In[44]:


market.session[a_1].history


# In[55]:


"""
持仓表增加
"""
market.session[a_1].hold


# In[58]:


"""
账户信息

可以看到 减少的资产 主要是因为收了手续费
"""
market.session[a_1].message


# In[61]:


"""结算事件"""
market._settle(QA.BROKER_TYPE.BACKETEST)


# In[62]:


"""
结算完以后 可卖数量就会变成和持仓数一样
"""
market.session[a_1].sell_available


# In[37]:


"""
结算完以后 待成交队列也被清空
"""



# In[60]:


market.broker[QA.BROKER_TYPE.BACKETEST].order_handler.order_queue()

