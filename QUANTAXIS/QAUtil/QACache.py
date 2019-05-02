#coding=utf-8

from time import time
from QUANTAXIS.QAUtil.QASingleton import singleton

@singleton
class QA_util_cache:
    '''简单的缓存系统
    把这个变量保存在内存里, 同时给它一个过期时间, 过期则失效.
    '''
    def __init__(self):
        '''初始化'''
        self.mem = {}
        self.time = {}

    def set(self, key, data, age=-1):
        '''保存键为key的值，存活时间为age秒'''
        self.mem[key] = data
        if age == -1:
            self.time[key] = -1
        else:
            self.time[key] = time() + age
        return True

    def get(self,key):
        '''获取键key对应的值'''
        if key in self.mem.keys():
            if self.time[key] == -1 or self.time[key] > time():
                return self.mem[key]
            else:
                self.delete(key)
                return None
        else:
            return None

    def delete(self,key):
        '''删除键为key的条目'''
        del self.mem[key]
        del self.time[key]
        return True

    def clear(self):
        '''清空所有缓存'''
        self.mem.clear()
        self.time.clear()

