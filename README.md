# QUANTAXIS 量化金融策略框架


[![Github workers](https://img.shields.io/github/watchers/yutiansut/quantaxis.svg?style=social&label=Watchers&)](https://github.com/yutiansut/quantaxis/watchers)
[![GitHub stars](https://img.shields.io/github/stars/yutiansut/quantaxis.svg?style=social&label=Star&)](https://github.com/yutiansut/quantaxis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yutiansut/quantaxis.svg?style=social&label=Fork&)](https://github.com/yutiansut/quantaxis/fork)

[点击右上角Star和Watch来跟踪项目进展! 点击Fork来创建属于你的QUANTAXIS!]

![main_1](http://osnhakmay.bkt.clouddn.com/Main_1.gif)
<img src="http://osnhakmay.bkt.clouddn.com/QUANTAXIS-white.png" width = "27.5%" />



![version](https://img.shields.io/badge/Version-%200.5.28-orange.svg)
![build](https://travis-ci.org/yutiansut/QUANTAXIS.svg?branch=master)
[![Stories in Ready](https://badge.waffle.io/yutiansut/QUANTAXIS.svg?label=ready&title=Ready)](http://waffle.io/yutiansut/QUANTAXIS)
[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/yutiansut/quantaxis)
![QAS](https://img.shields.io/badge/QAS-%200.0.8-brown.svg)
![Pypi](https://img.shields.io/badge/Pypi-%200.5.28-blue.svg)
![python](https://img.shields.io/badge/python-%203.6/3.5/3.4/win/ubuntu-darkgrey.svg)
![Npm](https://img.shields.io/badge/Npm-%200.4.0-yellow.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)


> 欢迎加群讨论: [群链接](https://jq.qq.com/?_wv=1027&k=4CEKGzn) 

QUANTAXIS量化金融策略框架,是一个面向中小型策略团队的量化分析解决方案. 我们通过高度解耦的模块化以及标准化协议,可以快速的实现面向场景的定制化解决方案.QUANTAXIS是一个渐进式的开放式框架,你可以根据自己的需要,引入自己的数据,分析方案,可视化过程等,也可以通过RESTful接口,快速实现多人局域网/广域网内的协作.

<!-- TOC -->

- [QUANTAXIS 量化金融策略框架](#quantaxis-量化金融策略框架)
    - [功能](#功能)
    - [安装和部署](#安装和部署)
    - [更新](#更新)
    - [Docker](#docker)
    - [使用说明](#使用说明)
    - [Jupyter示例](#jupyter示例)
    - [常见问题FAQ](#常见问题faq)
    - [项目捐赠](#项目捐赠)
    - [回测Webkit插件概览](#回测webkit插件概览)
    - [QUANTAXIS 标准化协议和未来协议](#quantaxis-标准化协议和未来协议)

<!-- /TOC -->




## 功能
======

![](http://i1.piimg.com/567571/dc3c811a5afcb4fb.png)

已经实现：

- 日线（自1990年）回测 [定点复权] (T+1)
- 分钟线 [1min/5min/15min/30min/60min]回测 (T+1)
- 股指期货日线(T+0)/指数日线/ETF日线
- 股指期货分钟线(T+0) / 指数分钟线/ETF分钟线 [1min/5min/15min/30min/60min]
- 期货日线/分钟线(期货指数/期货主连/期货合约)
- 基于[pytdx](https://github.com/rainx/pytdx)各种爬虫的数据源 
- 实时交易数据,实时tick
- 基于Vue.js的前端网站
- 自定义的数据结构QADataStruct
- 指标计算QAIndicator
- 板块数据(0.5.1新增)/同花顺,通达信板块
- 基本面数据(部分 最新一期财务报表)
- 行情分发
- 循环回测
- 回测管理优化(新增回测主题/版本号)


预计实现:

- 文档更新
- 期货回测
- 实盘
- 分析模块(行情分析/板块分析)

- 成交记录分析器

```
[注意: tushare最新版本因为单方面直接复制了pytdx  所以导致和最新版本的pytdx不兼容 如有安装0.8.7版本以上的tushare 请降级使用]

*** 降级时需注意: 直接pip uninstall tushare以后 还要去删掉tushare安装目录下的pytdx 再重新安装最新版本的pytdx ***

```



## 安装和部署
参见 [安装说明](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXISProtocol/install.md)

## 更新
参见 [更新说明](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXISProtocol/update.md)

## Docker
参见 [Docker](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXISProtocol/docker.md)
## 使用说明
参见 [使用说明](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXISProtocol/instruction.md)

## Jupyter示例
参见 [Jupyter示例](https://github.com/yutiansut/QUANTAXIS/tree/master/jupyterexample)

## 常见问题FAQ
参见 [FAQ](https://github.com/yutiansut/QUANTAXIS/tree/master/QUANTAXISProtocol/FAQ.md)

## 项目捐赠

写代码不易...请作者喝杯咖啡呗?

<img src="http://osnhakmay.bkt.clouddn.com/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20170923132018.jpg" width = "27.5%" />

(PS: 支付的时候 请带上你的名字/昵称呀 会维护一个赞助列表~ )

[捐赠列表](https://github.com/yutiansut/QUANTAXIS/blob/master/sponsorship.md)



## 回测Webkit插件概览

![](http://i2.muimg.com/567571/736ba4adda9fac85.png)
![](http://i2.muimg.com/588926/345e924a45cae6e5.png)
![](http://i1.piimg.com/1949/7b6e2fc347220f7b.png)
![](http://osnhakmay.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20171204183938.png)
![](http://i1.piimg.com/567571/09bd05c3698f2d38.png)
![](http://i1.piimg.com/567571/053ac3e3850f8f60.png)
![](http://osnhakmay.bkt.clouddn.com/quantaxis%20markdown.gif)


## QUANTAXIS 标准化协议和未来协议


QUANTAXIS-Stardand-Protocol 版本号0.0.8

详情参见  [QUANATXISProtocol](https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXISProtocol/readme.md)
