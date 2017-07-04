# coding:utf-8
import threading
from six.moves import queue
import time
import datetime,random
import QUANTAXIS as QA
from QUANTAXIS.QAUtil import QA_util_time_delay

"我们需要测试两个:\
    事件队列\
    事件分发"


def get_now_threading():
    print(threading.enumerate())


event_queue = queue.Queue()
event_engine = QA.QA_Queue(event_queue)
event_engine.setName('EVENT ENGINE')
event_engine.start()
@QA_util_time_delay(2)
def job(i):
    event_queue.put({'fn': print(datetime.datetime.now())})

    event_queue.put({'fn': print('jobs---id:'+str(i))})
    event_queue.put({'fn': print('\n')})
#这个是一个最简单的事件队列:
#隔一段时间,把一个函数放进去,事件引擎就会自动的响应这个事件,并且立即执行
#如果需要延时执行,可以在放进去的函数里面,先加入一个time.sleep
for i in range(1000):
    event_queue.put({'fn': print(datetime.datetime.now())})

    event_queue.put({'fn': print('jobs---id:'+str(i))})
    event_queue.put({'fn': print('\n')})
    time.sleep(random.randint(1,5)/5)
