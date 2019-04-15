# QUANTAXIS 的事件框架:
<!-- TOC -->

- [QUANTAXIS 的事件框架:](#quantaxis-的事件框架)
    - [QATASK - 存在于队列中的标准单元](#qatask---存在于队列中的标准单元)
    - [QAEVENT - 可扩展的事件任务](#qaevent---可扩展的事件任务)
    - [QA_Worker - 指定执行事件的对象](#qa_worker---指定执行事件的对象)
    - [QA_Thread - 可自定义线程的带队列方法](#qa_thread---可自定义线程的带队列方法)
    - [QA_Engine - 管理和分配任务的线程对象](#qa_engine---管理和分配任务的线程对象)
    - [参考示例:](#参考示例)

<!-- /TOC -->

QUANTAXIS的事件框架是一个多线程架构:

```QUANTAXIS
QUANTAXIS/QAENGINE

QAENGINE分三个部分

- QAEvent
- QATask
- QAThread
(可扩展 ProcessEngine/AsyncioEngine)
```

事件的核心可以简单理解为一个带队列的线程(进程/协程),将事件分类,做成生产者消费者模式,通过队列传递任务


![](http://pic.yutiansut.com/QUANTAXISEvent.png)

## QATASK - 存在于队列中的标准单元

```QUANTAXIS
QA_Task(worker, event, engine=None, callback=False)

QA_Task 是被event_queue.put()中的内容

worker参数指的是 QA_Worker 需要用worker类以及继承了worker类去实例化

event指的是QA_Event event会指定事件的类别,事件的任务,事件的参数以及事件的回调

engine参数指的是在多线程引擎中,使用哪个线程去执行这个task,默认是None,及当前的主线程

callback 是回调函数,该函数不能有参数 ```if callback: callback() else:pass```

```
## QAEVENT - 可扩展的事件任务

```QUANTAXIS
QA_Event是一个可以被继承的基础类,用于给QA_Worker指定事件任务

QA_Event(event_type=None, func=None, message=None, callback=False, *args, **kwargs)

QA_Event 必须要有的是event_type

func,message 一个是函数句柄,一个是消息句柄 可有可无
callback 是回调函数 根据自定义的worker去适配

除此以外 QA_Event可以通过**kwargs传入任何参数 

```

## QA_Worker - 指定执行事件的对象
```QUANTAXIS
QA_Worker是执行事件的对象,在QUANTAXIS内部 QA_Account,QA_Broker这些功能性的类都是继承自QA_Worker

QA_Worker以及继承的类需要实现run方法,如

from QUANTAXIS.QAEngine.QAEvent import QA_Worker

class SelfDesignedWorker(QA_Worker):
    def __init__(self):
        super().__init__()

    def run(self,event):
        if event.event_type is ....:
            [do something]
        elif event.event_type is ...:
            [do another thing]
```

## QA_Thread - 可自定义线程的带队列方法

```QUANTAXIS
QA_Thread是一个继承threading的带队列线程对象

通过threadengine 可以创建一个自定义的线程出来,使用event_queue来向线程推送任务(QA_Task),如果没有任务推送,线程会在后台等待
```
## QA_Engine - 管理和分配任务的线程对象

```QUANTAXIS
QAEngine是一个用于管理threadengine的分派器,可以自定义创建QAThreadEngine,向指定线程推送任务 QA_Task的engine参数
```


## 参考示例:

代码在[示例文件](about_event.py)中

```python
import QUANTAXIS as QA

""" 
在这里 我们演示两种方法 
1. 直接通过QA_Thread 创建一个事件线程做任务
2. 通过QA_Engine 来创建一个QA_Thread 来分派事件
"""

thread = QA.QA_Thread()  # 创建一个QA_Thread
engine = QA.QA_Engine()  # 创建一个QA_Engine
engine.start()  # engine 开启

engine.create_kernel('backtest')  # engine创建一个叫 backtest的线程
engine.start_kernel('backtest')  # engine 启动该线程

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


```
