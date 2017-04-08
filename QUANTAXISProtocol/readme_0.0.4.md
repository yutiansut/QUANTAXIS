QUANTAXIS-Protocol
标准化协议QAS/未来协议QAF
------

- 当前版本:0.0.4
- 协议最后修改日期:2017-04-08
- 项目版本:QUANTAXIS 0.3.8-dev-RC(ARP)

<!-- TOC -->

- [简介 Intro](#简介-intro)
    - [QUANTAXIS Standard Protocol  [QAS]](#quantaxis-standard-protocol--qas)
    - [QUANTAXIS Future Protocol  [QAF]](#quantaxis-future-protocol--qaf)
- [QAStandard-00x QUANTAXIS](#qastandard-00x-quantaxis)
    - [QAStandard-001 品牌](#qastandard-001-品牌)
    - [QAStandard-002 开源协议](#qastandard-002-开源协议)
- [QAStandard-10x 数据](#qastandard-10x-数据)
    - [QAStandard-101 行情数据](#qastandard-101-行情数据)
        - [QAS-101-1 Stock](#qas-101-1-stock)
        - [QAS-101-2 Future](#qas-101-2-future)
        - [QAS-101-3 Options](#qas-101-3-options)
        - [QAS-101-4 Indicator](#qas-101-4-indicator)
    - [QAStandard-102 文本信息数据](#qastandard-102-文本信息数据)
        - [QAS-102-1 舆情](#qas-102-1-舆情)
        - [QAS-102-2 财务](#qas-102-2-财务)
    - [QAStandard-103 爬虫](#qastandard-103-爬虫)
    - [QAStandard-104 自定义数据](#qastandard-104-自定义数据)
- [QAStandard-20x 市场](#qastandard-20x-市场)
    - [QAStandard-201 交易](#qastandard-201-交易)
        - [QAS-201-1 交易日](#qas-201-1-交易日)
        - [QAS-201-2 交易列表](#qas-201-2-交易列表)
        - [QAS-201-3 交易量](#qas-201-3-交易量)
    - [QAStandard-202 撮合机制](#qastandard-202-撮合机制)
- [QAStandard-30x 用户](#qastandard-30x-用户)
    - [QAStandard-301 账户状态](#qastandard-301-账户状态)
    - [QAStandard-302 账户策略](#qastandard-302-账户策略)
    - [QAStandard-303 账户自定义模块](#qastandard-303-账户自定义模块)
- [QAStandard-40x 状态](#qastandard-40x-状态)
    - [QAStandard-401 状态码](#qastandard-401-状态码)
- [QAStandard-50x API](#qastandard-50x-api)
    - [QAStandard-501 内部API](#qastandard-501-内部api)
        - [QAS_501_0 总规则](#qas_501_0-总规则)
        - [QAS-501-1 Fetch](#qas-501-1-fetch)
        - [QAS-501-2 Market](#qas-501-2-market)
        - [QAS-501-3 Account](#qas-501-3-account)
        - [QAS-501-4 Databases](#qas-501-4-databases)
    - [QAStandard-502 Http API/RESTFul](#qastandard-502-http-apirestful)
- [QAStandard-60x Util](#qastandard-60x-util)

<!-- /TOC -->
## 简介 Intro
QAProtocol是为了规范化和标准化QUANTAXIS的数据获取,数据存储,模拟市场交易,以及标准化输出而建立的协议.

QUANTAXIS是一个十分开放的框架，你可以自行引入自己的包括且不限于"历史数据","实时行情数据","多市场交易数据",
### QUANTAXIS Standard Protocol  [QAS]
QUANTAXISStandard是目前的协议标准,简称**QAS**
### QUANTAXIS Future Protocol  [QAF]
QUANTAXISFuture 是未来即将添加的或是在测试版中的功能标准,简称**QAF**
## QAStandard-00x QUANTAXIS
### QAStandard-001 品牌
QUANTAXIS的Logo需要遵循docs/logo标准下的logo,有两种形式的logo

<img width="150" height="150" src="http://i4.buimg.com/567571/62c510db7915837a.png"/>
<img width="150" height="150" src="http://i4.buimg.com/567571/2120bbe28a4a9a4b.png"/>

### QAStandard-002 开源协议
QUANTAXIS 基于MIT开源协议
```
The MIT License (MIT)

Copyright (c) 2016-2017 yutiansut/QUANTAXIS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

被授权人有权利使用、复制、修改、合并、出版发行、散布、再授权及贩售软体及软体的副本。

被授权人可根据程式的需要修改授权条款为适当的内容。

在软件和软件的所有副本中都必须包含版权声明和许可声明。

此授权条款并非属copyleft的自由软体授权条款，允许在自由/开放源码软体或非自由软体（proprietary software）所使用。

```
## QAStandard-10x 数据
QAS-10x需要遵循[QAS-501-4](#qas-501-4-databases)规范
### QAStandard-101 行情数据
#### QAS-101-1 Stock

- DataBase: quantaxis
- Collections: stock_day,stock_min
- BasicalName: code,name,date_stamp,open,high,low,close,volume 
- AdvanceName: 

**Basical**指的是存入数据库/更新数据时必须要有的字段

**Advance**指的是存入数据库/更新数据时定制的字段,非必须

#### QAS-101-2 Future

- DataBase: quantaxis
- Collections: future_day,future_min,future_ms
- BasicalName: code,name,open,high,low,close,volume
- AdvanceName: 

**Basical**指的是存入数据库/更新数据时必须要有的字段

**Advance**指的是存入数据库/更新数据时定制的字段,非必须

#### QAS-101-3 Options

- DataBase: quantaxis
- Collections: options_day,options_min,options_ms
- BasicalName: code,name,open,high,low,close,volume 
- AdvanceName: 

**Basical**指的是存入数据库/更新数据时必须要有的字段

**Advance**指的是存入数据库/更新数据时定制的字段,非必须

#### QAS-101-4 Indicator

- DataBase: quantaxis
- Collections: indicator_day,indicator_min,indicator_ms
- BasicalName:
- AdvanceName:

```
参考:

ADTM动态买卖气指标,ATR真实波幅,BBI多空指数,BBIBOLL多空布林线,BIAS乖离率,BOLL布林带,CCI顺势指标,CDP逆势操作,DMA平均线差,DMI趋向标准,DPO区间震荡线,ENV,EXPMA指数平滑移动平均,KDJ随机指标,slowKD慢速kd,MA简单移动平均,MACD指数平滑移动平均,MIKE麦克指数,MTM动力指标,PRICEOSC价格震荡指标,PVT量价趋势指标,RC变化率指数,ROC变动速率,RSI相对强弱指标,SAR抛物转向,SI摆动指标,SOBV能量潮,SRMI MI修正指标,STD 标准差,TAPI 加权指数成交值,TRIX 三重指数平滑平均,VHF纵横指标,VMA量简单移动平均,VMACD量指数平滑移动平均,VOSC成交量震荡,WVAD威廉变异离散量,vol_ratio量比
```
### QAStandard-102 文本信息数据
#### QAS-102-1 舆情

- DataBase: quantaxis
- Collections: news
- BasicalName: title,datetime,content,author,reference
- AdvanceName: comments,likeNum

#### QAS-102-2 财务

- DataBase: quantaxis
- Collections: finance_info,finance_balance,finance_profit,finance_cash


### QAStandard-103 爬虫
QAS103主要规范了爬虫的命名标准，UserAgent设置，cookie，session等规范。
### QAStandard-104 自定义数据
自定义数据需要按照分类标准引入数据库,如果是QAS101时间序列行情数据,QAS102文本信息数据,可以定制性的更新数据库(使用高级字段AdvanceName)


## QAStandard-20x 市场
### QAStandard-201 交易
#### QAS-201-1 交易日
分市场的交易日存储,属于行情序列,但是是分片数据[不遵循QAS101]
按时间序列存储当日交易的所有股票,期货名称


- DataBase: quantaxis
- Collections: trade_date
- BasicalName: date,date_stamp,exchangeName


#### QAS-201-2 交易列表
- DataBase: quantaxis
- Collections: stock_list
- BasicalName: date,date_stamp,stock[code,name]

#### QAS-201-3 交易量
交易量从[QAS-101](#qastandard-101-行情数据)的数据格式规范中获取,此处的规范主要针对撮合机制,当策略的请求交易量大于当日真实成交量的1/8,则判断无法成交.
### QAStandard-202 撮合机制
简单的行情判断机制是报价在[low,high]区间内 [#460 Commit](https://github.com/yutiansut/QUANTAXIS/commit/664d36bc350a43bf879e37c89741827bd9053ec1),同时bid_amount小于真实交易量的1/8
>QAF: 未来将加入更多的判断机制,z主要是粒度的问题

## QAStandard-30x 用户
### QAStandard-301 账户状态

### QAStandard-302 账户策略
### QAStandard-303 账户自定义模块
## QAStandard-40x 状态
### QAStandard-401 状态码

## QAStandard-50x API
### QAStandard-501 内部API
#### QAS_501_0 总规则
QA_(n.)_(verb)
n. 名词,一般是小类的名字
verb 动词，一般是这个小类的动作

```
QA_Spider_start
QA_Strategy_import
QA_util_log_info
```

#### QAS-501-1 Fetch
QAS501-1主要规定了数据获取的打包规范,遵循此规范,可以进行API二次打包

```python
QA_fetch_get_stock_day
QA_fetch_get_stock_min
QA_fetch_get_stock_tick
QA_fetch_get_stock_info
QA_fetch_get_stock_indicator
QA_fetch_get_future_day
QA_fetch_et_future_min
QA_fetch_get_future_tick
QA_fetch_get_future_info
QA_fetch_get_options_day
QA_fetch_get_options_min
QA_fetch_get_options_tick
QA_fetch_get_options_info




```

#### QAS-501-2 Market
QAS-501-2 主要规定了市场交易的调用接口规范，包括数据返回和响应状态码[遵循QAS-401](#qastandard-401-状态码)


#### QAS-501-3 Account

#### QAS-501-4 Databases
QAS-501-4 主要规定了数据库存储和调用时的命名规范,采用驼峰法则去定义
常见的Name定义
- code
- name
- open(double)
- high(double)
- low(double)
- close(double)
- volume(double)


### QAStandard-502 Http API/RESTFul

## QAStandard-60x Util