# QUANTAXIS_SPIDER 爬虫
###[QUANTAXIS 3.6](https://github.com/yutiansut/QUANTAXIS) 重构版本的爬虫部分


![build](https://img.shields.io/badge/Build-passing-green.svg)
![author](https://img.shields.io/badge/Powered%20by-%20%20yutiansut-red.svg)
![license](https://img.shields.io/badge/License-%20MIT-brightgreen.svg)

[QUANTAXIS_VISUALIZATION](https://github.com/yutiansut/QUANTAXIS_VISUALIZATION) 可视化(客户端/网页)| VISUALIZATION Client/Webpages

[QUANTAXIS](https://github.com/yutiansut/QUANTAXIS)  未来主分支,目前还是matlab版本 |Future Master Branch, now still a old 3.6 Version with matlab


## QUANTAXIS_SPIDER - Spider Branch

Spider这个分支是一个精简分支,为了QUANTAXIS4.0做准备的数据获取版本.
在这个版本中,我们去除了大量数据可视化的内容,也将原来的爬虫逻辑进行了重构.

Spider分支主要有两个语言版本爬虫

QUANTAXIS_Spider(Python Version)-- ctp,爬虫,股票,期货数据等

QUANTAXIS_Spider(Nodejs Version)--

等到后台逻辑确定,前端需求框架完善以后,我们会逐步的把python版本的爬虫去除

Tips:在合并到QUANTAXIS4.0版本时,这个spider会和QUANTAXIS_VISUALIZATION的backend/合并


### Python Version
* python with wind
* python with spider
* python with ctp


### Nodejs Version
这个爬虫还是基于express的后端+api调用+methods构成
会根据方法的不同,如
localhost:[port]/stock/
localhost:[port]/articles/
localhost:[port]/cmd/


## APIS

localhost:3000/stock
### /stock/history/all?code=xxx&feq=xxx
### /stock/history/time?code=xxx&start=(yyyy-mm-dd)&end=(yyyy-mm-dd)
### /stock/index/
### /stock/live?code=xxx
### /stock/quota/lhb?