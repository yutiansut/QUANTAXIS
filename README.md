# QUANTAXIS 2.0.0

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