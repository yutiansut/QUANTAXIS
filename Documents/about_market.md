# QUANTAXIS MARKET

在0.6版本以后,QA_MARKET从成交功能转化成交易前置,然后解耦出来用于成交的QA_Broker和用于撮合的QA_Dealer

QUANTAXIS的market前置可以理解为一个类似于没有界面的交易客户端,通过注册账户和注册broker 来连接

在backtest中,使用时间轴(一个生成器)去推动数据更新和时间前进,在真实环境中,就是真实的时间和行情驱动前进

![](http://pic.yutiansut.com/market_gen.png)

![](http://pic.yutiansut.com/%E9%87%8D%E6%9E%84%E6%96%87%E6%A1%A3-%E5%B8%82%E5%9C%BA.png)

![](http://pic.yutiansut.com/%E9%87%8D%E6%9E%84%E6%96%87%E6%A1%A3-%E5%BC%95%E6%93%8E.png)