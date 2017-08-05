# coding:utf-8
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
from six.moves import queue
import time
import datetime,random
import QUANTAXIS as QA


"我们需要测试两个:\
    事件队列\
    事件分发"


def get_now_threading():
    print(threading.enumerate())


event_queue = queue.Queue()
event_engine = QA.QA_Queue(event_queue)
event_engine.setName('EVENT ENGINE')
event_engine.start()
print(threading.enumerate())


def job(i):
    QA.QA_util_log_info('job--id:'+str(i))


#这个是一个最简单的事件队列:
#隔一段时间,把一个函数放进去,事件引擎就会自动的响应这个事件,并且立即执行
#如果需要延时执行,可以在放进去的函数里面,先加入一个time.sleep
for i in range(10):
    #print(event_engine.is_alive())
    event_engine.queue.put({'fn': job(i),'t':i})
    print(event_engine.queue.queue)
    print('\n')
    
    time.sleep(random.randint(1,5)/5)
print(event_engine.is_alive())
for i in range(2):
    print(threading.enumerate())
    time.sleep(1)

event_engine.queue.put({'fn': job(i),'t':i})
print(event_engine.queue.queue)
print(event_engine.is_alive())
print(threading.enumerate())