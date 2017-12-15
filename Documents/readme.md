QUANTAXIS-Protocol
标准化协议QAS/未来协议QAF
------------

- 当前版本:0.0.9
- 协议最后修改日期:2017-12-04
- 项目版本:QUANTAXIS 0.5.25
  <!-- TOC -->

- [QAS-00x Intro  简介](#qas-00x-intro--简介)
    - [QAS-001-x  About](#qas-001-x--about)
        - [QAS-001-1 关于QUANTAXIS](#qas-001-1-关于quantaxis)
        - [QAS-001-2 关于QUANTAXIS-Standard-Protocol](#qas-001-2-关于quantaxis-standard-protocol)
        - [QAS-001-3 关于QUANTAXIS-Future-Protocol](#qas-001-3-关于quantaxis-future-protocol)
    - [QAS-002-x Module 模块](#qas-002-x-module-模块)
        - [QAS-002-1 Basical Module 基础模块](#qas-002-1-basical-module-基础模块)
        - [QAS-002-2 Extension Module 扩展模块](#qas-002-2-extension-module-扩展模块)
        - [QAS-002-3 Mod 插件模块](#qas-002-3-mod-插件模块)
    - [QAS-003-x Criterion 规范](#qas-003-x-criterion-规范)
        - [QAS-003-1 模块命名方式](#qas-003-1-模块命名方式)
        - [QAS-003-2 类命名方式](#qas-003-2-类命名方式)
        - [QAS-003-3 函数命名方式](#qas-003-3-函数命名方式)
        - [QAS-003-4 数据库/表命名方式](#qas-003-4-数据库表命名方式)
        - [QAS-003-5 RESTful 通信命名方式](#qas-003-5-restful-通信命名方式)
- [QAS-10x QAFetch 数据获取类](#qas-10x-qafetch-数据获取类)
    - [QAS-101-x QA_fetch_get_](#qas-101-x-qa_fetch_get_)
    - [QAS-102x-x QAS_fetch_](#qas-102x-x-qas_fetch_)
- [QAS-20x QASU(save/update)数据存储/更新](#qas-20x-qasusaveupdate数据存储更新)
    - [QAS-201-x QA_SU_save_](#qas-201-x-qa_su_save_)
    - [QAS-_202-x QA_SU_update_](#qas-_202-x-qa_su_update_)
    - [QAS-203-x QA_SU_user](#qas-203-x-qa_su_user)
- [QAS-30x QAMarket 市场机制类](#qas-30x-qamarket-市场机制类)
    - [QAS-301-x QA_Market](#qas-301-x-qa_market)
    - [QAS-302-x QA_Order](#qas-302-x-QA_Order)
- [QAS-40x QABacktest 回测类](#qas-40x-qabacktest-回测类)
- [QAS-50x QAARP(account/risk/portfolio)账户/风险/组合管理类](#qas-50x-qaarpaccountriskportfolio账户风险组合管理类)
    - [QAS-501-x QA_Account](#qas-501-x-qa_account)
    - [QAS-501-x QA_Risk](#qas-501-x-qa_risk)
    - [QAS-501-x QA_Portfolio](#qas-501-x-qa_portfolio)
- [QAS-60x QAUtil 工具类](#qas-60x-qautil-工具类)
- [QAS-70x QASpider 爬虫类](#qas-70x-qaspider-爬虫类)
- [QAS-80x QASignal 信号/事件驱动类](#qas-80x-qasignal-信号事件驱动类)
- [QAS-90x QATask 任务/事件队列](#qas-90x-qatask-任务事件队列)
    - [QAS-901 QA_Event](#qas-901-qa_event)
    - [QAS-902 QA_Queue](#qas-902-qa_queue)
    - [QAS-903 QA_Task_Center](#qas-903-qa_task_center)
    - [QAS-904 QA_MultiProcessing](#qas-904-qa_multiprocessing)
    - [QAS-905 QA_schedule](#qas-905-qa_schedule)
- [QAS-100x QACmd 命令行扩展类](#qas-100x-qacmd-命令行扩展类)

<!-- /TOC -->


# QAS-00x Intro  简介
## QAS-001-x  About 
### QAS-001-1 关于QUANTAXIS
QUANTAXIS量化金融策略框架,是一个面向中小型策略团队的量化分析解决方案. 我们通过高度解耦的模块化以及标准化协议,可以快速的实现面向场景的定制化解决方案.QUANTAXIS是一个渐进式的开放式框架,你可以根据自己的需要,引入自己的数据,分析方案,可视化过程等,也可以通过RESTful接口,快速实现多人局域网/广域网内的协作.


### QAS-001-2 关于QUANTAXIS-Standard-Protocol
QUANTAXIS-Standard-Protocol(下称QAS)是为了规范化和标准化QUANTAXIS的数据获取,数据存储,模拟市场交易,以及标准化输出而建立的协议.通过遵守QAS协议,你可以快速的实现定制化需求,当然,你也可以在QAS的基础上增加自己的团队标准.

### QAS-001-3 关于QUANTAXIS-Future-Protocol
QUANTAXIS-Future-Protocol(下称QAF)是一些目前尚未实现或未添加的功能/想法,通过issue提交和pull request,你可以参与到QAF的定制与完善中来.

## QAS-002-x Module 模块
QUANTAXIS是一个渐进式框架,所以会有基础模块和扩展模块之分
### QAS-002-1 Basical Module 基础模块
- [数据获取类 QAFetch](#qas-10x-qafetch-数据获取类)
  QAFetch 主要是从固定的API获取数据,包括且不限于(Tushare,Wind,Gmsdk)等等,你也可以引入自己的数据模块接口.


- [数据存储/更新类 QASU](#qas-20x-qasusaveupdate数据存储更新类)
- [市场机制类 QAMarket](#qas-30x-qamarket-市场机制类)
- [回测类 QABacktest](#qas-40x-qabacktest-回测类)
- [账户/风险/组合管理类 QAARP](#qas-50x-qaarpaccountriskportfolio账户风险组合管理类)
- [工具类 QAUtil](#qas-60x-qautil-工具类)
### QAS-002-2 Extension Module 扩展模块
- [爬虫类 QASpider](#qas-70x-qaspider-爬虫类)
- [信号/事件驱动类 QASignal](#qas-80x-qasignal-信号事件驱动类)
- [任务机制/异步类 QATask](#qas-90x-qatask-任务机制异步类)
- [命令行扩展类 QACmd](#qas-100x-qacmd-命令行扩展类)
### QAS-002-3 Mod 插件模块
- [QUANTAXIS-Webkit 插件](https://github.com/yutiansut/QUANTAXIS_Webkit)
- [QUANTAXIS-OpenCenter 插件](https://github.com/yutiansut/QUANTAXIS_OpenCenter)

## QAS-003-x Criterion 规范
### QAS-003-1 模块命名方式
模块的命名 

- QA+首字母大写的方法(QASpider/QAFetch/QAMarket/QASignal/QATask/QAUtil)
- QA+纯大写字母的缩写(QASU,QAARP)

>一般而言,模块是不修改的,当然,如果你需要深度定制你的模块名,则不仅需要遵守QAS#003-1协议,还需要修改"__init__.py",才能使你的模块生效

### QAS-003-2 类命名方式
类的命名

- QA+ _大写字母类+_小写字母 ( QA_Account,QA_Risk,QA_Market,QA_Order,QA_Backtest )
### QAS-003-3 函数命名方式
函数的命名

- QA_模块名_小写字母的函数 (QA_util_date_stamp)

函数的命名除了QA,后面的模块已经函数全部小写,同时,以简单易懂,名词-动词形式为主

主要是为了区分和类的关系

> 但如果模块是缩写形式,则缩写部分还是大写,如 QA_SU_save_stock_day

```
QA_Order  这个是类
QA_util_time_stamp 这个是函数
```
### QAS-003-4 数据库/表命名方式
由于多数据源的问题,我们规定了基础指标和扩展指标,方便用户的不同权限的自定义需求

比如说,如果你只有免费的数据源通道,那么你可以选择基础的指标(pytdx,wind大奖章)

如果你具有wind机构版权限,那么你可以在免费的指标上扩展你的指标,但仍然保持原有的基础指标名不变

```
Client: ip:port
DataBase: quantaxis
Collections:
- trade_date,stock_list,options_list
- stock_day,future_day,options_day
- stock_tick,future_tick,options_tick
- log_signal
- user_setting,user_trade_history

Basical Key:
- date
- date_stamp
- open *stock
- high *stock
- low  *stock
- close *stock
- code
- name
```

### QAS-003-5 RESTful 通信命名方式

# QAS-10x QAFetch 数据获取类
## QAS-101-x QA_fetch_get_
QA_fetch_get 系列是数据从外部获取的方法,一般而言,这个系列的函数方法封装的都是api

在使用这个fetch_get系列的时候,一般要指定数据源,比如是wind,或者tushare,或者Gmsdk等等


在QUANTAXIS.QAFetch 可以直接用的
```python
from QUANTAXIS.QAFetch import *
```
- QA_fetch_get_stock_day
- QA_fetch_get_stock_realtime
- QA_fetch_get_stock_indicator
- QA_fetch_get_trade_date

在QUANTAXIS.QAFetch.QATushare中可以用的
``` python
from QUANTAXIS.QAFetch.QATushare import *
```
- QA_fetch_get_stock_day
- QA_fetch_get_stock_realtime
- QA_fetch_get_stock_info
- QA_fetch_get_stock_tick
- QA_fetch_get_stock_list
- QA_fetch_get_trade_date


## QAS-102x-x QAS_fetch_
这个没有get_头的,是从本地数据库中获取数据

一般是本地的交易回测引擎和策略会使用这个api

```python
from QUANTAXIS.QAFetch.QAQuery import *
```
- QA_fetch_stock_day
- QA_fetch_trade_date
- QA_fetch_stock_info
- QA_fetch_stocklist_day
- QA_fetch_index_day


# QAS-20x QASU(save/update)数据存储/更新 
## QAS-201-x QA_SU_save_

这个系列是QUANTAXIS的存储数据的api方法,使用的数据库是mongodb

## QAS-_202-x QA_SU_update_

## QAS-203-x QA_SU_user

# QAS-30x QAMarket 市场机制类 
## QAS-301-x QA_Market
## QAS-302-x QA_Order
bid是一个标准报价包
```python

    bid={
        'price':float(16),
        'date':str('2015-01-05'),
        'amount':int(10),
        'towards':int(1),
        'code':str('000001'),
        'user':str('root'),
        'strategy':str('example01'),
        'status':'0x01',
        'order_id':str(random.random())
        }
```

# QAS-40x QABacktest 回测类
- QA_Backtest
  QA_Backtest 里面有4个抽象类:
```python
account=QA_Account()
market=QA_Market()
bid=QA_Order()
setting=QA_Setting()
```
# QAS-50x QAARP(account/risk/portfolio)账户/风险/组合管理类
- QA_Account
- QA_Risk
- QA_Portfolio
## QAS-501-x QA_Account
## QAS-501-x QA_Risk
## QAS-501-x QA_Portfolio
# QAS-60x QAUtil 工具类
- QA_util_

# QAS-70x QASpider 爬虫类
# QAS-80x QASignal 信号/事件驱动类

# QAS-90x QATask 任务/事件队列

QATASK 给了5种不同场景下的解决方案:

- QA_Event  主要负责的是事件的一对多的分发和订阅

- QA_Queue  主要负责的是维护一个函数句柄队列,可以理解为一个生产者消费者模型

- QA_Task_Center  主要负责的是一个对外的兼容接口,无论是socket,还是zeromq,celery,rabbitmq,redis等等

- QA_Multi_Processing  主要是一个多线程和多进程的

- QA_Schedule 主要是一个定时/延时任务机制


## QAS-901 QA_Event
## QAS-902 QA_Queue
## QAS-903 QA_Task_Center
## QAS-904 QA_MultiProcessing
## QAS-905 QA_schedule


# QAS-100x QACmd 命令行扩展类
