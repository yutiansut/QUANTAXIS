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
import csv
import datetime
import json
import threading
import time
from threading import Thread


from QUANTAXIS.QAUtil import (QA_util_log_debug, QA_util_log_expection,
                              QA_util_log_info)
from six.moves import queue


"""
标准化的QUANATAXIS事件分发,可以快速引入和复用

每个事件需要携带一个方法,并且是需要立即被执行的时间才能使用这个事件方法
"""

def now_time(func):
    QA_util_log_info("From Engine %s"%str(threading.current_thread())+str(datetime.datetime.now()))
    QA_util_log_info('FROM QUANTAXIS SYS== now running '+str(len(threading.enumerate()))+' threads')
    func

class QA_Queue(threading.Thread):
    '这个是一个能够复用的多功能生产者消费者模型'

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_stop = False
        self.__type: dict

    def __QA_queue_distribute(self):
        pass

    def QA_queue_job_register(self, __job: dict):
        '首先对于任务进行类型判断,输入的job的类型一定是一个dict模式的,同时需要含有一个type的K-V对'
        assert type(__job) == dict
        assert type(__job['type']) == str
        

    def __QA_queue_put(self, args):
        return self.queue.put()
        
    @now_time
    def __QA_queue_pop(self, block=True, timeout=20):

        return self.queue.get()

    def __QA_queue_status(self):
        return self.queue.qsize()

    
    def run(self):
        while not self.thread_stop:
            '这是一个阻塞的队列,避免出现消息的遗漏'

            try: 
                if self.queue.empty() is False:
                    task = self.__QA_queue_pop()  # 接收消息
                    assert isinstance(task,dict)
                    eval(task['fn'])
                else:
                    QA_util_log_info("From Engine %s"%str(threading.current_thread())+"Task has been finished! " )
                    QA_util_log_info("From Engine %s"%str(threading.current_thread())+"Engine will waiting for new task ...")

            except:
                QA_util_log_info("From Engine %s"%str(threading.current_thread())+"Task has been finished!")
                #self.thread_stop = True
                break
            self.queue.task_done()  # 完成一个任务
            res = self.__QA_queue_status()  # 判断消息队列大小
            if res > 0:
                QA_util_log_info("From Engine %s: There are still %d tasks to do" % (str(threading.current_thread()),res))

    def stop(self):
        self.thread_stop = True

    def __start(self):
        self.queue.start()


if __name__ == '__main__':
    q = queue.Queue()
    worker = QA_Queue(q)
    worker.start()
    q.put({'type':'1x00','subtype':'1x01','fn':print('aa')}, block=False, timeout=None)
    QA_util_log_info('===now we will sleep 20 sec, and wait for the response')
    QA_util_log_info(datetime.datetime.now())
    time.sleep(20)
    q.put({'type':'1x00','subtype':'1x01','fn':print('vv')}, block=False, timeout=None)
    QA_util_log_info(datetime.datetime.now())
