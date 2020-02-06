import datetime
import random
import sys
import time
import unittest

import matplotlib as mpl
#from pandas import Series
import pandas as pd

import numpy as np
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import subprocess

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

        # index
        # Int64Index
        # MultiIndex
        # DatetimeIndex
        # PeriodIndex

        obj = pd.Series(range(3), index = ['a','b','c'])
        index = obj.index
        print(index)
        print(index[:1])

        obj2 = pd.Series(range(6,9,1), index = ['d','e','f'])

        #index append index
        print(obj2)
        newIndex = obj.index.append( obj2.index  )
        print(newIndex)


        print(obj)

        pass

    def test_essential_functionality(self):
        obj = pd.Series([4.5, 7.22, -5.3, 3.88], index=['d','e','a','c'])
        print(obj)
        obj = obj.reindex(['a','b','c','d','e'])
        print(obj)

        obj3 = pd.Series(['blue','purple','yellow'], index = [0,2,4])
        print(obj3)
        obj4 = obj3.reindex( range(6), method='ffill' )
        print(obj4)

        frame2 = pd.DataFrame(np.arange(9).reshape((3,3)), index = ['a','c','d'], columns=['Ohio','Texas','California'])
        print(frame2)

        states = ['Texas', 'Utah', 'California']
        frame2.ix[['a', 'b', 'c', 'd'], states]
        print(frame2)
        pass

    def test_dropping_entire(self):
        obj = pd.Series(np.arange(5.), index=['a','b','c','d','e'])
        # new_obj = obj.drop('c')
        # print(obj)
        # print(new_obj)
        #
        # new_obj2 = obj.drop(['d','c'])
        # print(new_obj2)
        #
        # new_obj3 = pd.Series(np.arange(5.), index=['a','b','c','d','es'])
        # print(new_obj3)
        # print(new_obj3['b'])

        data = pd.DataFrame(np.arange(16).reshape((4,4)), index=['Ohio','Colorado','Utha','New York'], columns=['one','two','three','four'])
        # d2=data.drop(['Colorado','Ohio'])
        # print(d2)
        #
        # d3=data.drop(['two','three'],axis=1)
        # print(d3)
        #
        # d4 = data.drop(['Ohio'], axis=0)
        # print(d4)
        #
        # pp = data.ix['Colorado', ['two', 'three']]
        # print(pp)
        ppp = data['two']
        print(ppp)
        kkk = data[0:2]
        print(kkk)

        jjj = data.ix['Colorado']
        print(jjj)

        jjjj = data.iloc[[0,1,2]]
        print(jjjj)

        cccc = data.loc[['Utha']]
        print(cccc)


    def test_Arithmetic_data_Alignment(self):

        s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
        s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
        print(s1+s2)

        df1 = pd.DataFrame(np.arange(9.0).reshape((3,3)), columns=list('bcd'), index=['Ohio','Texas','Colorado'])
        print(df1)
        df2 = pd.DataFrame(np.arange(12.).reshape((4,3)), columns=list('bde'), index=['Utah','Ohio','Texas','Oregon'])
        print(df2)
        print(df1+df2)

        print(df1.add(df2,fill_value=0))

    def test_Function_application_and_Mapping(self):
        


        pass

    def test_data_reader(self):
        # PG = wb.DataReader('PG', data_source = 'quandl', start="1995-1-1")
        # head0 = PG.head()
        # tail0 = PG.tail()
        # print(head0)
        # print(tail0)
        pass


class Test_sub_process_0(unittest.TestCase):
    def testRunSub(self):
        p = subprocess.Popen('cat', stdin=subprocess.PIPE)
        # for x in self.xrange(100):
        p.stdin.write(b'Line number %d.\n' % 1)
        p.stdin.write(b'Line number %d.\n' % 1)

        p.stdin.write(b'Line number %d.\n' % 1)
        p.stdin.write(b'Line number %d.\n' % 1)

        p.stdin.close()
        p.wait()

