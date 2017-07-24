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
        - [1.20 新增一个时间接口 QA_util_time_now()](#120-新增一个时间接口-qa_util_time_now)
        - [1.21 新增一个QAWeb的接口](#121-新增一个qaweb的接口)
        - [1.22 新增一个QACSV的接口](#122-新增一个qacsv的接口)
        - [1.23 新增一个交易时间的变量](#123-新增一个交易时间的变量)
        - [1.24 新增一个k线接口(通达信)](#124-新增一个k线接口通达信)
        - [1.25 在回测的时候,增加一个回测内全局变量](#125-在回测的时候增加一个回测内全局变量)
        - [1.26 新增一个创建多维list的函数](#126-新增一个创建多维list的函数)
        - [1.27 修改了一个QABacktest的传参, 现在在策略中,需要指定买卖状态](#127-修改了一个qabacktest的传参-现在在策略中需要指定买卖状态)
        - [1.28 对于backtest的加载的外部函数的接口进行修改](#128-对于backtest的加载的外部函数的接口进行修改)
        - [1.29 修改了QA_Query 里返回的数组格式](#129-修改了qa_query-里返回的数组格式)
        - [1.30 修改了QA_util_save_csv的模式](#130-修改了qa_util_save_csv的模式)
        - [1.31 通达信5分钟线解析保存](#131-通达信5分钟线解析保存)
        - [1.32 获取指数k线的api更新](#132-获取指数k线的api更新)
        - [1.33 QA_util更新 QA_util_time_stamp](#133-qa_util更新-qa_util_time_stamp)
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

### 1.20 新增一个时间接口 QA_util_time_now()
2017/7/10

返回的就是datetime.datetime.now()的结果

### 1.21 新增一个QAWeb的接口
2017/7/10

可以在命令行直接输入 quantaxis_web 来启动这个服务器,端口在5050(带socket)

### 1.22 新增一个QACSV的接口

2017/7/13

现在可以便捷的吧数据存成csv格式:

```python
import QUANTAXIS as QA

data=['1',2,'x','t']
QA.QA_util_save_csv(data,'test')

```


### 1.23 新增一个交易时间的变量
2017/7/13

```python
from QUANTAXIS import trade_date_sse

print(trade_date_sse)
```

### 1.24 新增一个k线接口(通达信)
2017/7/13

```python
import QUANTAXIS as QA
QA.QA_fetch_get_stock_day('tdx','601801','2017-01-01','2017-07-01')

```

```shell
Out[3]:
      open  close   high    low       vol       amount  year  month  day  \
0    14.39  14.70  14.76  14.36  164426.0  239606672.0  2016     12   14
1    14.55  14.99  15.10  14.55  188986.0  281594560.0  2016     12   15
2    15.03  16.00  16.11  14.86  180712.0  281681280.0  2016     12   16
3    15.93  16.79  17.05  15.93  207338.0  345849056.0  2016     12   19
4    16.87  16.80  16.87  16.39   81613.0  135869952.0  2016     12   20
5    16.90  16.88  17.12  16.66   98858.0  166289104.0  2016     12   21
6    16.95  16.61  16.96  16.28   92686.0  153868304.0  2016     12   22
7    16.58  16.51  17.05  16.03   89121.0  147409888.0  2016     12   23
8    16.59  17.30  17.65  16.26  226506.0  387817440.0  2016     12   26
9    17.35  17.49  17.62  17.14  106783.0  186348288.0  2016     12   27
10   17.56  17.89  17.96  17.40  181507.0  321431424.0  2016     12   28
11   17.69  17.59  17.84  17.35  109785.0  193161984.0  2016     12   29
12   17.58  17.57  17.90  17.24  142565.0  251420576.0  2016     12   30
13   17.60  17.45  17.60  17.15  106347.0  185482976.0  2017      1    3
14   17.40  17.00  17.40  16.41  204781.0  344751936.0  2017      1    4
15   16.85  16.86  17.00  16.55  102506.0  171934160.0  2017      1    5
16   16.89  16.90  17.13  16.73   77188.0  130475344.0  2017      1    6
17   16.86  16.81  17.10  16.76   77502.0  131223856.0  2017      1    9
18   16.81  17.40  17.53  16.10  193194.0  325042304.0  2017      1   10
19   17.20  17.68  17.84  17.10  368129.0  651724672.0  2017      1   11
20   17.68  17.96  18.24  17.61  408000.0  735998016.0  2017      1   12
21   17.96  18.31  18.84  17.80  337911.0  619458496.0  2017      1   13
22   18.30  18.56  18.66  17.36  284054.0  518380576.0  2017      1   16
23   18.39  18.57  19.00  17.60  263141.0  491844896.0  2017      1   17
24   18.23  17.99  18.80  17.90   95064.0  173332688.0  2017      1   18
25   17.81  18.24  18.39  17.80   49353.0   89376280.0  2017      1   19
26   18.32  18.46  18.69  18.19  143792.0  265606432.0  2017      1   20
27   18.28  18.84  19.00  18.26  228183.0  427935936.0  2017      1   23
28   18.80  19.00  19.10  18.50  113616.0  214593088.0  2017      1   24
29   19.00  18.78  19.14  18.72  265691.0  504179328.0  2017      1   25
..     ...    ...    ...    ...       ...          ...   ...    ...  ...
89   12.73  12.98  13.16  12.68  176499.0  228946128.0  2017      5   17
90   12.78  13.26  13.27  12.71  145098.0  189804288.0  2017      5   18
91   13.20  13.09  13.33  13.08   78134.0  102854576.0  2017      5   19
92   13.15  12.63  13.18  12.50   96282.0  123843520.0  2017      5   22
93   12.64  12.76  13.16  12.53  111309.0  141901152.0  2017      5   23
94   12.74  13.17  13.19  12.62  104595.0  136030272.0  2017      5   25
95   13.12  13.09  13.25  13.08   69110.0   90972200.0  2017      5   26
96   13.25  13.42  13.44  13.18  110524.0  147250112.0  2017      5   31
97   13.43  13.26  13.46  13.07   88958.0  117311632.0  2017      6    1
98   13.09  12.91  13.09  12.70   91351.0  117710656.0  2017      6    2
99   12.98  12.83  12.98  12.74  110453.0  141482496.0  2017      6    5
100  12.77  12.83  12.85  12.68   62182.0   79344728.0  2017      6    6
101  12.80  13.26  13.30  12.74  144478.0  188284080.0  2017      6    7
102  13.19  13.13  13.33  13.09  101171.0  133169712.0  2017      6    8
103  13.12  13.04  13.15  12.96   87196.0  113572160.0  2017      6    9
104  13.00  12.76  13.00  12.74   86848.0  111470976.0  2017      6   12
105  12.62  12.96  13.02  12.60   67389.0   87066136.0  2017      6   13
106  13.00  12.75  13.00  12.72   62876.0   80648232.0  2017      6   14
107  12.74  12.85  12.95  12.70   71232.0   91385064.0  2017      6   15
108  12.87  12.71  12.87  12.67   59412.0   75701632.0  2017      6   16
109  12.72  12.90  12.92  12.69   77521.0   98993784.0  2017      6   19
110  12.86  13.21  13.24  12.86  180431.0  237042944.0  2017      6   20
111  13.28  13.21  13.32  13.00  117902.0  154974640.0  2017      6   21
112  13.20  13.37  13.58  13.15  191968.0  256520880.0  2017      6   22
113  13.28  13.21  13.29  12.99  114182.0  150111952.0  2017      6   23
114  13.22  13.71  13.73  13.16  186511.0  252084368.0  2017      6   26
115  13.74  13.78  13.81  13.54  135037.0  184420320.0  2017      6   27
116  13.73  13.98  14.05  13.56  242043.0  335440128.0  2017      6   28
117  13.94  13.96  14.01  13.84  178812.0  248913488.0  2017      6   29
118  13.89  13.82  13.94  13.71   83402.0  115219784.0  2017      6   30

     hour  minute          datetime
0      15       0  2016-12-14 15:00
1      15       0  2016-12-15 15:00
2      15       0  2016-12-16 15:00
3      15       0  2016-12-19 15:00
4      15       0  2016-12-20 15:00
5      15       0  2016-12-21 15:00
6      15       0  2016-12-22 15:00
7      15       0  2016-12-23 15:00
8      15       0  2016-12-26 15:00
9      15       0  2016-12-27 15:00
10     15       0  2016-12-28 15:00
11     15       0  2016-12-29 15:00
12     15       0  2016-12-30 15:00
13     15       0  2017-01-03 15:00
14     15       0  2017-01-04 15:00
15     15       0  2017-01-05 15:00
16     15       0  2017-01-06 15:00
17     15       0  2017-01-09 15:00
18     15       0  2017-01-10 15:00
19     15       0  2017-01-11 15:00
20     15       0  2017-01-12 15:00
21     15       0  2017-01-13 15:00
22     15       0  2017-01-16 15:00
23     15       0  2017-01-17 15:00
24     15       0  2017-01-18 15:00
25     15       0  2017-01-19 15:00
26     15       0  2017-01-20 15:00
27     15       0  2017-01-23 15:00
28     15       0  2017-01-24 15:00
29     15       0  2017-01-25 15:00
..    ...     ...               ...
89     15       0  2017-05-17 15:00
90     15       0  2017-05-18 15:00
91     15       0  2017-05-19 15:00
92     15       0  2017-05-22 15:00
93     15       0  2017-05-23 15:00
94     15       0  2017-05-25 15:00
95     15       0  2017-05-26 15:00
96     15       0  2017-05-31 15:00
97     15       0  2017-06-01 15:00
98     15       0  2017-06-02 15:00
99     15       0  2017-06-05 15:00
100    15       0  2017-06-06 15:00
101    15       0  2017-06-07 15:00
102    15       0  2017-06-08 15:00
103    15       0  2017-06-09 15:00
104    15       0  2017-06-12 15:00
105    15       0  2017-06-13 15:00
106    15       0  2017-06-14 15:00
107    15       0  2017-06-15 15:00
108    15       0  2017-06-16 15:00
109    15       0  2017-06-19 15:00
110    15       0  2017-06-20 15:00
111    15       0  2017-06-21 15:00
112    15       0  2017-06-22 15:00
113    15       0  2017-06-23 15:00
114    15       0  2017-06-26 15:00
115    15       0  2017-06-27 15:00
116    15       0  2017-06-28 15:00
117    15       0  2017-06-29 15:00
118    15       0  2017-06-30 15:00

[119 rows x 12 columns]

```

### 1.25 在回测的时候,增加一个回测内全局变量
2017/7/14


现在的回测加载的函数句柄里面会增加一个叫info的句柄,这个句柄在引擎里面是交易日循环外部的变量,可以存贮一些连续周期信息,和一些点位信息


在quantaxis/test/new test的strategy里面可以看到改动


### 1.26 新增一个创建多维list的函数
2017/7/14

在QUANTAXIS.QAUtil中, 接口的名称是  QA_util_multi_demension_list(row_,col_)

如果需要创建一个[[],[]], 那就用 row_=2,col=0
其他时候,返回的都是[[None]]

```python
import QUANTAXIS as QA
QA.QAUtil.QA_util_multi_demension_list(3,0)
QA.QAUtil.QA_util_multi_demension_list(3,3)

```
```shell

[[], [], []]
[[None, None, None], [None, None, None], [None, None, None]]
```


### 1.27 修改了一个QABacktest的传参, 现在在策略中,需要指定买卖状态
2017/7/19

现在 QUANTAXIS在接受策略的传参的时候,需要指定买卖状态

在开始的时候,quantaxis使用的是if_buy和账户状态来判断是否买卖的

- 账户持仓, if_buy=1 视为卖出
- 账户空仓, if_buy=1 视为买入

买卖行为和账户状态相关联对于买卖的行为有很大的限制,现在对于这个行为和账户持仓状态进行了解耦

同时,为了兼容性,如果策略并没有给出if_buy或者if_sell,则会将其初始化为0,及不操作





以下是改动后的源代码

```python
    def __QA_backtest_excute_bid(self, __result,  __date, __hold, __code, __amount):
        """
        这里是处理报价的逻辑部分
        2017/7/19 修改

        __result传进来的变量重新区分: 现在需要有 if_buy, if_sell
        因为需要对于: 持仓状态下继续购买进行进一步的支持*简单的情形就是  浮盈加仓

        if_buy, if_sell都需要传入

        现在的 买卖状态 和 持仓状态 是解耦的
        """

        # 为了兼容性考虑,我们会在开始的时候检查是否有这些变量
        if 'if_buy' not in list(__result.keys()):
            __result['if_buy'] = 0

        if 'if_sell' not in list(__result.keys()):
            __result['if_sell'] = 0

        self.__QA_backtest_set_bid_model()
        if self.bid.bid['bid_model'] == 'strategy':
            __bid_price = __result['price']
        else:
            __bid_price = self.bid.bid['price']

        __bid = self.bid.bid

        __bid['order_id'] = str(random.random())
        __bid['user'] = self.setting.QA_setting_user_name
        __bid['strategy'] = self.strategy_name
        __bid['code'] = __code
        __bid['date'] = __date
        __bid['price'] = __bid_price
        __bid['amount'], __bid['amount_model'] = self.__QA_bid_amount(
            __result['amount'], __amount)

        if __result['if_buy'] == 1:
            # 这是买入的情况
            __bid['towards'] = 1
            __message = self.market.receive_bid(
                __bid, self.setting.client)

            if float(self.account.message['body']['account']['cash'][-1]) > \
                    float(__message['body']['bid']['price']) * \
                    float(__message['body']['bid']['amount']):
                    # 这里是买入资金充足的情况
                    # 不去考虑
                pass
            else:
                # 如果买入资金不充足,则按照可用资金去买入
                __message['body']['bid']['amount'] = int(float(
                    self.account.message['body']['account']['cash'][-1]) / float(
                        float(str(__message['body']['bid']['price'])[0:5]) * 100)) * 100

            if __message['body']['bid']['amount'] > 0:
                # 这个判断是为了 如果买入资金不充足,所以买入报了一个0量单的情况
                #如果买入量>0, 才判断为成功交易
                self.account.QA_account_receive_deal(__message)

        elif __result['if_buy'] == 0:
            # 如果买入状态为0,则不进行任何买入操作
            pass

        # 下面是卖出操作,这里在卖出前需要考虑一个是否有仓位的问题:
        # 因为在股票中是不允许卖空操作的,所以这里是股票的交易引擎和期货的交易引擎的不同所在

        if __result['if_sell'] == 1 and __hold == 1:
            __bid['towards'] = -1
            __message = self.market.receive_bid(
                __bid, self.setting.client)

            self.account.QA_account_receive_deal(
                __message)
```


### 1.28 对于backtest的加载的外部函数的接口进行修改
2017/7/20

对于backtest的加载的外部策略,现在暂时有以下三个句柄

- on_start
- strategy
- on_end

其中,on_start/on_end这两个句柄可有可无, strategy句柄是必须要有的

### 1.29 修改了QA_Query 里返回的数组格式
2017/7/21

```python
def QA_fetch_stock_day(code, startDate, endDate, collections=QA_Setting.client.quantaxis.stock_day, type_='numpy'):
    # print(datetime.datetime.now())
    startDate = str(startDate)[0:10]
    endDate = str(endDate)[0:10]

    if QA_util_date_valid(endDate) == True:

        list_a = []

        for item in collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": QA_util_date_stamp(endDate),
                "$gte": QA_util_date_stamp(startDate)}}):
            list_a.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['volume']), item['date'], float(item['turnover'])])
        ## 多种数据格式
        if type_ == 'numpy':
            data = numpy.asarray(list_a)
        elif type_ == 'list':
            data = list_a
        elif type_ == 'pandas':
            data = DataFrame(list_a, columns=[
                             'code', 'open', 'high', 'low', 'close', 'volume', 'date', 'turnover'])
        return data
    else:
        QA_util_log_info('something wrong with date')

```
现在可以通过QA_fetch_stock_day里面选择是返回list,numpy还是dataframe. 为了兼容性考虑,默认依然是numpy

### 1.30 修改了QA_util_save_csv的模式
2017/07/21


```python
def QA_util_save_csv(data: list, name: str, column=None, location=None):
    # 重写了一下保存的模式
    
    assert isinstance(data, list)
    if location == None:
        path = './' + str(name) + '.csv'
    else:
        path = location + str(name) + '.csv'
    with open(path, 'w', newline='') as f:
        csvwriter = csv.writer(f)
        if column == 'None':
            pass
        else:
            csvwriter.writerow(column)
        for item in data:
            csvwriter.writerow(item)

```

示例:

```python

import QUANTAXIS as QA

QA.QA_util_save_csv(QA.QA_fetch_stock_day('000001','2017-01-01','2017-07-01','list'),'000001')
```
```csv
000001,9.11,9.18,9.09,9.16,459840.47,2017-01-03,0.31
000001,9.15,9.18,9.14,9.16,449329.53,2017-01-04,0.31
000001,9.17,9.18,9.15,9.17,344372.91,2017-01-05,0.24
000001,9.17,9.17,9.11,9.13,358154.19,2017-01-06,0.24
000001,9.13,9.17,9.11,9.15,361081.56,2017-01-09,0.21
000001,9.15,9.16,9.14,9.15,241053.95,2017-01-10,0.14
000001,9.14,9.17,9.13,9.14,303430.88,2017-01-11,0.18
000001,9.13,9.17,9.13,9.15,428006.75,2017-01-12,0.25
000001,9.14,9.19,9.12,9.16,434301.38,2017-01-13,0.26
000001,9.15,9.16,9.07,9.14,683165.81,2017-01-16,0.4
000001,9.12,9.16,9.1,9.15,545552.38,2017-01-17,0.32
000001,9.14,9.19,9.13,9.17,574269.38,2017-01-18,0.34
000001,9.15,9.24,9.15,9.18,437712.88,2017-01-19,0.26
000001,9.17,9.23,9.17,9.22,393328.56,2017-01-20,0.23
000001,9.22,9.26,9.2,9.22,420299.31,2017-01-23,0.25
000001,9.23,9.28,9.2,9.27,470244.09,2017-01-24,0.28
000001,9.27,9.28,9.25,9.26,304401.97,2017-01-25,0.18
000001,9.27,9.34,9.26,9.33,420712.56,2017-01-26,0.25
000001,9.45,10.26,9.33,10.26,19345.0,2017-02-02,0.01
000001,9.34,9.36,9.23,9.26,315472.25,2017-02-03,0.19
000001,9.26,9.32,9.26,9.31,516786.12,2017-02-06,0.31
000001,9.31,9.32,9.27,9.3,396884.97,2017-02-07,0.23
...........
```
### 1.31 通达信5分钟线解析保存
2017/7/23

首先要下载:

- 深圳5分钟线

http://www.tdx.com.cn/products/data/data/vipdoc/sz5fz.zip

- 上证5分钟线

http://www.tdx.com.cn/products/data/data/vipdoc/sh5fz.zip

然后解压到一个目录里

```python

import QUANTAXIS as QA

QA.QA_SU_save_stock_min_5('你解压好的目录')


#例如 QA.QA_SU_save_stock_min_5('C:\\users\\yutiansut\\desktop\\sh5fz')
```
```bash

In [2]: QA.QA_SU_save_stock_min_5('C:\\users\\yutiansut\\desktop\\sz5fz')
QUANTAXIS>> Now_saving 000001's 5 min tick
QUANTAXIS>> Now_saving 000002's 5 min tick
QUANTAXIS>> Now_saving 000004's 5 min tick
QUANTAXIS>> Now_saving 000005's 5 min tick
QUANTAXIS>> Now_saving 000006's 5 min tick
QUANTAXIS>> Now_saving 000007's 5 min tick
QUANTAXIS>> Now_saving 000008's 5 min tick
QUANTAXIS>> Now_saving 000009's 5 min tick
QUANTAXIS>> Now_saving 000010's 5 min tick
QUANTAXIS>> Now_saving 000011's 5 min tick
QUANTAXIS>> Now_saving 000012's 5 min tick
QUANTAXIS>> Now_saving 000014's 5 min tick
QUANTAXIS>> Now_saving 000016's 5 min tick
QUANTAXIS>> Now_saving 000017's 5 min tick
QUANTAXIS>> Now_saving 000018's 5 min tick
QUANTAXIS>> Now_saving 000019's 5 min tick
QUANTAXIS>> Now_saving 000020's 5 min tick
QUANTAXIS>> Now_saving 000021's 5 min tick
QUANTAXIS>> Now_saving 000022's 5 min tick
QUANTAXIS>> Now_saving 000023's 5 min tick
QUANTAXIS>> Now_saving 000024's 5 min tick
QUANTAXIS>> Now_saving 000025's 5 min tick
QUANTAXIS>> Now_saving 000026's 5 min tick
QUANTAXIS>> Now_saving 000027's 5 min tick
QUANTAXIS>> Now_saving 000028's 5 min tick
```

### 1.32 获取指数k线的api更新
2017/7/24

```python
QA_fetch_index_day(code, startDate, endDate,type_='numpy' ,collections=QA_Setting.client.quantaxis.stock_day)

```

一般而言,直接使用QA_fetch_index_day(code, startDate, endDate)就可以了

### 1.33 QA_util更新 QA_util_time_stamp
2017/7/24

QA_util_time_stamp用于将时间转化成时间戳

```python
import QUANTAXIS as QA
QA.QA_util_time_stamp('2017-01-01 10:25:08')

```

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