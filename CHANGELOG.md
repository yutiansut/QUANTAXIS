# QUANTAXIS 更新纪要


## 1.0.25 

2018-04-27

1.0.25 增加对于查询的优化:

1. 优化了查询时输入的参数

当code的列表如果是[000001,000002... ]等int形式时,会出现不支持的错误,1.0.25进行了优化

常见原因是如果code从csv中取出,csv会自动讲code变成整数的形式,如果在传参之前没有进行 ```code.apply(str).tolist()```的话,会出现此错误

2. 优化了查询的返回

在偶见的数据库数据重复时,会对数据自动去重并返回结果


## 1.0.26

2018-05-02

1.0.26 对于回测进行了一些优化

1. 增加了对于RISK类的参数

- 增加了```init_assets```, ```last_assets```参数,更方便查看

- 修改了计算年化收益率的公式

2. 修改了simple_backtest 函数的逻辑:

- simple_backtest 之前的 重设账户资金的写法错误, 已更正

- simple_backtest 现在会随机下单(增加随机函数)


3. 修改了```QADATASTRUCT```中日线结构的参数

增加了 ```next_day_high_limit``` 和 ```next_day_low_limit```参数,方便计算,明日涨跌停


## 1.0.27

2018-05-06

修改并增加了大量的公式,统一成dataframe格式返回,可以被直接concat合并出来

预计将对于indicator类进行重写并缓存/本地存储,方便快速调用

修改了QA_Account的下单模式, 修复了下单的判断bug



## 1.0.28


ATTENTION CHANGELOG 1.0.28
修改了Account的send_order方法, 区分按数量下单和按金额下单两种方式

- AMOUNT_MODEL.BY_PRICE ==> AMOUNT_MODEL.BY_MONEY # 按金额下单
- AMOUNT_MODEL.BY_AMOUNT # 按数量下单

在按金额下单的时候,应给予 money参数
在按数量下单的时候,应给予 amount参数


```python
Account=QA.QA_Account()

Order_bymoney=Account.send_order(code='000001',
                                price=11,
                                money=0.3*Account.cash_available,
                                time='2018-05-09',
                                towards=QA.ORDER_DIRECTION.BUY,
                                order_model=QA.ORDER_MODEL.MARKET,
                                amount_model=QA.AMOUNT_MODEL.BY_MONEY
                                 )

Order_byamount=Account.send_order(code='000001',
                                price=11,
                                amount=100,
                                time='2018-05-09',
                                towards=QA.ORDER_DIRECTION.BUY,
                                order_model=QA.ORDER_MODEL.MARKET,
                                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                 )
```


## 1.0.29

1.0.29更新了关于数据查询的代码

1. 更新了前复权/后复权的计算,保证了即使在复权数据全无的时候,返回正确的复权结果
2. 更新了查询权息数据库的代码,现在支持多个股票同时查询
3. 加速了复权的效率

## 1.0.30

1.0.30更新了关于回测和数据查询的代码

1. 修改了查询股票info的代码, 支持多个股票同时查询
2. 修改了QA_Account下单时的```cash_available```结算bug