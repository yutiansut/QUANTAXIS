# QUANTAXIS的数据获取部分

<!-- TOC -->

- [QUANTAXIS的数据获取部分](#quantaxis的数据获取部分)
    - [1. 从网上获取 | FROM WEBSITE](#1-从网上获取--from-website)
        - [1.1. 股票/日线 | STOCK_CN/DAY](#11-股票日线--stock_cnday)
        - [1.2. 股票/分钟线 | STOCK_CN/MIN](#12-股票分钟线--stock_cnmin)
        - [1.3. 股票/权息数据 | STOCK_CN/XDXR](#13-股票权息数据--stock_cnxdxr)
        - [1.4. 股票/列表 | STOCK_CN/LIST](#14-股票列表--stock_cnlist)
        - [1.5. 指数/列表 | IDNEX_CN/LIST](#15-指数列表--idnex_cnlist)
        - [1.6. 指数/日线 | INDEX_CN/DAY](#16-指数日线--index_cnday)
        - [1.7. 指数/分钟线 | INDEX_CN/MIN](#17-指数分钟线--index_cnmin)
        - [1.8. 期货/日线 | FUTURE DAY](#18-期货日线--future-day)
        - [1.9. 期货分钟线 | Future_Min](#113-期货分钟线--future_min)
        - [1.10. 期货tick线 | Future_Transaction](#110-期货分钟线--future_tick)
        - [1.11. 最新交易价格STOCK | LAST PRICE](#111-最新交易价格stock--last-price)
        - [1.12. 实时上下五档 STOCK_CN/QUOTATION](#112-实时上下五档-stock_cnquotation)
        - [1.13. 分笔数据 | STOCK_CN/TRANSACTION](#113-分笔数据--stock_cntransaction)
        - [1.14. 版块数据 | STOCK_CN/BLOCK](#114-版块数据--stock_cnblock)
        - [1.15  债券列表 | BOND_CN/LIST)
        - [1.16  债券日线 | BOND_CN/DAY]
        - [1.17  债券分钟线 | BOND_CN/MIN]
        - [1.18  港股列表  |
        - [1.19  港股日线
        - [1.20  港股分钟线
        - [1.21  港股指数
        - [1.22  港股指数日线
        - [1.23  港股指数分钟线
        - [1.24  港股基金
        - [1.25  港股基金日线
        - [1.26  港股基金分钟线
        - [1.27  美股列表
        - [1.28  美股日线
        - [1.29  美股分钟线
        - [1.30  汇率列表
        - [1.31  汇率日线
        - [1.32  汇率分钟线
        - [1.33  国际期货
        - [1.34  国际期货日线
        - [1.35  国际期货分钟线
        - [1.36  宏观指数
        - [1.37  宏观指数日线
        - [1.38  宏观指数分钟线
        
        
        
        
    - [2. 从数据库获取 | FROM LOCALHOST](#2-从数据库获取--from-localhost)
        - [2.1. 股票日线 | STOCK_CN/DAY](#21-股票日线--stock_cnday)
        - [2.2. 股票分钟线 | STOCK_CN/MIN](#22-股票分钟线--stock_cnmin)
        - [2.3. 指数/基金日线 | INDEX_CN,ETF_CN/DAY](#23-指数基金日线--index_cnetf_cnday)
        - [2.4. 指数/基金分钟线 | INDEX_CN,ETF_CN/MIN](#24-指数基金分钟线--index_cnetf_cnmin)
        - [2.5. 板块 | STOCK_CN/ BLOCK](#25-板块--stock_cn-block)

<!-- /TOC -->

具体可以参见[jupyter notebook](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/EXAMPLE/1_%E6%95%B0%E6%8D%AE%E8%8E%B7%E5%8F%96/QAFetch.ipynb)


##  1. 从网上获取 | FROM WEBSITE

QA.QA_fetch_get_  系列:

从网上获取数据

###  1.1. 股票/日线 | STOCK_CN/DAY
```python
QA.QA_util_log_info('日线数据')
QA.QA_util_log_info('不复权')  
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31')

QA.QA_util_log_info('前复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','01')

QA.QA_util_log_info('后复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','02')

QA.QA_util_log_info('定点前复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','03')


QA.QA_util_log_info('定点后复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','04')
```

###  1.2. 股票/分钟线 | STOCK_CN/MIN
```python
QA.QA_util_log_info('分钟线')
QA.QA_util_log_info('1min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','1min')

QA.QA_util_log_info('5min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','5min')

QA.QA_util_log_info('15min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','15min')

QA.QA_util_log_info('30min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','30min')

QA.QA_util_log_info('60min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','60min')
```


###  1.3. 股票/权息数据 | STOCK_CN/XDXR
```python
QA.QA_util_log_info('除权除息')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_xdxr('00001')
```


###  1.4. 股票/列表 | STOCK_CN/LIST
```python
QA.QA_util_log_info('股票列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('stock')
```

###  1.5. 指数/列表 | IDNEX_CN/LIST
```python
QA.QA_util_log_info('指数列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('index')
```
###  1.6. 指数/日线 | INDEX_CN/DAY
```python
QA.QA_util_log_info('指数日线')
data=QA.QAFetch.QATdx.QA_fetch_get_index_day('000001','2017-01-01','2017-09-01')
```
###  1.7. 指数/分钟线 | INDEX_CN/MIN
```python
QA.QA_util_log_info('指数分钟线')
QA.QA_util_log_info('1min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','1min')


QA.QA_util_log_info('5min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','5min')


QA.QA_util_log_info('15min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','15min')
```


###  1.8. 期货/日线 | FUTURE DAY

```python

QA.QA_util_log_info('期货日线')

QA.QAFetch.QATdx.QA_fetch_get_future_day('RBL8','2018-08-01','2018-08-30')

```

###  1.9. 期货/分钟线 | FUTURE MIN

```python

QA.QA_util_log_info('期货分钟线')

QA.QAFetch.QATdx.QA_fetch_get_future_min('RB1905','2019-01-01','2019-01-30', '5min')

```
###  1.10. 期货/tick | FUTURE Transaction

```python

QA.QA_util_log_info('期货分钟线')

QA.QAFetch.QATdx.QA_fetch_get_future_transaction('RB1905','2019-01-01','2019-01-30')

```




###  1.11. 最新交易价格STOCK | LAST PRICE
```python
QA.QA_util_log_info('最后一次交易价格')
QA.QA_util_log_info('参数为列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest(['000001','000002'])


QA.QA_util_log_info('参数为一只股票')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest('000001')
```

###  1.12. 实时上下五档 STOCK_CN/QUOTATION
```python
QA.QA_util_log_info('实时价格')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_realtime(['000001','000002'])
```

###  1.13. 分笔数据 | STOCK_CN/TRANSACTION
```python
QA.QA_util_log_info('分笔成交')

历史分笔
data=QA.QAFetch.QATdx.QA_fetch_get_stock_transaction('000001','2001-01-01','2001-01-15')
实时分笔(当天)
data=QA.QAFetch.QATdx.QA_fetch_get_stock_transaction_realtime('000001')
```

###  1.14. 版块数据 | STOCK_CN/BLOCK
```python
QA.QA_util_log_info('板块数据')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_block()
```



##  2. 从数据库获取 | FROM LOCALHOST

QA.QA_fetch_ 系列 

从本地数据库获取数据

###  2.1. 股票日线 | STOCK_CN/DAY
```python
QA_fetch_stock_day_adv(code,start,end)
```
###  2.2. 股票分钟线 | STOCK_CN/MIN
```python
QA_fetch_stock_min_adv(code,start,end,frequence='1min') # frequence可以选1min/5min/15min/30min/60min 
```
###  2.3. 指数/基金日线 | INDEX_CN,ETF_CN/DAY
```python
QA_fetch_index_day_adv(code,start,end)
```
###  2.4. 指数/基金分钟线 | INDEX_CN,ETF_CN/MIN
```python
QA_fetch_index_min_adv(code,start,end,frequence='1min') # frequence可以选1min/5min/15min/30min/60min 
```
###  2.5. 板块 | STOCK_CN/ BLOCK
```python
QA_fetch_stock_block_adv(code)
```

