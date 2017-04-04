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
```mongodb
```