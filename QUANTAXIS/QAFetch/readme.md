# QUANTAXIS-Fetch
数据获取部分
QAFetch 参考了[quotation](https://github.com/Cuizi7/quotation)的思想,主要是将各种数据获取的途径标准化

QAFetch 同时也参考了[easyquotation](https://github.com/shidenggui/easyquotation)的'use'思想,通过use来引入模块包

QAFetch 遵循[QAStandard-10x]协议标准,如果需要自定义高级数据,需要遵循[QAS-104]

## 数据获取路径
### 免费的数据获取路径
- tushare
- gmsdk
- wind (大奖章)
- spider 爬虫
- wind 财经学子版

### 付费的数据获取路径

- wind (机构版)

### 自定义的数据导入

- 自定义的导入格式（尤其是各个策略团队的tick和ms级别的数据）
[QAS-104]

## 数据导入标准

### Stock 行情数据
[QAStandard-101-1] 行情数据格式-股票

- DataBase: quantaxis
- Collections: stock_day,stock_min
- collname: 

examples
```python
import pymongo
coll= pymongo.MongoClient(localhost,27017).quantaxis.stock_day
coll.find({}) # 查询数据
coll.find_one({}) # 查询一条
coll.insert({}) # 插入数据
coll.update({}) # 更新数据
```

### Future 行情数据
[QAStandard-101-2] 行情数据格式-期货

- DataBase: quantaxis
- Collections: future_day,future_min,future_ms
- collname: 

examples
```python
import pymongo
coll= pymongo.MongoClient(localhost,27017).quantaxis.future_day
coll.find({}) # 查询数据
coll.find_one({}) # 查询一条
coll.insert({}) # 插入数据
coll.update({}) # 
```
### Options 行情数据
[QAStandard-101-3] 行情数据格式-期权

- DataBase: quantaxis
- Collections: options_day,options_min,options_ms
- collname: 

examples
```python
import pymongo
coll= pymongo.MongoClient(localhost,27017).quantaxis.options_day
coll.find({}) # 查询数据
coll.find_one({}) # 查询一条
coll.insert({}) # 插入数据
coll.update({}) # 
```
### 舆情信息
[QAStandard-102-1] 文本信息格式-舆情
### 财务指标数据
[QAStandard-102-2] 文本信息格式-财务

### 指标数据
[QAStandard-101-4] 行情数据格式-指标
## 数据库

### MongoDB

### 其他
- MySQL
- PostgreSQL
- MSSQL SERVER