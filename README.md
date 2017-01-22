# QUANTAXIS 量化金融工具箱


![build](https://img.shields.io/badge/Build-passing-green.svg)
![version](https://img.shields.io/badge/Version-%203.5.0%20alpha-orange.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![website](https://img.shields.io/badge/Website-%20www.yutiansut.com-grey.svg)
![language](https://img.shields.io/badge/%20%20%20Language%20%20%20-%20%20%20Matlab%2FPython%2FJS%20%20-lightgrey.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
 


## 重新定义的量化金融工具箱

```
考虑的核心有三个
1. 部署,运行的 易用性,鲁棒性,稳健性
2. 运行速度与效率
3. 数据来源的多样性
```

纵观QA3.0系列,核心使命是matlab的平台下的快速回测和数据可视化,作为对于QA2.0的改进,对象化编程无疑让事件响应和调用效率大大提升,而3.2开始的数据可视化和交互系列,让数据的表达能力更加的多样化.
然而3.0最大的问题在于,matlab的linux部署问题,对于内存的大量消耗,以及matlab对于并行运算的低支持度.同时,对于matlab而言,不同版本号之间大量更换的函数名称使得程序的bug出现的猝不及防.

一个量化工具箱需要更多的考虑到程序的易用性,程序的快速部署和最佳性价比的效率优化.我开始的对于整个量化金融工具箱的逻辑重构和代码优化.

1.爬虫部分 采用python的Scrapy+Phantomjs+selenium构架,使用redis(coookies/cache)+Mongodb(data)架构
2.数据清洗部分 python+matlab
3.数据库 主数据库Mysql  爬虫数据库 Mongodb  性能数据库  redis
4.数据可视化  nodejs+vue.js+d3.js
5.统计学部分  增加传统金融的统计学函数,以及机器学习部分的函数

V3.5是一个重构版本,会有很多混乱的部分和逻辑需要重新梳理,3.5版本后应该会发布pre4.0
同时 DATACENTER数据可视化中心 在3.5中被单独抽出来,作为可视化组件单独成立,负责对于爬虫的数据可视化和量化策略和业绩的可视化部门


QUANTAXIS 将在3.5.x 系列中被拆分成
```
QUANTAXIS                       using matlab/python
QUANTAXIS SPIDER                using python/javascript
QUANTAXIS STORAGE               using poweshell/bash
QUANTAXIS DATACENTER            using nodejs/vue.js/dc.js/d3.js
QUANTAXIS TEST                  using matlab/grunt/Phantomjs
QUANTAXIS TRADE                 using matlab/python
```
QA4.0 会将这几部分重新打包


## 逻辑框架

### QUANTAXIS.SPIDER
QASpider 部署在linux服务器上,负责数据的爬取,包括且不限于股票日线/tick/公司信息/分析师推荐/各大财经网站信息/微信公众号信息
爬取的数据在服务器的Mongodb上,通过QUANTAXIS Storage转入 MYSQL
### QUANTAXIS.STORAGE
负责  管理redis,Mongodb与MySQL的同步
      策略代码的回测API
      用户策略,文章等
### QUANTAXIS.DATACENTER
负责  数据可视化,提供交互式的策略展示

### QUANTAXIS.TEST
负责  部署测试
      压力测试
      策略性能测试
### QUANTAXIS.TRADE
负责  模拟交易(本地)
      网上平台的模拟交易API


