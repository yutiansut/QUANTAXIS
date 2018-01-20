# QUANTAXIS_ENGINE


QUANTAXIS ENGINE 由三个部分组成:

```
QA_Worker/QAEvent

QA_Task

QA_Thread / QA_Engine
```

QA_Worker是做事情的主体,主体根据相应的事件(QA_Event),在实际的应用中,QA_Worker 是需要被继承,并修改run()方法的

QA_Task是主体在某一个时间点做的事件,他被放置于QA_Engine/QA_Thread的事件队列中

QA_Thread是一个可以快速创建的事件线程,通过向QA_Thread的事件队列推送事件,QA_Thread会完成推送的任务

QA_Engine是用于管理/创建多个QA_Thread的管理器