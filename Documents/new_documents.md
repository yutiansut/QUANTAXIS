# QUANTAXIS 重构文档


|       | Content   |
|-------|-----------|
| DATE  | 2017-12-25|
|Author  |yutiansut|

<!-- TOC -->

- [QUANTAXIS 重构文档](#quantaxis-重构文档)
    - [重构目标](#重构目标)
    - [ACCOUNT重构](#account重构)

<!-- /TOC -->

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

account 作为一个最小的账户单元,具有
1. 独立的下单属性*(此前在backtest中撮合)
2. 独立的账户更新规则
3. 可以被快速分配到portfolio上(基于account_cookie)


account 通过 account.message进行数据通信 
```
account.message记录了account的所有状态 用于

回测时和backtest通信
实盘时的message单元
组合管理和portfolio通信

快速存储-快速恢复account状态
```

2. account的属性

```
strategy_name=''  # 策略名称
user=''  # 用户
market_type=MARKET_TYPE.STOCK_CN  # market_type
hold=[['date', 'code', 'price', 'amount', 'order_id', 'trade_id']]  #list
sell_available=[['date', 'code', 'price', 'amount', 'order_id', 'trade_id']] #list
init_assest=1000000 #int
order_queue=pd.DataFrame() #pd.Dataframe
cash=[] #list
history=[] #history
detail #list
assets #list
account_cookie=None  # account_cookie
```