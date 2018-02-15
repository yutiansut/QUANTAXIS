# QUANTAXIS的数据获取部分

<!-- vscode-markdown-toc -->
* 1. [从网上获取 | FROM WEBSITE](#FROMWEBSITE)
	* 1.1. [股票/日线 | STOCK_CN/DAY](#STOCK_CNDAY)
	* 1.2. [股票/分钟线 | STOCK_CN/MIN](#STOCK_CNMIN)
	* 1.3. [股票/权息数据 | STOCK_CN/XDXR](#STOCK_CNXDXR)
	* 1.4. [股票/列表 | STOCK_CN/LIST](#STOCK_CNLIST)
	* 1.5. [指数/列表 | IDNEX_CN/LIST](#IDNEX_CNLIST)
	* 1.6. [指数/日线 | INDEX_CN/DAY](#INDEX_CNDAY)
	* 1.7. [指数/分钟线 | INDEX_CN/MIN](#INDEX_CNMIN)
	* 1.8. [最新交易价格STOCK | LAST PRICE](#STOCKLASTPRICE)
	* 1.9. [实时上下五档 STOCK_CN/QUOTATION](#STOCK_CNQUOTATION)
	* 1.10. [分笔数据 | STOCK_CN/TRANSACTION](#STOCK_CNTRANSACTION)
	* 1.11. [版块数据 | STOCK_CN/BLOCK](#STOCK_CNBLOCK)
* 2. [从数据库获取 | FROM LOCALHOST](#FROMLOCALHOST)
	* 2.1. [股票日线 | STOCK_CN/DAY](#STOCK_CNDAY-1)
	* 2.2. [股票分钟线 | STOCK_CN/MIN](#STOCK_CNMIN-1)
	* 2.3. [指数/基金日线 | INDEX_CN,ETF_CN/DAY](#INDEX_CNETF_CNDAY)
	* 2.4. [指数/基金分钟线 | INDEX_CN,ETF_CN/MIN](#INDEX_CNETF_CNMIN)
	* 2.5. [板块 | STOCK_CN/ BLOCK](#STOCK_CNBLOCK-1)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

具体可以参见[jupyter notebook](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/jupyterexample/QAFetch.ipynb)


##  1. <a name='FROMWEBSITE'></a>从网上获取 | FROM WEBSITE
"""
QA.QA_fetch_get_  系列:
从网上获取数据
"""

###  1.1. <a name='STOCK_CNDAY'></a>股票/日线 | STOCK_CN/DAY
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


###  1.2. <a name='STOCK_CNMIN'></a>股票/分钟线 | STOCK_CN/MIN

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



###  1.3. <a name='STOCK_CNXDXR'></a>股票/权息数据 | STOCK_CN/XDXR

QA.QA_util_log_info('除权除息')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_xdxr('00001')



###  1.4. <a name='STOCK_CNLIST'></a>股票/列表 | STOCK_CN/LIST

QA.QA_util_log_info('股票列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('stock')


###  1.5. <a name='IDNEX_CNLIST'></a>指数/列表 | IDNEX_CN/LIST

QA.QA_util_log_info('指数列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('index')

###  1.6. <a name='INDEX_CNDAY'></a>指数/日线 | INDEX_CN/DAY

QA.QA_util_log_info('指数日线')
data=QA.QAFetch.QATdx.QA_fetch_get_index_day('000001','2017-01-01','2017-09-01')

###  1.7. <a name='INDEX_CNMIN'></a>指数/分钟线 | INDEX_CN/MIN

QA.QA_util_log_info('指数分钟线')
QA.QA_util_log_info('1min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','1min')


QA.QA_util_log_info('5min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','5min')


QA.QA_util_log_info('15min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','15min')


###  1.8. <a name='STOCKLASTPRICE'></a>最新交易价格STOCK | LAST PRICE
QA.QA_util_log_info('最后一次交易价格')
QA.QA_util_log_info('参数为列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest(['000001','000002'])


QA.QA_util_log_info('参数为一只股票')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest('000001')


###  1.9. <a name='STOCK_CNQUOTATION'></a>实时上下五档 STOCK_CN/QUOTATION
QA.QA_util_log_info('实时价格')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_realtime(['000001','000002'])

###  1.10. <a name='STOCK_CNTRANSACTION'></a>分笔数据 | STOCK_CN/TRANSACTION
QA.QA_util_log_info('分笔成交')

历史分笔
data=QA.QAFetch.QATdx.QA_fetch_get_stock_transaction('000001','2001-01-01','2001-01-15')
实时分笔(当天)
data=QA.QAFetch.QATdx.QA_fetch_get_stock_transaction_realtime('000001')

###  1.11. <a name='STOCK_CNBLOCK'></a>版块数据 | STOCK_CN/BLOCK
QA.QA_util_log_info('板块数据')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_block()


"""
QA.QA_fetch_ 系列 
从本地数据库获取数据
"""

##  2. <a name='FROMLOCALHOST'></a>从数据库获取 | FROM LOCALHOST

###  2.1. <a name='STOCK_CNDAY-1'></a>股票日线 | STOCK_CN/DAY
QA_fetch_stock_day_adv(code,start,end)
###  2.2. <a name='STOCK_CNMIN-1'></a>股票分钟线 | STOCK_CN/MIN
QA_fetch_stock_min_adv(code,start,end,frequence='1min') # frequence可以选1min/5min/15min/30min/60min 
###  2.3. <a name='INDEX_CNETF_CNDAY'></a>指数/基金日线 | INDEX_CN,ETF_CN/DAY
QA_fetch_index_day_adv(code,start,end)
###  2.4. <a name='INDEX_CNETF_CNMIN'></a>指数/基金分钟线 | INDEX_CN,ETF_CN/MIN
QA_fetch_index_min_adv(code,start,end,frequence='1min') # frequence可以选1min/5min/15min/30min/60min 
###  2.5. <a name='STOCK_CNBLOCK-1'></a>板块 | STOCK_CN/ BLOCK
QA_fetch_stock_block_adv(code)

