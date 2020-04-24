
# coding: utf-8

# In[2]:


import QUANTAXIS as QA


# In[4]:


AC=QA.QA_Account().from_message(QA.QA_fetch_account()[-1])


# In[6]:


pr=QA.QA_Performance(AC)


# In[8]:


pr.pnl_fifo


# In[11]:


pr.plot_pnlmoney(pr.pnl_fifo)


# In[12]:


pr.plot_pnlratio(pr.pnl_fifo)

