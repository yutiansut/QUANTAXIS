# QUANTAXIS 量化金融工具箱
<style type="text/css"> 

</style>
![build](https://img.shields.io/badge/Build-passing-green.svg)
![download](https://img.shields.io/badge/Download-47~140Mb-green.svg)
![version](https://img.shields.io/badge/Version-%203.2.0%20alpha-orange.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![website](https://img.shields.io/badge/Website-%20www.yutiansut.com-lightgrey.svg)
![language](https://img.shields.io/badge/%20%20%20Language%20%20%20-%20%20%20Matlab%2FPython%2FJS%20%20-lightgrey.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)

![quantaxis 3.0 beta](https://github.com/yutiansut/QUANTAXIS/blob/3.0/Picture/QUANTAXIS.jpg)


[Website]:www.yutiansut.com | http://quantaxis.yutiansut.com<br>
[Contact]:QQ 279336410<br>

## Content

>+---++---++---++---++---++---+
* [1.QUANTAXIS 简介](https://github.com/yutiansut/QUANTAXIS#1-quantaxis-简介)
* [2. QUANTAXIS 特性](#2-quantaxis-特性)
* &emsp;[2.1 QUANTAXIS 模块化编程](#21-quantaxis-模块化编程)
* &emsp;&emsp;[2.1.1 QUANTAXIS 模块命名规则](#211-quantaxis-模块命名规则)
* &emsp;&emsp;[2.1.2 QUANTAXIS 模块调用](#212-quantaxis-模块调用)
* &emsp;[2.2 QUANTAXIS 数据可视化](#22-quantaxis-数据可视化)
* &emsp;&emsp;[2.2.1 数据可视化方法](#221-数据可视化方法)
* &emsp;&emsp;[2.2.2 运行NODEJS服务](#222-运行NODEJS服务)
* &emsp;&emsp;[2.2.3 后台管理，中间件，路由跳转，mysql连接，AJAX等](#223-后台管理中间件路由跳转mysql连接ajax等)
* &emsp;&emsp;[2.2.4 前端脚本](#224-前端脚本)

>+---++---++---++---++---++---+

=========================

## 1. QUANTAXIS 简介
QUANTAXIS 使用模块化对象化编程，使用matlab进行快速回测，mysql作为数据中心，nodejs建站，使用javascript作为前端交互式展示
核心组件均可独立调用

```
SYSTEM REQUIREMENTS
====================
MATLAB 2014a +    [best recommends]:MATLAB R2015b,R2016a
NODEJS 4.4 +      [best recommends]:NODEJS V5.9.1
JAVASCRIPT  JQUERY V1.4.4+
MYSQL  5.6 +      [best recommends]:MYSQL 5.7
Wind Personal API V2.0.0+
JDBC CONNECTOR  5.1.7bin +
```
快速搭建一个QUANTAXIS实例(todo list: shell语言自动部署)
```
win+R--cmd/powershell
cd D:
mkdir quantaxis
cd quantaxis
git clone https://github.com/yutiansut/quantaxis
····waiting····

cd quantaxis  (if powershell)
Copy-Item ('F:\QUANTAXIS\QUANTAXIS\Auxiliary\JDBC\mysql-connector-java-5.1.7-bin.jar')  ('C:\Program Files\MATLAB\R2016a\java\jar\toolbox')



```
## 2. QUANTAXIS 特性
通过[V2.0](https://github.com/yutiansut/QUANTAXIS/tree/v2.0),[V3.0](https://github.com/yutiansut/QUANTAXIS/tree/v3.0)和[V3.2.0](https://github.com/yutiansut/QUANTAXIS/tree/v3.0) 3个版本的升级以后，QUANTAXIS逐步发展成一个代码模块化和数据交互可视化的量化工具系统。
### 2.1 QUANTAXIS 模块化编程
QUANTAXIS致力于代码的功能分离和生命周期延长。在quantaxis中，所有的代码都被分成了不同的功能模块，通过类包(class package)的从属调用，来定义不同的功能块。

#### 2.1.1 QUANTAXIS 模块命名规则

1. 模块的命名
模块的命名首先考虑母目录
如
>+DataStorage<br>
 ++DSMysql.m
首先采用母目录的两个英文大写缩写 如DataStorage--DS，再加上本身代码名称。

2. 函数的命名
而对于模块内的函数命名，考虑到不同函数的重叠问题，主要以模块名+函数名,如
>DSMysqlInit();<br>
>DSMysqlCreateTable();

3. 类属性的命名
类属性的命名需要对比给出的api中已有类属性后进行确定

#### 2.1.2 QUANTAXIS 模块调用
对于类模块的调用，我们需要首先编辑类模块
```
>QAClassPackage.m
classdef QAClassPackage < DataFetch.DFWind & DataStorage.DSMysql & FreeMarkets.MultiDealer.FreeMarkets & Strategy.STBase
end
% 在一个classpackage中写好从属类，然后让quantaxis映射过去

>QUANTAXIS.m
classdef QUANTAXIS < QAClassPackage
end
```
当我们需要什么功能的时候，就调用什么功能模块即可。

### 2.2 QUANTAXIS 数据可视化
#### 2.2.1 数据可视化方法
虽然matlab中也能够画图，如plot(); histfit();等等，但是图片不够美观，且不能交互式的动态展示，于是我们将
#### 2.2.2 运行NODEJS服务
#### 2.2.3 后台管理，中间件，路由跳转，mysql连接，AJAX等
#### 2.2.4 前端脚本





























## 更新日志 QA3.2  模块化编程
----
将class重新改包，定义功能化模块，方便调用并增加生命周期



## 更新日志 QA3.0  新增数据中心 [DATACENTER 主要负责数据可视化](https://github.com/yutiansut/QUANTAXIS/blob/master/DataCenter/readme.md)
----
将matlab的及时数据以json格式保存到状态空间或者mysql中

使用ajax技术对于mysql数据进行抽取，使用dc.js等可视化javascript将数据展示在页面上，形成交互式的数据可视化方案

![quantaxis 3.0 beta](https://github.com/yutiansut/QUANTAXIS/blob/3.0/Picture/QA3.0.png)

![quantaxis datacenter](https://github.com/yutiansut/QUANTAXIS/blob/3.0/Picture/QADC.gif)

----
>QUANTAXIS本身是作者在大四时，学习量化交易以及策略实现的时候，发现matlab上面并没有称心如意的量化平台，而主流的量化平台则基于python和java，于是萌生了自己写一个量化工具箱的想法

## [Version History](https://github.com/yutiansut/QUANTAXIS/releases)
1.0版本使用的主要是新浪网的数据。<br>1.5版本是在了解了对象化编程OOP以后对于平台做的改进
<br>2.0版本主要是对于数据源进行了更换，并重新写了数据库连接和调用函数。从2.0起，quantaxis使用wind服务商提供的量化交易数据并选择mysql作为数据存储方式。
<br>2.5版本则主要增加了交易内核 QUANTCORE 1.0 QC1.0还是一个静态的交易系统，成交的判断方式是以策略报价和历史成交价区间的比较进行判定。


```
[Attention]:QUANTAXIS在使用之前需要安装Wind大奖章免费应用 以及 Mysql 5.6以上版本+JDBC-MYSQL的数据库
以上两个的安装文件都在QUANTAXIS/Auxiliary中 clone到本地后打开link.md下载安装即可

JDBC添加完成后需要在Classpath文件中增加

>  $matlabroot/java/jar/toolbox/mysql-connector-java-5.1.7-bin.jar

```
## [QUANTAXIS](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXIS.m)
调用类 classdef [xx] < QUANTAXIS
----
主函数 主要是一个量化平台，负责策略实现和数据更新
类似的平台 如python下的[easytrader](https://github.com/shidenggui/easytrader)
```
QA=QUANTAXIS;
QA.Init()   初始化平台（数据库连接设置等）
QA.Fetch()  数据更新平台
QA.Start()  策略回测平台
```

## [QUANTAXIS FREEMARKETS](https://github.com/yutiansut/QUANTAXIS/blob/master/%2BFreeMarkets/%2BMultiDealer/FreeMarkets.m)
调用类 classdef [xx] < FreeMarkets.MultiDealer.FreeMarkets
----
```
FM=FreeMarkets;
FM.Try();  一个随机策略的金融市场
>数据将在FM.Price.History 中呈现
>FM.BidPool中是报价池

```


<big>关于quantaxis-FreeMarkets</big>
### 动态匹配交易池系统和自衍生随机策略系统

-------

主要考虑的问题在于这个是一个闭环的复合机制

首先 价格会导致市场上所有的交易者的预期改变，交易者的预期改变会改变他们的报价
他们的报价改变会影响成交价和成交量

而成交价和量的改变会进一步形成新的市场价格进行下一个循环


使用id去控制每一步 或者说过程的每一步

-------
>循环

询价阶段
按照round
每一个[Memeber]进行报价,以一个对象的形式按包表达出来 
结构是  Strategy-BID[id]-Price-Amount
并回调给系统

系统会以这种形式接收
[Price-Amount-Date-Varities-StrategyID-SystemTime] 并记录到[FM.BidPool.Board]中

系统在记录了报价单并形成报价池之后，会进行下一步的回调

将报价单中的数据交给一个交易函数  并形成价格
`````
notify(FM,'transaction')
`````

FM.transaction 函数对于报价池中的报价按量进行对冲并形成价格


>>To Do List
需要对于撤单以及相关的功能进一步完善

几个函数的主要功能

### FM.TSBoard 价格形成函数

得到回调的价格并记录相关
改变当前系统价格


### FM.REPLY 客户端策略函数

不同的策略会根据价格的变化改变预期（报价），并将修改后的报价提交给系统
round控制

### FM.ASK 询价函数

系统根据用户的不同的报价，记录到报价池并动态匹配报价和量
如果出现可以对冲的报价就进行对冲并回调价格


## [QUANTAXIS-TEST 函数接口测试](https://github.com/yutiansut/QUANTAXIS/blob/master/TestMarkets.m)
测试类
```
TM=TestMarkets;  %初始化测试
```
集成类以后可以使用继承类的接口，同时，在使用了包package以后，不能直接调用FreeMarkets.m的函数