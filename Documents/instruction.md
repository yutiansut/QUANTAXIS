

## 一些基础的api介绍

QUANTAXIS 是一个渐进式的框架,也就是说 你可以很简单的只使用回测部分,也可以逐步深入开发,从数据源获取/数据库替代,到回测的引擎的修改,自定义交易模式,事件修改等等.

在0.5.0以前,api都不是很稳定,所以文档这块比较欠缺,暂时先给一些常用的api说明:

该部分文档可以配合 [Jupyter Example](https://github.com/yutiansut/QUANTAXIS/tree/master/jupyterexample) 一起使用

<!-- TOC -->

- [一些基础的api介绍](#一些基础的api介绍)
    - [QUANTAXIS.QABacktest 的 api](#quantaxisqabacktest-的-api)
    - [QUANTAXIS的核心数据结构](#quantaxis的核心数据结构)
    - [QUANTAXIS的指标系统](#quantaxis的指标系统)
    - [QUANTAXIS的行情分析/研究用](#quantaxis的行情分析研究用)
    - [QUANTAXIS的api](#quantaxis的api)

<!-- /TOC -->
### QUANTAXIS.QABacktest 的 api
```python
from QUANTAXIS import QA_Backtest as QB
#常量:
QB.backtest_type #回测类型 day/1min/5min/15min/30min/60min/index_day/index_1min/index_5min/index_15min/index_30min/index_60min/
QB.account.message  #当前账户消息
QB.account.cash  #当前可用资金
QB.account.hold # 当前账户持仓
QB.account.history #当前账户的历史交易记录
QB.account.assets #当前账户总资产
QB.account.detail #当前账户的交易对账单
QB.account.init_assest #账户的最初资金
QB.strategy_gap #前推日期
QB.strategy_name #策略名称

QB.strategy_stock_list #回测初始化的时候  输入的一个回测标的
QB.strategy_start_date #回测的开始时间
QB.strategy_end_date  #回测的结束时间


QB.today  #在策略里面代表策略执行时的日期
QB.now  #在策略里面代表策略执行时的时间
QB.benchmark_code  #策略业绩评价的对照行情

QB.backtest_print_log = True  # 是否在屏幕上输出结果


QB.setting.QA_setting_user_name = str('admin') #回测账户
QB.setting.QA_setting_user_password = str('admin') #回测密码


#函数:
#获取市场(基于gap)行情:
QB.QA_backtest_get_market_data(QB,code,QB.today/QB.now)
- 可选项: gap_ 
- 可选项: type_ 'lt','lte' 默认是lt
#获取单个bar
QB.QA_backtest_get_market_data_bar(QB,code,QB.today/QB.now)

#拿到开高收低量
Open,High,Low,Close,Volume=QB.QA_backtest_get_OHLCV(QB,QB.QA_backtest_get_market_data(QB,item,QB.today))

#获取市场自定义时间段行情:
QA.QA_fetch_stock_day(code,start,end,model)

#一键平仓:
QB.QA_backtest_sell_all(QB)

#报单:
QB.QA_backtest_send_order(QB, code,amount,towards,order: dict)
"""
order有三种方式:
1.限价成交 order['bid_model']=0或者l,L
  注意: 限价成交需要给出价格:
  order['price']=xxxx

2.市价成交 order['bid_model']=1或者m,M,market,Market  [其实是以bar的开盘价成交]
3.严格成交模式 order['bid_model']=2或者s,S
    及 买入按bar的最高价成交 卖出按bar的最低价成交
3.收盘价成交模式 order['bid_model']=3或者c,C
"""
#查询当前一只股票的持仓量
QB.QA_backtest_hold_amount(QB,code)
#查询当前一只股票的可卖数量
QB.QA_backtest_sell_available(QB,code)
#查询当前一只股票的持仓平均成本
QB.QA_backtest_hold_price(QB,code)

```


### QUANTAXIS的指标系统

QUANTAXIS的核心数据结构有一个方法叫add_func(func,*args,**kwargs),作为一个指标入口,会返回一个和DataStruct中股票数量一致长度的list

QUANTAXIS有两种类型的指标:

- 基础指标(输入为Series的指标)
- 应用级指标(可应用于DataStruct的指标)

其中,基础指标是为了应用级指标做准备的,及对应于Series的分析和dataframe的分析的关系

基础类指标 [基本和同花顺/通达信一致]
```python
import QUANTAXIS as QA
QA.MA(Series, N)
QA.EMA(Series, N)
QA.SMA(Series, N, M=1)
QA.DIFF(Series, N=1)
QA.HHV(Series, N)
QA.LLV(Series, N)
QA.SUM(Series, N)
QA.ABS(Series)
QA.MAX(A, B)
QA.MIN(A, B)
QA.CROSS(A, B)
QA.COUNT(COND, N)
QA.IF(COND, V1, V2)
QA.REF(Series, N)
QA.STD(Series, N)
QA.AVEDEV(Series, N)
QA.BBIBOLL(Series, N1, N2, N3, N4, N, M)
```
应用级指标  add_func(func)
```python
import QUANTAXIS as QA
QA.QA_indicator_OSC(DataFrame, N, M)
QA.QA_indicator_BBI(DataFrame, N1, N2, N3, N4)
QA.QA_indicator_PBX(DataFrame, N1, N2, N3, N4, N5, N6)
QA.QA_indicator_BOLL(DataFrame, N)
QA.QA_indicator_ROC(DataFrame, N, M)
QA.QA_indicator_MTM(DataFrame, N, M)
QA.QA_indicator_KDJ(DataFrame, N=9, M1=3, M2=3)
QA.QA_indicator_MFI(DataFrame, N)
QA.QA_indicator_ATR(DataFrame, N)
QA.QA_indicator_SKDJ(DataFrame, N, M)
QA.QA_indicator_WR(DataFrame, N, N1)
QA.QA_indicator_BIAS(DataFrame, N1, N2, N3)
QA.QA_indicator_RSI(DataFrame, N1, N2, N3)
QA.QA_indicator_ADTM(DataFrame, N, M)
QA.QA_indicator_DDI(DataFrame, N, N1, M, M1)
QA.QA_indicator_CCI(DataFrame, N=14)
```
自己写一个指标:

比如 绝路航标
```python
import QUANTAXIS as QA
def JLHB(data, m=7, n=5):
    """
    通达信定义
    VAR1:=(CLOSE-LLV(LOW,60))/(HHV(HIGH,60)-LLV(LOW,60))*80; 
    B:SMA(VAR1,N,1); 
    VAR2:SMA(B,M,1); 
    绝路航标:IF(CROSS(B,VAR2) AND B<40,50,0);
    """
    var1 = (data['close'] - QA.LLV(data['low'], 60)) / \
        (QA.HHV(data['high'], 60) - QA.LLV(data['low'], 60)) * 80
    B = QA.SMA(var1, m)
    var2 = QA.SMA(B, n)
    if QA.CROSS(B,var2) and B[-1]<40:
        return 1
    else:
        return 0

# 得到指标
QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-03-31').to_qfq().add_func(JLHB)
```

### QUANTAXIS的行情分析/研究用


主要是针对行情的各种统计学特征/指标等分析,支持QA_DataStruct_系列的add_func()功能

接收DataFrame形式的行情以及QUANTAXIS.QADATA格式的行情

目前有:


(属性)

- 一阶差分
- 样本方差
- 方差
- 标准差
- 样本标准差
- 平均数
- 调和平均数
- 众数
- 振幅(极差)
- 偏度
- 峰度
- 百分比变化
- 平均绝对偏差 

```python
import QUANTAXIS as QA

data=QA.QA_fetch_stock_day_adv('600066','2013-12-01','2017-10-01') #[可选to_qfq(),to_hfq()]
s=QA.QA_Analysis_stock(data)
# s 的属性是( < QA_Analysis_Stock > )

s.open # 开盘价序列
s.close # 收盘价序列
s.high # 最高价序列
s.low # 最低价序列
s.vol  # 量
s.volume # 同vol
s.date  # 日期
s.datetime
s.index  # 索引
s.price  # 平均价(O+H+L+C)/4
s.mean # price的平均数
s.max  # price的最大值
s.min # price的最小值
s.mad # price的平均绝对偏差
s.mode  # price的众数(没啥用)
s.price_diff # price的一阶差分
s.variance # price的方差
s.pvariance # price的样本方差
s.stdev  # price的标准差
s.pstdev # price的样本标准差
s.mean_harmonic # price的调和平均数
s.amplitude  #price的振幅[极差]
s.skewnewss # price的峰度 (4阶中心距)
s.kurtosis  # price的偏度 (3阶中心距)
s.pct_change # price的百分比变化序列


s.add_func(QA.QA_indicator_CCI) # 指标计算, 和DataStruct用法一致

```

### QUANTAXIS的api
```python

import QUANTAXIS as QA

"""
QA.QA_fetch_get_  系列:
从网上获取数据
"""


QA.QA_util_log_info('日线数据')
QA.QA_util_log_info('不复权')  
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31')


QA.QA_util_log_info('前复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','01')


QA.QA_util_log_info('后复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','02')


QA.QA_util_log_info('定点前复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','03')


QA.QA_util_log_info('定点后复权')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001','2017-01-01','2017-01-31','04')




QA.QA_util_log_info('分钟线')
QA.QA_util_log_info('1min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','1min')


QA.QA_util_log_info('5min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','5min')


QA.QA_util_log_info('15min')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_min('000001','2017-07-01','2017-08-01','15min')




QA.QA_util_log_info('除权除息')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_xdxr('00001')




QA.QA_util_log_info('股票列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('stock')


QA.QA_util_log_info('指数列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('index')


QA.QA_util_log_info('全部列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_list('all')




QA.QA_util_log_info('指数日线')
data=QA.QAFetch.QATdx.QA_fetch_get_index_day('000001','2017-01-01','2017-09-01')




QA.QA_util_log_info('指数分钟线')
QA.QA_util_log_info('1min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','1min')


QA.QA_util_log_info('5min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','5min')


QA.QA_util_log_info('15min')
data=QA.QAFetch.QATdx.QA_fetch_get_index_min('000001','2017-07-01','2017-08-01','15min')



QA.QA_util_log_info('最后一次交易价格')
QA.QA_util_log_info('参数为列表')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest(['000001','000002'])


QA.QA_util_log_info('参数为一只股票')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_latest('000001')




QA.QA_util_log_info('实时价格')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_realtime(['000001','000002'])




QA.QA_util_log_info('分笔成交')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_transaction('000001','2001-01-01','2001-01-15')

QA.QA_util_log_info('板块数据')
data=QA.QAFetch.QATdx.QA_fetch_get_stock_block()


"""
QA.QA_fetch_ 系列 
从本地数据库获取数据
"""
# 股票
QA_fetch_stock_day_adv(code,start,end)
QA_fetch_stock_min_adv(code,start,end,type_='1min') # type_可以选1min/5min/15min/30min/60min 
# 指数/ETF
QA_fetch_index_day_adv(code,start,end)
QA_fetch_index_min_adv(code,start,end,type_='1min') # type_可以选1min/5min/15min/30min/60min 
# 板块
QA_fetch_stock_block_adv(code)

```