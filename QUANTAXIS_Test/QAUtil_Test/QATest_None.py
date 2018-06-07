import datetime
import random
import sys
import time
import unittest

import matplotlib as mpl
#from pandas import Series
import pandas as pd

'''
 这个文件的代码 都是 实验性质的。 scribble code！
'''

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

class Test_LRU(unittest.TestCase):
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
        pass

class Test_DataFrame_0(unittest.TestCase):
    def test_make_Series(self):
        pass


    def test_make_dataframe(self):
        '''
        possible data inputs to dataframe constructor
        2d ndarray
        dict of array, list, or tuples
        numpy stuctured / record array
        dict of series
        dict of dict
        list of dict or series
        list of list or tuples
        another DataFrame
        Numpy masked
        :return:
        '''


        # demo the dict of dict
        self.pop = {'Nevada': {2001:2.4, 2002:2.9}, 'Ohio': {2000:1.5, 2001:1.7, 2002:6.6}}
        frame3 = pd.DataFrame(self.pop)
        print(frame3)

        frame3 = pd.DataFrame(self.pop, index=[2000, 2001, 2002])
        print(frame3)

        frame3 = pd.DataFrame(self.pop, index = [2000,2001, 2002, 2003])
        print(frame3)

        pass



    def test_assign_serial_to_data_frame(self):

        # when you assign list or arrays to columns, the value's length must match the length of the DataFrame.
        self.data = {
            'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
            'year': [2000, 2001, 2002, 2001, 2002],
            'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
        }

        frame2 = pd.DataFrame(self.data,
                              columns=['year', 'state', 'pop', 'debt'],
                              index = ['one', 'two', 'three', 'four','five'])

        val = pd.Series([-1.2,-1.5,-1.7,None], index=['two','four','five1','ss'])
        frame2['debt'] = val
        print(frame2)

        frame2['eastern'] = frame2.state == 'Ohio'
        print(frame2)
        del frame2['eastern']
        print(frame2)

        pass



    def test_index_object(self):
        #pandas's index objects are responsible for holding the axis labels nd other metadata ( like the axis name or names)
        obj = pd.Series(range(3), index = ['a','b','c'])
        index = obj.index
        print(index)
        print(index[:1])

        pass
