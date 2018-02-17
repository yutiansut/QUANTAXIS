# QUANTAXIS 对于本地数据的获取

<!-- vscode-markdown-toc -->
* 1. [一般封装 QA_fetch_类](#QA_fetch_)
	* 1.1. [股票日线 | STOCK_CN/DAY](#STOCK_CNDAY)
	* 1.2. [股票分钟线 | STOCK_CN/MIN](#STOCK_CNMIN)
* 2. [高级封装 *_adv类](#_adv)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

QUANTAXIS虽然对于从web获取做了许多的封装,但核心归根到底,quantaxis在获取数据的时候,主要还是要获取本地的数据(从稳定性和速度考虑).

QUANTAXIS对于本地数据的获取有两种级别的封装:

- [ ] 一般封装,返回各种各样的格式
- [ ] 高级封装,返回QUANTAXIS自定义格式(QADataStruct)

(自定义格式可以和别的格式相互转换)


##  1. <a name='QA_fetch_'></a>一般封装 QA_fetch_类


###  1.1. <a name='STOCK_CNDAY'></a>股票日线 | STOCK_CN/DAY
```python
QA.QA_fetch_stock_day(code, start, end, format='numpy', frequence='day', collection=DATABASE.stock_day)
```

- code 输入的股票 类型[str 6位代码]
- start 开始时间 [yyyy-mm-dd]
- end 结束时间 [yyyy-mm-dd]


- format 可以选择的输出格式[numpy/pandas/list/json/dict] 默认参数='numpy'
- frequence 周期(day) 默认参数'day'

- collection 指的是数据库连接 默认是本地[127.0.0.1:27017]的quantaxis数据库,可以使用pymongo.MongoClient(ip,port)来修改数据源

```python
QA.QA_fetch_stocklist_day(stock_list, date_range, collection=DATABASE.stock_day)
```

- stock_list 股票列表, list类型
- date_range 起止时间, list格式,可以理解为 [start,end]格式

- collection 指的是数据库连接 默认是本地[127.0.0.1:27017]的quantaxis数据库,可以使用pymongo.MongoClient(ip,port)来修改数据源

返回格式是list格式[dataframe1,dataframe2,...,dataframen],可以用pd.Concat(data,axis=0)

###  1.2. <a name='STOCK_CNMIN'></a>股票分钟线 | STOCK_CN/MIN
```python
QA.QA_fetch_stock_min(code, start, end, format='numpy', frequence='1min', collections=DATABASE.stock_min)
```


```python
QA.QA_fetch_stocklist_min(stock_list, date_range, frequence='1min', collections=DATABASE.stock_min)
```
##  2. <a name='_adv'></a>高级封装 *_adv类


