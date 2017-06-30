#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
import threading
from threading import Thread
from six.moves import queue
"""
标准化的QUANATAXIS队列,可以快速引入和复用
"""


class QA_Queue(threading.Thread):
    '这个是一个能够复用的多功能生产者消费者模型'
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_stop = False
        self.__type:dict
    def __QA_queue_distribute(self):
        pass
    def __QA_queue_job_register(self):
        pass
    def __QA_queue_put(self,args):
        return self.queue.put()

    def __QA_queue_pop(self):
        return self.queue.get()

    def __QA_queue_status(self):
        return self.queue.qsize()

    def run(self):
        while not self.thread_stop:
            print("thread%d %s: waiting for tast" % (self.ident, self.name))
            try:
                task = q.get(block=True, timeout=20)  # 接收消息
            except Queue.Empty:
                print("Nothing to do!i will go home!")
                self.thread_stop = True
                break
            print("task recv:%s ,task No:%d" % (task[0], task[1]))
            print("i am working")
            time.sleep(3)
            print("work finished!")
            q.task_done()  # 完成一个任务
            res = q.qsize()  # 判断消息队列大小
            if res > 0:
                print("fuck!There are still %d tasks to do" % (res))

    def stop(self):
        self.thread_stop = True

