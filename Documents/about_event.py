
# coding: utf-8


import QUANTAXIS as QA

""" 
在这里 我们演示两种方法 
1. 直接通过QA_Thread 创建一个事件线程做任务
2. 通过QA_Engine 来创建一个QA_Thread 来分派事件
"""

thread = QA.QA_Thread()  # 创建一个QA_Thread
engine = QA.QA_Engine()  # 创建一个QA_Engine
engine.start()  # engine 开启

engine.create_kernal('backtest')  # engine创建一个叫 backtest的线程
engine.start_kernal('backtest')  # engine 启动该线程

# 创建一个类,继承QA_Worker


class job(QA.QA_Worker):
    def __init__(self):
        super().__init__()

    def run(self, event):
        if event.event_type is 'selfdesign':
            print(vars(event))
            if event.callback:
                event.callback(event.message)
        else:
            print('unknown/unsupport event type')


jobx = job()  # 实例化这个类

# 创建一个event
event = QA.QA_Event(event_type='selfdesign', message='ssss', callback=print)

# 创建一个标准task
task = QA.QA_Task(event=event, worker=jobx, engine='backtest')

# task有result方法
print(task.result)

thread.start()  # 开启thread 线程

thread.put(task)  # 向thread线程推送任务

engine.run_job(task)  # 向engine推送任务


""" 运行结果
PS C:\quantaxis> & python c:/quantaxis/Documents/QA_ENGINE.py
QUANTAXIS>> start QUANTAXIS
QUANTAXIS>> Selecting the Best Server IP of TDX
QUANTAXIS>> === The BEST SERVER ===
 stock_ip 218.75.126.9 future_ip 61.152.107.141
QUANTAXIS>> Welcome to QUANTAXIS, the Version is remake-version
QUANTAXIS>>
 ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
  ``########`````##````````##``````````##`````````####````````##```##########````````#``````##``````###```##`````######``
  `##``````## ```##````````##`````````####````````##`##```````##```````##```````````###``````##````##`````##```##`````##`
  ##````````##```##````````##````````##`##````````##``##``````##```````##``````````####```````#```##``````##```##``````##
  ##````````##```##````````##```````##```##```````##```##`````##```````##`````````##`##```````##`##```````##````##```````
  ##````````##```##````````##``````##`````##``````##````##````##```````##````````##``###```````###````````##`````##``````
  ##````````##```##````````##``````##``````##`````##`````##```##```````##```````##````##```````###````````##``````###````
  ##````````##```##````````##`````##````````##````##``````##``##```````##``````##``````##`````##`##```````##````````##```
  ##````````##```##````````##````#############````##```````##`##```````##`````###########`````##``##``````##`````````##``
  ###```````##```##````````##```##```````````##```##```````##`##```````##````##`````````##```##```##``````##```##`````##`
  `##``````###````##``````###``##`````````````##``##````````####```````##```##``````````##``###````##`````##````##`````##
  ``#########``````########```##``````````````###`##``````````##```````##``##````````````##`##``````##````##`````##````##
  ````````#####`````````````````````````````````````````````````````````````````````````````````````````````````````####`
  ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
  ``````````````````````````Copyright``yutiansut``2017``````QUANTITATIVE FINANCIAL FRAMEWORK`````````````````````````````
  ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
 ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
 ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

{'task_id': 'Task_4h5eLdKy', 'result': None}
QUANTAXIS>> From Engine < QA_Thread backtest >: There are still 1 tasks to do
{'event_type': 'selfdesign', 'func': None, 'message': 'ssss', 'callback': <built-in function print>}QUANTAXIS>> From Engine <
QA_Thread QAWorker_A3y >: There are still 1 tasks to do
ssss

{'event_type': 'selfdesign', 'func': None, 'message': 'ssss', 'callback': <built-in function print>}
ssss


"""