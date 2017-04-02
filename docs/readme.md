QUANTAXIS-Protocol
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
    - [QAStandard-102 文本信息数据](#qastandard-102-文本信息数据)
    - [QAStandard-103 爬虫](#qastandard-103-爬虫)
    - [QAStandard-104 自定义数据](#qastandard-104-自定义数据)
- [QAStandard-20x 市场](#qastandard-20x-市场)
    - [QAStandard-201 交易](#qastandard-201-交易)
    - [QAStandard-202](#qastandard-202)
- [QAStandard-30x 用户](#qastandard-30x-用户)
    - [QAStandard-301 账户状态](#qastandard-301-账户状态)
    - [QAStandard-302 账户策略](#qastandard-302-账户策略)
    - [QAStandard-303 账户自定义模块](#qastandard-303-账户自定义模块)
- [QAStandard-40x 状态](#qastandard-40x-状态)
    - [QAStandard-401 状态码](#qastandard-401-状态码)

<!-- /TOC -->
## 简介
QAProtocol是为了规范化和标准化QUANTAXIS的数据获取,数据存储,模拟市场交易,以及标准化输出而建立的协议.
### a. QUANTAXISStandard
QUANTAXISStandard是目前的协议标准
### b. QUANTAXISFuture
QUANTAXISFuture 是未来即将添加的或是在测试版中的功能标准
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
- BasicalName: VarietyName,DateTime,Open,High,Low,Close 
- AdvanceName: 

**Basical**指的是存入数据库/更新数据时必须要有的字段

**Advance**指的是存入数据库/更新数据时定制的字段,非必须

#### QAS-101-2 Future
- Client: QUANTAXIS
- DataBase: Future
- Collections: day,min,ms
#### QAS-101-3 Options
- Client: QUANTAXIS
- DataBase: Options
- Collections: day,min,ms
### QAStandard-102 文本信息数据
### QAStandard-103 爬虫
### QAStandard-104 自定义数据
## QAStandard-20x 市场
### QAStandard-201 交易

### QAStandard-202 
## QAStandard-30x 用户
### QAStandard-301 账户状态
### QAStandard-302 账户策略
### QAStandard-303 账户自定义模块
## QAStandard-40x 状态
### QAStandard-401 状态码

