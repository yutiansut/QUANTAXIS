
# coding: utf-8

# In[1]:


import QUANTAXIS as QA
from QUANTAXIS.QAMarket import QA_Market
from QUANTAXIS.QAMarket.QAShipaneBroker import  QA_SPEBroker
from QUANTAXIS.QAMarket.QABacktestBroker import  QA_BacktestBroker
from concurrent import  futures
import threading
import asyncio

import datetime
import pandas as pd


# In[3]:


market = QA_Market(if_start_orderthreading=True)


# In[4]:


market.start()


# In[5]:



market.connect(QA.BROKER_TYPE.SHIPANE)


# In[6]:


market.login(QA.BROKER_TYPE.SHIPANE,'account:1391')


# In[7]:


market.login(QA.BROKER_TYPE.SHIPANE,'account:141')


# In[8]:


market.login(QA.BROKER_TYPE.SHIPANE,'account:813')


# In[9]:


market.get_account_cookie()


# In[10]:


#data
market._sync_orders()


# In[12]:


market.order_handler.order_status


# In[13]:


market.order_handler.deal_status

