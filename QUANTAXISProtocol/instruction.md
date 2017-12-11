

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
### QUANTAXIS的核心数据结构

QA_DataStruct


属性用@property装饰器装饰,进行懒运算 提高效率

DataStruct具有的功能:

- 数据容器
- 数据变换 [分拆/合并/倒序] split/merge/reverse
- 数据透视 pivot
- 数据筛选 select_time/select_time_with_gap/select_code/get_bar
- 数据复权 to_qfq/to_hfq
- 数据显示 show
- 格式变换 to_json/to_pandas/to_list/to_numpy
- 数据库式查询  query
- 画图 plot
- 计算指标 add_func


QA_DataStruct_Stock_block

- (属性)该类下的所有板块名称 block_name
- 查询某一只股票所在的所有板块 get_code(code)
- 查询某一个板块下的所有股票 get_block(block)
- 展示当前类下的所有数据 show





我们可以通过 
```
import QUANTAXIS as QA

# QA.QA_fetch_stock_day_adv
# QA.QA_fetch_stock_min_adv
# QA.QA_fetch_index_day_adv
# QA.QA_fetch_index_min_adv

```
day线的参数是code, start, end
min线的参数是code, start, end, type_='1min'

其中 code 可以是一个股票,也可以是一列股票(list)

取一个股票的数据
```
QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-10-01')
In [5]: QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-10-01')
Out[5]: QA_DataStruct_Stock_day with 1 securities
```
取多个股票的数据
```
QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-01-01','2017-10-01')
In [6]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-01-01','2017-10-01')
Out[6]: QA_DataStruct_Stock_day with 2 securities
```
显示结构体的数据 .data
```
In [10]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').data
Out[10]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-26 000001  000001  11.26  11.30  10.96  11.05  967460.0 2017-09-26
2017-09-27 000001  000001  11.01  11.08  10.90  10.93  727188.0 2017-09-27
2017-09-28 000001  000001  10.98  10.98  10.82  10.88  517220.0 2017-09-28
2017-09-29 000001  000001  10.92  11.16  10.86  11.11  682280.0 2017-09-29
2017-09-20 000002  000002  28.50  29.55  28.00  28.73  613095.0 2017-09-20
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
2017-09-25 000002  000002  27.20  27.20  26.10  26.12  722702.0 2017-09-25
2017-09-26 000002  000002  26.12  27.22  26.10  26.76  593044.0 2017-09-26
2017-09-27 000002  000002  27.00  27.28  26.52  26.84  367534.0 2017-09-27
2017-09-28 000002  000002  27.00  27.15  26.40  26.41  262347.0 2017-09-28
2017-09-29 000002  000002  26.56  26.80  26.00  26.25  345752.0 2017-09-29
```
显示结构体的开/高/收/低 .open/.high/.close/.low
```
In [5]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').high
Out[5]:
date        code
2017-09-20  000001    11.37
2017-09-21  000001    11.51
2017-09-22  000001    11.52
2017-09-25  000001    11.45
2017-09-26  000001    11.30
2017-09-27  000001    11.08
2017-09-28  000001    10.98
2017-09-29  000001    11.16
2017-09-20  000002    29.55
2017-09-21  000002    29.06
2017-09-22  000002    28.67
2017-09-25  000002    27.20
2017-09-26  000002    27.22
2017-09-27  000002    27.28
2017-09-28  000002    27.15
2017-09-29  000002    26.80
Name: high, dtype: float64
```
数据结构复权to_qfq()/to_hfq()

返回的是一个DataStruct,用.data展示返回的数据的结构

