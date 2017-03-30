# QUANTAXIS 量化金融策略框架
  
QUANTAXIS量化工具箱,实现了股票和期货市场的全品种回测.通过分布式爬虫进行数据抓取,构建了响应式的数据清洗和行情推送引擎.搭建了支持多语言的开放式回测框架.并构建了交互可视化的客户端和网站.

> 0.3.8 版本将对于一体化和模块化流程进行进一步的优化

![version](https://img.shields.io/badge/Version-%200.3.8alpha-orange.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
![QQ group](https://img.shields.io/badge/QQGroup-%20563280067-yellow.svg)
![WebSite](https://img.shields.io/badge/Website-%20www.yutiansut.com-brown.svg)
![QQ](https://img.shields.io/badge/AutherQQ-%20279336410-blue.svg)

## 写在前面 | Written Before

考虑到这样的一个业务情景,一个机构的策略团队一般由CS+Finance组成,Finance的同学们非常擅长数据分析,策略等,但却不是很了解代码的底层架构,代码风格和标准都各有差异.而CS出身的同学们虽然对于代码和框架了如指掌,但却对枯燥空洞的金融理论一脸懵逼.而目前国内对于量化的服务支持并不能解决这个常见的场景痛点,要么是针对金融的同学的易于操作的分析系统,但对于IT而言缺少可定制化的部分;要么是针对IT的底层数据和交易接口,而对于金融的同学想从底层接口封装出来一套能用的有效率的框架简直难如登天.

QUNATAXIS致力于解决这一场景痛点,我们通过建立一个前后端分离的,基于RESTful的局域网内的标准化框架来解决这一问题.同时我们希望我们的框架是高扩展和易于接入的,以方便各个公司的各个策略团队的个性化需求(这个是最关键的,基本上每个公司都会有自己的数据,自己的交易接口,自己的特定功能目标),所以我们希望构建的是一个标准化的,高扩展性的,易于部署的脚手架,而不是一个完整的难以定制的解决方案.

QUANTAXIS的前后端完全分离,高度拆分,各个组件依赖RESTful标准的URI来进行通信,这也给了我们开放式框架的无限可能,完全可以实现Matlab,r,python,JavaScript,C,C++,rust等各个用户的和谐共处,而不是增加大家学习成本的去学习一门共用语言.同时,只要一个公网IP和服务器,你也可以超越局域网的限制,实现异地的团队的需求.


![QUANTAXIS LOGO](http://i1.piimg.com/1949/62c510db7915837a.png)

<!-- TOC -->

- [QUANTAXIS 量化金融策略框架](#quantaxis-量化金融策略框架)
    - [写在前面 | Written Before](#写在前面--written-before)
    - [概览|Intro](#概览intro)
    - [部署| How To Setup](#部署-how-to-setup)
        - [环境](#环境)
        - [​部署](#​部署)
        - [适用场景](#适用场景)
        - [注意](#注意)
    - [逻辑框架|Logic](#逻辑框架logic)
    - [组件|Component](#组件component)
        - [Backend/  & Data/](#backend---data)
        - [Storage/](#storage)
        - [Client/ & web/](#client--web)
        - [Analysis/  & Strategy/](#analysis---strategy)
        - [Docs/](#docs)
        - [Tasks/](#tasks)
    - [版本历史|History](#版本历史history)
    - [QUANTAXIS 4.0 is coming soon.....](#quantaxis-40-is-coming-soon)

<!-- /TOC -->

## 概览|Intro

| 测试系统               | 语言环境                                 | 实现功能            |
| :----------------- | :----------------------------------- | :-------------- |
| Ubuntu 16.04 AMD64 | Python 2.7.6,2.7.11; 3.5,3.6         | 股票/期货回测         |
| Windows 10         | Matlab 2016a                         | 可视化界面           |
|                    | R 3.3                                | 全平台（W/L/M)客户端   |
| Mac 平台未测试          | Nodejs 7.7.1 npm4.3.0                | 定制化爬虫           |
|                    | Vue 2.0                              | 纯本地框架 免去策略保密等问题 |
|                    | MongoDB 3.2 / MySQL 5.7 /Redis 3.0.6 |                 |

| Test System        | Language Environment                 | Functions                   |
| :----------------- | :----------------------------------- | :-------------------------- |
| Ubuntu 16.04 AMD64 | Python 2.7.6,2.7.11; 3.5,3.6         | CN Stock/Future Backtest    |
| Windows 10         | Matlab 2016a                         | Visualization               |
|                    | R 3.3                                | Win/Linux/Mac Client        |
| Mac      unknown   | Nodejs 7.7.1 npm4.3.0                | Crawler                     |
|                    | Vue 2.0                              | Local Framework with Safety |
|                    | MongoDB 3.2 / MySQL 5.7 /Redis 3.0.6 |                             |

========

## 部署| How To Setup

### 环境

  - Python(2.7/3.6)  (necessary)
  - Nodejs  (necessary)
  - MongoDB (necessary)
  - Matlab (optional)
  - R(optional)
  - MySQL(optional)
  - Redis(optional)
  - Wind 万德数据库  财经学子版/大奖章免费版/机构版(optional)

  ```
  [python]: https://www.python.org/downloads/	"Python"

  [nodejs]: https://nodejs.org/en/download/	"NodeJS"    

  [MongoDB]: https://www.mongodb.com/download-center   "MongoDB"

  [Wind DataBases]  (非必须)

  - 大奖章版本 免费 注册可用  日线数据质量较好 其他基本不稳定

  - 财经学子版 需要学生证认证 申请地址(http://xz.wind.com.cn/university/home/index.html)

  - 机构版  

  ```

### ​部署

  ```
  git clone https://github.com/yutiansut/quantaxis
  cd quantaxis
  npm run quantaxis
  ```
  ![一键启动](http://i2.muimg.com/567571/e897132507ad736a.png)
  
  ===  以下步骤是为了启动后台,如果你不需要这些功能,可以不安装
  
  ===  根据你的网络速度不同,安装需要一定的时间
  ```
  一键安装
  npm run install
  一键启动所有服务:
  npm run all
 
  安装后台
  npm run install-backend
  安装web
  npm run install-web
  安装client
  npm run install-client
  

  一键启动web+后台
  npm run Xweb

  一键启动Client+后台
  npm run Xclient
  
  只启动backend (后台)
  npm run backend

  只启动前端web
  npm run website

  只启动客户端Client
  npm run client
  ```

  ```
  (后台的作用主要是为了给回测提供API,同时给两个前端提供调用,如果只需要爬虫等,也不需要启动)
  [新建一个命令行窗口](启动后台)[确保localhost:3000端口是空着的]
  cd backend | npm start
  (如果不需要网站,下面的步骤可以省略)
  [再新建一个命令行窗口](启动前端网站的后台)[确保localhost:8080端口是空着的]
  cd web | npm run dev
  (如果不需要启动客户端,下面的步骤可以省略)
  [再新建一个命令行窗口](启动客户端的后台)[确保localhost:9080端口是空着的]
  cd client | npm run dev
  ```
### 适用场景

QUANTAXIS推荐在局域网内或者单机使用,适用于中小型团队的回测情景:服务器+N个客户端,客户端--AJAX请求--服务器

![适用场景](http://i2.buimg.com/567571/e2e7b31b1f9a4307.png)

### 注意

  1. windows用户还面临MongoDB的注册服务问题,百度即可
  2. Mysql在Matlab回测时会用到,到QUANTAXIS 3.9版本 会增加Matlab-MongoDB支持
  3. 其他的问题 可以开issue

## 逻辑框架|Logic

Python作为胶水语言,贯穿项目的始终.Nodejs作为后台语言,为所有语言提供Api,并作为一个任务中转

(*)Python-Celery 作为任务调度+redis

Nodejs-Express作为后端部分,提供api分发和部分的爬虫

Nodejs-Vue 作为前端,提供前端和客户端框架

Matlab 作为一个回测中心,提供快速的原型实现

R语言作为数据分析的选项,并不是一定使用

1. 爬虫部分 采用python的Scrapy+Phantomjs+selenium构架,使用redis(coookies/cache)+Mongodb(data)架构

2. 数据清洗部分 python+matlab

3. 数据库 主数据库Mysql  爬虫数据库 Mongodb  性能数据库  redis

4. 数据可视化  nodejs+vue.js+d3.js

5. 统计学部分  增加传统金融的统计学函数,以及机器学习部分的函数



## 组件|Component

### Backend/  & Data/
![前后端分离](http://i1.piimg.com/567571/41fa8b9c16122bfd.png)
QASpider 部署在linux服务器上,负责数据的爬取,包括且不限于股票日线/tick/公司信息/分析师推荐/各大财经网站信息/微信公众号信息
爬取的数据在服务器的Mongodb上,通过QUANTAXIS Storage转入 MYSQL
```
localhost:3000/stock
### /stock/history/all?code=xxx&feq=xxx
### /stock/history/time?code=xxx&start=(yyyy-mm-dd)&end=(yyyy-mm-dd)
### /stock/index/
### /stock/live?code=xxx
### /stock/quota/lhb?
### /stock/quota/lhb?

localhost:3000/backtest
### /ts?bidCode=000001&bidTime=2001-01-04&bidPrice=4.08
返回Success  则成交 返回failed 则不成交
一定要给报价
```
![回测框架](http://i1.piimg.com/567571/151a21b61f4d6d63.png)
```
localhost:3000/users
### /signup?username=xxx&password=xxx
### /login?username=xxx&password=xxx

localhost:3000/apis 
### /queryContentbyName
### /queryTitlebyName
### /queryContentbyTitle
```
### Storage/
负责  管理redis,Mongodb与MySQL的同步
      策略代码的回测API
      用户策略,文章等
### Client/ & web/
负责  数据可视化,提供交互式的策略展示
负责 后端数据API打包
![quantaxis client](http://p1.bpimg.com/567571/1faef074efcdf485.png)

### Analysis/  & Strategy/
负责  模拟交易(本地),(多语言)回测
      网上平台的模拟交易API


python,matlab,r....等通过访问url来获取数据,也可以本地缓存

```python
#coding:utf-8
import requests

code='600010'
startdate='2015-06-02'
enddate='2016-06-02'
data=requests.get("http://localhost:3000/stock/history/time?code="+str(code)+"&start="+str(startdate)+"&end="+str(enddate))
lists=data.json()
print(lists[1])
"""
expected results
PS C:\quantaxis\analysis\python> python .\example.py
['2015-06-03', '6.650', '6.650', '6.500', '6.360', '5524387.00', '-0.150', '-2.26', '6.522', '6.752', '6.584', '6,709,222.70', '6,794,033.70', '6,807,961.80', '3.51']
"""
for item in lists:
    print (item)
    print (item[0])
    """
    expected results

    ['2016-05-25', '2.840', '2.860', '2.830', '2.810', '425533.31', '0.000', '0.00', '2.866', '2.856', '2.920', '860,444.06', '873,558.26', '786,931.30', '0.27']
    2016-05-25
    ['2016-05-26', '2.810', '2.870', '2.870', '2.770', '794664.00', '0.050', '1.77', '2.856', '2.857', '2.910', '704,760.36', '886,065.95', '787,090.14', '0.50']
    2016-05-26
    ['2016-05-27', '2.850', '2.870', '2.850', '2.820', '522716.97', '-0.020', '-0.70', '2.848', '2.860', '2.901', '591,625.25', '879,393.86', '772,030.30', '0.33']
    2016-05-27
    ['2016-05-30', '2.810', '2.940', '2.850', '2.790', '1112251.75', '0.000', '0.00', '2.844', '2.859', '2.891', '674,735.42', '904,095.74', '801,551.60', '0.71']
    2016-05-30
    ['2016-05-31', '2.840', '3.080', '3.050', '2.830', '2854263.75', '0.200', '7.02', '2.890', '2.876', '2.889', '1,141,885.96', '1,042,361.24', '907,747.91', '1.81']
    2016-05-31
    ['2016-06-01', '3.010', '3.080', '3.000', '2.980', '2053142.25', '-0.050', '-1.64', '2.924', '2.895', '2.886', '1,467,407.74', '1,163,925.90', '978,492.32', '1.30']
    2016-06-01
    ['2016-06-02', '2.970', '3.020', '2.990', '2.940', '1135590.38', '0.000', '0.00', '2.948', '2.902', '2.882', '1,535,593.02', '1,120,176.69', '1,007,985.72', '0.72']
    2016-06-02
    """

```
回测的主要思想是--交易api给出是否成交的判断,其余逻辑在各自语言框架内执行
```python
trade=requests.get("http://localhost:3000/backtest/ts?bidCode=000001&bidTime=2001-01-04&bidPrice=4.08")
if (trade.text == "success"):
    # do something
else :
    # do another thing
```

Strategy 部分是一些策略,有md文件,也有对应代码.策略才是最核心的东西

### Docs/
文档部分
### Tasks/
异步任务

## 版本历史|History
```
1.0版本使用的主要是新浪网的数据。
1.5版本是在了解了对象化编程OOP以后对于平台做的改进 
2.0版本主要是对于数据源进行了更换，并重新写了数据库连接和调用函数。从2.0起，quantaxis使用wind服务商提供的量化交易数据并选择mysql作为数据存储方式。 
2.5版本则主要增加了交易内核 QUANTCORE 1.0 QC1.0还是一个静态的交易系统，成交的判断方式是以策略报价和历史成交价区间的比较进行判定。 
3.0版本将matlab的及时数据以json格式保存到状态空间或者mysql中，使用ajax技术对于mysql数据进行抽取，使用dc.js等可视化javascript将数据展示在页面上，形成交互式的数据可视化方案 
3.2 模块化编程 将class重新改包，定义功能化模块，方便调用并增加生命周期
3.5 重构版本 重新定义前后端以及数据块逻辑.
3.6 重构版本 关于SPIDER和VIUSALIZATION的重大更改,去除DATACENTER模块
3.7 合并版本 同时增加期货部分(目前只支持国内期货市场),加入R语言支持
```

## QUANTAXIS 4.0 is coming soon.....
![quantaxis 4.0 logic](http://i1.piimg.com/1949/74a05d72d94b86c3.png)

In quantaxis4.0 version, we try to merge these components back together and rebuild and redefind a completely logic.