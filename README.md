# QUANTAXIS 2.0.0

[![Github workers](https://img.shields.io/github/watchers/quantaxis/quantaxis.svg?style=social&label=Watchers&)](https://github.com/quantaxis/quantaxis/watchers)
[![GitHub stars](https://img.shields.io/github/stars/quantaxis/quantaxis.svg?style=social&label=Star&)](https://github.com/quantaxis/quantaxis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/quantaxis/quantaxis.svg?style=social&label=Fork&)](https://github.com/quantaxis/quantaxis/fork)

[点击右上角Star和Watch来跟踪项目进展! 点击Fork来创建属于你的QUANTAXIS!]

![QUANTAXIS_LOGO_LAST_small.jpg](http://picx.gulizhu.com/Fn0TPEcwu_uhraf58_93Ul5yfvAz)

![gvp](http://picx.gulizhu.com/gvp.jpg)


更多文档在[QABook Release](https://github.com/QUANTAXIS/QUANTAXIS/releases/download/latest/quantaxis.pdf)

Quantitative Financial FrameWork

本项目分为几个大块:


1. QASU/ QAFetch 支持多市场数据存储/ 自动运维/ 数据获取(mongodb/ clickhouse)

2. QAUtil 支持交易时间, 交易日历, 时间向前向后推算, 市场识别, dataframe 数据转换等

3. QIFI/ QAMarket 一套统一的多市场 多语言账户体系
    - qifiaccount qifi 的标准账户体系,  在多语言上和 rust/cpp 版本的 qifi account 保持一致性
    - qifimanager  qifi 多账户管理体系 支持多个语言的账户统一管理
    - qaposition  单标的仓位管理模块, 支持对于单标的的精准多空控制(套利场景/ cta 场景/ 股票场景)
    - marketpreset 市场预制基类, 方便查询期货/股票/虚拟货币 品种 tick/ 保证金/ 手续费等

4. QAFactor 因子研究套件
    - 单因子研究入库
    - 因子管理, 测试
    - 因子合并

    - [ ] 优化器

5. QAData 多标的多市场的数据结构, 可以作为实时计算和回测的内存数据库使用

6. QAIndicator 支持自定义指标编写, 批量全市场 apply, 支持因子表达式构建

7. QAEngine 自定义线程进程基类, 可以自行修改计算的异步和局域网内分布式计算 agent

8. QAPubSub 基于 MQ 的消息队列, 支持 1-1 1-n n-n 的消息分发, 可用于计算任务分发收集, 实时订单流等场景

9. QAStrategy cta/套利回测套件, 支持 QIFI 模式

10. QAWebServer tornadobase 的 webserver 套件, 可以作为中台微服务构建

11. QASchedule 基于 QAWerbServer 的后台任务调度 支持自动运维, 远程任务调度等



本版本为不兼容升级的 2.0 quantaxis, 涉及一些改变

## 数据部分

- 增加 clickhouse client  自建数据源分发

- 增加数据格式 
    - 对于 tabular data 的支持
    - 支持因子化的数据结构

- 支持 tick/l2 order/transaction 的数据格式

## 微服务部分

- 增加 QAWEBSEBVER

- 支持动态的任务指派的 sechedule

- 增加 基于 DAG模型的pipeline

- 增加 QAPUBSUB模块 支持 rabbitmq

## 账户部分

- 删除 QAARP 不再维护老版本 account 系统

- 升级完整的 qifi 模块 支持多市场/跨市场的账户模型
    - 支持保证金模型
    - 支持股票
    - 支持期货

    - 期权[升级中]


## 实盘模拟盘部分

- 使用稳定的 qifi 结构对接

-  支持 CTP 接口的
    - 期货
    - 期权
-  支持股票部分
    - QMT 对接

- 母子账户的订单分发跟踪 [OMS]

- ordergateway 风控订单流规则

## 多语言部分

- 支持于 QUANTAXIS Rust 版本的通信
- 基于 arrow 库, 使用多语言支持的 pyarrow 格式, 对接 arrow-rs, datafusion-rs, libarrow(CPP)

- 支持 RUST/ CPP 账户
- 支持因子化的 rust job worker

## 社区/项目捐赠



### github

QUANTAXIS 是一个开放的项目, 在开源的3年中有大量的小伙伴加入了我, 并提交了相关的代码, 感谢以下的同学们

<a href="https://github.com/QUANTAXIS/QUANTAXIS/graphs/contributors"><img src="https://opencollective.com/QUANTAXIS/contributors.svg?width=890&button=false" /></a>



许多问题 可以在 [GITHUB ISSUE](https://github.com/QUANTAXIS/QUANTAXIS/issues)中找到, 你可以提出新的issue


### 捐赠

写代码不易...请作者喝杯咖啡呗?


![](http://picx.gulizhu.com/alipay.png)

(PS: 支付的时候 请带上你的名字/昵称呀 会维护一个赞助列表~ )


### QQ群

欢迎加群讨论: 563280067 [群链接](https://jq.qq.com/?_wv=1027&k=4CEKGzn) 

DISCORD 社区  https://discord.gg/mkk5RgN


QUANTAXIS 开发群: 773602202 (如果想要贡献代码 请加这个群 需要备注你的GITHUB ID)

QUANTAXIS 期货实盘多账户的本地部署群 (请勿浪费群资源 没有本地多账户部署的请勿加): 945822690

### 公共号

欢迎关注公众号: ![公众号](http://picx.gulizhu.com/Fr0pHbwB7-zrq_HAKsvB8g2zaP_A)

QAPRO公共号免费提供了下单推送接口, 关注公共号回复trade即可使用

### 论坛 QACLUB

QUANTAXIS 内测版论坛 [QUANTAXISCLUB上线](http://www.yutiansut.com:3000)

http://www.yutiansut.com:3000

凡通过论坛进行提问的 均有最高的回复优先级
