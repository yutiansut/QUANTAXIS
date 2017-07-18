# coding:utf-8
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.pool import Pool

def QA_util_MP_thread(num):
    pool=ThreadPool(num)
    return pool
def QA_util_MP_process(num):
    pool=Pool(num)
    return pool