# 关于第三方数据的导入和使用



1. 关于数据的存储:


quantaxis对于数据的存储格式的要求较为松散, 满足几个核心的字段即可


### 1.3 future_min

- code 品种
- open 开
- high 高
- low  低
- close 收
- position  *(不一定需要)持仓量
- price     *(不一定需要)均价
- trade     交易量=Volume
- datetime   真实时间
- tradetime  交易时间
- time_stamp 时间戳
- date  日期
- type  频率
