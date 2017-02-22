# QUANTAXIS 量化金融工具箱



![version](https://img.shields.io/badge/Version-%203.7.0-orange.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
 



Python作为胶水语言,贯穿项目的始终.

Python-Celery 作为任务调度+redis

Nodejs-Express作为后端部分,提供api分发和部分的爬虫

Nodejs-Vue 作为前端,提供前端和客户端框架

Matlab 作为一个回测中心,提供快速的原型实现


1.爬虫部分 采用python的Scrapy+Phantomjs+selenium构架,使用redis(coookies/cache)+Mongodb(data)架构
2.数据清洗部分 python+matlab
3.数据库 主数据库Mysql  爬虫数据库 Mongodb  性能数据库  redis
4.数据可视化  nodejs+vue.js+d3.js
5.统计学部分  增加传统金融的统计学函数,以及机器学习部分的函数



## 逻辑框架

### Backend/  & Data/
QASpider 部署在linux服务器上,负责数据的爬取,包括且不限于股票日线/tick/公司信息/分析师推荐/各大财经网站信息/微信公众号信息
爬取的数据在服务器的Mongodb上,通过QUANTAXIS Storage转入 MYSQL
### Storage/
负责  管理redis,Mongodb与MySQL的同步
      策略代码的回测API
      用户策略,文章等
### Client/ & web/
负责  数据可视化,提供交互式的策略展示
负责 后端数据API打包
### Test/
负责  部署测试
      压力测试
      策略性能测试
### Analysis/  & Strategy/
负责  模拟交易(本地)
      网上平台的模拟交易API
### Docs/
文档部分
### Tasks/
异步任务

## 版本历史
```
1.0版本使用的主要是新浪网的数据。
1.5版本是在了解了对象化编程OOP以后对于平台做的改进 
2.0版本主要是对于数据源进行了更换，并重新写了数据库连接和调用函数。从2.0起，quantaxis使用wind服务商提供的量化交易数据并选择mysql作为数据存储方式。 
2.5版本则主要增加了交易内核 QUANTCORE 1.0 QC1.0还是一个静态的交易系统，成交的判断方式是以策略报价和历史成交价区间的比较进行判定。 
3.0版本将matlab的及时数据以json格式保存到状态空间或者mysql中，使用ajax技术对于mysql数据进行抽取，使用dc.js等可视化javascript将数据展示在页面上，形成交互式的数据可视化方案 
3.2 模块化编程 将class重新改包，定义功能化模块，方便调用并增加生命周期
3.5 重构版本 重新定义前后端以及数据块逻辑.
3.6 重构版本 关于SPIDER和VIUSALIZATION的重大更改,去除DATACENTER模块
3.7 合并版本
```

## QUANTAXIS 4.0 is coming soon.....
![quantaxis 4.0 logic](https://github.com/yutiansut/QUANTAXIS/blob/V3.6/docs/pics/QA4.0.png)

In quantaxis4.0 version, we try to merge these components back together and rebuild and redefind a completely logic.