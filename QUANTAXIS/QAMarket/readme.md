# QA-Market

QAMarket 主要是做成一个市场撮合机制包,你可以理解为本地的交易所(合并2个股票交易所和4个期货交易所),你的所有模拟订单会发到这个包底下,然后经过这个包的判断,返回给你是否能完成交易.

## 简介
QAMarket 是为了降低代码的耦合性而拆分出来的模块.在以前的quantaxis中,他被放置于backend/服务器代码中,使用nodejs实现,随着0.3.8-dev-fetch的重构,我们逐渐将后端的REST使用python来重构,也将market部分拆开重构了

## QAMarket API

```python
from QAMarket import deal
```
