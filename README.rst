QUANTAXIS quantitative financial strategy framework
==========================

QUANTAXIS quantitative framework to achieve the stock and futures market, the whole species back to the test.Through the distributed crawler for data capture, to build a response to the data cleaning and market push engine to build a multi-language open response frame. And build interactive visualization of clients and websites.


0.3.9-beta Release Note
---------------------------------


Taking into account such a scenario, an organization's strategy team is generally composed of CS + Finance, Finance students are very good at data analysis, strategy, but not very understanding of the underlying structure of the code, code style and standards are different While CS students are well aware of the code and framework, they are struggling with the financial theory of boring holes, and the current domestic support for quantitative services can not solve this common scene pain points, or for financial students Easy to operate the analysis system, but for IT in terms of the lack of customizable part; either for the underlying IT data and transaction interface, and for financial students want to package out from the underlying interface, a set of available efficient framework It is difficult to ascend to heaven.

QUNATAXIS is committed to solving this problem, and we solve this problem by creating a standard framework within a RESTful-based LAN that is separated from front and back, and we hope that our framework is highly scalable and easy to access The company's individual strategy team's individual needs (this is the most critical, basically every company will have its own data, their own trading interface, their own specific functional goals), so we want to build a standardized, high Scalable, easy to deploy scaffolding, rather than a complete hard to customize solution.

QUANTAXIS front and back completely separated, highly split, each component relies on RESTful standard URI to communicate, which also gives us an open framework of infinite possibilities, can achieve Matlab, r, python, javascript, C, C + +, rust And other users of the harmonious coexistence, rather than increase the cost of learning to learn a common language.At the same time, as long as a public network IP and server, you can also go beyond the LAN restrictions, to achieve the needs of remote teams.


=============

[QAS] QUANTAXIS standard protocol

## Introduction Intro
QAProtocol is a protocol established to standardize and standardize QUANTAXIS data acquisition, data storage, simulated market transactions, and standardized output.
### QUANTAXIS Standard Protocol [QAS]
QUANTAXISStandard is the current protocol standard, referred to as ** QAS **
### QUANTTAXIS Future Protocol [QAF]
QUANTAXISFuture is the future will be added or in the beta version of the functional standards, referred to as ** QAF **
## QAStandard-00x QUANTAXIS
### QAStandard-001 brand
QUANTAXIS Logo needs to follow the docs / logo logo under the logo, there are two forms of logo

<Img width = "150" height = "150" src = "http://i4.buimg.com/567571/62c510db7915837a.png" />
<Img width = "150" height = "150" src = "http://i4.buimg.com/567571/2120bbe28a4a9a4b.png" />

### QAStandard-002 open source protocol
QUANTAXIS is based on the MIT open source protocol
`` ``
The MIT License (MIT)

Copyright (c) 2016-2017 yutiansut / QUANTAXIS

Permission is hereby granted, free of charge, to any person obtaining a copy
Of this software and associated documentation files (the "Software"), to deal
In the Software without restriction, including without limitation the rights
To use, copy, modify, merge, publish, distribute, sublicense, and / or sell
Copies of the Software, and to permit persons to whom the Software is
Furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
Copies or gt copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The licensor has the right to use, copy, modify, merge, publish, distribute, sublicense and sell copies of the Software and the Software.

The authorized person may modify the terms of the license as appropriate for the purpose of the program.

You must include a copyright notice and a permission statement in all copies of the software and software.

This license clause is not a copy of the free software license clause, which is permitted for use in free / open source software or proprietary software.

