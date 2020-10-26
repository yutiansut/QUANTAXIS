# QUANTAXIS 更新纪要

<!-- TOC -->

- [QUANTAXIS 更新纪要](#quantaxis-更新纪要)
    - [1.3.0 ](#130)
    - [1.2.9 ](#129)
    - [1.2.8 ](#128)
    - [1.2.7 ](#127)
    - [1.2.6 ](#126)
    - [1.2.5 ](#125)
    - [1.2.4 ](#124)
    - [1.2.3 ](#123)
    - [1.2.2 ](#122)
    - [1.2.1 ](#121)
    - [1.2.0](#120)
    - [1.1.10](#1110)
    - [1.1.9](#119)
    - [1.1.8](#118)
    - [1.1.7](#117)
    - [1.1.6](#116)
    - [1.1.5](#115)
    - [1.1.4.dev1](#114dev1)
    - [1.1.4](#114)
    - [1.1.3.dev3](#113dev3)
    - [1.1.3.dev2](#113dev2)
    - [1.1.3.dev1](#113dev1)
    - [1.1.3](#113)
    - [1.1.2.dev1](#112dev1)
    - [1.1.2](#112)
    - [1.1.1.dev2](#111dev2)
    - [1.1.1.dev1](#111dev1)
    - [1.1.0](#110)
    - [1.0.68](#1068)
    - [1.0.67](#1067)
    - [1.0.66](#1066)
    - [1.0.65](#1065)
    - [1.0.64](#1064)
    - [1.0.63](#1063)
    - [1.0.62](#1062)
    - [1.0.61](#1061)
    - [1.0.60](#1060)
    - [1.0.59](#1059)
    - [1.0.58](#1058)
    - [1.0.57](#1057)
    - [1.0.56](#1056)
    - [1.0.55](#1055)
    - [1.0.54](#1054)
    - [1.0.53](#1053)
    - [1.0.52](#1052)
    - [1.0.51](#1051)
    - [1.0.50](#1050)
    - [1.0.49](#1049)
    - [1.0.48](#1048)
    - [1.0.47](#1047)
    - [1.0.46](#1046)
    - [1.0.45](#1045)
    - [1.0.44](#1044)
    - [1.0.43](#1043)
    - [1.0.42](#1042)
    - [1.0.41](#1041)
    - [1.0.40](#1040)
    - [1.0.39](#1039)
    - [1.0.38](#1038)
    - [1.0.37](#1037)
    - [1.0.36](#1036)
    - [1.0.35](#1035)
    - [1.0.34](#1034)
    - [1.0.33](#1033)
    - [1.0.32](#1032)
    - [1.0.31](#1031)
    - [1.0.30](#1030)
    - [1.0.29](#1029)
    - [1.0.28](#1028)
    - [1.0.27](#1027)
    - [1.0.26](#1026)
    - [1.0.25](#1025)

<!-- /TOC -->
## 1.3.0

1. QAUSER/ QAPORTFOLIO/ QAACCOUNT 的联动更新
2. 账户/组合/用户的刷新与恢复

```

In [2]: import QUANTAXIS as QA

In [3]: user1= QA.QA_User(username='yutiansut',password='940809')

In [4]: user1
Out[4]: < QA_USER USER_b87YCy3U with 1 portfolio: {'RB_PORTFOLIO': < QA_Portfolio RB_PORTFOLIO with 3 Accounts >} >

In [5]: user1.portfolio_list
Out[5]: {'RB_PORTFOLIO': < QA_Portfolio RB_PORTFOLIO with 3 Accounts >}

In [6]: user1['RB_PORTFOLIO']
Out[6]: < QA_Portfolio RB_PORTFOLIO with 3 Accounts >

In [7]: user1['RB_PORTFOLIO'].accounts
Out[7]:
{'test1': < QA_Account test1 market: stock_cn>,
 'test2': < QA_Account test2 market: stock_cn>,
 'test3_future': < QA_Account test3_future market: stock_cn>}

In [8]: user1['RB_PORTFOLIO']['test1']
Out[8]: < QA_Account test1 market: stock_cn>

```



## 1.2.9
1. QAIndicator部分指标修正,base.py增加IFAND函数,indicator.py部分指标修正

## 1.2.8

1. market_preset 兼容 tdx的主连/指数获取 如JL8, JL9, RBL8 等
2. base指标 增加 BARLAST
3. market_preset 增加基础函数支持 get_exchange, get_name等
4. QA_USER 完善, 增加订阅策略和积分系统
5. 删除QADataStruct_min类中的 high_limit/low_limit, 修复daystruct的nextdayhighlimit字段
6. 增加tusharepro部分数据到postgresql的储存和调取方式
7. QATTSBroker发布


## 1.2.7

迁移目录:

1. 拆分 QUANTAXIS_CRAWLY 至 https://github.com/QUANTAXIS/QUANTAXIS_CRAWLY

- 减少twisted安装问题
- 模块解耦 功能分离

2. 拆分 QUANTAXIS_MONITOR_GUI 至 https://github.com/QUANTAXIS/QUANTAXIS_Monitor_GUI

- gui部分以插件形式提供

3. 使用yapf 大量修正格式





## 1.2.6

1. 优化QADOCKER文档
2. 增加QAORDER文档
3. 优化了QALog模块在打印大量日志的时候无法知道其用途的问题

现在的quantaxis log 会以这个模式作为name:
```
 'quantaxis_{}-{}-.log'.format(get_config(), os.sep, os.path.basename(sys.argv[0]).split('.py')[0], str(datetime.datetime.now().strftime(
        '%Y-%m-%d-%H-%M-%S')))
```
4. 修改了QAUser的注册模块逻辑
5. 增加了 QA_DataStruct_Min 和 QA_DataStruct_Day两个基类模型
6. 修复settle的一个bug



## 1.2.5

1. 对于QA.QA_util_code_tostr 增加 原先为list类型的支持 现在支持自动补全的  int/list/str 类型转 str
2. QA_DataStruct增加bar_gen  返回迭代的dataframe
3. 增加对于期货的日结算支持:

在期货的保证金模型中:

开仓会冻结保证金到frozen里面, 这时钱并未参与结算/  需要先在每日结算时结转冻结的保证金
4. 增加了QA_Account的 history_table字段,增加了一个  frozen字段, 用于记录历史的保证金增加
5. 大幅删减QA_Account的 receive_deal 精简代码  直接调用receive_simpledeal方法
6. QADATASTRUCT 增加一个 kline_echarts 方法 直接返回 echarts.kline类 可以在jupyter notebook中直接显示
7. QALog模块的默认输出为warning级别, 减少别的模块的无聊输出(点名: 尤其是macropy 疯狂输出)

plot的图示例:

- 可能需要先升级pyecharts 到最新版本 (```pip install pyecharts -U -i https://pypi.doubanio.com/simple```)

![](http://pic.yutiansut.com/QQ%E5%9B%BE%E7%89%8720190103220819.png)


## 1.2.4

1. 修复保证金的bug

PS: 真丢人 年末写个bug 2333


## 1.2.3 

1. 感谢@追梦, QA_Account的receive_simpledeal的成交方式中的 股票市场的印花税计算修正
2. 改写@地下的地下铁, 修正QA_Risk中计算assets的一个停牌无数据的bug
3. 感谢@风筝 修复了单标的多市场的获取bug
4. 重大修改:  增加保证金账户的支持(期货)


具体示例  参见: https://github.com/QUANTAXIS/QUANTAXIS/blob/master/EXAMPLE/test_backtest/FUTURE/TEST_%E4%BF%9D%E8%AF%81%E9%87%91%E8%B4%A6%E6%88%B7.ipynb

```python
#在QA_Account的初始化的时候带上 allow_margin=True

acc=QA.QA_Account(allow_sellopen=True,init_cash=10000,allow_t0=True,allow_margin=True,account_cookie='future_test',market_type=QA.MARKET_TYPE.FUTURE_CN,frequence=QA.FREQUENCE.FIFTEEN_MIN)



#快速撮合接口的测试

acc.reset_assets(init_cash=10000)

acc.receive_simpledeal(code='RB1901', trade_price=3420, trade_amount=1, trade_towards=QA.ORDER_DIRECTION.BUY_OPEN, trade_time='2018-12-28 09:30:00')

acc.receive_simpledeal(code='RB1901', trade_price=3425, trade_amount=1, trade_towards=QA.ORDER_DIRECTION.SELL_CLOSE, trade_time='2018-12-28 09:45:00')

acc.receive_simpledeal(code='RB1901', trade_price=3435, trade_amount=1, trade_towards=QA.ORDER_DIRECTION.SELL_OPEN, trade_time='2018-12-28 09:55:00')

acc.receive_simpledeal(code='RB1901', trade_price=3420, trade_amount=1, trade_towards=QA.ORDER_DIRECTION.BUY_CLOSE, trade_time='2018-12-28 10:45:00')

acc.history_table
"""
datetime	code	price	amount	cash	order_id	realorder_id	trade_id	account_cookie	commission	tax	message
0	2018-12-28 09:30:00	RB1901	3420	1	6918.580	None	None	None	future_test	3.420	0	None
1	2018-12-28 09:45:00	RB1901	3425	-1	10038.155	None	None	None	future_test	3.425	0	None
2	2018-12-28 09:55:00	RB1901	3435	-1	6943.220	None	None	None	future_test	3.435	0	None
3	2018-12-28 10:45:00	RB1901	3420	1	10166.300	None	None	None	future_test	3.420	0	None
"""
acc.frozen
"""
{'RB1901': {2: {'money': 0, 'amount': 0}, -2: {'money': 0, 'amount': 0}}}
"""
```

## 1.2.2

1. 重新构建docker compose，把主镜像拆分jupyter, cron和web三个镜像
2. 修改了QAFetch的mongo查询语句(感谢几何大佬) 优雅的在查询中去掉了_id  
3. 修正期货的DataStruct格式,统一volume字段
4. 更新交易日历到2019-12-31

```
mongo文档参见 https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/#return-the-specified-fields-and-the-id-field-only
```


## 1.2.1

1. 修改回测的时候的账户结算(终于算对了不容易...) @CODE-ORANGE
具体看 [期货冻结-释放资金示例](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/EXAMPLE/test_backtest/FUTURE/%E6%9C%9F%E8%B4%A7TEST.ipynb)
2. 增加 对于单月合约的存储  save future_all/ future_day_all / future_min_all
3. 增加对于future_data 的获取的去重处理
4. @barretthugh 修改了复权部分的代码
5. 优化了docker部分的使用
6. 增加对于jqdata的使用示例
7. 增加了1min的股票采样
8. 增加CTPtick的获取和采样

## 1.2.0

1. 增加对期货保证金冻结的修改
2. 增加对于TALIB的支持, 在talib_indicators中调用
3. 增加对于50ETF的支持
4. 优化cirrusCI的支持


## 1.1.10

1. 减少了一个深圳主站的服务器ip
2. 优化精简无用代码
3. 删除pymssql依赖
4. 优化了实盘易broker的一个小bug
5. 添加bitmex数据下载
6. 增加期权部分的列表等修改
7. 增加了命令行操作
8. 增加了分布式worker quantaxis_run (单独更新[QUANTAXIS/QUANTAXIS_RUN](https://github/quantaxis/quantaxis_run))
9. QAWEB 单独拆分成独立项目 [QUANTAXIS/QUANTAXIS_WEBSERVER](https://github.com/QUANTAXIS/QUANTAXIS_WEBSERVER)

## 1.1.9

为1.1.8的released版本

## 1.1.8

1. 增加了商品期权的分钟线获取
2. 优化了QA_Account的存储
3. 修复了QA_PortfolioView的bug
4. DataStruct 增加了 rolling(N), ndarray的方法
5. QAWEB增加对策略的存储功能
6. QADataStruct增加get_data函数,方便获取各种格式的数据
7. QADataStruct增加 apply函数 方便对自己应用函数
8. 增加了对于QA_Performance插件中先卖后买算差价的支持
9. QAMarket=QAShipaneBroker 支持通达信模拟客户端
10. QAIndicator 增加Talib的形态识别指标
11. 增加了qarun.exe 直接运行策略,实时输出
12. QAWEB 增加了/command/run?command=xxxx的命令行
13. QAWeb 增加了一个socket端口 /command/runbacktest

不兼容修改:

QAWeb 中/accounts/all 返回值修改 为list(之前是dict)

[released] 版本的版本号记错了 实际为1.1.9

## 1.1.7 

1. 优化 QA_DataStruct_future_day/min
2. 增加了QA_fetch_xxx_adv系列中的  QA_fetch_future_day_adv/QA_fetch_future_min_adv函数
3. 增加了QA_DataStruct的reindex方法, 方便从指标中提取部分行情
4. 增加了商品期权的支持

to do:

- 我们考虑在未来将QA_Crawl项目单独列出, 以免过多的无用依赖项


## 1.1.6

1. 优化QAWeb
2. 增加QASU中的QA_SU_save_strategy,用于保存策略
3. 优化QARisk/QAAccount的存储
4. 增加客户端 QUANTAXIS/QADesktop, 版本0.0.3
5. 优化QAFinancial的字段解析
6. 增加期货主连数据存储
7. 增加期货数据本地获取(QA_fetch_future_day/QA_fetch_future_list)
8. 修复了回测中账户的计算的bug,该bug会导致账户长期持仓/空仓的时候缺少记录

## 1.1.5

1. 修复了QA_Account的history_header在以前版本的不兼容问题
2. 增加receive_simpledeal函数接口,方便快速成交
3. QA_Parameter中ORDER_DIRECTION的买开买平卖开卖平的字段修改
4. 修复QA_data_tick_resample中的bug
5. 增加了对于QA_Risk中存储的Risk_message的字段
6. 增加了对于QA_Risk的存储兼容
7. 增加了存储策略的代码
8. 修改QAWeb, 增加了一个Rest的handler
9. QA_DataStruct 增加 normalized 归一化方法, 支持多品种多周期
10. 升级了linux一键安装文件, 升级一键安装的mongodb版本到4.0 删除nodejs的安装
11. 删除quantaxis的logo和启动显示


## 1.1.4.dev1

1. base_datastruct 增加了 avg 和 money 字段


## 1.1.4

1. 修复了期货分钟线的获取bug(期货一天的交易时间超过4小时 不能用股票的bar数量)
2. 修复了QAAccount的Allow_t0规则下的交易结转


## 1.1.3.dev3

1. 增加对于list获取的支持:

    QA_fetch_index_list()

    QA_fetch_index_list_adv()

    QA_fetch_future_list()

    QA_fetch_future_list_adv()

2. 优化 QA_DataStruct的返回Series的名称
3. 删除实盘易broker的TRADE_Event(已弃用)

## 1.1.3.dev2

1. 修复index_cn的列表获取

2. 增加save index_list和save future_list 选项



## 1.1.3.dev1

1. 增加 async for 在3.5上的兼容问题


## 1.1.3

1. 增加对于期货分钟线回测的支持


## 1.1.2.dev1

[QAFetch]


1. QA_Query 优化对于指数数据的字段

[QAData]

1. base_datastruct 优化对于指数DataStruct的支持



## 1.1.2 

[QAData]

1. 修复分钟线降采样bug
2. QADataStruct_Future_day/min 修改

[QAMarket]

1. 修改QADealer以支持期货回测

[QARisk]

1. 修改QARisk 以支持期货账户分析

[test_backtest]

1. 增加期货回测(日线) 简单回测示例

## 1.1.1.dev2

[QAARP]

1. QA_Account 修改默认印花税 千1.5 ==> 千1

[QAData]

1. QA_DataStruct_xxx_day/min 增加 select_day(day) 函数, 一般用于分钟线选取某一日

[test_backtest]

1. 增加分钟线简单回测(单线程) 
2. @尧 提供了一个日线级 多线程的带指标回测





## 1.1.1.dev1

[QAData]

1. 修改了market_value的计算, 对于一日内出现多个权息事件的股票做了兼容处理


## 1.1.0 

[QAAnalysis]

1. QA_Analysis_Block 修改 支持板块指数/自定义指数 以及4种计算方法

[QAData]

1. 修改了采样函数的写法
2. 修复了tick采样成60min的bug
3. 修复了因为multiindex导致的QA_DataStruct.to_json方法缺失 datetime/code 字段的问题
4. 优化了QADataStruct的plot方法
5. 新增自动计算任意时间 流动市值/总市值函数 QA_data_marketvalue  使用不复权DataStruct(DataStruct.add_func(QA_data_marketvalue))

[QAMARKET]


1. 增加对于实盘易的支持
2. 将一些基础解析字段挪至基类QABroker中
3. 基于QAMarket创建的broker/order线程全部变成后台线程
4. QA_OrderHandler 增加持久化 订单/成交单部分
5. 修改QAOrder 变成有限状态机, 通过状态机的动作自动改变Order的状态
6. 修改QABacktest_Broker 适配新的order类
7. 优化QABroker的状态显示
8. 将撮合缓存字典重构进QADealer, dealer加入 deal_message(dict) 和deal_df(dataframe),并增加dealer的settle函数
9. 大量更新QABacktest_Broker方法,使之适配新版本回测
10. 适配实盘,增加字段解析 trade_towards_cn_en, order_status_cn_en
11. 修改order的撮合机制, 使用创建order时的callback回调来更新账户


[QAEngine]

1. QAThread 初始化增加 daemon选项, 用于创建守护线程

[QAARP]

1. QA_Account 增加 cancel_order方法 撤单操作
2. 重写QA_Account的receive_deal方法, 适配新版本更新账户
3. 优化和修改QA_Portfolio 增加对于history/history_table的支持


[QASU]

1. save_orderhandler.py 增加 QA_SU_save_order/ QA_SU_save_deal 方法
2. 增加对于运行时出错的容错处理

[QAUtil]

1. QADate_Trade 增加QA_util_get_order_datetime() 用于获取委托的真实日期 QA_util_get_trade_datetime() 用于获取成交的真实日期
2. QA_Parameter 修改订单状态

[QAWEB]

1. QAWEB 增加查询股票名称的接口 http://ip:port/marketdata/stock/code?code=xxxxx

released in 2018/08/23

## 1.0.68 

1. 更新了财务方法/财务类 QA_DataStruct_Financial

    - QA.QA_fetch_financial_report(code,report_date)

    其中, report_date 是需要手动指定的财务时间, 可以是单个时间,也可以是一列时间:
    > '2018-03-31'  或者['2017-03-31','2017-06-30','2017-09-31','2017-12-31','2018-03-31']
    > 此方法的意义在于指定特定的财务时间(如年报)
    
    返回的是一个MultiIndex的dataframe
    
    - QA.QA_fetch_financial_report_adv(code,start,end)

    支持随意的跨时间索引, start 和end不用刻意指定

    如果end不写,则start参数等同于report_date的用法

    返回的是QA_DataStruct_Financial 类

    - QA_DataStruct_Financial 类, 可以直接加载在基础方法返回的dataframe中

    > QDF.get_report_by_date(code,date) 返回某个股票的某个时间点的财报

    > QDF.get_key(code,date,key) 返回某个股票某个时间点的财报的某个指标

2. 更改了两个财务字段:

    - 159 流动比率: liquidityRatio  ==> currentRatio
    - 211 流动资产比率:  liquidityRatio  ==> currentAssetsRatio
        
3. 使用md5计算财报数据包的更新状况,确保财报是最新状态
4. DataStruct 更新自动降采样字段:

    - DataStruct_Stock_day 增加
        + week
        + month
        + year
    - DataStruct_Stock_min 增加
        + min5
        + min15
        + min30
        + min60
        
    直接调用以后及可返回,如果失败,则返回None

5. QADataStruct.pivot代码更新
6. QADataStruct.to_qfq/hfq 更新

( 此处切记:: 使用groupby之后的 data的index 一定要先做 remove_unused_levels()!!!)

6. 添加了 QUANTAXIS_Monitor_GUI 目录，初步实现了 日周月年线下载的 PYQT5 界面。
7. 对于DataStruct的stock_min的初始化进行了修改,之前有对datetime/code的选取, 现已经删除(dev 1)

released in : July 19, 2018

dev1 released in : July 20, 2018

## 1.0.67 

1. 修改了版本限制 增加3.7,3.8的支持
2. 修改qatdx, 在获取部分不加入复权处理
3. 修改reample, 和通达信的周线.月线标准一致

released in : JULY 17, 2018

## 1.0.66 

1. 修改series_struct 适配单个index的情景
2. 增加马科维茨有效前沿的研究/ 增加盘中涨停分析的研究 (research/)
3. QA_DataStruct_Stock_realtime 类发布, 支持自采样

```python
# 给一个完整版的 (包含 DataStruct合并, DataStruct包装, DataStruct_Realtime采样)
QA.concat([QA.QA_DataStruct_Stock_min(QA.QA_DataStruct_Stock_realtime(QA.QA_fetch_quotation('000636')).resample('1min')),
          QA.QA_DataStruct_Stock_min(QA.QA_DataStruct_Stock_realtime(QA.QA_fetch_quotation('000001')).resample('1min'))])
```
4. 修改了QA.QAFetch.QATushare.QA_fetch_get_stock_info(name)的返回结果
5. @逝去的亮光 增加了LINUX环境下的CTP撤单接口
6. 增加了日线数据的降采样 QA.QA_data_day_resample(data,'w')

released in : JULY 17, 2018

## 1.0.65 

1. 更新了同花顺版块爬虫, 集成进```save stock_block```中
2. 完善了读取本地通达信软件下载的数据的日线数据对比
3. 加入对于多周期采样的处理
4. 加入对于异步数据查询的支持(测试)
5. 修复了一个因为数据库无数据导致返回为None, 又被np.asarray加载成 None,导致无法识别为None且无法被len()加载的问题

released in : JULY 15, 2018

## 1.0.64

1. 修复了QA_RISK的bug
2. 实时采集的数据,支持实时采样 (QA_fetch_quotation/QA_data_tick_resample)
3. 修复后复权bug
4. 增加一个default(默认ip的选项),可以在qadir/setting/config.ini中进行修改, 避免不必要的多次重复测速
5. QA_Setting 增加 ```set_config``` 函数, 用于设置config.ini的值

released in : JULY 11, 2018

## 1.0.63 

1. 紧急修复因为ts.get_stock_basics()获取error导致的无法存储问题
2. 增加了对于选股的需求(选股模块.md)

released in : JULY 9, 2018

## 1.0.62 

1. QA_DataStruct_Indicator 类增加 ```groupby``` 函数和  ```add_func```函数 ,用法和QA_DataStruct_xxxx_DAY/MIN 一致
2. QA_DataStruct_Block 增加两个视图 ```view_code``` 和 ```view_block```
3. QA_DataStruct_xxx_Day/Min 增加一个 ```fast_moving(pct)``` 函数, 用于表达bar的快速涨跌幅(返回series)
4. QA_Data 增加一个 QA_DataStruct_Series() 类, 用于分析行情的series数据
5. QA_DataStruct_Block 重写, 改成Multiindex驱动的数据格式
6. 实现了一个快速分析全市场一段时间内异动的代码
    ```python
    # 引入QUANTAXIS
    import QUANTAXIS as QA
    # 获取全市场版块
    block=QA.QA_fetch_stock_block_adv()
    # 获取全市场股票
    code=QA.QA_fetch_stock_list_adv().code.tolist()
    # 获取全市场2018-07-05的1分钟线
    min_data=QA.QA_fetch_stock_min_adv(code,'2018-07-05','2018-07-05','1min')
    # 查找1分钟线bar涨幅超过3%的股票
    L=min_data.fast_moving(0.03)
    # 使用SeriesDataStruct加载结果
    L1=QA.QA_DataStruct_Series(L)
    # 查看某一个时刻的股票代码
    L1.select_time('2018-07-05 09:33:00').code
    # 使用版块查找这个时段的代码归属版块
    block.get_code(L1.select_time('2018-07-05 09:31:00').code).view_block
    block.get_code(L1.select_time('2018-07-05 09:31:00','2018-07-05 09:41:00').code).view_block
    ```

    返回
    ```text
    blockname
    IP变现                     [300426]
    ST板块                     [000953]
    上周强势                     [300547]
    两年新股             [002808, 300547]
    低市净率                     [002541]
    军民融合                     [300265]
    创业300            [300278, 300426]
    参股金融                     [000953]
    国防军工             [300265, 300278]
    小盘股              [002808, 300265]
    已高送转             [002541, 300547]
    户数减少                     [300042]
    户数增加             [300278, 300547]
    新能源车                     [300547]
    昨日振荡                     [300265]
    昨日涨停                     [300426]
    昨曾涨停                     [300265]
    昨高换手                     [601990]
    智能机器                     [300278]
    次新开板                     [601990]
    次新股                      [601990]
    皖江区域                     [002541]
    破净资产                     [002541]
    股权激励             [300278, 300547]
    股权转让             [000953, 300042]
    近期新低                     [002541]
    送转潜力                     [300042]
    送转超跌             [002808, 300426]
    高质押股     [300042, 300265, 300278]
    ```
7. 修复了save financialfiles的代码
8. 修复了QAWEB在非windows机器上的bug
9. 添加了 save option_day 保存50etf期权的命令到数据库中
10. 增加了config文件的 update_all.py 和 update_x.py 文件, 用于自动化任务管理
11. 增加QASetting模块, 用于QUANTAXIS的设置/配置/任务管理

released in : JULY 8, 2018


## 1.0.61 

1. QA_MARKET 增加订单查询子线程函数```start_order_threading```,线程名称('ORDER') (如股票无回报,需要另外开线程查询是否成交)[如果需要在初始化的时候开启: if_start_orderthreading=True]

    ```python
    threading.enumerate()
    [<_MainThread(MainThread, started 23780)>,
    <Thread(Thread-4, started daemon 4504)>,
    <Heartbeat(Thread-5, started daemon 7760)>,
    <HistorySavingThread(IPythonHistorySavingThread, started 23764)>,
    <ParentPollerWindows(Thread-3, started daemon 17028)>,  
    <Thread(pymongo_server_monitor_thread, started daemon 20440)>,
    <Thread(pymongo_kill_cursors_thread, started daemon 20216)>,
    <QA_ENGINE with ['ORDER', 'SPE_BROKER', 'BACKTEST_BROKER'] kernels>,
    <QA_ThreadORDER  id=2226925613408>,
    <QA_ThreadSPE_BROKER  id=2226855623648>,
    <QA_ThreadBACKTEST_BROKER  id=2226925616992>]
    ```
    
2. QA_ORDER 增加一个 ```realorder_id ``` 用于记录订单在报给交易所后返回的order_id
3. 修复了QA_fetch_get_exchangerate_list的bug

released in : JULY 4, 2018

## 1.0.60 

1. groupy 默认参数中 sort设置为false
2. 加速指标运算/前后复权 (视股票数量而定,3000多只股票提速20倍)
3. 回测加速(test_backtest/MACD_JCSC.py) 从14秒提速到2秒
4. QA_Risk 增加

> max_holdmarketvalue 最大持仓市值,min_holdmarketvalue 最小持仓市值, average_holdmarketvalue 平均持仓市值
> max_cashhold 最大闲置现金, min_cashhold 最小持仓现金, average_cashhold 平均持仓现金

5. QA_Performance 增加:

> win_rate(methods='FIFO') 胜率
> average_profit(methods='FIFO') 平均利润

6. 增加QA_Trade模块,QATrade_Realtime类(未完成)

7. 支持 期权数据/ 港股数据获取/ 部分美股数据/ 国际期货数据/ 宏观指标/ 汇率数据/

- QA_fetch_get_option_list 获取期权列表(郑州商品期权/大连商品期权/上海商品期权/中金所期权/上海股票期权)
- QA_fetch_get_globalfuture_list 获取国际期货列表(伦敦金属/伦敦石油/纽约商品/纽约石油/芝加哥谷/东京工业品/纽约期货/新加坡期货/马来期货)
- QA_fetch_get_hkstock_list 获取香港主板/创业板股票
- QA_fetch_get_hkfund_list  获取香港基金列表
- QA_fetch_get_hkindex_list 获取香港指数列表
- QA_fetch_get_usstock_list 获取美股股票列表
- QA_fetch_get_macroindex_list 获取宏观指数列表
- QA_fetch_get_exchangerate_list 获取汇率数据(基础汇率/交叉汇率)

- QA_fetch_get_option_day 获取期权(郑州商品期权/大连商品期权/上海商品期权/中金所期权/上海股票期权)日线
- QA_fetch_get_globalfuture_day 获取国际期货日线(伦敦金属/伦敦石油/纽约商品/纽约石油/芝加哥谷/东京工业品/纽约期货/新加坡期货/马来期货)
- QA_fetch_get_hkstock_day 获取香港主板/创业板股票日线
- QA_fetch_get_hkfund_day  获取香港基金日线
- QA_fetch_get_hkindex_day 获取香港指数日线
- QA_fetch_get_usstock_day 获取美股股票日线
- QA_fetch_get_macroindex_day 获取宏观指数日线
- QA_fetch_get_exchangerate_day 获取汇率数据(基础汇率/交叉汇率)日线

- QA_fetch_get_option_min 获取期权(郑州商品期权/大连商品期权/上海商品期权/中金所期权/上海股票期权)分钟线
- QA_fetch_get_globalfuture_min 获取国际期货分钟线(伦敦金属/伦敦石油/纽约商品/纽约石油/芝加哥谷/东京工业品/纽约期货/新加坡期货/马来期货)
- QA_fetch_get_hkstock_min 获取香港主板/创业板股票分钟线
- QA_fetch_get_hkfund_min  获取香港基金分钟线
- QA_fetch_get_hkindex_min 获取香港指数分钟线
- QA_fetch_get_usstock_min 获取美股股票分钟线
- QA_fetch_get_macroindex_min 获取宏观指数分钟线
- QA_fetch_get_exchangerate_min 获取汇率数据(基础汇率/交叉汇率)分钟线

8. python3 CTP接口 [WINDOWS/LINUX]
9. shipane broker增加key参数, 安全性保障
10. QA_MARKET 增加在注册账户的时候的交易同步(实盘/模拟盘)
11. @yehoha 增加了对QA_DATASTRUCT的振幅的修改
12. @zsluedem 对虚拟货币币安交易所的数据进行了优化
13. QA_WEB 增加本地实时5挡行情接口 ip:port/marketdata/stock/price?code=xxxxxx
14. QA_WEB 增加了对于非windows下的机器多进程的支持

released in : JULY 4, 2018

## 1.0.59 

1. 修改了DataStruct的high_limit和low_limit的计算方式
    - 惰性计算,取消在初始化的时候的计算
    - 修复了多code的时候的bug

2. 修改了groupby写法, 增加的QADataStruct的groupby参数
3. 修改了前复权等各种涉及groupby('code')可能报错的情况,改成level层面的操作,以后不会出现warning
    
released in : JUNE 27, 2018


## 1.0.58 
1. QA_Account 增加hold_time属性, 显示持仓时间
2. 对于QA_Query 的 QA_fetch_financialfiles进行修改, 优化返回结果
3. QA_DataStruct_Block 修改了get_block方法, 可以获取多个block_name
4. 修改了financialdicts里面,两个重复的净利润,将现金流量表中的改成netProfitFromOperatingActivities
5. QA_SU_save_stock_info_tushare加到主函数中
6. QAAnalysis_Block细微修改,增加__repr__
7. 文档增加回测和测试账户部分(Documents/)
8. 增加指数装饰器@QDS_IndexDayWarpper, @QDS_IndexMinWarpper
9. 更新jupyter的文档(Documents/usejupyter.md)
10. DataStruct的high_limit和low_limit的bug修复
11. @喜欢你 更新了mac下的financialfiles存储问题

released in : JUNE 27, 2018

## 1.0.57 

1. 重新修改了依赖项
released in : JUNE 24, 2018

## 1.0.56 
1. 优化了 'crawl eastmoney zjlx all' 获取东方财富资金流向的操作，保存到mongodb数据库中
2. @pchaos 完善了通过配置文件排除ip(某些ip长期BAD RESPONSE),同时补充一个requirements
3. 实盘易单账户测试完毕
4. 期货实时tick的接口修复
5. 数据获取QAFetch的jupyter例子更新(jupyterexample/QAFetch.ipynb)
6. 修改ORDER_MODEL 中的对应values为 大写
7. 增加实盘易broker的query_clients方法
8. 修改了QAWeb的获取数据优先级,避免在无mongodb的时候的```connection timeout```问题
9. QA_Account 修改了两个函数(```account.get_history(start,end)``` 获取历史成交,```hold_table``` 修改去除0持仓的股票 )
10. QA_Risk 增加一个property(```risk.daily_market_value```每日总市值)
11. 优化了Backtest_broker的market_data的判定,加入series的支持
released in : JUNE 24, 2018

## 1.0.55

优化了save financialfiles 的逻辑
released in : JUNE 18, 2018

## 1.0.54

优化了save financialfiles 的逻辑
released in : JUNE 17, 2018

## 1.0.53

优化了save financialfiles 的逻辑
released in : JUNE 17, 2018

## 1.0.52 

1. @几何提交了 比特币部分的爬虫
2. QAWEB部分后台增加了基于account_cookie的查询(ip:port/accounts?account_cookie=xxx)
3. @几何 优化了setup.py文件
4. 财务数据的存储,获取
5. QA_fetch_financial_report
6. QACLI--> save financialfiles
7. QASU.QA_SU_save_financial_files()

released in : JUNE 17, 2018

## 1.0.51 

1. 增加三个函数到QA主函数中: QA_fetch_get_future_transaction, QA_fetch_get_future_transaction_realtime, QA_fetch_get_future_realtime

released in : JUNE 14, 2018

## 1.0.50 
1. 添加了获取东方财富个股资金流向保存到sqlite的命令， windows 和 mac 下测试过
2. crawl eastmoney zjlx 6位股票代码 命令 和获取所有股票资金流向 crawl eastmoney zjlx all 的命令，
3. 添加了 QUANTAXIS_CRAWLY 目录，一个scrapy的空的项目，后期支持 各种经济新闻，证券报刊信息，热点咨询的获取
4. QUANTAXIS/QAWeb 用tornado的后台重写
5. 基于websocket的实时数据推送
6. 期货历史tick,期货实时数据支持

released in : JUNE 14, 2018

## 1.0.49 

1. @喜欢你 提交了资金流向爬虫(QUANTAXIS CLI/ crawl)
2. 修复1.0.48-2的引入,使用ImportError错误项
3. dockerfile更新

released in : JUNE 14, 2018


## 1.0.48

1. 修改了QA_Portfolio, 增加init_hold, init_hold_table 字段,可以查看组合的初始化持仓,以及带account的初始化持仓
2. 修改了QA_Risk的引入, 测试引入import tkinter

released in : JUNE 12, 2018

## 1.0.47

1. 修改了QAMARKET 适配t0回测
2. 增加t0回测示例
3. 分钟线撮合不再加一分钟
4. T0回测买入限额,QA_Account.buy_available
5. 修改示例,使用随机买卖来测试框架 https://github.com/QUANTAXIS/QUANTAXIS/blob/master/test_backtest/T0backtest.ipynb
6. 增加对于多个标的的t0账户的支持
7. 修复一个QA_Account下计算account.trade因为pivot_table默认使用np.mean作为arg_func的bug,该bug会导致在相同时间开了方向相反的仓位,会被计算成平均数
8. 修复了一个QA_fetch_stock_day_full()中set_index的bug

released in : JUNE 12, 2018

## 1.0.46
1. 命令行中 添加了 save stock_info_tushare 保存tushare股票列表的信息到数据库中
2. 修改了实盘易 broker 增加对接
3. 修改了base_datastruct的 selects,select_time,select_month,get_bar,select_code,增加异常处理(ValueError)
4. 基于pandas的反馈,使用remove_unused_levels来对索引进行更新
5. 大幅修改 base_datastruct方法的 select_time_by_gap, splits, add_func方法,优化性能
6. 增加了一个期货下单接口(QUANTAXIS_trade/WYFFuture)
7. 成交量复权修正
8. 实盘易下单对接(单账户)
9. 删除emoji导致的windows输出不兼容
10. 增加部分广州ip
11. 增加一个通达信的成交记录读取接口
12. 修改存储打印
13. 修改了分钟线初始化的column请求,使用if in columns来代替
14. 修改了Backtest内部在获取_quotation时候的dict匹配,使用pd.Timestamp来代替
15. 修改了threadeng, 使用raise error 报错
16. 修改了QA_Account/QA_Portfolio的账户初始化过程, init_assets==> init_cash, 新版的init_assets(只读属性)会返回一个dict{'cash':xx,'hold':{}}
17. 删除了初始化过程中cash/history的输入
18. QA_Account 增加两个property self.datetime/self.date 均为account运行的时候的实时时间和日期
19. QA_Account 增加一个close_positions_order 属性, 仅限T0账户使用, 返回一个list,里面都是封装好的QA_Order
20. 对于QA_Account的T0模式增加一系列适配
21. 修改一个example,展示T0的使用,更多文档正在补充
22. QA_RISK 修改了利润的计算模式,以及benchmark的assets(改为从收盘价计算资产)
23. QA_RISK 增加一个利润构成表 risk.profit_construct
24. QA_RISK 增加总手续费,总印花税(risk.total_commission,risk.total_tax)
25. QA_RISK 增加市值表计算(risk.market_value)
26. 修复了QA_Account的一个计算daily_cash的bug

released in : JUNE 11, 2018

## 1.0.45 

1. 在安装完毕后,会弹出一个浏览器页面,告知最新更新
2. 修复1.0.42出现的一个bug (select_code的问题), 同时兼顾1.0.44的写法进行修改

```
因此先用set_index去重做一次index
影响的有selects,select_time,select_month,get_bar,select_code
```

released in :JUNE 03, 2018



## 1.0.44

1. @2018/06/03 pandas 的索引问题导致
https://github.com/pandas-dev/pandas/issues/21299

因此先用set_index去重做一次index
影响的有selects,select_time,select_month,get_bar

released in :JUNE 03, 2018


## 1.0.43
1. quantaxis 命令行 save 命令错误的 异常处理
2. QA_Risk 插件增加对于assets计算的修改(如果撮合按不复权撮合,risk也按不复权去计算assets)

released in :JUNE 03, 2018
 

## 1.0.42 

1. QDS的DataStruct 删除 __reversed__ 和 reverse方法
2. QDS增加回__reversed__方法 但是会raise NotImplementError,方便在reversed内置方法调用时报错
3. _quotation_base 类中 __add__ __sub__ 的测试代码
4. _quotation_base 类中 __getitem__  类型判断，的测试代码 
5. QAQuery_Advance 中函数获取数据的参数检查
6. QA_DataStruct_Indicators 增加指标类
7. QADATASTRUCT 的selects, select_time,get_bar函数的速度更新
8. QADataStruct_Indicators 指标类的索引速度更新(详见 [QUANTAXIS INDICATOR](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/Documents/indicators.md))

released in :JUNE 01, 2018


## 1.0.41
 1. 增加了财务表的注释和翻译QAData/financial_means.py
 2. @喜欢你 更新了布林带的回测示例
 3. @Roy T.Burns 提交了关于回测Risk插件画图的显示错误
 4. @尧 对于无GUI的机器引入matplotlib做了测试和修改
 5. 增加 QARisk的 benchmark_profit
 6. 新增两个装饰器 关于QUANTAXIS DATAStruct ==> 简称QDS 
    ```
    @QDS_StockDayWarpper 
    @QDS_StockMinWarpper
    ```
 7. 将QDS的方法暴露出来 [concat,from_tushare](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/QUANTAXIS/QAData/dsmethods.py)
    QDS的装饰器主要是用于将别处获取的数据之间转化为QDS格式
    ```python
    import QUANTAXIS as QA
    import tushare as ts


    @QA.QDS_StockDayWarpper
    def get_stockday_adv(code,start,end):
        return QA.QA_fetch_get_stock_day('tdx',code,start,end)


    @QA.QDS_StockDayWarpper
    def get_stockday_ts(code,start,end):
        return ts.get_k_data(code,start,end)

    print(get_stockday_adv('000001','2018-05-01','2018-05-21'))
    print(get_stockday_ts('000001','2018-05-01','2018-05-21'))

    ```
 8. @喜欢你 按照test_backtest中的MACD_JCSC.py的写法移植到了unittest来运行，后期加入assert来自动测试
 9. @喜欢你 修改了QA_Risk的显示,以及更新PR说明

released in :May 30, 2018


## 1.0.40

 1. 修改base的函数 AVEDEV 返回SERIES
 2. @宋 @喜欢你 修改kernal,kernal_dict --> kernel, kernel_dict
 3. QA_Performance 增加两个属性 pnl_lifo, pnl_fifo
 4. QA_Performance 增加两个方法 plot_pnlmoney.plot_pnlratio
 5. @尧 在无GUI的电脑上的matplotlib引入时报错的兼容处理
 6. @yehonghao 增加了龙虎榜数据的获取和存储

released in :May 28, 2018

## 1.0.39

 1. 增加seaborn依赖项  需要pip install seaborn 
 2. QA_Risk 增加两个画图方法: plot_dailyhold() plot_signal()

released in :May 24, 2018

## 1.0.38

 1. 修改了COUNT函数,现在返回series格式 在@musicx的[ISSUE 429](https://github.com/QUANTAXIS/QUANTAXIS/issues/429)问题上进行了改进
 2. 修改了PortfolioView类,修改account_cookie为PVIEW_xxx,增加contained_cookie 作为承载的account的cookie集合
 3. @taurusWang 对于QA_fetch_stock_day_adv的异常值进行了修改
 4. @taurusWang 对于代码进行了大量的注释
 5. @royburns 提供了金叉死叉的回测代码 test_backtest/目录下
 6. 修改了QA_RISK 增加了一个画图方法: plot_assets_curve()方法

released in :May 23, 2018

## 1.0.37

 1. @yssource将log文件都放入~/.quantaxis/log目录中 (* 在windows中,users/username/.quantaxis/log),减少log文件的垃圾输出
 2. @cc/pchaos 的建议: 将log的位置放在setting文件中

released in :May 22, 2018

## 1.0.36

 对于策略示例做了一些适当性的调整

released in :May 21, 2018

## 1.0.35

1. 增加 QA_Account 增加一个方法 hold_table(datetime) 方便在复盘的时候查看某一个时间点的账户持仓
2. 增加 QA_Account 增加一个方法 hold_price(datetime) 使用vwap成交量加权算法计算持仓均价
3. 增加 QA_Account 增加一个属性 trade_range 返回账户的交易时间段(所有交易日)
4. 修改 base_datastruct 修改以便兼容多个股票的DataStruct的指标计算

受影响的方法/属性
 - self.max
 - self.min
 - self.mean
 - self.price_diff
 - self.pvariance
 - self.variance
 - self.stdev
 - self.pstdev
 - self.mode
 - self.mean_harmonic
 - self.amplitude
 - self.skew
 - self.kurt
 - self.pct_change
 - self.mad

released in :May 21, 2018

## 1.0.34 

1. 增加: QA_Account增加一个属性 running_time 用于记录该账户的运行时间(会同步到数据库,所以从数据库取出的account也是当时运行的时间)
2. @Roy T.Burns 对于QAUSER的修改 增加了自定义user_cookie的功能
3. @几何提出的对于MONGODB uri以及本地文件设置的问题 
```
1.0.34会在本地创建一个.quantaxis目录,用于存储设置等
同时可以对于.quantaxis/setting/config.ini进行修改,配置默认数据库
```
4. @taurusWang对于QA的整体注释和代码结构做了系统性的优化

released in :May 19, 2018

## 1.0.33

1. 取消初始化quantaxis的时候选择服务器,改成获取事件触发时选取

released in :May 18, 2018

## 1.0.32

1. 对于账户的修改: 增加了QA_Account.orders 作为委托/订单记录器
2. 对于base_datastruct的修改 : 增加了部分代码的注释
3. 对于QA_BACKTESTBROKER做了修改: 增加了对于市价单等的bug修复
4. 对于QA_BACKTESTBROKER做了修改: 修改了BY_MONEY/BY_AMOUNT的成交机制
5. 对于QA_DEALER进行了修改,减少成交回报报文,去除MARKET_DATA部分数据
6. 对于QAUtil.QADate_trade做了修改,更改交易时间为9:15-11:30/1:00-3:00的时间,加入盘前集合竞价的数据
7. 对于QARisk做了修改,更改了最大回撤的计算

感谢@尧 zhongjy1992@outlook.com 对于该版本做出的巨大贡献

released in :May 17, 2018

## 1.0.31

1.0.31 更新了关于DATAStruct的易用性

1. 增加了一个参数 split_dicts, 以KV对形式拆分DataStruct,可以快速寻找个股的DataStruct

```python


[In1]: datafq.split_dicts

{'000014': < QA_DataStruct_Stock_day with 1 securities >,
 '000037': < QA_DataStruct_Stock_day with 1 securities >,
 '000555': < QA_DataStruct_Stock_day with 1 securities >,
 '000670': < QA_DataStruct_Stock_day with 1 securities >,
 '000677': < QA_DataStruct_Stock_day with 1 securities >,
 '000681': < QA_DataStruct_Stock_day with 1 securities >,
 '000687': < QA_DataStruct_Stock_day with 1 securities >,
 '000801': < QA_DataStruct_Stock_day with 1 securities >,
 '000868': < QA_DataStruct_Stock_day with 1 securities >,
 '002068': < QA_DataStruct_Stock_day with 1 securities >,
 '002077': < QA_DataStruct_Stock_day with 1 securities >,
 '002137': < QA_DataStruct_Stock_day with 1 securities >,
 '002203': < QA_DataStruct_Stock_day with 1 securities >,
 '002258': < QA_DataStruct_Stock_day with 1 securities >,
 '002371': < QA_DataStruct_Stock_day with 1 securities >,
 '002376': < QA_DataStruct_Stock_day with 1 securities >}
```

example:

从一个DataStruct包里面快速拿到000014的股票,选择2018-04-01以前15天的数据,计算这部分数据的MACD
```python
R=datafq.split_dicts
R['000014'].select_time_with_gap('2018-04-01',15,'<=').add_func(QA.QA_indicator_MACD,1,2)
```
released in :May 15, 2018

## 1.0.30

1.0.30更新了关于回测和数据查询的代码

1. 修改了查询股票info的代码, 支持多个股票同时查询
2. 修改了QA_Account下单时的```cash_available```结算bug
3. 

released in :May 14, 2018



## 1.0.29

1.0.29更新了关于数据查询的代码

1. 更新了前复权/后复权的计算,保证了即使在复权数据全无的时候,返回正确的复权结果
2. 更新了查询权息数据库的代码,现在支持多个股票同时查询
3. 加速了复权的效率

released in :May 14, 2018


## 1.0.28


ATTENTION CHANGELOG 1.0.28
修改了Account的send_order方法, 区分按数量下单和按金额下单两种方式

- AMOUNT_MODEL.BY_PRICE ==> AMOUNT_MODEL.BY_MONEY # 按金额下单
- AMOUNT_MODEL.BY_AMOUNT # 按数量下单

在按金额下单的时候,应给予 money参数
在按数量下单的时候,应给予 amount参数


```python
Account=QA.QA_Account()

Order_bymoney=Account.send_order(code='000001',
                                price=11,
                                money=0.3*Account.cash_available,
                                time='2018-05-09',
                                towards=QA.ORDER_DIRECTION.BUY,
                                order_model=QA.ORDER_MODEL.MARKET,
                                amount_model=QA.AMOUNT_MODEL.BY_MONEY
                                 )

Order_byamount=Account.send_order(code='000001',
                                price=11,
                                amount=100,
                                time='2018-05-09',
                                towards=QA.ORDER_DIRECTION.BUY,
                                order_model=QA.ORDER_MODEL.MARKET,
                                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                 )
```

released in :May 10, 2018

## 1.0.27

2018-05-06

修改并增加了大量的公式,统一成dataframe格式返回,可以被直接concat合并出来

预计将对于indicator类进行重写并缓存/本地存储,方便快速调用

修改了QA_Account的下单模式, 修复了下单的判断bug

released in :May 10, 2018

## 1.0.26

2018-05-02

1.0.26 对于回测进行了一些优化

1. 增加了对于RISK类的参数

- 增加了```init_assets```, ```last_assets```参数,更方便查看

- 修改了计算年化收益率的公式

2. 修改了simple_backtest 函数的逻辑:

- simple_backtest 之前的 重设账户资金的写法错误, 已更正

- simple_backtest 现在会随机下单(增加随机函数)


3. 修改了```QADATASTRUCT```中日线结构的参数

增加了 ```next_day_high_limit``` 和 ```next_day_low_limit```参数,方便计算,明日涨跌停

released in :May 02, 2018


## 1.0.25 

2018-04-27

1.0.25 增加对于查询的优化:

1. 优化了查询时输入的参数

当code的列表如果是[000001,000002... ]等int形式时,会出现不支持的错误,1.0.25进行了优化

常见原因是如果code从csv中取出,csv会自动讲code变成整数的形式,如果在传参之前没有进行 ```code.apply(str).tolist()```的话,会出现此错误

2. 优化了查询的返回

在偶见的数据库数据重复时,会对数据自动去重并返回结果

released in :Apr 27, 2018


