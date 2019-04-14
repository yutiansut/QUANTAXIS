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