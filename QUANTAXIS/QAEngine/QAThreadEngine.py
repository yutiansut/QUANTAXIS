# coding:utf-8

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

import datetime
import threading
import time
from queue import Queue

from QUANTAXIS.QAEngine.QATask import QA_Task
from QUANTAXIS.QAUtil import QA_util_log_info, QA_util_random_with_topic


"""标准化的QUANATAXIS事件分发,可以快速引入和复用
每个事件需要携带一个方法,并且是需要立即被执行的时间才能使用这个事件方法"""


class QA_Thread(threading.Thread):
    '''
        '这是一个随意新建线程的生产者消费者模型'
        其实有个队列， 队列中保存的是 QA_Task 对象 ， callback 很重要，指定任务的时候可以绑定 函数执行
        QA_Engine 继承这个类。
    '''

    def __init__(self, queue=None, name=None):
        threading.Thread.__init__(self)
        self.queue = Queue() if queue is None else queue
        self.thread_stop = False
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        self.name = QA_util_random_with_topic(topic='QA_Thread', lens=3) if name is None else name
        self.idle = False

    def __repr__(self):
        return '<QA_Thread{}  id={}>'.format(self.name, id(self))

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            while not self.thread_stop:
                '这是一个阻塞的队列,避免出现消息的遗漏'
                try:
                    if self.queue.empty() is False:
                        _task = self.queue.get()  # 接收消息
                        assert isinstance(_task, QA_Task)
                        if _task.worker != None:

                            _task.do()

                            self.queue.task_done()  # 完成一个任务
                        else:
                            pass
                    else:
                        self.idle = True
                except Exception as e:
                    pass

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        # self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()
        self.thread_stop = True        # 设置为False

    def __start(self):
        self.queue.start()

    def put(self, task):
        self.queue.put(task)

    def put_nowait(self, task):
        self.queue.put_nowait(task)

    def get(self, task):
        return self.get(task)

    def get_nowait(self, task):
        return self.get_nowait(task)

    def qsize(self):
        return self.queue.qsize()


class QA_Engine(QA_Thread):
    '''
        QA_Thread的区别是，
        QA_Thread 只是单纯一个线程，里面有个队列执行 QA_Task 的do 方法

        QA_Engine 有 kernels_dict词典，可以指定 {名字：QA_Thread}，
        QA_Engine自己有一个线程可以 遍历kernels_dict中QA_Thread 中的多个线程去执行

        kernel 已更正(之前误写成kernal) @2018/05/28
    '''
    def __init__(self, queue=None, *args, **kwargs):
        super().__init__(queue=queue, name='QA_Engine')
        self.kernels_dict = {}
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def __repr__(self):
        return ' <QA_ENGINE with {} kernels>'.format(list(self.kernels_dict.keys()))

    @property
    def kernel_num(self):
        return len(self.kernels_dict.keys())

    def create_kernel(self, name):
        # ENGINE线程创建一个事件线程
        self.kernels_dict[name] = QA_Thread(name=name)

    def register_kernel(self, name, kernel):
        if name not in self.kernels_dict.keys():
            self.kernels_dict[name] = kernel

    def start_kernel(self, name):
        self.kernels_dict[name].start()

    def stop_kernel(self, name):
        self.kernels_dict[name].stop()
        del self.kernels_dict[name]

    def run_job(self, task):
        '''
        把QA_Task 放到 kerneals_dict 词典中的task.engine 名字， 对应的 QA_Thread中的队列中，
        :param task:  type str 字符串
        :return: None
        '''
        # todo 建议把 engine 变量名字 改成  engine_in_kerneals_dict_name, 便于理解
        self.kernels_dict[task.engine].put(task)

    def stop_all(self):
        for item in self.kernels_dict.values():
            item.stop()
        self.kernels_dict = {}

    def stop(self):
        # self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()
        self.thread_stop = True

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            while not self.thread_stop:
                '这是一个阻塞的队列,避免出现消息的遗漏'
                try:
                    if self.queue.empty() is False:
                        _task = self.queue.get()  # 接收消息
                        #print("queue left %d"%self.queue.qsize())
                        assert isinstance(_task, QA_Task)
                        #print(_task)

                        # todo 建议把 engine 变量名字 改成  engine_in_kerneals_dict_name, 便于理解
                        if _task.engine is None:  # _task.engine 是字符串，对于的是 kernels_dict 中的 线程对象
                            # 如果不指定线程 就在ENGINE线程中运行
                            _task.do()
                            self.queue.task_done()
                        else:
                            # 把当前任务，用_task.engin名字对应的  kernels_dict 线程去执行
                            self.run_job(_task)
                            self.queue.task_done()
                    else:
                        self.idle = True
                except Exception as e:
                    raise e
                    # self.run()

    def clear(self):
        res = True
        for item in self.kernels_dict.values():
            if not item.queue.empty():
                res = False
            if not item.idle:
                res = False

            item.queue.join()
        if not self.queue.empty():
            res = False

        return res

    def join(self):
        for item in self.kernels_dict.values():
            item.queue.join()
        self.queue.join()


if __name__ == '__main__':
    import queue
    q = queue.Queue()
