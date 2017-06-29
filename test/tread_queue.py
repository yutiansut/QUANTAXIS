# coding:utf-8
import threading
import time
from six.moves import queue
import random
from tabulate import tabulate
import pprint
import datetime
from QUANTAXIS.QAUtil import QA_util_log_info
a = queue.Queue()


class QA_Task_Thread(threading.Thread, queue.Queue):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        queue.Queue().__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.queue=queue.Queue()
        self.__start=True

    def run(self):
        exec(self.pop)

    def insert(self,__task):
        self.queue.put_nowait(__task)

    def pop(self):
        assert self.queue.empty()==False
        return self.queue.get()

    def register(self):
        pass
    def unregister(self):
        pass
    def close(self):
        self.__start=False
    def start(self):
        assert self.__start==True
        self.run()

def engine():
    if a.empty():
        print('FROM ENGINE====all-been-finished')

    else:
        print('====task-board===')
        print(a.queue)
        task = a.get()
        if str(task[0]) == 'b':
            time.sleep(0.3)
        elif task[0] == 'm':
            time.sleep(0.1)
        elif task[0] == 'f':
            time.sleep(0.5)
        elif task[0] == 'b':
            time.sleep(0.02)
        print('FROM ENGINE====' + task + 'has been done!')

        engine()
        time.sleep(0.5)
        engine()


def insert(a, msg):
    a.put(msg)
    # print(a.queue)
    print(msg)


ls = 0.1

thread = []
l1 = threading.Thread(target=engine, args=())
thread.append(l1)
for i in range(100):
    i = str(random.random())[3:6]
    t = ['bid', 'market', 'fetch-spider', 'update', 'backtest-id']
    task = t[random.randint(0, 4)]
    msg = 'taskmsg--' + task + '--' + str(i) + ' has been  dispatched'
    print('FROM EVENT====' + msg)
    l2 = threading.Thread(target=insert(a, task + '--' + str(i)))
    ls = ls + 0.1
    time.sleep(ls)
    print('FROM EVENT====' + str(datetime.datetime.now()))
    thread.append(l2)
    print(threading.enumerate())
for i in thread:
    i.start()




if __name__=='__main__':
    l1.start()

    l2.start()
    l1.join()