`` ``
## QAStandard-10x data
QAS-10x is required to follow the [QAS-501-4] (# qas-501-4-databases) specification
### QAStandard-101 Quotes data
#### QAS-101-1 Stock

- DataBase: quantaxis
- Collections: stock_day, stock_min
- BasicalName: code, name, date_stamp, open, high, low, close, volume
- AdvanceName:

** Basical ** refers to the fields that must be stored when storing the database / update data

** Advance ** refers to the field that is customized when it is stored in the database / update data

#### QAS-101-2 Future

- DataBase: quantaxis
- Collections: future_day, future_min, future_ms
- BasicalName: code, name, open, high, low, close, volume
- AdvanceName:

** Basical ** refers to the fields that must be stored when storing the database / update data

** Advance ** refers to the field that is customized when it is stored in the database / update data

#### QAS-101-3 Options

- DataBase: quantaxis
- Collections: options_day, options_min, options_ms
- BasicalName: code, name, open, high, low, close, volume
- AdvanceName:

** Basical ** refers to the fields that must be stored when storing the database / update data

** Advance ** refers to the field that is customized when it is stored in the database / update data

#### QAS-101-4 Indicator

- DataBase: quantaxis
- Collections: indicator_day, indicator_min, indicator_ms
- BasicalName:
- AdvanceName:

`` ``
reference:

ADF dynamic buying and selling index, ATR real volatility, BBI long and short index, BBIBOLL long and short berlin line, BIAS deviation rate, BOLL cloth belt, CCI homeopathic index, CDP contrarian operation, DMA average line difference, DMI trend standard, DPO interval The MACD index smooth moving average, the MIKE microphone index, the MTM power index, the PRICEOSC price fluctuation index, the PVT volume and price trend index, the MACD index, the moving average of the MAD, RC change rate index, ROC change rate, RSI relative strength index, SAR parabolic steering, SI swing index, SOBV energy tide, SRMI MI correction index, STD standard deviation, TAPI weighted index transaction value, TRIX triple index smooth average, VHF vertical and horizontal Index, VMA volume simple moving average, VMACD volume index smooth moving average, VOSC volume shock, WVAD William variation discrete, vol_ratio ratio
`` ``
### QAStandard-102 text information data
#### QAS-102-1 public opinion

- DataBase: quantaxis
- Collections: news
- BasicalName: title, datetime, content, author, reference
- AdvanceName: comments, likeNum

#### QAS-102-2 Finance

- DataBase: quantaxis
- Collections: finance_info, finance_balance, finance_profit, finance_cash


### QAStandard-103 reptiles
QAS103 mainly standardize the naming standards for reptiles, UserAgent settings, cookies, session and other norms.
### QAStandard-104 custom data
The custom data needs to be introduced into the database according to the classification criteria. If it is QAS101 time series quotation data, QAS102 text information data can be customized to update the database (using advanced field AdvanceName)


## QAStandard-20x market
### QAStandard-201 transaction
#### QAS-201-1 trading day
The trading day of the market is stored in the market, but it is fragmented data [do not follow QAS101]
Store all stock and futures names on the day of trading by time series


- DataBase: quantaxis
- Collections: trade_date
- BasicalName: date, date_stamp, exchangeName


#### QAS-201-2 transaction list
- DataBase: quantaxis
- Collections: stock_list
- BasicalName: date, date_stamp, stock [code, name]

#### QAS-201-3 trading volume
The transaction volume is obtained from the data format specification of [QAS-101] (# qastandard-101- quot; market data). The specification here is mainly for the matching mechanism. When the requested transaction volume of the strategy is greater than 1/8 of the true volume of the day, Judgment can not be traded.
### QAStandard-202 Matching mechanism
The simple market judgment mechanism is quoted in the [low, high] range, while bid_amount is less than the true trading volume of 1/8
> QAF: the future will add more judging mechanism, especially the depth of the pool

## QAStandard-30x users
### QAStandard-301 account status

### QAStandard-302 account policy
### QAStandard-303 Account custom module
## QAStandard-40x status
### QAStandard-401 status code

## QAStandard-50x API
### QAStandard-501 internal API
#### QAS-501-1 Fetch
QAS501-1 mainly provides the data acquisition package specification, follow this specification, you can carry out the secondary packaging API
`` `Python
Get_stock_day
Get_stock_min
Get_stock_tick
Get_stock_info
Get_stock_indicator
Get_future_day
Get_future_min
Get_future_tick
Get_future_info
Get_options_day
Get_options_min
Get_options_tick
Get_options_info


Save_stock
Save_future
Save_options
Save_all

`` ``

#### QAS-501-2 Market
QAS-501-2 mainly specifies the interface specification for the market transaction, including the data return and response status code [follow QAS-401] (# qastandard-401- status code)


#### QAS-501-3 Account

#### QAS-501-4 Databases
QAS-501-4 mainly specifies the database storage and call naming conventions, the use of hump law to define
Common Name Definitions
- code
- name
- open (double)
- high (double)
- low (double)
- close (double)
- volume (double)
### QAStandard-502 Http API / RESTFul

## QAStandard-60x Util