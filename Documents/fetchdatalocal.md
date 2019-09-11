# QUANTAXIS 对于本地数据的获取

<!-- TOC -->

- [QUANTAXIS 对于本地数据的获取](#quantaxis-对于本地数据的获取)
    - [1. 一般封装 QA_fetch_类](#1-一般封装-qa_fetch_类)
        - [1.1. 股票日线 | STOCK_CN/DAY](#11-股票日线--stock_cnday)
        - [1.2.股票分钟线 | STOCK_CN/MIN](#12股票分钟线--stock_cnmin)
    - [2. 高级封装 *adv](#2-高级封装-adv)
        - [2.1. 股票日线 | STOCK_CN/DAY](#21-股票日线--stock_cnday)
        - [](#)

<!-- /TOC -->

QUANTAXIS虽然对于从web获取做了许多的封装,但核心归根到底,quantaxis在获取数据的时候,主要还是要获取本地的数据(从稳定性和速度考虑).

QUANTAXIS对于本地数据的获取有两种级别的封装:

- [ ] 一般封装,返回各种各样的格式
- [ ] 高级封装,返回QUANTAXIS自定义格式(QADataStruct)

(自定义格式可以和别的格式相互转换)


##  1. 一般封装 QA_fetch_类


###  1.1. 股票日线 | STOCK_CN/DAY
```python
QA.QA_fetch_stock_day(code, start, end, format='numpy', frequence='day', collection=DATABASE.stock_day)
```

- code 输入的股票 类型[str 6位代码]/list
- start 开始时间 [yyyy-mm-dd]
- end 结束时间 [yyyy-mm-dd]


- format 可以选择的输出格式[numpy/pandas/list/json/dict] 默认参数='numpy'
- frequence 周期(day) 默认参数'day'

- collection 指的是数据库连接 默认是本地[127.0.0.1:27017]的quantaxis数据库,可以使用pymongo.MongoClient(ip,port)来修改数据源


- stock_list 股票列表, list类型
- date_range 起止时间, list格式,可以理解为 [start,end]格式

- collection 指的是数据库连接 默认是本地[127.0.0.1:27017]的quantaxis数据库,可以使用pymongo.MongoClient(ip,port)来修改数据源

返回格式是list格式[dataframe1,dataframe2,...,dataframen],可以用pd.Concat(data,axis=0)

###  1.2.股票分钟线 | STOCK_CN/MIN
```python
QA.QA_fetch_stock_min(code, start, end, format='numpy', frequence='1min', collections=DATABASE.stock_min)
```



##  2. 高级封装 *adv

###  2.1. 股票日线 | STOCK_CN/DAY

```python
QA.QA_fetch_stock_day_adv(code, start='all', end=None, if_drop_index=False, collections=DATABASE.stock_day)
```

- code 股票 可以是一只股票/一列股票
- start 开始日期 如果不给定或者参数是'all' 则为股票的所有交易日
- end 结束日期(yyyy-mm-dd) 如果不给定 则为和开始日期同一天, 如果开始日期为'all'参数,则为今天

- if_drop_index 默认false 强烈建议不要改
- collection 指的是数据库连接 默认是本地[127.0.0.1:27017]的quantaxis数据库,可以使用pymongo.MongoClient(ip,port)来修改数据源

返回 

type QA_DATASTRUCT_STOCK_DAY
具体用法参见[](DataStruct.md)


### 


```python
In [28]: QA.QA_fetch_stock_day_adv?
Signature: QA.QA_fetch_stock_day_adv(code, start='all', end=None, if_drop_index=False, collections=Collection(Database(MongoClient(host=['127.0.0.1:27017'], document_class=dict, tz_aware=False, connect=True), 'quantaxis'), 'stock_day'))


In [29]: QA.QA_fetch_stock_min_adv?
Signature: QA.QA_fetch_stock_min_adv(code, start, end=None, frequence='1min', if_drop_index=False, collections=Collection(Database(MongoClient(host=['127.0.0.1:27017'], document_class=dict, tz_aware=False, connect=True), 'quantaxis'), 'stock_min'))

```