QUANTAXIS-Protocol
标准化协议QAS/未来协议QAF
------------

- 当前版本:0.0.6
- 协议最后修改日期:2017-04-11
- 项目版本:QUANTAXIS 0.3.8

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
    - [QAS-102x-x QAS_fetch_data](#qas-102x-x-qas_fetch_data)
- [QAS-20x QASU(save/update)数据存储/更新](#qas-20x-qasusaveupdate数据存储更新)
    - [QAS-201-x QA_SU_save_](#qas-201-x-qa_su_save_)
    - [QAS-_202-x QA_SU_update_](#qas-_202-x-qa_su_update_)
    - [QAS-203-x QA_SU_user](#qas-203-x-qa_su_user)
- [QAS-30x QAMarket 市场机制类](#qas-30x-qamarket-市场机制类)
    - [QAS-301-x QA_Market](#qas-301-x-qa_market)
    - [QAS-302-x QA_QAMarket_bid](#qas-302-x-qa_qamarket_bid)
- [QAS-40x QABacktest 回测类](#qas-40x-qabacktest-回测类)
- [QAS-50x QAARP(account/risk/portfolio)账户/风险/组合管理类](#qas-50x-qaarpaccountriskportfolio账户风险组合管理类)
- [QAS-60x QAUtil 工具类](#qas-60x-qautil-工具类)
- [QAS-70x QASpider 爬虫类](#qas-70x-qaspider-爬虫类)
- [QAS-80x QASignal 信号/事件驱动类](#qas-80x-qasignal-信号事件驱动类)
    - [QAS-801-x QA_signal_](#qas-801-x-qa_signal_)
        - [QAS-801-1 QA_signal_send 协议](#qas-801-1-qa_signal_send-协议)
        - [QAS-801-1 QA_signal_resend 协议](#qas-801-1-qa_signal_resend-协议)
- [QAS-90x QATask 任务机制/异步类](#qas-90x-qatask-任务机制异步类)
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

- QA+ _大写字母类+_小写字母 ( QA_Account,QA_Risk,QA_Market,QA_QAMarket_bid,QA_Backtest )
### QAS-003-3 函数命名方式
函数的命名

- QA_模块名_小写字母的函数 (QA_util_date_stamp)

函数的命名除了QA,后面的模块已经函数全部小写,同时,以简单易懂,名词-动词形式为主

主要是为了区分和类的关系

> 但如果模块是缩写形式,则缩写部分还是大写,如 QA_SU_save_stock_day

```
QA_QAMarket_bid  这个是类
QA_util_time_stamp 这个是函数
```
### QAS-003-4 数据库/表命名方式
由于多数据源的问题,我们规定了基础指标和扩展指标,方便用户的不同权限的自定义需求

比如说,如果你只有免费的数据源通道,那么你可以选择基础的指标(tushare,wind大奖章)

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

## QAS-102x-x QAS_fetch_data

# QAS-20x QASU(save/update)数据存储/更新 
## QAS-201-x QA_SU_save_

## QAS-_202-x QA_SU_update_

## QAS-203-x QA_SU_user

# QAS-30x QAMarket 市场机制类 
## QAS-301-x QA_Market
## QAS-302-x QA_QAMarket_bid
bid是一个标准报价包
```python

    price=4.5
    time='2000-01-17'
    amount=10
    towards=1
    code=str('000001.SZ')
    user='root'
    strategy='root01'
```

# QAS-40x QABacktest 回测类
- QA_Backtest
# QAS-50x QAARP(account/risk/portfolio)账户/风险/组合管理类
- QA_Account
- QA_Risk
- QA_Portfolio
# QAS-60x QAUtil 工具类
- QA_util_

# QAS-70x QASpider 爬虫类
# QAS-80x QASignal 信号/事件驱动类
## QAS-801-x QA_signal_
### QAS-801-1 QA_signal_send 协议
打包出标准化协议,模仿http协议
```python
message={
    'header':{
        'source':source_name,
        'cookie':xxxx,
        'session':{
            'user':xxx,
            'strategy':xxxx
        }
        
    },
    'body':{
        
    }
}
```
###  QAS-801-1 QA_signal_resend 协议
# QAS-90x QATask 任务机制/异步类

# QAS-100x QACmd 命令行扩展类
