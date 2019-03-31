# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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


from multiprocessing import Pool, cpu_count


class Parallelism(object):
    """ 多进程map类
        pl = ParallelSim()
        pl.add(yourFunc, yourIter)
        data = pl.get_results()
        data = list(data)
        print(data)
    """

    def __init__(self, processes=cpu_count()):
        '''

        :param processes: 进程数量，默认为cpu个数
        '''
        self.pool = Pool(processes=processes)
        self.total_processes = 0
        self.completed_processes = 0
        self.results = []
        self.data = None
        self.cores = processes  # cpu核心数量

    def add(self, func, iter):
        if isinstance(iter, list) and self.cores > 1 and len(iter) > self.cores:
            for i in range(self.cores):
                pLen = int(len(iter) / self.cores) + 1
                self.data = self.pool.starmap_async(func, iter[int(i * pLen):int((i + 1) * pLen)],
                                                    callback=self.complete,
                                                    error_callback=self.exception)
                self.total_processes += 1
        else:
            self.data = self.pool.starmap_async(func=func, iterable=iter, callback=self.complete,
                                                error_callback=self.exception)
            self.total_processes += 1
        # self.data.get()

    def complete(self, result):
        self.results.extend(result)
        self.completed_processes += 1
        print('Progress: {:.2f}%'.format((self.completed_processes / self.total_processes) * 100))

    def exception(self, exception = None):
        print(exception)

    def run(self):
        self.data.get()
        self.pool.close()
        self.pool.join()

    def get_results(self):
        return self.results
