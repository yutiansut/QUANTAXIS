# coding:utf-8
import threading
from six.moves import queue
import time
import QUANTAXIS as QA


"我们需要测试两个:\
    事件队列\
    事件分发"
event_queue=queue.Queue()
event_engine=QA.QA_Queue(event_queue)
event_engine.setName('EVENT ENGINE')
event_engine.start()
event_engine.ident()