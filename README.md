# QUANTAXIS 量化金融策略框架
  
QUANTAXIS量化工具箱,实现了股票和期货市场的全品种回测.通过分布式爬虫进行数据抓取,构建了响应式的数据清洗和行情推送引擎.搭建了支持多语言的开放式回测框架.并构建了交互可视化的客户端和网站.

> 0.3.8 版本将对于一体化和模块化流程进行进一步的优化

![version](https://img.shields.io/badge/Version-%200.3.8dev/alpha/packages-orange.svg)
![Pypi](https://img.shields.io/badge/Pypi-%200.3.8-blue.svg)
![Npm](https://img.shields.io/badge/Npm-%200.3.8-yellow.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)
![QQ group](https://img.shields.io/badge/QQGroup-%20563280067-yellow.svg)
![WebSite](https://img.shields.io/badge/Website-%20www.yutiansut.com-brown.svg)
![QQ](https://img.shields.io/badge/AutherQQ-%20279336410-blue.svg)


![QUANTAXIS LOGO](http://i1.piimg.com/1949/62c510db7915837a.png)

## 0.3.8-dev-alpha(packages)版本说明

该版本将几个语言包分别合并封装,以python为目前quantaxis的主语言，负责数据获取，封装，数据库维护，回测等一系列工作。同时将nodejs(javascript)变为2级语言，成为quantaxis的插件一样的存在，你可以引入也可以选择不引入，因此，此时的nodejs以及庞大的node_modules可以无视。matlab，r的支持放在QUANTAXISAnalysis中，也是可选项。

通过这个改动，方便了用户的下载部署过程，也减少了上手难度曲线

### quantaxis
```bash
pip install quantaxis

git clone https://github.com/yutiansut/quantaxis
cd quantaxis
python setup.py install
```

### quantaxis-webkit
``` nodejs
npm install quantaxis
```