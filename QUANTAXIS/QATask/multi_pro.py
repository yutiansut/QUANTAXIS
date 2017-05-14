# coding:utf-8

# %%
import multiprocessing
import threading
import time,sys,datetime,json
import pymongo,redis
from six.moves import queue 


# %%
que=queue.Queue()
que.put(19)
que.put(23)

# %% 
que.get()