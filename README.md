# QUANTAXIS 量化金融策略框架


[![Github workers](https://img.shields.io/github/watchers/yutiansut/quantaxis.svg?style=social&label=Watchers&)](https://github.com/yutiansut/quantaxis/watchers)
[![GitHub stars](https://img.shields.io/github/stars/yutiansut/quantaxis.svg?style=social&label=Star&)](https://github.com/yutiansut/quantaxis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yutiansut/quantaxis.svg?style=social&label=Fork&)](https://github.com/yutiansut/quantaxis/fork)

[点击右上角Star和Watch来跟踪项目进展! 点击Fork来创建属于你的QUANTAXIS!]

![main_1](http://osnhakmay.bkt.clouddn.com/Main_1.gif)
<img src="http://osnhakmay.bkt.clouddn.com/QUANTAXIS-white.png" width = "27.5%" />



![version](https://img.shields.io/badge/Version-%200.5.20-orange.svg)
![build](https://travis-ci.org/yutiansut/QUANTAXIS.svg?branch=master)
[![Stories in Ready](https://badge.waffle.io/yutiansut/QUANTAXIS.svg?label=ready&title=Ready)](http://waffle.io/yutiansut/QUANTAXIS)
[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/yutiansut/quantaxis)
![QAS](https://img.shields.io/badge/QAS-%200.0.8-brown.svg)
![Pypi](https://img.shields.io/badge/Pypi-%200.5.20-blue.svg)
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
- 股指期货日线(T+0)/指数日线/ETF日线
- 股指期货分钟线(T+0) / 指数分钟线/ETF分钟线 [1min/5min/15min/30min/60min] 
- 基于pytdx/各种爬虫的数据源 
```
[注意: tushare最新版本因为单方面直接复制了pytdx  所以导致和最新版本的pytdx不兼容 如有安装0.8.7版本以上的tushare 请降级使用]

*** 降级时需注意: 直接pip uninstall tushare以后 还要去删掉tushare安装目录下的pytdx 再重新安装最新版本的pytdx ***

```
- 实时交易数据
- 基于Vue.js的前端网站
- 自定义的数据结构
- 指标计算
- 板块数据(0.5.1新增)/同花顺,通达信板块
- 基本面数据(部分 最新一期财务报表)
- 行情分发
- 循环回测
- 回测管理优化(新增回测主题/版本号)


预计实现:

- 文档更新
- 期货数据/回测
- 实盘
- 分析模块(行情分析/板块分析)

- 成交记录分析器

<!-- TOC -->

- [QUANTAXIS 量化金融策略框架](#quantaxis-量化金融策略框架)
    - [框架结构](#框架结构)
    - [部署问题:](#部署问题)
        - [git](#git)
        - [MongoDB](#mongodb)
        - [Nodejs](#nodejs)
        - [python](#python)
        - [安装QUANTAXIS](#安装quantaxis)
        - [安装QUANATXIS_WebKit](#安装quanatxis_webkit)
        - [启动QUANTAXIS CLI 并进行数据的初始化存储](#启动quantaxis-cli-并进行数据的初始化存储)
        - [启动QUANTAXIS_Webkit来查看回测的结果](#启动quantaxis_webkit来查看回测的结果)
        - [更新QUANTAXIS](#更新quantaxis)
    - [项目捐赠](#项目捐赠)
    - [关于QUANTAXIS基金](#关于quantaxis基金)
    - [一些基础的api介绍](#一些基础的api介绍)
        - [QUANTAXIS.QABacktest 的 api](#quantaxisqabacktest-的-api)
        - [QUANTAXIS的核心数据结构](#quantaxis的核心数据结构)
        - [QUANTAXIS的指标系统](#quantaxis的指标系统)
        - [QUANTAXIS的行情分析/研究用](#quantaxis的行情分析研究用)
        - [QUANTAXIS的api](#quantaxis的api)
    - [回测Webkit插件概览](#回测webkit插件概览)
    - [QUANTAXIS 标准化协议和未来协议](#quantaxis-标准化协议和未来协议)

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
sudo n stable
sudo npm install npm -g #更新npm
sudo npm install forever -g #安装一个全局的forever 用于之后启动
(如果forever 安装卡住/耗时过长 使用淘宝镜像CNPM)

(sudo npm install cnpm -g)
(sudo cnpm install forever -g)

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

> python的一些需要编译的包的安装

安装TA-Lib
> Ubuntu
```
sudo apt-get update
sudo apt-get install python3.6-dev
# 装talib前要先装numpy
sudo python3.6 -m pip install numpy -i https://pypi.doubanio.com/simple
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
cd ..
sudo python3.6 -m pip install TA-Lib
# 安装剩余的依赖项
sudo python3.6 -m pip install -r requirements.txt -i https://pypi.doubanio.com/simple
sudo python3.6 -m pip install tushare==0.8.7 -i https://pypi.doubanio.com/simple

```
> Windows
```

# 访问http://www.lfd.uci.edu/~gohlke/pythonlibs/  下载对应的whl安装包
# pip install xxxxx(文件名).whl
```
### 安装QUANTAXIS
```
git clone https://github.com/yutiansut/quantaxis
cd quantaxis .
pip install -r requirements.txt -i https://pypi.doubanio.com/simple
pip install tushare==0.8.7
(sudo) pip install -e . # 一定要用这种方法,python setup.py install方法无法解压 安装在本目录下的开发模式
# 注: 安装成本地开发模式以后,只需要git pull 就可以更新代码 无需重新 pip install -e .
```

```
[注意: tushare最新版本因为单方面直接复制了pytdx  所以导致和最新版本的pytdx不兼容 如有安装0.8.7版本以上的tushare 请降级使用]

典型表现是: 即使已经安装了pytdx 依然会报错找不到pytdx

*** 降级时需注意: 直接pip uninstall tushare以后 还要去删掉tushare安装目录下(一般是lib\site-packages\)的pytdx 再重新安装最新版本的pytdx ***

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
quantaxis> save stock_block
quantaxis> save stock_info
随意新建一个目录:(不要跟QUANTAXIS文件夹在一个目录)

在命令行输入 quantaxis 进去quantaxis CLI


输入examples 在当前目录下生成一个示例策略

运行这个示例策略:

python  backtest.py

一般而言 日线4个组合的回测(一年)在14-17秒左右 5min级别4个组合的回测(一年)在3-4分钟左右


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
(sudo) npm run dev 或者 forever start build/dev-server.js
```

会自动启动localhost:8080网页端口,用账户名admin,密码admin登录
(注明: admin注册是在python的QUANTAXIS save all时候执行的)

另外 如果save all已经执行,依然登录不进去 点击插件状态 查看3000端口是否打开


登录后点击左上角 <模拟回测> 在模拟回测的选择界面的用户名搜索框输入回测的时候的用户名(默认是admin),回车

选择和你回测策略中名称一致的结果即可进入可视化界面


### 更新QUANTAXIS

由于目前项目还在开发中,所以需要使用Git来更新项目:

点击右上角的Star和watch来持续跟踪项目进展~

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

写代码不易...写文档最难过...请作者喝杯咖啡呗?

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

QB.backtest_print_log = True  # 是否在屏幕上输出结果


QB.setting.QA_setting_user_name = str('admin') #回测账户
QB.setting.QA_setting_user_password = str('admin') #回测密码


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
#查询当前一只股票的可卖数量
QB.QA_backtest_sell_available(QB,code)
#查询当前一只股票的持仓平均成本
QB.QA_backtest_hold_price(QB,code)

```
### QUANTAXIS的核心数据结构

QA_DataStruct


属性用@property装饰器装饰,进行懒运算 提高效率

DataStruct具有的功能:

- 数据容器
- 数据变换 [分拆/合并/倒序] split/merge/reverse
- 数据透视 pivot
- 数据筛选 select_time/select_time_with_gap/select_code/get_bar
- 数据复权 to_qfq/to_hfq
- 数据显示 show
- 格式变换 to_json/to_pandas/to_list/to_numpy
- 数据库式查询  query
- 画图 plot
- 计算指标 add_func


QA_DataStruct_Stock_block

- (属性)该类下的所有板块名称 block_name
- 查询某一只股票所在的所有板块 get_code(code)
- 查询某一个板块下的所有股票 get_block(block)
- 展示当前类下的所有数据 show





我们可以通过 
```
import QUANTAXIS as QA

# QA.QA_fetch_stock_day_adv
# QA.QA_fetch_stock_min_adv
# QA.QA_fetch_index_day_adv
# QA.QA_fetch_index_min_adv

```
day线的参数是code, start, end
min线的参数是code, start, end, type_='1min'

其中 code 可以是一个股票,也可以是一列股票(list)

取一个股票的数据
```
QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-10-01')
In [5]: QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-10-01')
Out[5]: QA_DataStruct_Stock_day with 1 securities
```
取多个股票的数据
```
QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-01-01','2017-10-01')
In [6]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-01-01','2017-10-01')
Out[6]: QA_DataStruct_Stock_day with 2 securities
```
显示结构体的数据 .data
```
In [10]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').data
Out[10]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-26 000001  000001  11.26  11.30  10.96  11.05  967460.0 2017-09-26
2017-09-27 000001  000001  11.01  11.08  10.90  10.93  727188.0 2017-09-27
2017-09-28 000001  000001  10.98  10.98  10.82  10.88  517220.0 2017-09-28
2017-09-29 000001  000001  10.92  11.16  10.86  11.11  682280.0 2017-09-29
2017-09-20 000002  000002  28.50  29.55  28.00  28.73  613095.0 2017-09-20
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
2017-09-25 000002  000002  27.20  27.20  26.10  26.12  722702.0 2017-09-25
2017-09-26 000002  000002  26.12  27.22  26.10  26.76  593044.0 2017-09-26
2017-09-27 000002  000002  27.00  27.28  26.52  26.84  367534.0 2017-09-27
2017-09-28 000002  000002  27.00  27.15  26.40  26.41  262347.0 2017-09-28
2017-09-29 000002  000002  26.56  26.80  26.00  26.25  345752.0 2017-09-29
```
显示结构体的开/高/收/低 .open/.high/.close/.low
```
In [5]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').high
Out[5]:
date        code
2017-09-20  000001    11.37
2017-09-21  000001    11.51
2017-09-22  000001    11.52
2017-09-25  000001    11.45
2017-09-26  000001    11.30
2017-09-27  000001    11.08
2017-09-28  000001    10.98
2017-09-29  000001    11.16
2017-09-20  000002    29.55
2017-09-21  000002    29.06
2017-09-22  000002    28.67
2017-09-25  000002    27.20
2017-09-26  000002    27.22
2017-09-27  000002    27.28
2017-09-28  000002    27.15
2017-09-29  000002    26.80
Name: high, dtype: float64
```
数据结构复权to_qfq()/to_hfq()

返回的是一个DataStruct,用.data展示返回的数据的结构

其中DataStruct.if_fq的属性会改变
```
In [4]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').to_qfq().data

Out[4]:
                     code   open   high    low  close    volume       date  \
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-26 000001  000001  11.26  11.30  10.96  11.05  967460.0 2017-09-26
2017-09-27 000001  000001  11.01  11.08  10.90  10.93  727188.0 2017-09-27
2017-09-28 000001  000001  10.98  10.98  10.82  10.88  517220.0 2017-09-28
2017-09-29 000001  000001  10.92  11.16  10.86  11.11  682280.0 2017-09-29
2017-09-20 000002  000002  28.50  29.55  28.00  28.73  613095.0 2017-09-20
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
2017-09-25 000002  000002  27.20  27.20  26.10  26.12  722702.0 2017-09-25
2017-09-26 000002  000002  26.12  27.22  26.10  26.76  593044.0 2017-09-26
2017-09-27 000002  000002  27.00  27.28  26.52  26.84  367534.0 2017-09-27
2017-09-28 000002  000002  27.00  27.15  26.40  26.41  262347.0 2017-09-28
2017-09-29 000002  000002  26.56  26.80  26.00  26.25  345752.0 2017-09-29

                   preclose  adj
date       code
2017-09-20 000001       NaN  1.0
2017-09-21 000001     11.29  1.0
2017-09-22 000001     11.46  1.0
2017-09-25 000001     11.44  1.0
2017-09-26 000001     11.29  1.0
2017-09-27 000001     11.05  1.0
2017-09-28 000001     10.93  1.0
2017-09-29 000001     10.88  1.0
2017-09-20 000002       NaN  1.0
2017-09-21 000002     28.73  1.0
2017-09-22 000002     28.40  1.0
2017-09-25 000002     27.81  1.0
2017-09-26 000002     26.12  1.0
2017-09-27 000002     26.76  1.0
2017-09-28 000002     26.84  1.0
2017-09-29 000002     26.41  1.0
```
数据透视 .pivot()
```
In [6]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').pivot('open')
Out[6]:
code        000001  000002
date
2017-09-20   11.14   28.50
2017-09-21   11.26   28.50
2017-09-22   11.43   28.39
2017-09-25   11.44   27.20
2017-09-26   11.26   26.12
2017-09-27   11.01   27.00
2017-09-28   10.98   27.00
2017-09-29   10.92   26.56
```
数据的时间筛选.select_time(start,end)
```
In [10]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time('2017-09-20','2017-09-25')
Out[10]: QA_DataStruct_Stock_day with 2 securities

In [11]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time('2017-09-20','2017-09-25').data
Out[11]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-20 000002  000002  28.50  29.55  28.00  28.73  613095.0 2017-09-20
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
2017-09-25 000002  000002  27.20  27.20  26.10  26.12  722702.0 2017-09-25
```
数据按时间往前/往后推 select_time_with_gap(time,gap,methods)

time是你选择的时间
gap是长度 (int)
methods有 '<=','lte','<','lt','eq','==','>','gt','>=','gte'的选项
```
In [14]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time_with_gap('2017-09-20',2,'gt')
Out[14]: QA_DataStruct_Stock_day with 2 securities

In [15]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time_with_gap('2017-09-20',2,'gt').data
Out[15]:
                     code   open   high    low  close    volume       date
date       code
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
```
选取结构组里面某一只股票select_code(code)

```
In [16]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_code('000001')
Out[16]: QA_DataStruct_Stock_day with 1 securities
In [17]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_code('000001').data
Out[17]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-26 000001  000001  11.26  11.30  10.96  11.05  967460.0 2017-09-26
2017-09-27 000001  000001  11.01  11.08  10.90  10.93  727188.0 2017-09-27
2017-09-28 000001  000001  10.98  10.98  10.82  10.88  517220.0 2017-09-28
2017-09-29 000001  000001  10.92  11.16  10.86  11.11  682280.0 2017-09-29
```
取某一只股票的某一个时间的bar(code,time,if_trade)

第三个选项 默认是True  
第三选项的意义在于,如果出现了停牌,参数如果是True 那么就会返回空值 而如果是False,就会返回停牌前最后一个交易日的值
```
In [18]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').get_bar('000001','2017-09-20',True)
Out[18]: QA_DataStruct_Stock_day with 1 securities

In [19]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').get_bar('000001','2017-09-20',True).data
Out[19]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20

```
画图 plot(code)

如果是()空值 就会把全部的股票都画出来
```
In [20]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').plot()
QUANTAXIS>> The Pic has been saved to your path: .\QA_stock_day_codepackage_bfq.html

In [21]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').plot('000001')
QUANTAXIS>> The Pic has been saved to your path: .\QA_stock_day_000001_bfq.html

```

![](http://osnhakmay.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20171004125336.png)

### QUANTAXIS的指标系统

QUANTAXIS的核心数据结构有一个方法叫add_func(func,*args,**kwargs),作为一个指标入口,会返回一个和DataStruct中股票数量一致长度的list

QUANTAXIS有两种类型的指标:

- 基础指标(输入为Series的指标)
- 应用级指标(可应用于DataStruct的指标)

其中,基础指标是为了应用级指标做准备的,及对应于Series的分析和dataframe的分析的关系

基础类指标 [基本和同花顺/通达信一致]
```python
import QUANTAXIS as QA
QA.MA(Series, N)
QA.EMA(Series, N)
QA.DIFF(Series, N=1)
QA.HHV(Series, N)
QA.LLV(Series, N)
QA.SUM(Series, N)
QA.ABS(Series)
QA.MAX(A, B)
QA.MIN(A, B)
QA.CROSS(A, B)
QA.COUNT(COND, N)
QA.IF(COND, V1, V2)
QA.REF(Series, N)
QA.STD(Series, N)
QA.AVEDEV(Series, N)
QA.BBIBOLL(Series, N1, N2, N3, N4, N, M)
```
应用级指标  add_func(func)
```python
import QUANTAXIS as QA
QA.QA_indicator_OSC(DataFrame, N, M)
QA.QA_indicator_BBI(DataFrame, N1, N2, N3, N4)
QA.QA_indicator_PBX(DataFrame, N1, N2, N3, N4, N5, N6)
QA.QA_indicator_BOLL(DataFrame, N)
QA.QA_indicator_ROC(DataFrame, N, M)
QA.QA_indicator_MTM(DataFrame, N, M)
QA.QA_indicator_KDJ(DataFrame, N=9, M1=3, M2=3)
QA.QA_indicator_MFI(DataFrame, N)
QA.QA_indicator_ATR(DataFrame, N)
QA.QA_indicator_SKDJ(DataFrame, N, M)
QA.QA_indicator_WR(DataFrame, N, N1)
QA.QA_indicator_BIAS(DataFrame, N1, N2, N3)
QA.QA_indicator_RSI(DataFrame, N1, N2, N3)
QA.QA_indicator_ADTM(DataFrame, N, M)
QA.QA_indicator_DDI(DataFrame, N, N1, M, M1)
QA.QA_indicator_CCI(DataFrame, N=14)
```
自己写一个指标:

比如 绝路航标
```python
import QUANTAXIS as QA
def JLHB(data, m=7, n=5):
    """
    通达信定义
    VAR1:=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80; 
    B:SMA(VAR1,N,1); 
    VAR2:SMA(B,M,1); 
    绝路航标:IF(CROSS(B,VAR2) AND B<40,50,0);
    """
    var1 = (data['close'] - QA.LLV(data['low'], 60)) / \
        (QA.HHV(data['high'], 60) - QA.LLV(data['low'], 60)) * 80
    B = QA.MA(var1, m)
    var2 = QA.MA(B, n)
    if QA.CROSS(B,var2) and B[-1]<40:
        return 1
    else:
        return 0

# 得到指标
QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-01-31').to_qfq().add_func(JLHB)
```

### QUANTAXIS的行情分析/研究用


主要是针对行情的各种统计学特征/指标等分析,支持QA_DataStruct_系列的add_func()功能

接收DataFrame形式的行情以及QUANTAXIS.QADATA格式的行情

目前有:


(属性)

- 一阶差分
- 样本方差
- 方差
- 标准差
- 样本标准差
- 平均数
- 调和平均数
- 众数
- 振幅(极差)
- 偏度
- 峰度
- 百分比变化
- 平均绝对偏差 

```python
import QUANTAXIS as QA

data=QA.QA_fetch_stock_day_adv('600066','2013-12-01','2017-10-01') #[可选to_qfq(),to_hfq()]
s=QA.QA_Analysis_stock(data)
# s 的属性是( < QA_Analysis_Stock > )

s.open # 开盘价序列
s.close # 收盘价序列
s.high # 最高价序列
s.low # 最低价序列
s.vol  # 量
s.volume # 同vol
s.date  # 日期
s.datetime
s.index  # 索引
s.price  # 平均价(O+H+L+C)/4
s.mean # price的平均数
s.max  # price的最大值
s.min # price的最小值
s.mad # price的平均绝对偏差
s.mode  # price的众数(没啥用)
s.price_diff # price的一阶差分
s.variance # price的方差
s.pvariance # price的样本方差
s.stdev  # price的标准差
s.pstdev # price的样本标准差
s.mean_harmonic # price的调和平均数
s.amplitude  #price的振幅[极差]
s.skewnewss # price的峰度 (4阶中心距)
s.kurtosis  # price的偏度 (3阶中心距)
s.pct_change # price的百分比变化序列


s.add_func(QA.QA_indicator_CCI) # 指标计算, 和DataStruct用法一致

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

QA.QA_util_log_info('板块数据')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_block()


"""
QA.QA_fetch_ 系列 
从本地数据库获取数据
"""
# 股票
QA_fetch_stock_day_adv(code,start,end)
QA_fetch_stock_min_adv(code,start,end,type_='1min') # type_可以选1min/5min/15min/30min/60min 
# 指数/ETF
QA_fetch_index_day_adv(code,start,end)
QA_fetch_index_min_adv(code,start,end,type_='1min') # type_可以选1min/5min/15min/30min/60min 
# 板块
QA_fetch_stock_block_adv(code)

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
