#coding:utf-8
# %%
import QUANTAXIS as QA
import pymongo


# 下面都是对应的bug问题
# 复现Backtest_info的情景
# In[1]
stock_code='600358'
account_cookie='0.6269804593455515'

# %%
client=pymongo.MongoClient().quantaxis
coll_info=client.backtest_info
coll_history=client.backtest_history
coll_stock_day=client.stock_day
coll_stock_info=client.stock_info
coll_stock_list=client.stock_list

# %%

print(coll_info.find_one({'account_cookie':account_cookie}))
print(coll_history.find({'cookie':account_cookie}[0]))