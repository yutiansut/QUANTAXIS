# QUANTAXIS STU: 基于场景的QUANTAXIS使用指南

QUANTAXIS从毕业论文的模型框架到现在成为一个闭环解决方案已经有2年多的时间了, 相关的代码和bug没有少写, 但是文档却迟迟跟不上节奏, 导致开发和使用常常脱节, 但是当想有个时间来写文档的时候, 你会发现函数太多, 很难找到一个很好的切入点来进行讲解和描述, 因此这就是QUANTAXIS STU诞生的契机了-- 基于一些实际场景, 我们来对于QUANTAXIS 或者 量化这个事情进行一些有意义的探索和讨论


在开始这个 STU之前, 我们需要首先明白和清楚以下三个问题:

1. 在现实场景中, 我们需要解决哪些问题?
2. QUANTAXIS是什么, 他能怎么样帮助我快速高效的解决问题
3. 我应该从哪里获得支持以及 当我想把项目经验/心得/代码回馈给社区应该如何去做

首先我们来讨论第一个事情:

## 在现实场景中, 我们一般需要解决哪些问题?


从自身的实践以及在quantaxis社区的答疑中, 我大致总结了几个方向:


### 意向阶段的问题:

1. 当我对于行情进行了观察/有了一定理解以后, 我想将这个理解==> 转变成代码来看看能否实现自动化

2. 在学习了金融或者风险的理论以后, 想将其变成可以被模拟的场景分析/理论复现

3. 已有模型/初步代码, 想进行优化/完善 使其变得更加稳定,方便

4. 已有商业服务, 想提供相应的数据/分析等服务


### 回测阶段的问题:

1. 如何进行简单的日线/分钟线/单品种的回测?

2. 如何进行单一市场多品种的回测?

3. 如何进行单一市场多品种多周期的回测?

4. 如何进行多市场多周期多品种的回测?

5. 如何对回测进行优化(性能/绩效/风险/归因)

6. 如何组合多个策略?

7. 如何快速查看策略的结果并进行展示

### 分析阶段的问题:

1. 如何快速分析多个市场的数据

2. 如何基于我的需求去实现/构建代码

3. 如何连接第三方库(机器学习/线性规划)等


### 模拟阶段的问题:

1. 如何将回测的代码变成模拟交易的代码

2. 如何构建本地的模拟交易

3. 如何快速添加一个模拟交易

4. 实时状态下的模拟交易背后的运维

### 实盘阶段的问题

1. 如何快速的接入一个交易市场的api

2. 如何对于账户进行配置

3. 如何构建一个完整的闭环的实盘流程

4. 风控问题

### 应用/效率相关

1. 如何快速进行大量的回测

2. 定时/周期/单次的任务管理

3. 如何使用分布式来加速你的效率

4. 如何使用集群来加速你的稳定性

5. 如何使用docker来加速你的运维

6. 如何基于QA以及周边的解决方案解决现实的应用需求


基本上以上列举的场景和需求是每一个试图给出答案的量化框架必须解决的问题, 不同的项目的方向和侧重点有所不同, 但本质都绕不过这些核心问题的拷问


## QUANTAXIS是什么, 他能怎么样帮助我快速高效的解决问题

QUANTAXIS的核心是构建一个闭环的标准流程(SOP), 面向问题和场景来灵活的提供解决方案

### 什么是闭环, 为什么需要闭环

闭环是一个完整解决能力的体现, 包含了一个最小的完整量化流程(想法 - 分析 - 策略 - 回测 - 模拟 - 实盘 - 可视化展示), 依赖于这个闭环, 你可以在生产的任意角度切入并使用这个闭环加速你的流程, 节约时间/人员成本

### 什么是SOP, 为什么需要SOP

SOP(Standard Operating Procedure), 是用于定义每个阶段点的标准步骤和统一格式, 代表的是这个标准下的最基础功能集

在数据流程使用SOP, 最简单且显而易见的便利就是方便任意市场任意数据源的接入, 只要满足数据的格式标准, 以及接入的标准, 就可以很方便的将你的特定需求的数据接入到这个流程之中

