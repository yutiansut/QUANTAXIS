
# QUANTAXIS 量化金融策略框架


## ATTENTION!!!  QUANTAXIS无任何收费项目 请勿相信任何渠道的私聊!!!!
------------------
 

[![Github workers](https://img.shields.io/github/watchers/quantaxis/quantaxis.svg?style=social&label=Watchers&)](https://github.com/quantaxis/quantaxis/watchers)
[![GitHub stars](https://img.shields.io/github/stars/quantaxis/quantaxis.svg?style=social&label=Star&)](https://github.com/quantaxis/quantaxis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/quantaxis/quantaxis.svg?style=social&label=Fork&)](https://github.com/quantaxis/quantaxis/fork)

[点击右上角Star和Watch来跟踪项目进展! 点击Fork来创建属于你的QUANTAXIS!]

![QUANTAXIS_LOGO_LAST_small.jpg](http://pic.yutiansut.com/Fn0TPEcwu_uhraf58_93Ul5yfvAz)

![gvp](http://pic.yutiansut.com/gvp.jpg)

Quantitative Financial FrameWork

从数据爬取-清洗存储-分析回测-可视化-交易复盘的本地一站式解决方案

支持 python/rust 的数据下载 自动运维(a 股/期货/期权/港美股/数字货币), 支持可配置的自定义账户和组合协议(QIFI), 支持股票/期货市场全推的数据协议(MIFI), 支持策略打点和动态画图的界面可视化协议(VIFI), 支持 a 股/ 期货/ 港美股的实盘交易及本地无限制账户的模拟盘. 支持 docker 一键部署和局域网内的 k8s 集群部署, 基于 celery/rabbitmq 实现分布式的回测/模拟/实盘的任务队列. 支持行情二次重采样, 账户订单二次转发, 订单流风控. 支持完全自定义的行情分发(模拟/真实/OU 随机过程)以及行情回放(用于复盘/模拟环境创建).  支持基于 QIFI 协议的各种客户端的自行接入(手机 APP/网页 web/终端) 

目前为私募([杭州波粒二象资产管理有限公司](https://dc.simuwang.com/company/CO00000XXI.html))自用框架, python 部分完全开源, rust 部分以 docker 微服务形式提供




QUANTAXIS 项目从2017年开始  已经从一个写毕业论文时没有框架  到现在实际在私募中稳定运行的项目了 因此QUANTAXIS对于刚接触的人会感觉较为庞大和无从入手, 在经历了群里的同学和一些实际企业的部署以后 , 我们希望你可以从以下方式逐步入手和了解QUANTAXIS



## QUANTAXIS提供什么

简单的讲 QUANTAXIS 提供的是一个从0到一个完整的可以上实盘的支持多市场多周期多策略的框架, 支持局域网/互联网远程部署

- 投研分析

  - 全市场数据(日线/分钟线/tick)
  - 财务数据
  - 股票/期货/期权/港股/美股/(以及自定义数据源)
  - 为多品种优化的数据结构QADataStruct
  - 为大批量指标计算优化的QAIndicator [支持和通达信/同花顺指标无缝切换]
  - 基于docker提供远程的投研环境
  - 自动数据运维

- 回测

  - 纯本地部署/开源
  - 全市场(股票/期货/自定义市场[需要按规则配置])
  - 多账户(不限制账户个数, 不限制组合个数)
  - 多品种(QADataStruct原生为多品种场景进行了优化)
  - 跨周期(基于动态的resample机制)
  - 多周期(日线/周线/月线/1min/5min/15min/30min/60min/tick)
  - 可视化(提供可视化界面)
  - 自定义的风控分析/绩效分析

- 模拟

  - 支持股票/期货的实时模拟(不限制账户)
  - 支持定向推送/全市场推送
  - 支持多周期实时推送/ 跨周期推送
  - 模拟和回测一套代码
  - 模拟和实盘一套代码
  - 可视化界面
  - 提供微信通知模版

- 实盘

  - 支持股票(需要自行对接)
  - 支持期货(支持CTP接口)
  - 和模拟一套代码
  - 不限制账户数量
  - 基于策略实现条件单/风控单等
  - 可视化界面
  - 提供微信通知模版

- 终端

  - 提供mac/windows的可安装版本(QACommunity)
  - 提供全平台可用的web界面
  - 提供手机客户端(ios/andriod)  [内测中]

  



## QUANTAXIS如何部署/使用

因为QUANTAXIS和其相关联的项目约有19个之多, 包括了从本地账户系统到数据收集, 数据分发, 数据存储, 实时的消息分发, 策略挂载, 可视化, 投研环境 等大量内容, 因此 不推荐用户在不熟悉的情况下进行本地部署, 我们推荐的路径(也是我们在私募中实际使用也是)是docker模式



### 部署

docker可以理解为一个高效的虚拟机环境(性能损失不到2%), 每个虚拟机包含了一部分独立的代码内容, 因此我们通过类似叠积木的形式就可以将我们所需要的环境一个一个搭建起来

我们推荐:

| Win10 企业版/教育版 | 路径                                                  |      |
| ------------------- | ----------------------------------------------------- | ---- |
| Win10 企业版/教育版 | 通过docker-desktop                                    |      |
| Win10 家庭版/Win7   | 推荐升级系统至win10企业版, 或者使用docker-toolbox部署 |      |
| Linux用户           | 支持一键部署脚本, 快速拉起docker                      |      |
| Mac用户             | 通过docker-desktop                                    |      |
| 强行需要代码部署    | 19个项目 8个服务需要自行手动开启                      |      |

### 使用

对于初学者, 我们推荐直接上手```QAStrategy```来直接编写回测/模拟/实盘


    QAStrategy传送门: 
    
    [QAStrategy](https://github.com/yutiansut/QAStrategy）

PS: 除了可视化的桌面端/网页端 QACommunity(内置在docker/ 群文件自行下载) 以外,  QAStrategy专属的APP也即将上架, 支持自定义的服务器后端连接, 实时的实盘账户手动干预, 行情处理, 持仓管理以及多策略的运行调整等 



### QUANTAXIS的结构



![QUANTAXIS 2019.png](http://pic.yutiansut.com/FnRlMW2LQpFBrsdRv7E_uJ9RvzHt)

技术栈: python/nodejs/vue/mongodb/rabbitmq/c++

### 核心工具链(生产环境在用)

![QQ图片20191029223640.png](http://pic.yutiansut.com/FuVrzcbWJUBNrj4Wa0zlRl-YlBY_)

#### 已开源

> 数据存储/数据分析/回测

- [QUANTAXIS](https://github.com/QUANTAXIS/QUANTAXIS) QUANTAXIS的核心部分

> WEB相关, http/websocket/开放数据接口

- [QUANTAXIS_WEBSERVER](https://github.com/QUANTAXIS/QUANTAXIS_WEBSERVER) 基于tornado的web api/ websocket

> 分布式相关, 任务异步执行, 跨进程分布式消息订阅分发

- [QUANTAXIS_RUN](https://github.com/QUANTAXIS/quantaxis_run) 基于rabbitmq/celery的分布式任务部署
- [QUANTAXIS_PUBSUB](https://github.com/QUANTAXIS/QAPUBSUB) 基于RABBITMQ的消息分发订阅

> 接口相关: 交易账户/ 期货接口封装/ Trader实例
- [QATradeG](https://github.com/yutiansut/QAtradeG)  期货的直连版本接口的docker
- [QUANTAXIS OTGBROKER](https://github.com/QUANTAXIS/QAOTGBROKER) 基于OPEN_TRADE_GATEWAY的接口封装
- [QUANTAXIS CTPBEEBROKER](https://github.com/QUANTAXIS/QACTPBeeBroker) 基于CTPBee的接口封装
- [QUANTAXIS_ATBROKER](https://github.com/QUANTAXIS/QA_AtBroker) 基于海风at的接口封装
- [QUANTAXIS TRADER](https://github.com/yutiansut/QATrader) 一个开源的websocket版本的期货交易实例

> 策略相关 
- [QASTRATEGY101](https://github.com/yutiansut/QAStrategy101) 101个基础策略[逐步更新中...]

> 行情相关: 主推行情实现/ 基于OU过程的模拟行情
- [QUNATAXIS MARKETCOLLECTOR](https://github.com/yutiansut/QUANTAXIS_RealtimeCollector) 全市场订阅分发的行情推送
- [QUANTAXIS_RandomPrice](https://github.com/yutiansut/QUANTAXIS_RandomPrice) 基于OU过程的随机行情模拟

> 账户协议

- [QIFI](https://github.com/QUANTAXIS/QIFI) 一个基于快期DIFF协议的QA实时账户协议
- [QIFIAccount](https://github.com/yutiansut/qifiaccount) 一个基于QIFI协议的多市场兼容的 实时账户实现
- [QAStrategy](https://github.com/yutiansut/qastrategy) 一个完整的 支持 模拟/回测/实盘一键切换的策略基类

> 多语言实现

- [qatrader-rs](https://github.com/yutiansut/qatrader-rs) 一个rust实现的qatrader
- [qamarket-rs](https://github.com/yutiansut/qamarket-rs)  一个rust实现的期货全市场行情多周期采样分发



#### 未开源

未开源部分为 目前私募自用部分, 因此暂时不开源 一些相关的项目会经过选取和完善后逐步开源

> 实时交易解决方案/ 无人值守/状态汇报/实时账户评估/多账户/策略账户拆分/事件流风控/PB系统/CEP引擎/多系统终端

- [QUANTAXIS_REALTIME_RESOLUTION](https://github.com/yutiansut/QUANTAXIS_REALTIME_RESOLUTION) 实时交易/部署解决方案(未开源)
- [QUANTAXIS UNICORN](https://github.com/yutiansut/quantaxis_unicorn) QUANTAXIS 策略托管, 交易监控解决方案(未开源)
- [QUANTAXIS_RANK](https://github.com/yutiansut/QARank) QUANTAXIS实时账户评估
- [QUANTAXIS_CEPEngine](https://github.com/yutiansut/QACEPEngine) QUANTAXIS 复杂事件处理引擎
- [QUANTAXIS_PBSystem](https://github.com/yutiansut/QAPBSystem) QUANTAXIS PB系统
- [QUANTAXIS_QARISKPRO](https://github.com/yutiansut/QARISKPRO) QUANTAXIS 多市场多账户集成的实时风控系统
- [QUANTAXIS QADESKPRO](https://github.com/yutiansut/qadeskpro) 新版本客户端网页(部分开源)
- [QUANTAXIS PMS](https://github.com/yutiansut/QAPMS) 一个轻量级的纯python实现的  兼容QIFI协议的账户/仓位管理系统

> tick回测

- [QUANTAXIS TICKBacktest](https://github.com/yutiansut/QATickBacktest) tick回测 支持真实tick/仿真tick

> jupyterhub 定制(多人编辑)

- [QUANTAXIS JUPYTERHUB](https://github.com/yutiansut/QAJupyter)

> docker cluster

- [QUANTAXIS PROCluster](https://github.com/yutiansut/QAPRO_dockercluster) 一键部署的docker集群, 2地3中心的高可用灾备投研/交易环境

> Runtime 一个标准化的策略运行时

- [QUANTAXIS RUNTIME-RS](https://github.com/yutiansut/qaruntime-rs) 一个rust-base的策略标准化运行时  单机可以拉起10k+ 策略
- [QAStrategy-rs](https://github.com/yutiansut/qamom-rs) rust-base的策略标准化封装工具
- [QUANTAXIS-RS](https://github.com/yutiansut/quantaxis-rs) 全新的rust版本的quantaxis底层账户
- [QADATA-RS](https://github.com/yutiansut/qadata-rs) 标准化的数据结构 数据获取封装



### 社区提供的工具链

- [QUANTAXIS_MONITOR_GUI](https://github.com/QUANTAXIS/QUANTAXIS_Monitor_GUI) 基于QT的python监控
- (目前废弃)[QUANTAXIS_DESKTOP](https://github.com/QUANTAXIS/QADESKTOP) 基于VUE.js/ ELECTRON的 桌面终端
- [portable_QA](https://github.com/QUANTAXIS/portable_QA) 一个独立的python环境,免配置
- [QUANTAXIS_CRAWLY](https://github.com/QUANTAXIS/QUANTAXIS_CRAWLY) 爬虫部分

## 社区/项目捐赠

### github

QUANTAXIS 是一个开放的项目, 在开源的3年中有大量的小伙伴加入了我, 并提交了相关的代码, 感谢以下的同学们

<a href="https://github.com/QUANTAXIS/QUANTAXIS/graphs/contributors"><img src="https://opencollective.com/QUANTAXIS/contributors.svg?width=890&button=false" /></a>



许多问题 可以在 [GITHUB ISSUE](https://github.com/QUANTAXIS/QUANTAXIS/issues)中找到, 你可以提出新的issue



### QQ群

欢迎加群讨论: 563280067 [群链接](https://jq.qq.com/?_wv=1027&k=4CEKGzn) 

DISCORD 社区  https://discord.gg/mkk5RgN


QUANTAXIS 开发群: 773602202 (如果想要贡献代码 请加这个群 需要备注你的GITHUB ID)

QUANTAXIS 期货实盘多账户的本地部署群 (请勿浪费群资源 没有本地多账户部署的请勿加): 945822690

### 公共号

欢迎关注公众号: ![公众号](http://data.yutiansut.com/qrcode_for_gh_bbb47e0550f7_258.jpg)

QAPRO公共号免费提供了下单推送接口, 关注公共号回复trade即可使用

### 论坛 QACLUB

QUANTAXIS 内测版论坛 [QUANTAXISCLUB上线](http://www.yutiansut.com:3000)

http://www.yutiansut.com:3000

凡通过论坛进行提问的 均有最高的回复优先级

### 文档

全新文档界面 [QUANTAXISDocs](http://doc.yutiansut.com)

http://doc.yutiansut.com

 ### 捐赠

写代码不易...请作者喝杯咖啡呗?


![](http://pic.yutiansut.com/alipay.png)

(PS: 支付的时候 请带上你的名字/昵称呀 会维护一个赞助列表~ )

[捐赠列表](CONTRIBUTING.md)



##  QUANTAXIS 桌面级产品(全平台 WIN/MAC/LINUX)




首页

![image.png](http://pic.yutiansut.com/FnGCyLQ8nRLFOYX8elP4PhJ7IQuq)

登陆

![image.png](http://pic.yutiansut.com/FmDc4ZPxHeNncZICoMr9dqz46h78)

行情/键盘精灵

![image.png](http://pic.yutiansut.com/FhiN_asx158UobclVpCY00e61pjr)

lab 投研

![image.png](http://pic.yutiansut.com/FlkJTKu7iG-FD7Rz2DwUhvs2Cy3j)

回测/组合

![image.png](http://pic.yutiansut.com/FuB_dC5vX5Y1_Z8At0MiMRXcE5ZT)
![image.png](http://pic.yutiansut.com/Fqvh8m1ka4jdmwYwBn8MAHixpZOm)

模拟实盘多账户管理
![image.png](http://pic.yutiansut.com/Fh0fZzqORNRmY5txaXYgHWJUCPqw)
![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20190311015440.png)
![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20190311015451.png)
![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20190311015550.png)
![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20190311015537.png)



致谢:

感谢JetBrain 公司提供的开源社区全系列License
