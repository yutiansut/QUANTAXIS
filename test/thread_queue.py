# coding:utf-8
import threading
from six.moves import queue
import time



"""
多线程的队列模式,vnpy里面说是事件驱动模型,其实本质还是一个生产者消费者模型,然后使用python的dict队列来分发函数

首先对于整个引擎进行初始化和注册事件
然后将一个轮询的定时器启动(比如vnpy里面是一个QT的timer,也可以使用threading里面的timer,也可以有其他的触发机制来进行轮询)

队列在不同线程上分别启动生产任务和消费任务,然后依据dict来分发不同函数句柄,实现这个所谓的事件驱动引擎
"""



class worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_stop = False

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


if __name__ == "__main__":
    q = queue.Queue()
    worker = worker(q)
    worker.start()
    q.put(["produce one cup!", 1], block=True, timeout=None)  # 产生任务消息
    q.put(["produce one desk!", 2], block=True, timeout=None)
    q.put(["produce one apple!", 3], block=True, timeout=None)
    q.put(["produce one banana!", 4], block=True, timeout=None)
    q.put(["produce one bag!", 5], block=True, timeout=None)
    print("***************leader:wait for finish!")
    q.join()  # 等待所有任务完成
    print("***************leader:all task finished!")
