# 升级日志
```shell
 ...................................................................................................................... 
 ..########.....##........##..........##.........####........##...##########.......##......##......###...##.....######.. 
 .##......## ...##........##.........####........##.##.......##.......##..........###.......##....##.....##...##.....##. 
 ##........##...##........##........##.##........##..##......##.......##.........####........#...##......##...##......## 
 ##........##...##........##.......##...##.......##...##.....##.......##.........##.##.......##.##.......##....##....... 
 ##........##...##........##......##.....##......##....##....##.......##........##..###.......###........##.....##...... 
 ##........##...##........##......##......##.....##.....##...##.......##.......##....##.......###........##......###.... 
 ##........##...##........##.....##........##....##......##..##.......##......##......##.....##.##.......##........##... 
 ##........##...##........##....#############....##.......##.##.......##.....###########.....##..##......##.........##.. 
 ###.......##...##........##...##...........##...##.......##.##.......##....##.........##...##...##......##...##.....##. 
 .##......###....##......###..##.............##..##........####.......##...##..........##..###....##.....##....##.....## 
 ..#########......########...##..............###.##..........##.......##..##............##.##......##....##.....##....## 
 ........#####.....................................................................................................####.. 
 ...................................................................................................................... 
 ..........................Copyright..yutiansut..2017......QUANTITATIVE FINANCIAL FRAMEWORK.............................. 
 ...................................................................................................................... 
 ........................................................................................................................ 
```
最新版本 :0.4.0-alpha
<!-- TOC -->

