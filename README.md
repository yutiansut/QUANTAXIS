# QUANTAXIS 量化金融策略框架


[![Github workers](https://img.shields.io/github/watchers/yutiansut/quantaxis.svg?style=social&label=Watchers&)](https://github.com/yutiansut/quantaxis/watchers)
[![GitHub stars](https://img.shields.io/github/stars/yutiansut/quantaxis.svg?style=social&label=Star&)](https://github.com/yutiansut/quantaxis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yutiansut/quantaxis.svg?style=social&label=Fork&)](https://github.com/yutiansut/quantaxis/fork)

![main_1](http://osnhakmay.bkt.clouddn.com/Main_1.gif)
<img src="http://i1.piimg.com/1949/62c510db7915837a.png" width = "27.5%" />



![version](https://img.shields.io/badge/Version-%200.4.50-orange.svg)
![build](https://travis-ci.org/yutiansut/QUANTAXIS.svg?branch=master)
[![Stories in Ready](https://badge.waffle.io/yutiansut/QUANTAXIS.svg?label=ready&title=Ready)](http://waffle.io/yutiansut/QUANTAXIS)
[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/yutiansut/quantaxis)
![QAS](https://img.shields.io/badge/QAS-%200.0.8-brown.svg)
![Pypi](https://img.shields.io/badge/Pypi-%200.4.50-blue.svg)
![python](https://img.shields.io/badge/python-%203.6/3.5/3.4/win/ubuntu-darkgrey.svg)
![Npm](https://img.shields.io/badge/Npm-%200.4.0-yellow.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)


> 欢迎加群讨论: [群链接](https://jq.qq.com/?_wv=1027&k=4CEKGzn) 

QUANTAXIS量化金融策略框架,是一个面向中小型策略团队的量化分析解决方案. 我们通过高度解耦的模块化以及标准化协议,可以快速的实现面向场景的定制化解决方案.QUANTAXIS是一个渐进式的开放式框架,你可以根据自己的需要,引入自己的数据,分析方案,可视化过程等,也可以通过RESTful接口,快速实现多人局域网/广域网内的协作.

======

已经实现：

- 日线（自1990年）回测 [定点复权] (T+1)
- 分钟线 [1min/5min/15min/30min/60min]回测 (T+1)
- 股指期货日线(T+0)
- 股指期货分钟线 [1min/5min/15min/30min/60min] (T+0)
- 基于tushare/pytdx/各种爬虫的数据源
- 实时交易数据
- 基于Vue.js的前端网站

预计实现:

- 文档更新
- 基本面数据
- 指标数据
<!-- TOC -->

- [QUANTAXIS 量化金融策略框架](#quantaxis-%E9%87%8F%E5%8C%96%E9%87%91%E8%9E%8D%E7%AD%96%E7%95%A5%E6%A1%86%E6%9E%B6)
    - [框架结构](#%E6%A1%86%E6%9E%B6%E7%BB%93%E6%9E%84)
    - [部署问题:](#%E9%83%A8%E7%BD%B2%E9%97%AE%E9%A2%98)
        - [git](#git)
        - [MongoDB](#mongodb)
        - [Nodejs](#nodejs)
        - [python](#python)
            - [python的一些需要编译的包的安装](#python%E7%9A%84%E4%B8%80%E4%BA%9B%E9%9C%80%E8%A6%81%E7%BC%96%E8%AF%91%E7%9A%84%E5%8C%85%E7%9A%84%E5%AE%89%E8%A3%85)
        - [安装QUANTAXIS](#%E5%AE%89%E8%A3%85quantaxis)
        - [安装QUANATXIS_WebKit](#%E5%AE%89%E8%A3%85quanatxiswebkit)
        - [启动QUANTAXIS CLI 并进行数据的初始化存储](#%E5%90%AF%E5%8A%A8quantaxis-cli-%E5%B9%B6%E8%BF%9B%E8%A1%8C%E6%95%B0%E6%8D%AE%E7%9A%84%E5%88%9D%E5%A7%8B%E5%8C%96%E5%AD%98%E5%82%A8)
        - [启动QUANTAXIS_Webkit来查看回测的结果](#%E5%90%AF%E5%8A%A8quantaxiswebkit%E6%9D%A5%E6%9F%A5%E7%9C%8B%E5%9B%9E%E6%B5%8B%E7%9A%84%E7%BB%93%E6%9E%9C)
        - [更新QUANTAXIS](#%E6%9B%B4%E6%96%B0quantaxis)
    - [项目捐赠](#%E9%A1%B9%E7%9B%AE%E6%8D%90%E8%B5%A0)
    - [关于QUANTAXIS基金](#%E5%85%B3%E4%BA%8Equantaxis%E5%9F%BA%E9%87%91)
    - [一些基础的api介绍](#%E4%B8%80%E4%BA%9B%E5%9F%BA%E7%A1%80%E7%9A%84api%E4%BB%8B%E7%BB%8D)
        - [QUANTAXIS.QABacktest 的 api](#quantaxisqabacktest-%E7%9A%84-api)
        - [QUANTAXIS的api](#quantaxis%E7%9A%84api)
    - [回测Webkit插件概览](#%E5%9B%9E%E6%B5%8Bwebkit%E6%8F%92%E4%BB%B6%E6%A6%82%E8%A7%88)
    - [QUANTAXIS 标准化协议和未来协议](#quantaxis-%E6%A0%87%E5%87%86%E5%8C%96%E5%8D%8F%E8%AE%AE%E5%92%8C%E6%9C%AA%E6%9D%A5%E5%8D%8F%E8%AE%AE)

<!-- /TOC -->

## 框架结构
![](http://i1.piimg.com/567571/dc3c811a5afcb4fb.png)


## 部署问题:

- Windows/Linux(ubuntu) 已测试通过
- python3.6(开发环境) python2 回测框架不兼容(attention! 之后会逐步用更多高级语法)   [*] 如果需要交易,请下载32位的python3.6
- nodejs 需要安装>7的版本,来支持es6语法
- mongodb是必须要装的
- 强烈推荐mongodb的可视化库  robomongo 百度即可下载

一个简易demo(需要先安装并启动mongodb,python版本需要大于3)

### git
>windows

百度搜索:git 下载--exe安装

>linux

自带 无需安装

### MongoDB 
> Windows

- 下载地址 MongoDB 64位 3.4.7:[下载链接](https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-3.4.7-signed.msi)

- 可以使用迅雷下载加速

- 下载完毕以后双击MSI文件安装,一般会安装到C:\Program Files\MongoDB\Server\3.4\bin

* MongoDB需要一个data目录一个logo目录,一般我们会在D:中新建一个data目录
```powershell
# 打开Powershell(Win键+R 在运行中输入Powershell)
cd D:
md data
# 然后在data目录下 新建一个data目录用于存放mongo的数据,log目录用于存放log
cd data
md data
md log
# 到Mongo的程序文件夹下,使用命令
cd C:\Program Files\MongoDB\Server\3.4\bin
# 用mongod 命令安装
.\mongod.exe --dbpath  D:\data\data  --logpath D:\data\log\mongo.log --httpinterface --rest --serviceName 'MongoDB' --install
# 启动mongodb服务
net start MongoDB
```
> linux
- Ubuntu

```shell
#  添加源
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
# Ubuntu 12.04
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
# Ubuntu 14.04
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
# Ubuntu 16.04
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
# 更新源
sudo apt-get update
# 安装MongoDB
sudo apt-get install -y mongodb-org
# 开启MongoDB服务
sudo service mongod start

```
### Nodejs
> windows

官网链接: https://nodejs.org/zh-cn/download/current/

直接下载exe 按要求安装即可 最新版本 8.2.1

> Linux

- Ubuntu

```shell
sudo apt-get install npm
sudo npm install n -g
sudo n latest
sudo npm install npm -g #更新npm
sudo npm install forever -g #安装一个全局的forever 用于之后启动
```

linux/mac下的nodejs有一个版本管理包 叫n 需要全局安装 -g

所以无论装了什么版本的nodejs  只需要npm install n -g  就行  
### python

> Linux
```shell

#install python3.6 in linux
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
wget https://bootstrap.pypa.io/get-pip.py
sudo -H python3.6 get-pip.py
```
> Windows

建议直接安装Anaconda包,记住在安装时 选择添加path不然后面会很麻烦

#### python的一些需要编译的包的安装

安装TA-Lib
```
sudo apt-get update
sudo apt-get install python3.6-dev
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
cd ..
pip install TA-Lib
# 安装剩余的依赖项
python3.6 -m pip install -r requirements.txt -i https://pypi.doubanio.com/simple
python3.6 -m pip install tushare https://pypi.doubanio.com/simple
#####

# Windows 下安装一些需要编译的包:
# 访问http://www.lfd.uci.edu/~gohlke/pythonlibs/  下载对应的whl安装包
# pip install xxxxx(文件名).whl
```
### 安装QUANTAXIS
```
git clone https://github.com/yutiansut/quantaxis
cd quantaxis 
(sudo) pip install -e . # 一定要用这种方法,python setup.py install方法无法解压 安装在本目录下的开发模式

```
### 安装QUANATXIS_WebKit
```shell
cd QUANTAXIS_Webkit
(sudo) npm install forever -g

# 先去后台项目的文件夹安装
cd backend
(sudo) npm install
# 再去前端的文件夹安装
cd ..
cd web
(sudo) npm install
```
### 启动QUANTAXIS CLI 并进行数据的初始化存储

在命令行输入 quantaxis 进去quantaxis CLI
quantaxis> save all

随意新建一个目录:(不要跟QUANTAXIS文件夹在一个目录)

在命令行输入 quantaxis 进去quantaxis CLI


输入examples 在当前目录下生成一个示例策略

运行这个示例策略:

python  backtest.py


### 启动QUANTAXIS_Webkit来查看回测的结果


启动网络插件(nodejs 版本号需要大于6,最好是7)
```shell
cd QUANTAXIS_Webkit
# 先启动后台服务器  在3000端口
cd backend
(sudo) forever start bin/www
cd ..
# 再启动前端服务器  在8080端口
cd web
(sudo) npm install
(sudo) npm run dev 或者 forever start build/dev-server.js
```

会自动启动localhost:8080网页端口,用账户名admin,密码admin登录
(注明: admin注册是在python的QUANTAXIS save all时候执行的)

另外 如果save all已经执行,依然登录不进去 点击插件状态 查看3000端口是否打开

### 更新QUANTAXIS

由于目前项目还在开发中,所以需要使用Git来更新项目:

常规更新:
```
cd QUANTAXIS
git pull
```

如果本地有进行更改,遇到更新失败:

(注意: 最好不要在本地修改该项目文件,如果需要做一些自定义功能,可以进fork[在项目的右上角])

```
git reset --hard origin/master
git pull
```

## 项目捐赠

写代码不易...写文档最难过...请....作者喝杯咖啡呗?

<img src="http://osnhakmay.bkt.clouddn.com/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20170923132018.jpg" width = "27.5%" />

(PS: 支付的时候 请带上你的名字/昵称呀 会维护一个赞助列表~ )

[捐赠列表](https://github.com/yutiansut/QUANTAXIS/blob/master/sponsorship.md)


## 关于QUANTAXIS基金

第一天挂上项目捐赠就有童靴赞助支持~~蟹蟹蟹蟹~~

准备把项目捐赠的钱 以及我自己会补一部分进来 维护一个基金会  主要是奖励文档编写和bug提交的童鞋们~



## 一些基础的api介绍

QUANTAXIS 是一个渐进式的框架,也就是说 你可以很简单的只使用回测部分,也可以逐步深入开发,从数据源获取/数据库替代,到回测的引擎的修改,自定义交易模式,事件修改等等.

在0.5.0以前,api都不是很稳定,所以文档这块比较欠缺,暂时先给一些常用的api说明:

### QUANTAXIS.QABacktest 的 api
```python
from QUANTAXIS import QA_Backtest as QB
#常量:
QB.backtest_type #回测类型 day/1min/5min/15min/30min/60min/index_day/index_1min/index_5min/index_15min/index_30min/index_60min/
QB.account.message  #当前账户消息
QB.account.cash  #当前可用资金
QB.account.hold # 当前账户持仓
QB.account.history #当前账户的历史交易记录
QB.account.assets #当前账户总资产
QB.account.detail #当前账户的交易对账单
QB.account.init_assest #账户的最初资金
QB.strategy_gap #前推日期
QB.strategy_name #策略名称

QB.strategy_stock_list #回测初始化的时候  输入的一个回测标的
QB.strategy_start_date #回测的开始时间
QB.strategy_end_date  #回测的结束时间


QB.today  #在策略里面代表策略执行时的日期
QB.now  #在策略里面代表策略执行时的时间
QB.benchmark_code  #策略业绩评价的对照行情




#函数:
#获取市场(基于gap)行情:
QB.QA_backtest_get_market_data(QB,code,QB.today/QB.now)
- 可选项: gap_ 
- 可选项: type_ 'lt','lte' 默认是lt
#获取单个bar
QB.QA_backtest_get_market_data_bar(QB,code,QB.today/QB.now)

#拿到开高收低量
Open,High,Low,Close,Volume=QB.QA_backtest_get_OHLCV(QB,QB.QA_backtest_get_market_data(QB,item,QB.today))

#获取市场自定义时间段行情:
QA.QA_fetch_stock_day(code,start,end,model)

#一键平仓:
QB.QA_backtest_sell_all(QB)

#报单:
QB.QA_backtest_send_order(QB, code,amount,towards,order: dict)
"""
order有三种方式:
1.限价成交 order['bid_model']=0或者l,L
  注意: 限价成交需要给出价格:
  order['price']=xxxx

2.市价成交 order['bid_model']=1或者m,M,market,Market  [其实是以bar的开盘价成交]
3.严格成交模式 order['bid_model']=2或者s,S
    及 买入按bar的最高价成交 卖出按bar的最低价成交
3.收盘价成交模式 order['bid_model']=3或者c,C
"""
#查询当前一只股票的持仓量
QB.QA_backtest_hold_amount(QB,code)


```


### QUANTAXIS的api
```python

import QUANTAXIS as QA

"""
QA.QA_fetch_get_  系列:
从网上获取数据
"""


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




QA.QA_util_log_info('分钟线')
QA.QA_util_log_info('1min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','1min')


QA.QA_util_log_info('5min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','5min')


QA.QA_util_log_info('15min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','15min')




QA.QA_util_log_info('除权除息')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_xdxr('00001')




QA.QA_util_log_info('股票列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('stock')


QA.QA_util_log_info('指数列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('index')


QA.QA_util_log_info('全部列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('all')




QA.QA_util_log_info('指数日线')
data=QA.QAFetch.QATdx.QA_fetch_get_index_day('000001','2017-01-01','2017-09-01')




QA.QA_util_log_info('指数分钟线')
QA.QA_util_log_info('1min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','1min')


QA.QA_util_log_info('5min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','5min')


QA.QA_util_log_info('15min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','15min')



QA.QA_util_log_info('最后一次交易价格')
QA.QA_util_log_info('参数为列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest(['000001','000002'])


QA.QA_util_log_info('参数为一只股票')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest('000001')




QA.QA_util_log_info('实时价格')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_realtime(['000001','000002'])




QA.QA_util_log_info('分笔成交')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_transaction('000001','2001-01-01','2001-01-15')


"""
QA.QA_fetch_ 系列 
从本地数据库获取数据
"""

QA.QA_fetch_stock_day()

QA.QA_fetch_stocklist_day()

QA.QA_fetch_stock_day_adv()

QA.QA_fetch_stocklist_day_adv()



```

## 回测Webkit插件概览

![](http://i2.muimg.com/567571/736ba4adda9fac85.png)
![](http://i2.muimg.com/588926/345e924a45cae6e5.png)
![](http://i1.piimg.com/1949/7b6e2fc347220f7b.png)
![](http://i1.piimg.com/567571/09bd05c3698f2d38.png)
![](http://i1.piimg.com/567571/053ac3e3850f8f60.png)
![](http://osnhakmay.bkt.clouddn.com/quantaxis%20markdown.gif)


## QUANTAXIS 标准化协议和未来协议


QUANTAXIS-Stardand-Protocol 版本号0.0.8

详情参见  [QUANATXISProtocol](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXISProtocol/readme.md)
