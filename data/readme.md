# QUANTAXIS-Data
数据获取部分

这部分分两块:

## python核心的爬虫(手动操作/定时部署)

## Nodejs核心的爬虫(在测试后会加入到backend/模块下的method中)

主要需要将数据存储的格式,内容规范化

======

文本信息数据

    -- 财经网站舆情数据

    -- 跟单网站的持仓换仓数据

    -- 天眼查等公司信息数据

    -- 财经网站的公司数据

    -- 期货标的的影响因素信息
    
======

数字型数据
    -- 股票/期货的历史Bar/Tick数据
    
    -- 公司财务数据/期货合约等

    -- 用户行为模拟数据接口
    
    -- 回测数据

=======

用户自定义数据

    -- XXXX

======

目前项目已经有:

    -- 华尔街中文网的文章爬虫

    -- tushare数据接口

    -- 期货数据的数据接口(tq)

    -- wind 数据接口

    -- btc的数据接口


也可以自己定义爬虫,接入数据库

windows下需要phantomjs.exe 

Linux需要phantomjs(Ubuntu用户不能直接apt-get install phantomjs 那个包有问题,只能去github上下载)



### 一些备用资源

```
财经资讯
=========
东方财富网 http://www.eastmoney.com/
新浪财经 http://finance.sina.com.cn/
证券之星 http://www.stockstar.com/home.htm
和讯财经 http://www.hexun.com/
中国证券网 http://www.cnstock.com/
中金在线 http://www.cnfol.com/
股吧 http://guba.eastmoney.com/
凤凰财经 http://finance.ifeng.com/
中财网 http://www.cfi.net.cn/
金融界 http://www.jrj.com.cn/
搜狐财经 http://business.sohu.com/
天天基金网 http://fund.eastmoney.com/
腾讯财经 http://finance.qq.com/
纸黄金 http://www.zhihuangjin.com/
第一财经 http://www.yicai.com/
网易财经 http://money.163.com/
中国证券报 http://www.cs.com.cn/
中国金融网 http://www.financeun.com/
全景网 http://www.p5w.net/
FT中文网 http://www.ftchinese.com/
华股财经 http://www.huagu.com/
2258财经网 http://www.2258.com/
中国网财经 http://finance.china.com.cn/
财经网 http://www.caijing.com.cn/
财新网 http://www.caixin.com/
丰华财经 http://www.jfinfo.com/
i美股 http://www.imeigu.com/
证券时报 http://www.stcn.com/
大公财经 http://finance.takungpao.com/
赢在投资 http://www.yztz.com/
巴山财经 http://www.bashan.com/
----------


数据行情
========
新浪股市行情 http://finance.sina.com.cn/realstock/index.shtml
东方财富网行情 http://quote.eastmoney.com/
新股申购与中签查询 http://data.eastmoney.com/xg/xg/default.html
上证指数 http://quote.eastmoney.com/zs000001.html
外汇牌价 http://www.boc.cn/sourcedb/whpj/
今日黄金价格 http://gold.hexun.com/hjxh/
白银价格 http://gold.hexun.com/byxh/
基金净值查询 http://fund.eastmoney.com/fund.html
商品期货报价中心 http://quote.eastmoney.com/center/futures.html#_5
新股发行一览表 http://newstock.cfi.cn/
中国货币网http://newstock.cfi.cn/

------

财经博客
==========
中金博客 http://blog.cnfol.com/
新浪财经博客 http://blog.sina.com.cn/lm/stock/
东方财富网博客 http://blog.eastmoney.com/
搜狐财经博客 http://stock.sohu.com/blog/
和讯财经博客 http://f.blog.hexun.com/
中国证券网博客 http://blog.cnstock.com/
徐小明博客 http://blog.sina.com.cn/xuxiaoming8
老沙博客 http://blog.sina.com.cn/shaminnong
叶弘博客 http://blog.sina.com.cn/yehong
占豪新浪博客 http://blog.sina.com.cn/huzhanhao
郎咸平博客 http://blog.sina.com.cn/jsmedia
凯恩斯博客 http://blog.sina.com.cn/cannes
王国强博客 http://wangguoqiang.blog.cnstock.com/
淘金客 http://blog.sina.com.cn/ff88

------------

证券机构
============
上海证券交易所 http://www.sse.com.cn/
深圳证券交易所 http://www.szse.cn/
国泰君安 http://www.gtja.com/i/
广发证券 http://new.gf.com.cn/
银河证券 http://www.chinastock.com.cn/
招商证券 http://www.newone.com.cn/
国信证券 http://www.guosen.com.cn/gxzq/index.jsp
华泰证券 http://www.htsc.com.cn/htzq/index/index.html
光大证券 http://www.ebscn.com/
华西证券 http://www.hx168.com.cn/hxzq/hxindex.html
方正证券 http://www.foundersc.com/
安信证券 http://www.essence.com.cn/essence/index.html
西部证券 http://www.westsecu.com/jdw/
申银万国 http://www.sywg.com/sw/index.html
华安证券 http://www.hazq.com/
中信证券 http://www.cs.ecitic.com/
长江证券 https://www.95579.com/
国海证券 http://www.ghzq.com.cn/ghzq/index.html
中泰证券 http://www.zts.com.cn/
中国证监会 http://www.csrc.gov.cn/pub/newsite/
上海黄金交易所 http://www.sge.sh/publish/sge/
上海期货交易所 http://www.shfe.com.cn/
中国证券业协会 http://www.sac.net.cn/
南京证券 http://www.njzq.com.cn/njzq/index.jsp
平安证券 http://stock.pingan.com/

-------

股市周边
========
中国黄金投资网 http://www.cngold.org/
巨潮资讯网 http://www.cninfo.com.cn/cninfo-new/index
第一白银网 http://www.silver.org.cn/
第一黄金网 http://www.dyhjw.com/
模拟炒股 http://www.cofool.com/
雪球网 http://xueqiu.com/
理想论坛 http://www.55188.com/index.php
央视网经济 http://jingji.cctv.com/
中国企业家 http://www.iceo.com.cn/
华尔街见闻 https://wallstreetcn.com/
经济观察网 http://www.eeo.com.cn/
牛仔网 http://www.9666.cn/
中国经营报 http://www.cb.com.cn/
和讯期货 http://futures.hexun.com/
每日经济新闻 http://www.nbd.com.cn/
经济参考报 http://jjckb.xinhuanet.com/
财经郎眼 http://www.iqiyi.com/a_19rrgu9qmt.html?src=aldzy
fx168外汇宝 http://www.fx168.com/
纸金网 http://www.zhijinwang.com/
网贷天眼 http://www.p2peye.com/
犀牛之星 http://www.ipo3.com/
-------

炒股软件
=======
大智慧 http://www.gw.com.cn/
同花顺 http://www.10jqka.com.cn/
证券之星 http://www.stockstar.com
益盟操盘手 http://www.emoney.cn/
钱龙 http://www.ql18.com.cn
```