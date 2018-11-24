QUANTAXIS-Protocol
标准化协议QAS/未来协议QAF
------------

- 当前版本:0.1.0
- 协议最后修改日期:2018-04-21
- 项目版本:QUANTAXIS 1.0.22

<!-- vscode-markdown-toc -->
* 1. [QAS-A 综述](#QAS-A)
* 2. [QAS-B 模块](#QAS-B)
	* 2.1. [QAFetch 数据获取模块](#QAFetch)
	* 2.2. [QASU 数据存储和更新模块](#QASU)
	* 2.3. [QAEngine 线程引擎/事件模块](#QAEngine)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. QAS-A 综述

ABOUT | 关于QUANTAXIS

QUANTAXIS致力于提供一个高自由度的渐进式的量化解决方案. 


以下是对于QUANTAXIS几个基本模块的介绍:

``` 基本模块 ```

QAFetch 数据获取模块

QASU 数据存储和更新模块

QAEngine 线程引擎/事件模块

``` 处理模块 ```

QAData 数据处理模块

QAMARKET 交易/回测底层模块

``` 应用模块 ```

QAARP 账户/风险/业绩评价模块

QABacktest 回测模块

QAAnalysis 分析模块

QAIndicator 指标模块

``` 辅助及其他模块 ```

QAUtil 辅助模块

QACmd 命令行交互模块

QAWeb web后台模块


##  2. QAS-B 模块

###  2.1. QAFetch 数据获取模块

| 类别 | 实时 | 从数据库中 | QADataStruct格式|
| --------------- | ------------------- | --------------- |  --------------- |
| 股票日线 | QA_fetch_get_stock_day | QA_fetch_stock_day | QA_fetch_stock_day_adv |
| 股票分钟线 | QA_fetch_get_stock_min | QA_fetch_stock_min | QA_fetch_stock_min_adv |
| 股票列表 | QA_fetch_get_stock_list | QA_fetch_stock_list | QA_fetch_stock_list_adv |
| 股票版块 | QA_fetch_get_stock_block | QA_fetch_stock_block | QA_fetch_stock_block_adv |
| 股票分笔 | QA_fetch_get_stock_transaction | | |
| 股票实时分笔 | QA_fetch_get_stock_transaction_realtime | | |
| 股票权息 | QA_fetch_get_stock_xdxr | QA_fetch_stock_xdxr | |
| 股票信息 | QA_fetch_get_stock_info | QA_fetch_stock_info| |
| 股票实时5挡价格 | QA_fetch_get_stock_realtime | | |
| 指数日线 | QA_fetch_get_index_day | QA_fetch_index_day | QA_fetch_index_day_adv |
| 指数分钟线 | QA_fetch_get_index_min | QA_fetch_index_min | QA_fetch_index_day_min |
| ETF日线 | QA_fetch_get_etf_day | QA_fetch_etf_day | QA_fetch_etf_day_adv |
| ETF分钟线 | QA_fetch_get_etf_min | QA_fetch_etf_min | QA_fetch_etf_min_adv |
| 期货日线 | QA_fetch_get_future_day | | |
| 期货分钟线 | QA_fetch_get_future_min | | |
| 期货历史分笔 | QA_fetch_get_future_transaction | | |
| 期货实时分笔 | QA_fetch_get_future_transaction_realtime | | |
| 期货列表 | QA_fetch_get_future_list | | |

###  2.2. QASU 数据存储和更新模块

存储/更新模块在QASU, 按获取函数对应

存储更新的CLI指令在QACmd模块的```__init__.py```下

###  2.3. QAEngine 线程引擎/事件模块


### 2.4 QAData 数据处理模块

### 2.5 QAMARKET 交易/回测底层模块