其中DataStruct.if_fq的属性会改变
```
In [4]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').to_qfq().data

Out[4]:
                     code   open   high    low  close    volume       date  \
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-26 000001  000001  11.26  11.30  10.96  11.05  967460.0 2017-09-26
2017-09-27 000001  000001  11.01  11.08  10.90  10.93  727188.0 2017-09-27
2017-09-28 000001  000001  10.98  10.98  10.82  10.88  517220.0 2017-09-28
2017-09-29 000001  000001  10.92  11.16  10.86  11.11  682280.0 2017-09-29
2017-09-20 000002  000002  28.50  29.55  28.00  28.73  613095.0 2017-09-20
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
2017-09-25 000002  000002  27.20  27.20  26.10  26.12  722702.0 2017-09-25
2017-09-26 000002  000002  26.12  27.22  26.10  26.76  593044.0 2017-09-26
2017-09-27 000002  000002  27.00  27.28  26.52  26.84  367534.0 2017-09-27
2017-09-28 000002  000002  27.00  27.15  26.40  26.41  262347.0 2017-09-28
2017-09-29 000002  000002  26.56  26.80  26.00  26.25  345752.0 2017-09-29

                   preclose  adj
date       code
2017-09-20 000001       NaN  1.0
2017-09-21 000001     11.29  1.0
2017-09-22 000001     11.46  1.0
2017-09-25 000001     11.44  1.0
2017-09-26 000001     11.29  1.0
2017-09-27 000001     11.05  1.0
2017-09-28 000001     10.93  1.0
2017-09-29 000001     10.88  1.0
2017-09-20 000002       NaN  1.0
2017-09-21 000002     28.73  1.0
2017-09-22 000002     28.40  1.0
2017-09-25 000002     27.81  1.0
2017-09-26 000002     26.12  1.0
2017-09-27 000002     26.76  1.0
2017-09-28 000002     26.84  1.0
2017-09-29 000002     26.41  1.0
```
数据透视 .pivot()
```
In [6]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').pivot('open')
Out[6]:
code        000001  000002
date
2017-09-20   11.14   28.50
2017-09-21   11.26   28.50
2017-09-22   11.43   28.39
2017-09-25   11.44   27.20
2017-09-26   11.26   26.12
2017-09-27   11.01   27.00
2017-09-28   10.98   27.00
2017-09-29   10.92   26.56
```
数据的时间筛选.select_time(start,end)
```
In [10]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time('2017-09-20','2017-09-25')
Out[10]: QA_DataStruct_Stock_day with 2 securities

In [11]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time('2017-09-20','2017-09-25').data
Out[11]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-20 000002  000002  28.50  29.55  28.00  28.73  613095.0 2017-09-20
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
2017-09-25 000002  000002  27.20  27.20  26.10  26.12  722702.0 2017-09-25
```
数据按时间往前/往后推 select_time_with_gap(time,gap,methods)

time是你选择的时间
gap是长度 (int)
methods有 '<=','lte','<','lt','eq','==','>','gt','>=','gte'的选项
```
In [14]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time_with_gap('2017-09-20',2,'gt')
Out[14]: QA_DataStruct_Stock_day with 2 securities

In [15]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_time_with_gap('2017-09-20',2,'gt').data
Out[15]:
                     code   open   high    low  close    volume       date
date       code
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-21 000002  000002  28.50  29.06  27.75  28.40  536324.0 2017-09-21
2017-09-22 000002  000002  28.39  28.67  27.52  27.81  423093.0 2017-09-22
```
选取结构组里面某一只股票select_code(code)

```
In [16]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_code('000001')
Out[16]: QA_DataStruct_Stock_day with 1 securities
In [17]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').select_code('000001').data
Out[17]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20
2017-09-21 000001  000001  11.26  11.51  11.20  11.46  692407.0 2017-09-21
2017-09-22 000001  000001  11.43  11.52  11.31  11.44  593927.0 2017-09-22
2017-09-25 000001  000001  11.44  11.45  11.18  11.29  532391.0 2017-09-25
2017-09-26 000001  000001  11.26  11.30  10.96  11.05  967460.0 2017-09-26
2017-09-27 000001  000001  11.01  11.08  10.90  10.93  727188.0 2017-09-27
2017-09-28 000001  000001  10.98  10.98  10.82  10.88  517220.0 2017-09-28
2017-09-29 000001  000001  10.92  11.16  10.86  11.11  682280.0 2017-09-29
```
取某一只股票的某一个时间的bar(code,time,if_trade)

第三个选项 默认是True  
第三选项的意义在于,如果出现了停牌,参数如果是True 那么就会返回空值 而如果是False,就会返回停牌前最后一个交易日的值
```
In [18]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').get_bar('000001','2017-09-20',True)
Out[18]: QA_DataStruct_Stock_day with 1 securities

In [19]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').get_bar('000001','2017-09-20',True).data
Out[19]:
                     code   open   high    low  close    volume       date
date       code
2017-09-20 000001  000001  11.14  11.37  11.05  11.29  787154.0 2017-09-20

```
画图 plot(code)

如果是()空值 就会把全部的股票都画出来
```
In [20]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').plot()
QUANTAXIS>> The Pic has been saved to your path: .\QA_stock_day_codepackage_bfq.html

In [21]: QA.QA_fetch_stock_day_adv(['000001','000002'],'2017-09-20','2017-10-01').plot('000001')
QUANTAXIS>> The Pic has been saved to your path: .\QA_stock_day_000001_bfq.html

```

![](http://osnhakmay.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20171004125336.png)

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
    B = QA.MA(var1, m)
    var2 = QA.MA(B, n)
    if QA.CROSS(B,var2) and B[-1]<40:
        return 1
    else:
        return 0

# 得到指标
QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-01-31').to_qfq().add_func(JLHB)
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