- [升级日志](#升级日志)
    - [新的功能:](#新的功能)
        - [1.1 组合回测支持](#11-组合回测支持)
        - [1.2 多种交易状态支持](#12-多种交易状态支持)
        - [1.3 实盘交易的支持](#13-实盘交易的支持)
        - [1.4 更加方便的数据更新接口](#14-更加方便的数据更新接口)
        - [1.5 手续费/滑点](#15-手续费滑点)
        - [1.6 QUANTAXIS-Log 优化](#16-quantaxis-log-优化)
        - [1.7 重构了回测流程,简化回测设置步骤](#17-重构了回测流程简化回测设置步骤)
        - [1.8 对于QACMD进行改进](#18-对于qacmd进行改进)
        - [1.9 新增QADataStruct模块](#19-新增qadatastruct模块)
        - [1.10 对于backtest的一个bug修改:](#110-对于backtest的一个bug修改)
        - [1.11 对于SU中心的修改](#111-对于su中心的修改)
        - [1.12 增加了界面的logo以及log的logo](#112-增加了界面的logo以及log的logo)
        - [1.13 增加一个标准化的QUANTAXIS事件队列(0.3.9)](#113-增加一个标准化的quantaxis事件队列039)
        - [1.14 增加了两个时间选择的api(0.3.9)](#114-增加了两个时间选择的api039)
        - [1.15 增加了一个事件订阅的方式QA.QA_Event(0.3.9):](#115-增加了一个事件订阅的方式qaqa_event039)
        - [1.16 修改了CLI中的创建example内容(0.3.9):](#116-修改了cli中的创建example内容039)
        - [1.17 增加了一个带参数的延时装饰器](#117-增加了一个带参数的延时装饰器)
        - [1.18 web 部分的改进](#118-web-部分的改进)
        - [1.19 回测部分的最后一天停牌情况的处理](#119-回测部分的最后一天停牌情况的处理)
    - [巨大改动/重构](#巨大改动重构)
        - [2.1 QA.QAARP.QAAccount](#21-qaqaarpqaaccount)
        - [2.2 QA.QABacktest.Backtest_analysis](#22-qaqabacktestbacktest_analysis)
        - [2.3 QA.QABacktest.QABacktest](#23-qaqabacktestqabacktest)
        - [2.4 QA.QA_Queue](#24-qaqa_queue)
        - [2.5 彻底放弃QUANTAXIS-WEBKIT-CLIENT](#25-彻底放弃quantaxis-webkit-client)
    - [重要性能优化  重新定义回测流程,减少数据库IO压力](#重要性能优化--重新定义回测流程减少数据库io压力)
    - [废弃的接口](#废弃的接口)
    - [to do list](#to-do-list)

<!-- /TOC -->

作者: yutiansut


## 新的功能:

### 1.1 组合回测支持
2017/6/13
在之前的版本里,quantaxis是通过穿透性测试去做unit测试.然后对于unit结果进行组合.这种构建组合的方式虽然行之有效,但是在一些情境下会比较笨重.

好比如,你只是想对于特定的股票(如小市值股票)的一些方法进行回测分析,由于这些股票组合是固定的,所以本来只需要进行一次回测,但是在穿透性测试下要进行n次回测并重新组合

新的模式在原有基础上推出了基于组合的unit测试,在固定组合的时候,只需要进行一个测试,就可以得到结果


### 1.2 多种交易状态支持
2017/6/14
之前的版本中,quantaxis只支持单次持仓,及(不能进行买入-继续买入的状态)

0.3.9-gamma进行了一定的修改和优化,目前支持了多次连续买入和卖出的交易状态,并通过order_id和trade_id来锁定买卖的对应关系


### 1.3 实盘交易的支持
2017/6/14
通过tradex的接口,quantaxis实现了一套实盘的解决方案,在quantaxistrade文件夹下,具体详见quantaxis_trade


### 1.4 更加方便的数据更新接口
2017/6/15
```python

import QUANTAXIS as QA

QA.QA_SU_update_stock_day(client=QA.QA_Setting.client,engine='ts')
```
### 1.5 手续费/滑点
2017/6/16

重写了交易撮合引擎,区分不同市场/状态,同时对于股票交易量的区分有了更加接近实盘的表现

1. 对于滑点的设置:

    - 如果报价单的购买数量小于1/16当日成交量
    > 按正常报价进行交易

    - 如果报价单的购买数量在1/16-1/8 当日成交量, 成交价会进行一个浮动:
    > 买入价=mean(max{o,c},h)  卖出价=mean(min{o,c},l)

    - 如果报价单的数量在1/8当日成交量以上,则只能成交1/8的当日成交量
    > 买入价=high  卖出价=low 交易数量=1/8当日成交量


2. 对于手续费的设置:

    买入的时候无需付费,卖出的时候,按成交额收万分之五的手续费,并在现金中扣除



### 1.6 QUANTAXIS-Log 优化
2017/6/15

```shell

ipython

In [1]: import QUANTAXIS as QA

QUANTAXIS>> start QUANTAXIS

QUANTAXIS>> ip:127.0.0.1   port:27017

QUANTAXIS>> Welcome to QUANTAXIS, the Version is 0.3.9-beta-dev20
```



### 1.7 重构了回测流程,简化回测设置步骤
2017/6/21

在quantaxis的backtest的基础上,对于回测的流程和模式进行了重构,通过ini的读取以及函数式编程的方法,把回测简化到一个ini+策略即可进行回测的步骤

具体参见 test/new test 文件夹


### 1.8 对于QACMD进行改进
2017/6/26

对于QACMD的模式进行了修改,现在直接在命令行中输入quantaxis即可进入quantaxis的交互式界面进行操作


### 1.9 新增QADataStruct模块
2017/6/27

datastruct将在未来对于不同的场景下的数据进行重构和规范化处理,目前新增了基础数据类,机器学习类,ohlc价格序列类等

### 1.10 对于backtest的一个bug修改:
2017/6/27

修改了购买的时候的方式,其中mean的报价方式改变为当前可用资金/股票列表数量的资金分配方式

修改了对于cash小于买入报单总量的修正,以免出现在不能买入的时候的误操作

### 1.11 对于SU中心的修改

修改并优化了对于QUANTAXIS backtest的回测过程的资金曲线的存储过程,增加了存为csv的方法,并优化和修正了存储时的结果

### 1.12 增加了界面的logo以及log的logo
![Markdown](http://i2.kiimg.com/1949/4123de6743af4810.png)
![Markdown](http://i2.kiimg.com/1949/ce8c3ee69f64976e.png)

### 1.13 增加一个标准化的QUANTAXIS事件队列(0.3.9)
2017/6/30-2017/7/2,2017/7/4

引入方式:
```python
from QUANTAXIS import QA_Queue
```

使用方式:

首先需要引入一个标准化的队列:

``` python
from six.moves import queue
import queue # python3
import Queue # python2 

qa=queue.Queue()# 你可以自定义队列的大小
#启动一个事件队列:
qa_event=QA_Queue(qa)
# 往事件引擎里发事件,需要有函数
"""
标准的事件是:
{'type':'xxx','fn':'func'}
"""
qa.put({'type':'xxx','fn':'func'})
```
事件引擎会默认一直监听这个队列
2017/7/4 update  重新优化了这个事件引擎 参见test/test_job_queue.py
```shell
13:35:45 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:45 QUANTAXIS>>> job--id:0
13:35:46 QUANTAXIS>>> job--id:1
13:35:46 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 2 tasks to do
13:35:46 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 1 tasks to do
13:35:46 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:47 QUANTAXIS>>> job--id:2
13:35:47 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 1 tasks to do
13:35:47 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:47 QUANTAXIS>>> job--id:3
13:35:48 QUANTAXIS>>> job--id:4
13:35:48 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 2 tasks to do
13:35:48 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 1 tasks to do
13:35:48 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:49 QUANTAXIS>>> job--id:5
13:35:49 QUANTAXIS>>> job--id:6
13:35:49 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 2 tasks to do
13:35:49 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 1 tasks to do
13:35:49 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:50 QUANTAXIS>>> job--id:7
13:35:50 QUANTAXIS>>> job--id:8
13:35:50 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 2 tasks to do
13:35:50 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 1 tasks to do
13:35:50 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:51 QUANTAXIS>>> job--id:9
13:35:51 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 1 tasks to do
13:35:51 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:52 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:53 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:54 QUANTAXIS>>> job--id:1
13:35:54 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>: There are still 1 tasks to do
13:35:54 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:55 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:56 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:57 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:58 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:35:59 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:36:00 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...
13:36:01 QUANTAXIS>>> From Engine <QA_Queue(EVENT ENGINE, started 12488)>Engine will waiting for new task ...


```




### 1.14 增加了两个时间选择的api(0.3.9)
2017/7/3

- QUANTAXIS.QAUtil.QADate.QA_select_hours

- QUANTAXIS.QAUtil.QADate.QA_select_min

引入方式

```python
from QUANTAXIS.QAUtil import QA_select_hours,QA_select_min
```

### 1.15 增加了一个事件订阅的方式QA.QA_Event(0.3.9):
2017/7/3
```python

from QUANTAXIS.QATask import QA_Event

class MyEvent(QA_Event):
    ASK = "askMyEvent"
    RESPOND = "respondMyEvent"

class WhoAsk(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event_listener(
            MyEvent.RESPOND, self.on_answer_event
        )

    def ask(self):
        print("who are listener to me?")
        self.event_dispatcher.dispatch_event(MyEvent(MyEvent.ASK, self))

    def on_answer_event(self, event):
        print("receive event %s", event.data)

class WhoRespond(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event_listener(
            MyEvent.ASK, self.on_ask_event)

    def on_ask_event(self, event):
        self.event_dispatcher.dispatch_event(
            MyEvent(MyEvent.RESPOND, self))

dispatcher = QA_EventDispatcher()
who_ask = WhoAsk(dispatcher)
who_responde1 = WhoRespond(dispatcher)
who_responde2 = WhoRespond(dispatcher)

# WhoAsk ask
who_ask.ask()
```

result:
```shell
who are listener to me?
receive event %s <__main__.WhoRespond object at 0x02361D50>
receive event %s <__main__.WhoRespond object at 0x02361DB0>
```



### 1.16 修改了CLI中的创建example内容(0.3.9):
2017/7/3

现在在命令行中输入QUANTAXIS:
```shell
λ  quantaxis
QUANTAXIS>> start QUANTAXIS
QUANTAXIS>> ip:127.0.0.1   port:27017
QUANTAXIS>> From Engine <_MainThread(MainThread, started 19040)>2017-07-03 14:22:08.218800
QUANTAXIS>> FROM QUANTAXIS SYS== now running 3 threads
QUANTAXIS>> Welcome to QUANTAXIS, the Version is 0.3.9-beta-dev29


QUANTAXIS> examples
QUANTAXIS>> QUANTAXIS example
QUANTAXIS>> successfully generate a example strategy inC:\Users\yutiansut\strategy\A05-CCI
QUANTAXIS> exit

λ  ls


    目录: C:\Users\yutiansut\strategy\A05-CCI


Mode                LastWriteTime     Length Name
----                -------------     ------ ----
-a---          2017/7/3     14:22        358 backtest.ini
-a---          2017/7/3     14:22        905 backtest.py
-a---          2017/7/3     14:22       2738 quantaxis-2017-07-03-14-22-08-.log

```
### 1.17 增加了一个带参数的延时装饰器
2017/7/4

QUANTAXIS.QAUtil.QADate.QA_util_time_delay()

使用方式

```python
from QUANTAXIS import QA_util_time_dalay


@QA_util_time_dalay(2)
#延时2秒
def pp():
    print(1)


```


### 1.18 web 部分的改进
2017/7/10

web部分,修改了页面布局和回测的显示方式

去除了之前单个股票和行情的对比

改成了资金曲线和组合分析的方式


### 1.19 回测部分的最后一天停牌情况的处理
2017/7/10


```python
_remains_day=0
while __message['header']['status']==500:
    #停牌状态,这个时候按停牌的最后一天计算价值(假设平仓)
    
    __last_bid['date'] = self.trade_list[self.end_real_id-_remains_day]
    _remains_day+=1
    __message = self.market.receive_bid(__last_bid, self.setting.client)

    #直到市场不是为0状态位置,停止前推日期
```
在原来的代码里,组合的最后一天需要被平仓,而如果恰巧这一天停牌:(600127,601001 在2017/6/30都是停牌状态)

那么就会一直陷入市场返回500错误,而回测框架一直在组装报价,来回轮询,陷入死循环

现在加入了对于市场的数据的检测,如果是500状态,则会将交易日向前递推一天,重新组装报价,直到停牌的最后一天为止


## 巨大改动/重构

### 2.1 QA.QAARP.QAAccount
在0.3.9-gamma中,quantaxis对于account账户方法进行了重构.优化了回测逻辑以及数组的存储方式.

现在的account只有如下几个变量:

- assets: 总资金曲线
- hold: 持仓列表
- history : 历史交易列表
- cash: 历史现金列表
- detail: 买卖明细表(有买入id和卖出id对应关系)



新版的quantaxis并不在回测框架中定义利润的计算以及其他的逻辑,这些在backtest_analysis中会涉及计算,当然也可以自己定义利润的计算方法
### 2.2 QA.QABacktest.Backtest_analysis

对于quantaxis_backtest_analysis进行了巨大的修改,现在的backtest_analysis的接口调用函数有了一定程度的修改.

对于交易组合而言,quantaxis的backtest_analysis 可以直接对于组合进行分析,计算组合的情况

增加了可以自己选定组合的benchmark标的

### 2.3 QA.QABacktest.QABacktest

对于QABacktest进行了彻底的重构,重新写入了读取数据方法和函数句柄的接受方法,具体参见test/new test


### 2.4 QA.QA_Queue

事件队列,参见 ###1.14


### 2.5 彻底放弃QUANTAXIS-WEBKIT-CLIENT

webkit/client 是一个基于electronic的客户端,但是其功能本质上和网页版并无区别,且缺乏维护

0.4.0-alpha中将其去除,之后也不会再维护

## 重要性能优化  重新定义回测流程,减少数据库IO压力

在新的回测框架中,大幅优化了数据的读取方式,通过大量的内存结构来进行数据缓存,之后的数据调用请求都通过内存中的数据接口来获得,这样大大减少了数据库IO

同时,通过对于Account账户的修改,大幅优化了回测数据的存储方式,以及存储的的模式,大大减少了回测数据存储的数量


## 废弃的接口


## to do list