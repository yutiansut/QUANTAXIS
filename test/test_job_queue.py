# coding:utf-8
import threading
from six.moves import queue
import time
import QUANTAXIS as QA

bid_queue = queue.Queue()
bid_server = QA.QA_Queue(bid_queue)
bid_server.setName('bid-server')
bid_server.start()


market_queue = queue.Queue()
market_server = QA.QA_Queue(market_queue)
market_server.setName('market-server')
market_server.start()


task_queue=queue.Queue()
task_server= QA.QA_Queue(task_queue)
task_server.setName('task-server')
task_server.start()


print(threading.enumerate())


task_queue.put({'fn':bid_queue.put({'fn':print('aaa')})})