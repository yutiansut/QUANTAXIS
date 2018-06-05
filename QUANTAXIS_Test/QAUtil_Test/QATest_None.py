import datetime
import random
import sys
import time
import unittest

import matplotlib as mpl
#from pandas import Series
import pandas as pd

#from QUANTAXIS.QAFetch import (QATdx );
from QUANTAXIS.QAUtil import QADate, QADate_trade

# 学习 lru_cache


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
        self.cache[key] = {
            'date_accessed': datetime.datetime.now(), 'value': value}

    def remove_oldest(self):
        """
        删除具备最早访问日期的输入数据
        """
        oldest_entry = None

        for key in self.cache:
            if oldest_entry == None:
                oldest_entry = key
                print('assign oldest_entry key', oldest_entry)
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key
                print('delete oles key', oldest_entry)

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
        keys = ['test', 'red', 'fox', 'fence', 'junk',
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

    def fab(self, max):
        n, a, b = 0, 0, 1
        while n < max:
            print(b)
            a, b = b, a + b
            n = n + 1

    def test_Generator(self):
        self.fab(10)

    def test_None(self):

        print("----------------------------")
        obj = pd.Series([3, 4, -2, 2])
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

    def test_make_Series(self):
        # demo the series
        obj = pd.Series([1, 2, 3, 4])
        print(obj.index)
        print(obj.values)
        print("-------------------------------------------")
        obj2 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
        print(obj2)
        print(obj2.index)
        print(obj2.values)
        print("-------------------------------------------")
        # another way to think about a Series is as a fixed-length, ordered dict, as it is a mapping of index value to data values.
        # it can be substituted into many functions that expect a dict
        sdata = {'Ohio': 3000, 'Texas': 71000, 'Oregon': 1600, 'Utah': 5000}
        obj4 = pd.Series(sdata)
        print(obj4)
        print("-------------------------------------------")
        state = ['California', 'Ohio', 'Oregon', 'Taxes']
        obj4 = pd.Series(sdata, index=state)
        print(obj4)
        print("-------------------------------------------")
        print(pd.isnull(obj4))
        print("-------------------------------------------")
        print(pd.notnull(obj4))
        print("-------------------------------------------")

        obj_01 = pd.Series([1, 2, 3, 4])
        obj_o2 = pd.Series([11, 22, 33, 44], index=['aa', 'bb', 'cc', 'dd'])
        obj_03 = pd.Series([55, 66, 77, 88], index=['bb', 'cc', 'dd', 'ee'])
        print(obj_01)
        print(obj_o2)
        print("-------------------------------------------")
        print(obj_01 + obj_o2)
        print("-------------------------------------------")
        print(obj_o2 + obj_03)

    def test_make_dataframe(self):
        # the dataframe has both a row and column index
        dict_data = {
            'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002],
            'pop': [1.4, 1.7, 3.6, 2.4, 2.9]
        }

        frame = pd.DataFrame(dict_data)
        print(frame)
        print("-------------------------------------------")

        frame2 = pd.DataFrame(dict_data, columns=[
                              'year', 'state', 'pop', 'area'])
        print(frame2)
        print("-------------------------------------------")

        print(frame2.index)
        print("-------------------------------------------")

        print(frame2.ix[0])
        print("-------------------------------------------")

        print(frame2.iloc[0])

        print("-------------------------------------------")
        print(frame2.loc[[0]])
        print("-------------------------------------------")

        print(frame2.T)
        print("-------------------------------------------")

        pop = {'Nevada': {2001: 2.4, 2002: 2.9},
               "Ohio": {2000: 1.4, 2000: 1.7, 2002: 3.4}}
        frame3 = pd.DataFrame(pop)
        print(frame3)
