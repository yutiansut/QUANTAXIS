# QUANTAXIS的功能


### 1. 行情服务

#### 1.1 股票/期货/期权/美股/外汇/宏观的历史/实时行情(日线/分钟线/tick/实时五档)服务

参见 [QUANTAXIS的数据获取指南](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/DataFetch.md)

#### 1.2 财务/基本面/宏观数据

参见 [QUANTAXIS财务指标](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/financial_means.md)

#### 1.3 自定义数据源的数据

参见 [QUANTAXIS WEB 爬虫](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/crawler.md)

### 2. 数据运维服务

一键更新 参见[WINDOWS数据自动更新](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/config/windows_autojob_updatedata.md)


### 3 分析服务

#### 3.1 专门为A股股票数据适配的数据结构

参见 [QUANTAXIS的数据结构](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/DataStruct.md)

参见 [QUANTAXIS行情研究](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/analysis.md)

#### 3.2 精心为A股指标计算适配的指标类

参见 [QUANTAXIS指标系统](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/indicators.md)


### 4. 可扩展事件驱动框架

参见 [QUANTAXIS事件框架](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/about_event.md)


### 5. 回测服务

#### 5.1 股票/日内t0/ 的日线/分钟线级别回测

参见 [QUANTAXIS的账户结构](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/account.md)

参见 [QUANTAXIS 账户风险分析插件指南](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/risk.md)

参见 [QUANTAXIS回测委托成交结算的说明](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/orderanddeal.md)

参见 [QUANTAXIS回测分析](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/backtestanalysis.md)

参见 [常见策略整理](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/strategy.md)

参见 [简单策略回测详解](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/QUANTAXIS回测分析全过程讲解.md)

参见 [T0交易的账户详解](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/TEST_ORDER_BACKTEST_T0.md)

### 6 实盘

#### 6.1 股票(实盘易)

实盘易插件 参见[实盘易](http://www.iguuu.com/e?x=18839)

实盘易安装注意 参见[安装注意](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/shipane_install_memo.md)

#### 6.2 期货(python3 CTP win/mac/linux)

参见 [LINUX CTP](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/QUANTAXIS_Trade/LINUXCTP)

参见 [WINDOWS CTP](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/QUANTAXIS_Trade/WindowsCTP)

### 7 网站HTTP服务

#### 7.1 网站后台标准化接口

参见 [QUANTAXIS WEB API说明](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/backendapi.md)



预计实现:
- 选股模式 (最好是一行代码能实现选股  或者是组合选股) .
    ```
    https://github.com/QUANTAXIS/QUANTAXIS/blob/master/blob/master/%E9%80%89%E8%82%A1%E6%A8%A1%E5%9D%97.md
    ```
- 财务函数的fetch优化(一个函数 全市场/多来源/多类型)

-  日内实时的检测/实时采样重采样

    ```
    https://github.com/QUANTAXIS/QUANTAXIS/blob/master/blob/master/QUANTAXIS_Runtime/readme.md
    ```

-  版块--版块产业链--版块消息面-- 异动个股

    ```
    https://github.com/QUANTAXIS/market_review
    ```

-  基于react/electron的桌面级可视化客户端

    ```
    https://github.com/QUANTAXIS/qadesk
    ```