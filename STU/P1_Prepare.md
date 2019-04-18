# QUANTAXIS STU 01 PREPARE 使用QUANTAXIS之前的准备工作

工欲善其事必先利其器, 在正式讨论QUANTAXIS如何使用之前, 我们需要首先对于QUANTAXIS进行一些基本的了解

## QUANTAXIS项目/功能介绍

### QUANTAXIS
QUANTAXIS 的核心项目是 [QUANTAXIS/QUANTAXIS](https://github.com/quantaxis/quantaxis), 核心项目负责是一个基础的闭环流程, 包括

- 账户/组合/风险类  QAARP
- 市场/多市场接入/本地回测类/订单 QAMARKET
- 应用: QAApplication
- 数据获取/存储: QAFetch/ QASU
- 数据分析: QAData
- 指标系统: QAIndicator
- 配置/辅助功能: QASetting/QAUtil

通过以上几点, 我们可以实现一个完整的基于数据流/账户流的闭环解决方案: 

```
数据获取/存储/分析 ==> 策略/回测 ==> 模拟/实盘
```


QUANTAXIS的周边项目主要是对于QUANTAXIS的有效/必要补充, 依据个人使用场景/实际需求进行选配:

### QUANTAXIS_WEBSERVER

网站后台(用于提供行情/交易数据)  [QUANTAXIS/QUANTAXIS_WBESERVER](https://github.com/quantaxis/quantaxis_webserver)

### QUANTAXIS_Community

前端界面

win 安装版本: [下载](https://gitee.com/yutiansut/QUANTAXIS/attach_files/225937/download)

mac 安装版本: [下载](https://gitee.com/yutiansut/QUANTAXIS/attach_files/225940/download)

web 版本: [下载](https://gitee.com/yutiansut/QUANTAXIS/attach_files/225938/download)

### QUANTAXIS_RUN

[QUANTAXIS/QUANTAXIS_RUN](https://github.com/QUANTAXIS/quantaxis_run)

一个基于Rabbitmq的分布式运行库, 已经集成在quantaxis_webserver中

### QUANTAXIS_PUBSUB

[QUANTAXIS/QUANTAXIS_PUBSUB](https://github.com/QUANTAXIS/QAPUBSUB)

一个基于Rabbitmq的消息分发/订阅的模块

### QUANTAXIS_ATBROKER 

[QUANTAXIS/QUANTAXIS_ATBROKER](https://github.com/QUANTAXIS/QA_AtBroker)

一个基于海风AT封装的 CTP的BROKER

## QUANTAXIS的技术栈/依赖库

quantaxis主要使用的是python/mongodb作为核心技术栈, 在未来会更多的使用 rabbitmq/websocket等来加强系统的低耦合性和健壮性

一些你必须要知道的库/编辑器/技术方案


- python3.6+ 
- mongodb3.6+/ mongodb4.0/ robomongo(mongodb的可视化工具)

- ipython/ jupyter notebook 一个交互式的命令行/用于加速代码调试
- vscode 微软的代码编辑器/ 轻量级全平台的编辑器

- rabbitmq/ celery/ QAPUBSUB / 老牌MQ/以及相应的python的绑定库
- tornado/ QUANTAXIS_WEBSERVER 一个python的后台库, 用于提供http/websocket服务
- nodejs/ vue.js/ echarts.js/  前端开发库 适当了解即可

- docker 一个集群服务/ 用于加速/简化部署



在使用quantaxis的时候, 你需要的最小功能的单元工具栈是  

- python3.6/3.7
- mongodb

- 一个代码编辑器
- 一个命令行

##  如何使用quantaxis 并进行初始化

首先你需要知道的是, quantaxis是一个纯本地的框架服务, 也就是意味着数据是放在你的本地数据库中, 因此 首先需要开启mongodb

- 如何安装mongodb/ python / quantaxis的初始化环境请[参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/Documents/install.md)

- 在安装完毕后, 需要打开mongodb的服务, 并进行一些数据的初始化存储(按需) [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/Documents/about_updatedata.md)

在存储完毕数据以后, 你可能会陷入迷茫, 因为你不知道该做什么来进行下一步, 因为下面的场景是因人而异的, 我们对于下面的几种场景提供一些推荐的路径:


### IF: 你是一个学生/初学者/ 对于python 几乎0基础的同学:

首先的推荐是搞清楚自己的目的,诸如:

- 实现一个模型
- 验证一个想法
- 把行情软件的指标复现

然后基于这个目的, 来quantaxis中匹配你的需求:

- 我们推荐:

    - 阅读QUANTAXIS QAFETCH的文档, 了解如何从数据库中获取你想要的数据 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/Documents/DataFetch.md)

    - 阅读QUANTAXIS QADataStruct的文档, 了解QUANTAXIS是如何处理 多标的/多日期的的情况 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/Documents/DataStruct.md)

    - 阅读QUANTAXIS QAIndicator的文档, 了解如何在QUANTAXIS中使用一些默认指标/ 写出你自己的指标/ 移植通达信/同花顺的指标 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/Documents/indicators.md)

### IF: 你已经在别的平台撰写过回测/ 对于如何进行回测有了一定的了解:


我们推荐的是首先做一个回测样例体验一下, 目前QUANTAXIS支持的是:

股票/期货的 日线/分钟线 的回测(支持保证金交易)

相关的回测代码你可以在 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/EXAMPLE/4_回测实盘交易) 中找到

当然, 由于QUANTAXIS QAAccount的灵活配置的机制, 你可以快速的接入各个你想要的市场中, 关于 QA_Account 你可以参见

- QUANTAXIS USER 的属性 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/EXAMPLE/2_%E7%B1%BB%E7%9A%84%E6%B5%8B%E8%AF%95%E4%B8%8E%E8%AE%B2%E8%A7%A3/QAUSER.ipynb)

- QUANTAXIS QAAccount的保证金测试 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/EXAMPLE/2_类的测试与讲解/QAACCOUNT%20保证金冻结释放测试.ipynb)

- QUANTAXIS QAAccount [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/EXAMPLE/2_%E7%B1%BB%E7%9A%84%E6%B5%8B%E8%AF%95%E4%B8%8E%E8%AE%B2%E8%A7%A3/QAAccount.ipynb)


### IF: 你已经对于QUANTAXIS有了相当的理解, 需要自定义一些自己的代码:

我们推荐你参考阅读:

- QUANTAXIS的源代码 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/QUANTAXIS)
- QUANTAXIS QAEngine 有关的多线程引擎的代码 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/Documents/about_event.md)
- QUANTAXIS MARKET 关于市场和broker的关系 [参见](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/Documents/about_market.md)
- QUANTAXIS RUN 如何进行分布式回测/任务 [参见](https://github.com/QUANTAXIS/QUANTAXIS_RUN)


P1课程基本结束, 在下一个P2课程中, 我们将完整讨论如何进行回测/ 在回测场景中你常常会遇到的问题