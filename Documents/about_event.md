# QUANTAXIS 的事件框架:
<!-- TOC -->

- [QUANTAXIS 的事件框架:](#quantaxis-的事件框架)
    - [QATASK - 存在于队列中的标准单元](#qatask---存在于队列中的标准单元)
    - [QAEVNET - 可扩展的事件任务](#qaevnet---可扩展的事件任务)
    - [QAWorker - 指定执行事件的对象](#qaworker---指定执行事件的对象)
    - [QAThreadEngine - 可自定义线程的带队列方法](#qathreadengine---可自定义线程的带队列方法)
    - [QAEngine - 管理和分配任务的线程对象](#qaengine---管理和分配任务的线程对象)

<!-- /TOC -->

QUANTAXIS的事件框架是一个多线程架构:

```QUANTAXIS
QUANTAXIS/QAENGINE

QAENGINE分三个部分

- QAEvent
- QATask
- QAThreadEngine
(可扩展 ProcessEngine/AsyncioEngine)
```

事件的核心可以简单理解为一个带队列的线程(进程/协程),将事件分类,做成生产者消费者模式,通过队列传递任务

## QATASK - 存在于队列中的标准单元

```QUANTAXIS
QA_Task(worker, event, engine=None, callback=False)

QA_Task 是被event_queue.put()中的内容

worker参数指的是 QA_Worker 需要用worker类以及继承了worker类去实例化

event指的是QA_Event event会指定事件的类别,事件的任务,事件的参数以及事件的回调

engine参数指的是在多线程引擎中,使用哪个线程去执行这个task,默认是None,及当前的主线程

callback 是回调函数,该函数不能有参数 ```if callback: callback() else:pass```

```
## QAEVNET - 可扩展的事件任务

```QUANTAXIS
QA_Event是一个可以被继承的基础类,用于给QA_Worker指定事件任务

QA_Event(event_type=None, func=None, message=None, callback=False, *args, **kwargs)

QA_Event 必须要有的是event_type

func,message 一个是函数句柄,一个是消息句柄 可有可无
callback 是回调函数 根据自定义的worker去适配

除此以外 QA_Event可以通过**kwargs传入任何参数 

```

## QAWorker - 指定执行事件的对象
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

## QAThreadEngine - 可自定义线程的带队列方法

```QUANTAXIS
QAThreadEngine是一个继承threading的带队列线程对象

通过threadengine 可以创建一个自定义的线程出来,使用event_queue来向线程推送任务(QA_Task),如果没有任务推送,线程会在后台等待
```
## QAEngine - 管理和分配任务的线程对象

```QUANTAXIS
QAEngine是一个用于管理threadengine的分派器,可以自定义创建QAThreadEngine,向指定线程推送任务 QA_Task的engine参数
```

