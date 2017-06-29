# coding:utf-8
import threading
import time
from six.moves import queue
import random
from tabulate import tabulate
import pprint
import datetime

a = queue.Queue()


def exec():
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

        exec()
        global l
        l = threading.Timer(0.5, exec)
        l.start()


def insert(a, msg):
    a.put(msg)
    # print(a.queue)
    print(msg)


l = threading.Timer(0.5, exec)
l.start()
ls = 0.1
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
    print(threading.enumerate())

l1 = threading.Thread(target=exec())
l1.setDaemon(True)
l1.start()
l2.start()
