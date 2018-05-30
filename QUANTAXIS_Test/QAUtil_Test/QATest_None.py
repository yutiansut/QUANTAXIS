import unittest

import sys
import time
import datetime
import random

#from QUANTAXIS.QAFetch import (QATdx );
from QUANTAXIS.QAUtil import (QADate, QADate_trade );

#from pandas import Series
import pandas as pd
import matplotlib as mpl

#学习 lru_cache
class MyCache:
    '''

    '''
    def __init__(self):
        '''constructor'''
        self.cache = {}
        self.max_cache_size = 10

    def __contains__(self, key):
        '''
        根据该键是否存在于缓存当中返回True或者False
        :param key:
        :return:
        '''
        return key in self.cache

    def update(self, key, value):
        '''
         更新该缓存字典，您可选择性删除最早条目
        :param key:
        :param value:
        :return:
        '''
        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()
        self.cache[key] = { 'date_accessed': datetime.datetime.now(), 'value': value}

    def remove_oldest(self):
        """
        删除具备最早访问日期的输入数据
        """
        oldest_entry = None

        for key in self.cache:
            if oldest_entry == None:
                oldest_entry = key
                print('assign oldest_entry key',oldest_entry)
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key
                print('delete oles key',oldest_entry)

        self.cache.pop(oldest_entry)

    @property
    def size(self):
        """
        返回缓存容量大小
        """
        return len(self.cache)



class Test_QA_None(unittest.TestCase):

    def test_LRU(self):
        # 测试缓存
        keys = ['test', 'red', 'fox', 'fence', 'junk', \
                'other7', 'alpha8', 'bravo9', 'cal10', 'devo11', 'ele12',
                'other1', 'alpha2', 'bravo3', 'cal4', 'devo5', 'ele6',
                ]
        s = 'abcdefghijklmnop'
        cache = MyCache()
        for i, key in enumerate(keys):
            if key in cache:
                continue
            else:
                value = ''.join([random.choice(s) for i in range(20)])
                cache.update(key, value)
            print("#%s iterations, #%s cached entries" % (i + 1, cache.size))
        pass


    def fab(self,max):
        n, a, b = 0, 0, 1
        while n < max:
            print (b)
            a, b = b, a + b
            n = n + 1

    def test_Generator(self):
        self.fab(10)

    def test_None(self):

        print("----------------------------")
        obj = pd.Series([3,4,-2,2])
        print(obj)


        pd.Series([1, 23, 4]).plot()

        #now = QADate.QA_util_time_now()
        #print( type(now) )

        #today = QADate.QA_util_date_today()
        #print( type(today))

        #print("okok---> do the task")

        # for i in range(101):
        #     s1 = "\r%d%%[%s%s]" % (i, "*" * i, " " * (100 - i))
        #     time.sleep(1)
        #     sys.stdout.write(s1)
        #     sys.stdout.flush()
        # pass


