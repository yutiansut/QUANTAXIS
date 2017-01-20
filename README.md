# QUANTAXIS 量化金融工具箱


![build](https://img.shields.io/badge/Build-passing-green.svg)
![download](https://img.shields.io/badge/Download-47~140Mb-green.svg)
![version](https://img.shields.io/badge/Version-%203.2.0%20alpha-orange.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![website](https://img.shields.io/badge/Website-%20www.yutiansut.com-lightgrey.svg)
![language](https://img.shields.io/badge/%20%20%20Language%20%20%20-%20%20%20Matlab%2FPython%2FJS%20%20-lightgrey.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
![quantaxis 3.0 beta](https://github.com/yutiansut/QUANTAXIS/blob/3.0/Picture/QUANTAXIS.jpg)



[Contact]:QQ 279336410<br>


## 写在前面

  QUANTAXIS 致力于快速策略测试,轻量化实盘部署和交互式数据分析的三者有机统一.通过有机结合MATLAB,MYSQL,Python,Javascript,NODEJS和Wind,实现一套完整的自动化量化平台.


## Content 目录

>+---++---++---++---++---++---++---++---++---+
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
* [3. QUANTAXIS 功能介绍](#3-quantaxis-功能介绍)
* &emsp;[3.1 数据获取  DF类 Data Fetch](#31-数据获取--df类-data-fetch)
* &emsp;&emsp;[3.1.1 Data Fetch 核心函数](#311-核心函数)
* &emsp;[3.2 数据存贮 DS类 Data Storage](#32-数据存贮--ds类-data-storage)
* &emsp;&emsp;[3.2.1 数据存储](#321-数据存储)
* &emsp;&emsp;[3.2.2 涉及到数据库的操作](#322-涉及到数据库的操作)
* &emsp;&emsp;[3.2.3 安装前的准备](#323-安装前的准备)
* &emsp;&emsp;[3.2.4 APIS](#324-apis)
* &emsp;[3.3 数据分析 DA类 Data Analysis](#33-数据分析--da类-data-analysis)
* &emsp;&emsp;[3.3.1 数据分析常用内置工具箱](#331-数据分析常用内置工具箱)
* &emsp;&emsp;[3.3.2 策略回测](#332-策略回测)
* &emsp;&emsp;[3.3.3 交易内核](#333-交易内核)
* &emsp;&emsp;[3.3.4 指标分析](#334-指标分析)
* &emsp;&emsp;[3.3.5 APIS](#335-apis)
* &emsp;[3.4 数据交互 DI类 Data Intergration](#34-数据交互--di类-data-intergration)
* &emsp;&emsp;[3.4.1 JSON/Matlab](#341-jsonmatlab)
* &emsp;&emsp;[3.4.2 NODEJS](#342-nodejs)
* &emsp;&emsp;[3.4.3 NODEJS/MYSQL](#343-nodejsmysql)
* &emsp;&emsp;[3.4.4 AJAX](#344-ajax)
* &emsp;&emsp;[3.4.5 dc.js](#345-dcjs)
* &emsp;&emsp;[3.4.6 APIS](#346-apis)
* &emsp;[3.5 消息存贮 SM类 System Message](#35-消息存贮--sm类-system-message)
* &emsp;&emsp;[3.5.1 MES方式](#351-mes方式)
* &emsp;&emsp;[3.5.2 APIS](#352-apis)
* [4. 版本历史](#4-版本历史)

>+---++---++---++---++---++---++---++---++---+

=========================

## 1. QUANTAXIS 简介
QUANTAXIS 使用python进行数据挖掘和自然语言处理，使用matlab进行快速回测，mysql作为数据中心，nodejs建站，使用javascript作为前端交互式展示
核心组件均可独立调用
![quantaxis 3.0 beta](https://github.com/yutiansut/QUANTAXIS/blob/3.0/Picture/QA3.0.png)

```
SYSTEM REQUIREMENTS
====================
MATLAB 2014a +    [best recommends]:MATLAB R2015b,R2016a
                  (如果使用的是2015b以下版本 将isopen语句全部替换成isconnection语句)
NODEJS 4.4 +      [best recommends]:NODEJS V5.9.1
JAVASCRIPT  JQUERY V1.4.4+
MYSQL  5.6 +      [best recommends]:MYSQL 5.7
Wind Personal API V2.0.0+
JDBC CONNECTOR  5.1.7bin +
Python 2.7.x
MongoDB 
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
Copy-Item ('D:\QUANTAXIS\QUANTAXIS\Auxiliary\JDBC\mysql-connector-java-5.1.7-bin.jar')  ('C:\Program Files\MATLAB\R2016a\java\jar\toolbox')



```

![quantaxis datacenter](https://github.com/yutiansut/QUANTAXIS/blob/3.0/Picture/QADC.gif)

## 2. QUANTAXIS 特性
通过[V2.0](https://github.com/yutiansut/QUANTAXIS/tree/v2.0),[V3.0](https://github.com/yutiansut/QUANTAXIS/tree/v3.0)和[V3.2.0](https://github.com/yutiansut/QUANTAXIS/tree/v3.0) 3个版本的升级以后，QUANTAXIS逐步发展成一个代码模块化和数据交互可视化的量化工具系统。
### 2.1 QUANTAXIS 模块化编程
QUANTAXIS致力于代码的功能分离和生命周期延长。在quantaxis中，所有的代码都被分成了不同的功能模块，通过类包(class package)的从属调用，来定义不同的功能块。
类的模板与继承如下
```
类 TESTQUANTAXIS 的属性:

    w
    FET
    MES
    ID
    ING
    MYSQL


类 TESTQUANTAXIS 的事件:

    DFwindhistory
    QAMessage
    ObjectBeingDestroyed
    mysqlexec


ans = 

    'w  % Inherited from DataFetch.Methods.DFWind'
    'FET  % Inherited from DataFetch.Methods.Core.DFCore'
    'MES  % Inherited from Message.QMMes'
    'ID  % Inherited from Message.QMMes'
    'ING  % Inherited from DataIntegration.DINodeJS'
    'MYSQL  % Inherited from DataStorage.DSMysql'
```
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
```
cd quantaxis
node datacenter/bin/www.js
```
打开浏览器 默认端口是3030
#### 2.2.3 后台管理，中间件，路由跳转，mysql连接，AJAX等
DataCenter/mysql --- 数据库组件
--conn.js 数据库连接函数
--sqlmapping.js 数据库脚本
--sqlexec.js  数据库执行

DataCenter/routes  --- 路由跳转组件
--index.js 主路由
data.js user.js 都可以在DataCenter/app.js中重新定义


#### 2.2.4 前端脚本
DataCenter/views  --jade页面文件
DataCenter/public  --资源文件  css样表，javascript，图片等等

## 3. QUANTAXIS 功能介绍

### 3.1 数据获取  DF类 Data Fetch
传送门--[关于Data Fetch 类](https://github.com/yutiansut/QUANTAXIS/blob/master/%2BDataFetch/README.md)
#### 3.1.1 核心函数
>[DataFetch]<br>DFMain.m (类包函数，同时兼具初始化的任务)
>>[+Methods]工具函数<br> DFSina.m (新浪接口)<br> DFTushare.m (Python tushare接口)<br> DFWind.m (Wind 接口)<br> DFYahoo.m (Yahoo 接口)
>>>[+Core]<br> DFCore.m (核心包函数，指定该类的属性 FET 以及消息响应控制 MES族)

#### 3.1.2 调用方式：
```
classdef QAClassPackage< DataFetch.DFMain 
end

classdef QUANTAXIS < QAClassPackage
end
```
#### 3.1.3 APIS
所有被获取到的数据都在QA.FET族中<br>
如果从wind获取数据，数据在QA.FET.Data中<br>
具体参见 [关于Data Fetch 类](https://github.com/yutiansut/QUANTAXIS/blob/master/%2BDataFetch/README.md)

### 3.2 数据存贮  DS类 Data Storage
传送门--[关于DataStorage 类](https://github.com/yutiansut/QUANTAXIS/blob/master/%2BDataStorage/README.md)
#### 3.2.1 数据存储
我们在考虑和比较了各种数据存储的方便性易用度以后，选择了使用MySQL作为QUANTAXIS的数据库。
如果需要，也可以自行开发SQLSERVER, MongoDB, db2, Oracle等等。
#### 3.2.2 涉及到数据库的操作
QA.Fetch
数据获取
数据更新<br>
![](https://github.com/yutiansut/QUANTAXIS/blob/master/Picture/DatabaseUpdate.png)
#### 3.2.3 安装前的准备
> Attention
1.将quantaxis/auxiliary/JDBC中的jar文件复制到  .\MATLAB\R2015a\java\jar\toolbox
2.打开C:\Program Files\MATLAB\MATLAB Production Server\R2015a\toolbox\local下的classpath.txt文件，在最末加入
$matlabroot/java/jar/toolbox/mysql-connector-java-5.1.7-bin.jar

如果不添加JDBC数据库，matlab会报错：
“未定义与 'struct' 类型的输入参数相对应的函数 'fetch'。

#### 3.2.4 APIS

### 3.3 数据分析  DA类 Data Analysis
#### 3.3.1 数据分析常用内置工具箱
#### 3.3.2 策略回测
QUANTAXIS提供了一种快速的回测方式，通过简单的价格判断来形成对于策略报价的成交判断。
![data](https://github.com/yutiansut/QUANTAXIS/blob/master/Picture/DAExample.png)
回测后的数据会自动以策略的形式存入mysql
![](https://github.com/yutiansut/QUANTAXIS/blob/master/Picture/StrategyMysql.png)
#### 3.3.3 交易内核
#### 3.3.4 指标分析
ROC曲线分析
盈利分析
#### 3.3.5 APIS
### 3.4 数据交互  DI类 Data Intergration
#### 3.4.1 JSON/Matlab
将matlab转化为JSON

#### 3.4.2 NODEJS
#### 3.4.3 数据库(主数据库和缓存数据库)
数据展示,用户策略等数据存在MYSQL数据库中, 使用felixge/node-mysql的 sql 接口进行传值与数据交互
#### 3.4.4 AJAX
#### 3.4.5 dc.js
#### 3.4.6 APIS
### 3.5 消息存贮  SM类 System Message
#### 3.5.1 MES方式
在程序中，我们设置了监听及系统日志，如果需要查看记录的消息，可以点击当前类下的
MES类
在MES.History中，你可以看到记录的消息日志

如果需要另外响应消息，请参见3.5.2的APIS
#### 3.5.2 APIS

```
# 首先加入MES类包
classdef QA < Message.QMMes
end

QA.MES.Str='';
notify(QA,'QAMessage')

```

## 4. [版本历史](https://github.com/yutiansut/QUANTAXIS/releases)


1.0版本使用的主要是新浪网的数据。<br>1.5版本是在了解了对象化编程OOP以后对于平台做的改进
<br>2.0版本主要是对于数据源进行了更换，并重新写了数据库连接和调用函数。从2.0起，quantaxis使用wind服务商提供的量化交易数据并选择mysql作为数据存储方式。
<br>2.5版本则主要增加了交易内核 QUANTCORE 1.0 QC1.0还是一个静态的交易系统，成交的判断方式是以策略报价和历史成交价区间的比较进行判定。
<br>3.0版本将matlab的及时数据以json格式保存到状态空间或者mysql中，使用ajax技术对于mysql数据进行抽取，使用dc.js等可视化javascript将数据展示在页面上，形成交互式的数据可视化方案
<br>3.2 模块化编程 将class重新改包，定义功能化模块，方便调用并增加生命周期




## [QUANTAXIS](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXIS.m)
调用类 classdef [xx] < QUANTAXIS
----
主函数 主要是一个量化平台，负责策略实现和数据更新
类似的平台 如python下的[easytrader](https://github.com/shidenggui/easytrader)

