
# coding: utf-8

# In[1]:


import QUANTAXIS as QA

import threading
import pandas as pd

import time


# In[2]:


# utf-8
import QUANTAXIS as QA

market = QA.QA_Market(if_start_orderthreading=True)
portfolio = QA.QA_Portfolio()
# 创建两个account
# 这里是创建一个资产组合,然后在组合里面创建两个account  你可以想象成股票里面的两个策略账户
# 然后返回的是这个账户的id
a_1 = portfolio.new_account()
a_1.reset_assets(100000000)
a_1.frequence = QA.FREQUENCE.ONE_MIN
market.start()
market._sync_orders()
market.connect(QA.BROKER_TYPE.BACKETEST)
market.login(QA.BROKER_TYPE.BACKETEST, a_1.account_cookie, a_1)

market.order_handler.monitor


# In[3]:


for code in ['000001', '000002', '000004', '600010', '000007', '600000']:
    market.insert_order(a_1.account_cookie, code=code,
                        price=0,
                        amount=1000,
                        time='2018-08-14 14:58:00',
                        towards=QA.ORDER_DIRECTION.BUY,
                        order_model=QA.ORDER_MODEL.MARKET,
                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT,
                        market_type=QA.MARKET_TYPE.STOCK_CN,
                        frequence=QA.FREQUENCE.ONE_MIN,
                        broker_name=QA.BROKER_TYPE.BACKETEST,
                        )


# In[4]:


print(market.trade_engine.queue.qsize())


# In[5]:


print(market.trade_engine.kernels_dict['ORDER'].queue.qsize())


# In[6]:


print(market.trade_engine.kernels_dict[QA.BROKER_TYPE.BACKETEST].queue.qsize())


# In[7]:


# ma


# In[8]:


# In[ ]:


# market.trade_engine.kernels_dict['ORDER'].queue.task_done()

market.settle_order()


# In[ ]:

market.trade_engine.join()
# market.trade_engine.kernels_dict['ORDER'].queue.join()

print(a_1.history_table)
# In[ ]:


# market.trade_engine.join()


# In[ ]:
