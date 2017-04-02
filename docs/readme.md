QUANTAXIS-Protocol
QUANTAXIS 标准化协议QAS/未来协议QAF
------

<!-- TOC -->

- [简介](#简介)
    - [a. QUANTAXISStandard](#a-quantaxisstandard)
    - [b. QUANTAXISFuture](#b-quantaxisfuture)
- [QAStandard-00x QUANTAXIS](#qastandard-00x-quantaxis)
    - [QUANTAXIS-001 品牌](#quantaxis-001-品牌)
    - [QUANTAXIS-002 开源协议](#quantaxis-002-开源协议)
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
        - [QAS-201-2 交易量](#qas-201-2-交易量)
    - [QAStandard-202 撮合机制](#qastandard-202-撮合机制)
- [QAStandard-30x 用户](#qastandard-30x-用户)
    - [QAStandard-301 账户状态](#qastandard-301-账户状态)
    - [QAStandard-302 账户策略](#qastandard-302-账户策略)
    - [QAStandard-303 账户自定义模块](#qastandard-303-账户自定义模块)
- [QAStandard-40x 状态](#qastandard-40x-状态)
    - [QAStandard-401 状态码](#qastandard-401-状态码)
- [QAStandard-50x API](#qastandard-50x-api)
    - [QAStandard-501 内部API](#qastandard-501-内部api)
        - [QAS-501-1 Fetch](#qas-501-1-fetch)
        - [QAS-501-2 Market](#qas-501-2-market)
        - [QAS-501-3 Account](#qas-501-3-account)
    - [QAStandard-502 Http API/RESTFul](#qastandard-502-http-apirestful)

<!-- /TOC -->
## 简介
QAProtocol是为了规范化和标准化QUANTAXIS的数据获取,数据存储,模拟市场交易,以及标准化输出而建立的协议.
### a. QUANTAXISStandard
QUANTAXISStandard是目前的协议标准,简称**QAS**
### b. QUANTAXISFuture
QUANTAXISFuture 是未来即将添加的或是在测试版中的功能标准,简称**QAF**
## QAStandard-00x QUANTAXIS
### QUANTAXIS-001 品牌
QUANTAXIS的Logo需要遵循docs/logo标准下的logo,有两种形式的logo

<img width="150" height="150" src="http://i4.buimg.com/567571/62c510db7915837a.png"/>
<img width="150" height="150" src="http://i4.buimg.com/567571/2120bbe28a4a9a4b.png"/>

### QUANTAXIS-002 开源协议
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
### QAStandard-101 行情数据
#### QAS-101-1 Stock
- Client: QUANTAXIS
- DataBase: Stock
- Collections: day,min
- BasicalName: VarietyName,DateTime,Open,High,Low,Close,Volume  
- AdvanceName: 

**Basical**指的是存入数据库/更新数据时必须要有的字段

**Advance**指的是存入数据库/更新数据时定制的字段,非必须

#### QAS-101-2 Future
- Client: QUANTAXIS
- DataBase: Future
- Collections: day,min,ms
- BasicalName: VarietyName,DateTime,Open,High,Low,Close,Volume 
- AdvanceName: 

**Basical**指的是存入数据库/更新数据时必须要有的字段

**Advance**指的是存入数据库/更新数据时定制的字段,非必须

#### QAS-101-3 Options
- Client: QUANTAXIS
- DataBase: Options
- Collections: day,min,ms
- BasicalName: VarietyName,DateTime,Open,High,Low,Close,Volume 
- AdvanceName: 

**Basical**指的是存入数据库/更新数据时必须要有的字段

**Advance**指的是存入数据库/更新数据时定制的字段,非必须

#### QAS-101-4 Indicator
- Client: QUANTAXIS
- DataBase: Indicator
- Collections: day,min,ms
- BasicalName:
- AdvanceName:

```
参考:

ADTM动态买卖气指标,ATR真实波幅,BBI多空指数,BBIBOLL多空布林线,BIAS乖离率,BOLL布林带,CCI顺势指标,CDP逆势操作,DMA平均线差,DMI趋向标准,DPO区间震荡线,ENV,EXPMA指数平滑移动平均,KDJ随机指标,slowKD慢速kd,MA简单移动平均,MACD指数平滑移动平均,MIKE麦克指数,MTM动力指标,PRICEOSC价格震荡指标,PVT量价趋势指标,RC变化率指数,ROC变动速率,RSI相对强弱指标,SAR抛物转向,SI摆动指标,SOBV能量潮,SRMI MI修正指标,STD 标准差,TAPI 加权指数成交值,TRIX 三重指数平滑平均,VHF纵横指标,VMA量简单移动平均,VMACD量指数平滑移动平均,VOSC成交量震荡,WVAD威廉变异离散量,vol_ratio量比
```
### QAStandard-102 文本信息数据
#### QAS-102-1 舆情
- Client: QUANTAXIS
- DataBase: Info
- Collections: news/opinion
- BasicalName: title,datetime,content,author,refence
- AdvanceName: comments,likenum

#### QAS-102-2 财务
- Client: QUANTAXIS
- DataBase: Financial
- Collections: info,balance,profit,cash


### QAStandard-103 爬虫

### QAStandard-104 自定义数据
自定义数据需要按照分类标准引入数据库,如果是QAS101时间序列行情数据,QAS102文本信息数据,可以定制性的更新数据库(使用高级字段AdvanceName)


## QAStandard-20x 市场
### QAStandard-201 交易
#### QAS-201-1 交易日
分市场的交易日存储,属于行情序列,但是是分片数据[不遵循QAS101]
按时间序列存储当日交易的所有股票,期货名称
#### QAS-201-2 交易量
交易量从[QAS-101](#qastandard-101-行情数据)的数据格式规范中获取,此处的规范主要针对撮合机制,当策略的请求交易量大于当日真实成交量的1/8,则判断无法成交.
### QAStandard-202 撮合机制
简单的行情判断机制是报价在[low,high]区间内,同时bid_amount小于真实交易量的1/8
>QAF: 未来将加入更多的判断机制,尤其是深度池

## QAStandard-30x 用户
### QAStandard-301 账户状态

### QAStandard-302 账户策略
### QAStandard-303 账户自定义模块
## QAStandard-40x 状态
### QAStandard-401 状态码

## QAStandard-50x API
### QAStandard-501 内部API
#### QAS-501-1 Fetch
QAS501-1主要规定了数据获取的打包规范,遵循此规范,可以进行API二次打包
```python
get_stock_day
get_stock_min
get_stock_tick
get_stock_info
get_stock_indicator
get_future_day
get_future_min
get_future_tick
get_future_info
get_future_day
get_options_min
get_options_tick
get_options_info


save_stock
save_future
save_options
save_all

```

#### QAS-501-2 Market
#### QAS-501-3 Account
### QAStandard-502 Http API/RESTFul