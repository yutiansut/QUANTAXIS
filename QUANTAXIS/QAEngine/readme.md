# QATASK

关于QATASK的一些说明:

QATASK主要负责维护一些不确定时间的状态流,比如订单状态,或者是多目标源的事件流

QATASK 给了5种不同场景下的解决方案:

- QA_Event  主要负责的是事件的一对多的分发和订阅

- QA_Thread  主要负责的是维护一个函数句柄队列,可以理解为一个生产者消费者模型

- QA_Engine_Center  主要负责的是一个对外的兼容接口,无论是socket,还是zeromq,celery,rabbitmq,redis等等

- QA_Multi_Processing  主要是一个多线程和多进程的

- QA_Schedule 主要是一个定时/延时任务机制