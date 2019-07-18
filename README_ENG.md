# QUANTAXIS Quantitative Financial Framework



[![Github workers](https://img.shields.io/github/watchers/quantaxis/quantaxis.svg?style=social&label=Watchers&)](https://github.com/quantaxis/quantaxis/watchers)
[![GitHub stars](https://img.shields.io/github/stars/quantaxis/quantaxis.svg?style=social&label=Star&)](https://github.com/quantaxis/quantaxis/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/quantaxis/quantaxis.svg?style=social&label=Fork&)](https://github.com/quantaxis/quantaxis/fork)


[Click on Star and Watch in the upper right corner to track project progress! Click on Fork to create your own QUANTAXIS!]

![post201802](http://pic.yutiansut.com/quantaxis-post201802.png)
![main_1](http://pic.yutiansut.com/Main_1.gif)
![logo](http://pic.yutiansut.com/QUANTAXIS-small.png)
![presentbyyutiansut](http://pic.yutiansut.com/yutiansut-logo.png)


![version](https://img.shields.io/pypi/v/quantaxis.svg)
![build](https://travis-ci.org/QUANTAXIS/QUANTAXIS.svg?branch=master)
[![Codefresh build status](https://g.codefresh.io/api/badges/build?repoOwner=yutiansut&repoName=QUANTAXIS&branch=master&pipelineName=QUANTAXIS&accountName=yutiansut_marketplace&type=cf-1)]( https://g.codefresh.Io/repositories/yutiansut/QUANTAXIS/builds?filter=trigger:build;branch:master;service:5a30c1026e9d6c0001c5143b~QUANTAXIS)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d8504e4af33747bb8117579212425af9)](https://www.codacy.com/app/yutiansut/QUANTAXIS?utm_source=github.com&utm_medium=referral&utm_content=yutiansut/QUANTAXIS&utm_campaign=badger)
[![Stories in Ready](https://badge.waffle.io/yutiansut/QUANTAXIS.svg?label=ready&title=Ready)](http://waffle.io/yutiansut/QUANTAXIS)
[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/yutiansut/quantaxis)
![QAS](https://img.shields.io/badge/QAS-%200.0.8-brown.svg)
![python](https://img.shields.io/badge/python-%203.6/3.5/3.4/win/ubuntu-darkgrey.svg)
![Npm](https://img.shields.io/badge/Npm-%200.4.0-yellow.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FQUANTAXIS%2FQUANTAXIS.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FQUANTAXIS%2FQUANTAXIS?ref=badge_shield)




> Welcome to group discussion: [group link](https://jq.qq.com/?_wv=1027&k=4CEKGzn)

> Welcome to the public number: ![Public](http://pic.yutiansut.com/qrcode_for_gh_bbb47e0550f7_258%20%281%29.jpg)

> Many questions can be found in [GITHUB ISSUE](https://github.com/QUANTAXIS/QUANTAXIS/issues), you can make a new issue

QUANTAXIS Quantitative Financial Strategy Framework is a quantitative analysis solution for small and medium-sized strategic teams. We can quickly realize scenario-oriented customized solutions through highly decoupled modular and standardized protocols. QUANTAXIS is a progressive openness. With the framework, you can introduce your own data, analysis plans, and visualization processes according to your own needs. You can also quickly achieve multi-person LAN/WAN collaboration through RESTful interfaces.

<!-- vscode-markdown-toc -->
* 1. [Function](#)
* 2. [Document](#-1)
* 3. [Installation and Deployment](#-1)
* 4. [Update](#-1)
* 5. [Docker](#Docker)
* 6. [Instructions for use](#-1)
* 7. [Jupyter example](#Jupyter)
* 8. [Development Plan](#-1)
* 9. [FAQ FAQ](#FAQ)
* 10. [Project donation](#-1)
* 11. [Backtesting Webkit Plugin Overview](#Webkit)
* 12. [QUANTAXIS Standardization Agreement and Future Agreements](#QUANTAXIS)

<!-- vscode-markdown-toc-config
Numbering=true
autoSave=true
/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

## computer configuration recommended

Recommended configuration:
More than 6 generations of CPU + 16/32GB DDR3/DDR4 memory + 256GB or more SSD hard disk

Minimum configuration:
Supports X64-bit CPU

Because when storing local data, it needs to store more than 2GB of local data, while the 32-bit MONGODB supports only about 2GB of data storage, so at least one X64-bit CPU is needed.

If SSD resources are sufficient, try to store data in SSD and increase the speed of ```wiretiger``` disk.

If it is an Alibaba Cloud/Tencent Cloud server, please select the 64-bit operating system at the very beginning


## 1. <a name=''></a> Features


![](http://pic.yutiansut.com/framework.png)

Already achieved:

- [x] Backline (from 1990) Backtest [Rights of Right] (T+1)
- [x] Minute line [1min/5min/15min/30min/60min] backtest (T+1)
- [x] Stock Index Futures Daily (T+0)/Index Daily/ETF Daily
- [x] Minor index futures line (T+0) / Index minute line / ETF minute line [1min/5min/15min/30min/60min]
- [x] Futures Daily/Minute (Futures Index/Future Futures/ Futures Contracts)
- [x] Based on [pytdx](https://github.com/rainx/pytdx)/[tushare](https://github.com/waditu/tushare) and various crawler data sources
- [x] Real-time trading data, real-time tick
- [x] Vue.js-based front-end website
- [x] Custom Data Structure QADataStruct
- [x] Index Calculation QAIndicator
- [x] Block Data (0.5.1 New)/Flush, Tongdaxin Board
- [x] Fundamental data (part of latest financial statement)
- [x] Quote distribution
- [x] Loop Back Test
- [x] Backtesting Management Optimization (Add Backtest Topic/Version Number)


Expected to achieve:

- [ ] Document Updates
- [ ] Futures Backtesting
- [x] firm
- [ ] Analysis Module (quotation/block analysis)
- [ ] Multiple database support
- [x] authority management
- [x] Transaction Recorder

- [QUANTAXIS 2018 Development Schedule] (job_list.md)


## 2. <a name='-1'></a> Documentation

For documentation see: [book](http://book.yutiansut.com)

Download document manual

[PDF](https://www.gitbook.com/download/pdf/book/quantaxis/quantaxis) | [MOBI](https://www.gitbook.com/download/mobi/book/quantaxis/quantaxis) | [EPUB](https://www.gitbook.com/download/epub/book/quantaxis/quantaxis)

## 3. <a name='-1'></a> Installation and Deployment

```
Git clone https://github.com/yutiansut/quantaxis --depth 1
```

See also [Installation Instructions](Documents/install.md)

## 4. <a name='-1'></a> Update
See also [Update Instructions](Documents/update.md)

## 5. <a name='Docker'></a>Docker
See also [Docker](Documents/docker.md)
## 6. <a name='-1'></a> Instructions for use
See also


* [Example of using QUANTAXIS](https://github.com/quantaxis/QADemo)

* [QUANTAXIS Testing API](Documents/backtest_api.md)
* [Data Structure of QUANTAXIS](Documents/DataStruct.md)
* [QUANTAXIS Indicator System](Documents/indicators.md)
* [QUANTAXIS Data Acquisition Guide](Documents/DataFetch.md)
* [QUANTAXIS Quotes Research](Documents/analysis.md)
* [QUANTAXIS Backtest Analysis](Documents/backtestanalysis.md)
* [Common Strategy Order](Documents/strategy.md)

## 7. <a name='Jupyter'></a>Jupyter Examples
See [Jupyter example](jupyterexample)


## 8. <a name='-1'></a> Development Plan
See [Development Plan](job_list.md)
## 9. <a name='FAQ'></a> Frequently Asked Questions FAQ
See [FAQ](Documents/FAQ.md)

## 10. <a name='-1'></a> Project Donation

Writing code is not easy... Please ask the author for a cup of coffee?


![](http://pic.yutiansut.com/alipay.png)

(PS: When you pay, please bring your name/nickname. Will maintain a sponsorship list~)

[Donation list](CONTRIBUTING.md)



## 11. <a name='Webkit'></a> Backtesting Webkit Plugin Overview

![](http://pic.yutiansut.com/homepage.png)
![](http://pic.yutiansut.com/loginpage.png)
![](http://pic.yutiansut.com/adminpage.png)
![](http://pic.yutiansut.com/backtestpage.png)
![](http://pic.yutiansut.com/rebacktest.png)
![](http://pic.yutiansut.com/backtestpic.png)
![](http://pic.yutiansut.com/strategy.png)
![](http://pic.yutiansut.com/kline.png)
![](http://pic.yutiansut.com/settings.png)


## 12. <a name='QUANTAXIS'></a>QUANTAXIS Standardization Agreement and Future Agreement


QUANTAXIS-Stardand-Protocol version number 0.0.8

For details, see [QUANATXISProtocol](Documents/readme.md)


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FQUANTAXIS%2FQUANTAXIS.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FQUANTAXIS%2FQUANTAXIS?ref=badge_large)
