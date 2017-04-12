# QUANTAXIS 量化金融策略框架

QUANTAXIS量化金融策略框架,是一个面向中小型策略团队的量化分析解决方案. 我们通过高度解耦的模块化以及标准化协议,可以快速的实现面向场景的定制化解决方案.QUANTAXIS是一个渐进式的开放式框架,你可以根据自己的需要,引入自己的数据,分析方案,可视化过程等,也可以通过RESTful接口,快速实现多人局域网/广域网内的协作.

QUANTAXIS与国内很多优秀的量化平台的区别在于,QA更多关注的是用户体验和实际情景,对于用户需求会有较多的优化.所以会更加注重开放性,引入自定义的便捷性,以及团队协作的细节处理.好比如自定义的数据引入,自定义的策略图表对比,自定义的风险和策略组合管理等等.

## 关键词: 局域网协作/开放式渐进框架/高度自定义


![version](https://img.shields.io/badge/Version-%200.3.8-orange.svg)
![QAS](https://img.shields.io/badge/QAS-%200.0.5-brown.svg)
![Pypi](https://img.shields.io/badge/Pypi-%200.3.8RC3-blue.svg)
![python](https://img.shields.io/badge/python-%203.5/3.6/win/ubuntu-darkgrey.svg)
![Npm](https://img.shields.io/badge/Npm-%200.3.8-yellow.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
![QQ group](https://img.shields.io/badge/QQGroup-%20563280067-yellow.svg)
![WebSite](https://img.shields.io/badge/Website-%20www.yutiansut.com-brown.svg)
![QQ](https://img.shields.io/badge/AutherQQ-%20279336410-blue.svg)


![QUANTAXIS LOGO](http://i1.piimg.com/1949/62c510db7915837a.png)

<!-- TOC -->

- [QUANTAXIS 量化金融策略框架](#quantaxis-量化金融策略框架)
    - [关键词: 局域网协作/开放式渐进框架/高度自定义](#关键词-局域网协作开放式渐进框架高度自定义)
    - [QUANTAXIS-Stardand-Protocol](#quantaxis-stardand-protocol)
    - [适用场景](#适用场景)
    - [Webkit大礼包](#webkit大礼包)

<!-- /TOC -->



## QUANTAXIS-Stardand-Protocol
QUANTAXIS 标准化协议和未来协议

QUANTAXIS-Stardand-Protocol 版本号0.0.5

详情参见  [QUANATXISProtocol](https://github.com/yutiansut/QUANTAXIS/tree/0.3.8-dev-RC-ARP/QUANTAXISProtocol)


## 适用场景
![适用场景](http://i2.buimg.com/567571/e2e7b31b1f9a4307.png)
考虑到这样的一个业务情景,一个机构的策略团队一般由CS+Finance组成,Finance的同学们非常擅长数据分析,策略等,但却不是很了解代码的底层架构,代码风格和标准都各有差异.而CS出身的同学们虽然对于代码和框架了如指掌,但却对枯燥空洞的金融理论一脸懵逼.而目前国内对于量化的服务支持并不能解决这个常见的场景痛点,要么是针对金融的同学的易于操作的分析系统,但对于IT而言缺少可定制化的部分;要么是针对IT的底层数据和交易接口,而对于金融的同学想从底层接口封装出来一套能用的有效率的框架简直难如登天.

QUNATAXIS致力于解决这一场景痛点,我们通过建立一个前后端分离的,基于RESTful的局域网内的标准化框架来解决这一问题.同时我们希望我们的框架是高扩展和易于接入的,以方便各个公司的各个策略团队的个性化需求(这个是最关键的,基本上每个公司都会有自己的数据,自己的交易接口,自己的特定功能目标),所以我们希望构建的是一个标准化的,高扩展性的,易于部署的脚手架,而不是一个完整的难以定制的解决方案.

QUANTAXIS的前后端完全分离,高度拆分,各个组件依赖RESTful标准的URI来进行通信,这也给了我们开放式框架的无限可能,完全可以实现Matlab,r,python,JavaScript,C,C++,rust等各个用户的和谐共处,而不是增加大家学习成本的去学习一门共用语言.同时,只要一个公网IP和服务器,你也可以超越局域网的限制,实现异地的团队的需求.




## Webkit大礼包

即将重构 #QAF03

![前后端分离](http://i1.piimg.com/567571/41fa8b9c16122bfd.png)
