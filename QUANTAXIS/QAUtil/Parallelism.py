# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from abc import ABCMeta
from multiprocessing import Pool, cpu_count
import time
from concurrent.futures import ThreadPoolExecutor


class Parallelism_abs(object, metaclass=ABCMeta):
    def __init__(self, processes=cpu_count()):
        '''

        :param processes: 进程数量，默认为cpu个数
        '''
        self.total_processes = 0
        self.completed_processes = 0
        self.results = []
        self.data = []
        self.cores = processes  # cpu核心数量
        self._loginfolist = []  # 保存打印信息

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        print(self.__dict__)
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        print(state)
        self.__dict__.update(state)

    def get_results(self):
        return self.results

    def complete(self, result):
        self.results.extend(result)
        self.completed_processes += 1
        print('Progress: {:.2f}%'.format(
            (self.completed_processes / self.total_processes) * 100))


class Parallelism(Parallelism_abs):
    """ 多进程map类
        pl = ParallelSim()
        pl.run(yourFunc, yourIter)
        data = pl.get_results()
        data = list(data)
        print(data)
    """

    def __init__(self, processes=cpu_count()):
        super(Parallelism, self).__init__(processes)
        self.pool = Pool(processes=processes)

    def run(self, func, iter):
        if isinstance(iter, list) and self.cores > 1 and len(
                iter) > self.cores:
            j = self.cores
            for i in range(j):
                pLen = int(len(iter) / j) + 1
                self.data.append(
                    self.pool.starmap_async(func,
                                            iter[i * pLen:(i + 1) * pLen],
                                            callback=self.complete,
                                            error_callback=self.exception))
                self.total_processes += 1
        else:
            self.data.append(
                self.pool.starmap_async(func=func,
                                        iterable=iter,
                                        callback=self.complete,
                                        error_callback=self.exception)
            )
            self.total_processes += 1
        for i in range(self.total_processes):
            try:
                while not self.data[i].ready():
                    time.sleep(0.5)
                self.data[i].get()
            except Exception as e:
                print(e.args)
        self.pool.close()
        self.pool.join()

    def exception(self, exception=None):
        print(exception)


class Parallelism_Thread(Parallelism_abs):
    """ 多线程map类
        pl = ParallelSim()
        pl.run(yourIter)
        data = list(data)
        print(data)
    """

    def __init__(self, processes=cpu_count()):
        super(Parallelism_Thread, self).__init__(processes)
        self.pool = ThreadPoolExecutor(self.cores)


    def run(self, iter):
        ''' 使用concurrent.futures import ThreadPoolExecutor线程

        :param iter:
        :return:
        '''
        if isinstance(iter, list) and self.cores > 1 and \
                len(iter) > self.cores:
            j = self.cores
            for i in range(j):
                pLen = int(len(iter) / j) + 1
                self.data.append(
                    self.pool.map(self.do_working,
                                  iter[i * pLen:(i + 1) * pLen]))
                self.total_processes += 1
        else:
            self.data.append(self.pool.map(self.do_working, iter))
            self.total_processes += 1
        for i in range(self.total_processes):
            adata = list(self.data[i])
            print('{} SAVED: {}'.format(len(adata), adata))
            self.complete(adata)

    def do_working(self, code):
        raise Exception('你要在子类中实现此方法!')
