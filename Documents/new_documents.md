# QUANTAXIS 重构文档


|       | Content   |
|-------|-----------|
| DATE  | 2017-12-25|
|Author  |yutiansut|



## 重构目标

重构账户类、市场类、订单类 用于支持

- 多账户回测管理
- 组合管理、风险控制
- 期货回测
- 卖空规则
- 优化状态恢复
- 模拟盘
- 实盘对接


## ACCOUNT重构

1. 账户的修改部分：

修改了account的创建方式和组合方式
```
{USER}-{PORTFOLIO}-{ACCOUNT}-{ORDER}-{MARKET}
```