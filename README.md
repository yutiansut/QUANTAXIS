# QUANTAXIS 量化金融策略框架
  
QUANTAXIS量化工具箱,实现了股票和期货市场的全品种回测.通过分布式爬虫进行数据抓取,构建了响应式的数据清洗和行情推送引擎.搭建了支持多语言的开放式回测框架.并构建了交互可视化的客户端和网站.

> 0.3.8 版本将对于一体化和模块化流程进行进一步的优化

![version](https://img.shields.io/badge/Version-%200.3.8dev/beta/pypi-orange.svg)
![Pypi](https://img.shields.io/badge/Pypi-%200.3.8-blue.svg)
![Npm](https://img.shields.io/badge/Npm-%200.3.8-yellow.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
![QQ group](https://img.shields.io/badge/QQGroup-%20563280067-yellow.svg)
![WebSite](https://img.shields.io/badge/Website-%20www.yutiansut.com-brown.svg)
![QQ](https://img.shields.io/badge/AutherQQ-%20279336410-blue.svg)


![QUANTAXIS LOGO](http://i1.piimg.com/1949/62c510db7915837a.png)
## QUANTAXIS-Stardand-Protocol
QUANTAXIS 标准化协议和未来协议

QUANTAXIS-Stardand-Protocol 版本号0.0.1

详情参见  [QUANATXISProtocol](https://github.com/yutiansut/QUANTAXIS/tree/0.3.8-dev-beta-pypi/QUANTAXISProtocol)
## 0.3.8-dev-beta(pypi)版本说明

0.3.8-dev-beta(pypi)是在dev-alpha(packages)上的bug修改版本，主要修复pip的问题

> attention: 最好有wind的包,免费/机构版都可以

> pypi version: 0.3.8-b0

[为了保证最新更新，请使用git clone的方式安装]

### quantaxis
```bash
pip install quantaxis

git clone https://github.com/yutiansut/quantaxis
cd quantaxis
python setup.py install
```

### quantaxis-webkit
> 为了防止手残党打错代码,我把NPM下的quantaxis词条也注册了，因此支持npm install quantaxis  和npm install quantaxiswebkit是一个效果

``` nodejs
mkdir web && cd web
npm install quantaxiswebkit
cd node_modules/quantaxiswebkit
npm run all
```


## 使用示例
```python
import QUANTAXIS as QA

# get data
print(QA.get_stock_day("ts","000001.SZ","2000-01-01","2017-04-01"))
print(QA.get_stock_day("wind","000001.SZ","2000-01-01","2017-04-01"))
print(QA.QAWind.get_stock_list('2017-04-04'))
print(QA.QAWind.get_stock_indicator(name,startDate,endDate))
print(QA.QAWind.get_stock_shape(name,startDate,endDate))

# save data
QA.QAUpdate.windsave.save_trade_date()
QA.QAUpdate.windsave.save_stock_list()
QA.QAUpdate.windsave.save_stock_day(name,startDate,endDate)
#trade

# utils
print(QA.QAUtil.util_date_stamp('2017-01-01'))
```

初始化脚本

![init](http://i4.buimg.com/567571/a3ae817d47d4529e.png)

```mongodb
```

## 适用场景
![适用场景](http://i2.buimg.com/567571/e2e7b31b1f9a4307.png)
考虑到这样的一个业务情景,一个机构的策略团队一般由CS+Finance组成,Finance的同学们非常擅长数据分析,策略等,但却不是很了解代码的底层架构,代码风格和标准都各有差异.而CS出身的同学们虽然对于代码和框架了如指掌,但却对枯燥空洞的金融理论一脸懵逼.而目前国内对于量化的服务支持并不能解决这个常见的场景痛点,要么是针对金融的同学的易于操作的分析系统,但对于IT而言缺少可定制化的部分;要么是针对IT的底层数据和交易接口,而对于金融的同学想从底层接口封装出来一套能用的有效率的框架简直难如登天.

QUNATAXIS致力于解决这一场景痛点,我们通过建立一个前后端分离的,基于RESTful的局域网内的标准化框架来解决这一问题.同时我们希望我们的框架是高扩展和易于接入的,以方便各个公司的各个策略团队的个性化需求(这个是最关键的,基本上每个公司都会有自己的数据,自己的交易接口,自己的特定功能目标),所以我们希望构建的是一个标准化的,高扩展性的,易于部署的脚手架,而不是一个完整的难以定制的解决方案.

QUANTAXIS的前后端完全分离,高度拆分,各个组件依赖RESTful标准的URI来进行通信,这也给了我们开放式框架的无限可能,完全可以实现Matlab,r,python,JavaScript,C,C++,rust等各个用户的和谐共处,而不是增加大家学习成本的去学习一门共用语言.同时,只要一个公网IP和服务器,你也可以超越局域网的限制,实现异地的团队的需求.




## Webkit大礼包

即将重构 #QAF03

![前后端分离](http://i1.piimg.com/567571/41fa8b9c16122bfd.png)

## 回测框架

正在重构 QAF#01

![回测框架](http://i1.piimg.com/567571/151a21b61f4d6d63.png)