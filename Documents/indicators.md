# QUANTAXIS的指标系统
<!-- TOC -->

- [QUANTAXIS的指标系统](#quantaxis的指标系统)
    - [指标计算入口](#指标计算入口)
        - [基础类指标 [基本和同花顺/通达信一致]](#基础类指标-基本和同花顺通达信一致)
        - [应用级指标  add_func(func)](#应用级指标--add_funcfunc)
        - [得到指标](#得到指标)
    - [QUANTAXIS的指标类 QA_DataStruct_Indicators()](#quantaxis的指标类-qa_datastruct_indicators)
        - [指标类可以直接加载计算出来的指标](#指标类可以直接加载计算出来的指标)
        - [获取一段时段时间的某个股票的指标序列](#获取一段时段时间的某个股票的指标序列)
        - [获取一个股票的指标序列](#获取一个股票的指标序列)
        - [获取某一个时刻的某个股票的某个指标值](#获取某一个时刻的某个股票的某个指标值)
        - [获取某个时刻某个股票的所有指标值](#获取某个时刻某个股票的所有指标值)

<!-- /TOC -->
## 指标计算入口
QUANTAXIS的核心数据结构有一个方法叫add_func(func,*args,**kwargs),作为一个指标入口,会返回一个和DataStruct中股票数量一致长度的Dataframe

QUANTAXIS有两种类型的指标:

- 基础指标(输入为Series的指标)
- 应用级指标(可应用于DataStruct的指标)

其中,基础指标是为了应用级指标做准备的,及对应于Series的分析和dataframe的分析的关系

### 基础类指标 [基本和同花顺/通达信一致]
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
### 应用级指标  add_func(func)
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
    return pd.DataFrame({'JLHB':QA.CROSS(B,var2)*(B<40)})
```
金叉死叉
```python        
def MACD_JCSC(dataframe, SHORT=12, LONG=26, M=9):
    """
    1.DIF向上突破DEA，买入信号参考。
    2.DIF向下跌破DEA，卖出信号参考。
    """
    CLOSE = dataframe.close
    DIFF = QA.EMA(CLOSE, SHORT) - QA.EMA(CLOSE, LONG)
    DEA = QA.EMA(DIFF, M)
    MACD = 2*(DIFF-DEA)

    CROSS_JC = QA.CROSS(DIFF, DEA)
    CROSS_SC = QA.CROSS(DEA, DIFF)
    ZERO = 0
    return pd.DataFrame({'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD, 'CROSS_JC': CROSS_JC, 'CROSS_SC': CROSS_SC, 'ZERO': ZERO})
```

### 得到指标

QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-05-31').to_qfq().add_func(JLHB)



## QUANTAXIS的指标类 QA_DataStruct_Indicators()

(新增于1.0.42)


### 指标类可以直接加载计算出来的指标

```python
ind=data.add_func(QA.QA_indicator_WR,1,2)
inc=QA.QA_DataStruct_Indicators(ind)
```
```
inc
< QA_DATASTRUCT_INDICATOR FROM 2018-01-02 00:00:00 TO 2018-01-31 00:00:00 WITH 2 CODES >
```

### 获取一段时段时间的某个股票的指标序列
```python
inc.get_timerange('2018-01-07','2018-01-12','000001')
		                WR1	        WR2
date	code		
2018-01-08	000001	76.744186	79.591837
2018-01-09	000001	42.857143	48.837209
2018-01-10	000001	3.508772	3.508772
2018-01-11	000001	59.375000	28.358209
2018-01-12	000001	48.148148	31.707317
```
### 获取一个股票的指标序列

```python
inc.get_code('000002')

                    WR1	        WR2
date	code		
2018-01-02	000002	27.922078	NaN
2018-01-03	000002	93.548387	62.231760
2018-01-04	000002	28.671329	39.285714
2018-01-05	000002	36.363636	29.629630
2018-01-08	000002	52.432432	23.317308
2018-01-09	000002	23.275862	55.721393
2018-01-10	000002	85.833333	58.857143
2018-01-11	000002	50.806452	71.759259
2018-01-12	000002	69.934641	51.442308
2018-01-15	000002	38.075314	31.271478
2018-01-16	000002	11.627907	9.823183
2018-01-17	000002	36.086957	21.627907
2018-01-18	000002	50.574713	37.606838
2018-01-19	000002	90.760870	76.255708
2018-01-22	000002	23.308271	60.465116
2018-01-23	000002	34.868421	17.666667
2018-01-24	000002	62.359551	49.333333
2018-01-25	000002	39.655172	59.302326
2018-01-26	000002	40.259740	46.551724
2018-01-29	000002	80.566802	81.322957
2018-01-30	000002	94.797688	97.902098
2018-01-31	000002	9.345794	18.487395
```

### 获取某一个时刻的某个股票的某个指标值
```python
inc.get_indicator('2018-01-12','000001','WR1')

WR1    48.148148
Name: (2018-01-12 00:00:00, 000001), dtype: float64
```
### 获取某个时刻某个股票的所有指标值
```python
inc.get_indicator('2018-01-12','000001')

WR1    48.148148
WR2    31.707317
Name: (2018-01-12 00:00:00, 000001), dtype: float64

```
