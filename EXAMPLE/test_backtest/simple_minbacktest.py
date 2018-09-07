
# coding: utf-8

# In[21]:


import QUANTAXIS as QA
import pandas as pd


# # 这是一个单独股票上30分钟  KDJ金叉死叉的简单回测的例子
# 
# 

# In[2]:


data=QA.QA_fetch_stock_min_adv('601318','2018-03-22','2018-08-23','30min')


# In[3]:


res=data.add_func(QA.QA_indicator_KDJ)
sig=QA.CROSS(res.KDJ_J,res.KDJ_K)
sig2=QA.CROSS(res.KDJ_K,res.KDJ_J)


# In[8]:


Account = QA.QA_Account(init_cash=100000,init_hold={},frequence=QA.FREQUENCE.THIRTY_MIN)
Broker = QA.QA_BacktestBroker()

Account.account_cookie = 'user_admin_macd'


# In[10]:


_date = None
for items in data.panel_gen:
    if _date != items.date[0]:
        print('try to settle')
        _date=items.date[0]
        Account.settle()
    
    for item in items.security_gen:
        if sig[item.index].iloc[0]>0:
            order=Account.send_order(
                code=item.code[0], 
                time=item.datetime[0], 
                amount=1000, 
                towards=QA.ORDER_DIRECTION.BUY, 
                price=0, 
                order_model=QA.ORDER_MODEL.CLOSE, 
                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                )
            Broker.receive_order(QA.QA_Event(order=order,market_data=item))
            trade_mes=Broker.query_orders(Account.account_cookie,'filled')
            res=trade_mes.loc[order.account_cookie,order.realorder_id]
            print('buy')
            order.trade(res.trade_id,res.trade_price,res.trade_amount,res.trade_time)
        elif sig2[item.index].iloc[0]>0:
            if Account.sell_available.get(item.code[0], 0)>0:
                order1=Account.send_order(
                    code=item.code[0], 
                    time=item.datetime[0],
                    amount=1000, 
                    towards=QA.ORDER_DIRECTION.SELL, 
                    price=0, 
                    order_model=QA.ORDER_MODEL.CLOSE, 
                    amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                Broker.receive_order(QA.QA_Event(order=order1,market_data=item))
                trade_mes=Broker.query_orders(Account.account_cookie,'filled')
                res=trade_mes.loc[order1.account_cookie,order1.realorder_id]
                print('sell')
                order1.trade(res.trade_id,res.trade_price,res.trade_amount,res.trade_time)


# In[12]:


Account.history_table


# In[14]:


r=QA.QA_Risk(Account)


# In[16]:


r.plot_assets_curve()


# In[18]:


r.profit_construct


# In[19]:


p=QA.QA_Performance(Account)


# In[20]:


p.pnl_fifo