在策略角度使用SOP, 可以方便且快速的通过配置来接入多个市场:

```python
QA.QA_Account(
    market_type= QA.MARKET_TYPE.FUTURE_CN,
    allow_t0 = True,
    allow_marigin = True,
    allow_sellopen = True
)
```
我们使用QA_Account来举一个实例, QA_Account方便接入多个市场的原因是他可以通过规则的配置来快速的接入多个市场, 是否允许t+0, 是否允许保证金交易, 是否允许卖出开仓, 三个规则的配置可以方便的让你接入 A股, 期货, 美股, 港股, 期权, 虚拟货币等多个市场

在模拟/实盘中使用SOP, 可以方便且快速的接入到多个市场

基于 QABroker/QAMarket 的配对, 可以快速加载某个市场的broker, 通过一致的api, 大量减少用户的迁移成本


### 什么是面向问题/场景, 如何灵活的使用解决方案(QUANTAXIS)

每个人需要解决的问题各不相同, 需求也经常大相径庭, 基础背景(代码能力, 有无原有项目)因人而异, 因此一个灵活可以配置的解决方案才是从用户角度出发的完美选择

- 减少项目迁移成本
- 减少语言成本
- 灵活快速解决问题



## 我应该从哪里获得支持以及 当我想把项目经验/心得/代码回馈给社区应该如何去做

### QUANTAXIS在哪里

QUANTAXIS是一个开源社区, 我们提倡在一定能力和必要下的开放和相互帮助, 在保证自身利益的前提下, 我们也鼓励大家更积极的参与社区的开发和维护

QUANTAXIS的项目地址> (https://github.com/QUANTAXIS/QUANTAXIS)

QUANTAXIS_MONITOR_GUI 基于QT的python监控 (https://github.com/QUANTAXIS/QUANTAXIS_Monitor_GUI)

QUANTAXIS_WEBSERVER 基于tornado的web api/ websocket (https://github.com/QUANTAXIS/QUANTAXIS_WEBSERVER)

QUANTAXIS_RUN 基于rabbitmq/celery的分布式任务部署 (https://github.com/QUANTAXIS/quantaxis_run)

QUANTAXIS_PUBSUB 基于RABBITMQ的消息分发订阅 (https://github.com/QUANTAXIS/QAPUBSUB)

QUANTAXIS_DESKTOP 基于VUE.js/ ELECTRON的 桌面终端 (https://github.com/quantaxisdesign/qamazing_community)

QUANTAXIS QADESKPRO 新版本客户端网页(部分开源) (https://github.com/yutiansut/qadeskpro)

portable_QA 一个独立的python环境,免配置 (https://github.com/QUANTAXIS/portable_QA)

QUANTAXIS_ATBROKER 基于海风at的接口封装 (https://github.com/QUANTAXIS/QA_AtBroker)

QUANTAXIS_CRAWLY 爬虫部分 (https://github.com/QUANTAXIS/QUANTAXIS_CRAWLY)

QUANTAXIS_REALTIME_RESOLUTION 实时交易/部署解决方案(未开源) (https://github.com/yutiansut/QUANTAXIS_REALTIME_RESOLUTION)

QUANTAXIS UNICORN QUANTAXIS 策略托管, 交易监控解决方案(未开源) (https://github.com/yutiansut/quantaxis_unicorn)

QUANTAXIS的QQ群> 563280067

### 如何提交 BUG/项目经验/心得/代码回馈


如果在使用过程中发现了bug, 请回报给社区: (https://github.com/QUANTAXIS/QUANTAXIS/issues/new)



当你想把你的一些项目经验/ 心得/ 代码反馈给社区, 欢迎使用 GITHUB PUll REQUEST (https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/about_pr.md)

项目经验/心得 请放在 Documents文件夹下

代码则在 QUANTAXIS目录下

示例代码在 Examples目录下


以上是一些关于QUANTAXIS STU的基础, 我们将在下一篇讨论和讲述 QUANTAXIS使用的一些基础准备

