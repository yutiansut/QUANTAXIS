# QUANTAXIS 量化金融策略框架



[![Github workers](https://img.shields.io/github/watchers/yutiansut/quantaxis.svg?style=social&label=Watchers&)](https://github.com/yutiansut/quantaxis/watchers)
[![GitHub stars](https://img.shields.io/github/stars/yutiansut/quantaxis.svg?style=social&label=Star&)](https://github.com/yutiansut/quantaxis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yutiansut/quantaxis.svg?style=social&label=Fork&)](https://github.com/yutiansut/quantaxis/fork)

[点击右上角Star和Watch来跟踪项目进展! 点击Fork来创建属于你的QUANTAXIS!]

![post201802](http://osnhakmay.bkt.clouddn.com/quantaxis-post201802.png)
![main_1](http://osnhakmay.bkt.clouddn.com/Main_1.gif)
![logo](http://osnhakmay.bkt.clouddn.com/QUANTAXIS-small.png)
![presentbyyutiansut](http://osnhakmay.bkt.clouddn.com/yutiansut-logo.png)


![version](https://img.shields.io/badge/Version-%201.0.12-orange.svg)
![build](https://travis-ci.org/QUANTAXIS/QUANTAXIS.svg?branch=master)
[![Codefresh build status]( https://g.codefresh.io/api/badges/build?repoOwner=yutiansut&repoName=QUANTAXIS&branch=master&pipelineName=QUANTAXIS&accountName=yutiansut_marketplace&type=cf-1)]( https://g.codefresh.io/repositories/yutiansut/QUANTAXIS/builds?filter=trigger:build;branch:master;service:5a30c1026e9d6c0001c5143b~QUANTAXIS)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d8504e4af33747bb8117579212425af9)](https://www.codacy.com/app/yutiansut/QUANTAXIS?utm_source=github.com&utm_medium=referral&utm_content=yutiansut/QUANTAXIS&utm_campaign=badger)
[![Stories in Ready](https://badge.waffle.io/yutiansut/QUANTAXIS.svg?label=ready&title=Ready)](http://waffle.io/yutiansut/QUANTAXIS)
[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/yutiansut/quantaxis)
![QAS](https://img.shields.io/badge/QAS-%200.0.8-brown.svg)
![Pypi](https://img.shields.io/badge/Pypi-%201.0.12-blue.svg)
![python](https://img.shields.io/badge/python-%203.6/3.5/3.4/win/ubuntu-darkgrey.svg)
![Npm](https://img.shields.io/badge/Npm-%200.4.0-yellow.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)


----------

![happynewyear](http://osnhakmay.bkt.clouddn.com/quantaxishappynewyear.png)

新年寄语:

QUANTAXIS 祝大家在2018年 新年大吉 ~

主要还是要注意身体 (^-^)

@yutiansut 2018/2/16


---


> 欢迎加群讨论: [群链接](https://jq.qq.com/?_wv=1027&k=4CEKGzn) 

QUANTAXIS量化金融策略框架,是一个面向中小型策略团队的量化分析解决方案. 我们通过高度解耦的模块化以及标准化协议,可以快速的实现面向场景的定制化解决方案.QUANTAXIS是一个渐进式的开放式框架,你可以根据自己的需要,引入自己的数据,分析方案,可视化过程等,也可以通过RESTful接口,快速实现多人局域网/广域网内的协作.

<!-- vscode-markdown-toc -->
* 1. [功能](#)
* 2. [文档](#-1)
* 3. [安装和部署](#-1)
* 4. [更新](#-1)
* 5. [Docker](#Docker)
* 6. [使用说明](#-1)
* 7. [Jupyter示例](#Jupyter)
* 8. [常见问题FAQ](#FAQ)
* 9. [项目捐赠](#-1)
* 10. [回测Webkit插件概览](#Webkit)
* 11. [QUANTAXIS 标准化协议和未来协议](#QUANTAXIS)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->



##  1. <a name=''></a>功能
======

![](http://osnhakmay.bkt.clouddn.com/framework.png)

已经实现：

- [x] 日线（自1990年）回测 [定点复权] (T+1)
- [x] 分钟线 [1min/5min/15min/30min/60min]回测 (T+1)
- [x] 股指期货日线(T+0)/指数日线/ETF日线
- [x] 股指期货分钟线(T+0) / 指数分钟线/ETF分钟线 [1min/5min/15min/30min/60min]
- [x] 期货日线/分钟线(期货指数/期货主连/期货合约)
- [x] 基于[pytdx](https://github.com/rainx/pytdx)/[tushare](https://github.com/waditu/tushare)以及各种爬虫的数据源 
- [x] 实时交易数据,实时tick
- [x] 基于Vue.js的前端网站
- [x] 自定义的数据结构QADataStruct
- [x] 指标计算QAIndicator
- [x] 板块数据(0.5.1新增)/同花顺,通达信板块
- [x] 基本面数据(部分 最新一期财务报表)
- [x] 行情分发
- [x] 循环回测
- [x] 回测管理优化(新增回测主题/版本号)


预计实现:

- [ ] 文档更新
- [ ] 期货回测
- [ ] 实盘
- [ ] 分析模块(行情分析/板块分析)

- [ ] 成交记录分析器

- [QUANTAXIS 2018开发计划表](job_list.md)


##  2. <a name='-1'></a>文档

文档参见: [book](http://book.yutiansut.com)

下载文档手册 

[PDF](https://www.gitbook.com/download/pdf/book/quantaxis/quantaxis) | [MOBI](https://www.gitbook.com/download/mobi/book/quantaxis/quantaxis) | [EPUB](https://www.gitbook.com/download/epub/book/quantaxis/quantaxis)

##  3. <a name='-1'></a>安装和部署

```
git clone https://github.com/yutiansut/quantaxis --depth 1
```

参见 [安装说明](Documents/install.md)

##  4. <a name='-1'></a>更新
参见 [更新说明](Documents/update.md)

##  5. <a name='Docker'></a>Docker
参见 [Docker](Documents/docker.md)
##  6. <a name='-1'></a>使用说明
参见 

* [QUANTAXIS回测API](Documents/backtest_api.md)
* [QUANTAXIS的数据结构](Documents/DataStruct.md)
* [QUANTAXIS指标系统](Documents/indicators.md)
* [QUANTAXIS的数据获取指南](Documents/DataFetch.md)
* [QUANTAXIS行情研究](Documents/analysis.md)
* [QUANTAXIS回测分析](Documents/backtestanalysis.md)
* [常见策略整理](Documents/strategy.md)

##  7. <a name='Jupyter'></a>Jupyter示例
参见 [Jupyter示例](jupyterexample)

##  8. <a name='FAQ'></a>常见问题FAQ
参见 [FAQ](Documents/FAQ.md)

##  9. <a name='-1'></a>项目捐赠

写代码不易...请作者喝杯咖啡呗?


![](http://osnhakmay.bkt.clouddn.com/alipay.png)

(PS: 支付的时候 请带上你的名字/昵称呀 会维护一个赞助列表~ )

[捐赠列表](CONTRIBUTING.md)



##  10. <a name='Webkit'></a>回测Webkit插件概览

![](http://osnhakmay.bkt.clouddn.com/homepage.png)
![](http://osnhakmay.bkt.clouddn.com/loginpage.png)
![](http://osnhakmay.bkt.clouddn.com/adminpage.png)
![](http://osnhakmay.bkt.clouddn.com/backtestpage.png)
![](http://osnhakmay.bkt.clouddn.com/rebacktest.png)
![](http://osnhakmay.bkt.clouddn.com/backtestpic.png)
![](http://osnhakmay.bkt.clouddn.com/strategy.png)
![](http://osnhakmay.bkt.clouddn.com/kline.png)
![](http://osnhakmay.bkt.clouddn.com/settings.png)


##  11. <a name='QUANTAXIS'></a>QUANTAXIS 标准化协议和未来协议


QUANTAXIS-Stardand-Protocol 版本号0.0.8

详情参见  [QUANATXISProtocol](Documents/readme.md)
