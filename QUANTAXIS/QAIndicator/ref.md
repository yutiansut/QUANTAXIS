JOINQUANT 技术分析指标（持续更新中~）

因子说明

为了让用户有更多可直接调用的技术分析指标因子，我们计划基于通达信、东方财富、同花顺等的公式，来完善我们的技术分析指标因子库。

我们给出了公式的API、参数说明、返回值的结果及类型说明、备注（相较于上述三家结果及算法的比对）、用法注释及示例，旨在帮助您更方便、更快速的在策略研究中使用这些因子函数。

重要提示 ★

在使用之前请导入 technical_analysis 库

# 导入 technical_analysis 库
>>> from jqlib.technical_analysis import *
超买超卖型

ACCER-幅度涨速

ACCER(security_list, check_date, N = 8)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

ACCER 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 0.0013989466754443464, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.024078586658544048, ‘601211.XSHG’: -0.0056372951942572323}
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同，东方财富和同花顺没有该指标
用法注释：

算法：先求出斜率，再对其价格进行归一
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 ACCER 值
ACCER1 = ACCER(security_list1, check_date='2017-01-04', N = 8)
print ACCER1[security_list1]

# 输出 security_list2 的 ACCER 值
ACCER2 = ACCER(security_list2, check_date='2017-01-04', N = 8)
for stock in security_list2:
    print ACCER2[stock]
ADTM-动态买卖气指标

ADTM(security_list, check_date, N = 23, M = 8)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

ADTM和MAADTM 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.49999999999999584, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.83612040133779286, ‘601211.XSHG’: -0.050991501416427533}, {‘000001.XSHE’: 0.46909197819443404, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.79181488308861514, ‘601211.XSHG’: 0.10434158941106236})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

该指标在+1到-1之间波动;
低于-0.5时为很好的买入点,高于+0.5时需注意风险.
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 ADTM 值
ADTM1, MAADTM1 = ADTM(security_list1, check_date='2017-01-04', N = 23, M = 8)
print ADTM1[security_list1]
print MAADTM1[security_list1]

# 输出 security_list2 的 ADTM 值
ADTM2, MAADTM2 = ADTM(security_list2, check_date='2017-01-04', N = 23, M = 8)
for stock in security_list2:
    print ADTM2[stock]
    print MAADTM2[stock]
ATR-真实波幅

ATR(security_list, check_date, timeperiod=14)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数 timeperiod
返回：

MTR和ATR 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 0.080000000000000071, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.16000000000000014, ‘601211.XSHG’: 0.19000000000000128}, {‘000001.XSHE’: 0.059999999999999866, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.51142857142857168, ‘601211.XSHG’: 0.28571428571428648})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

算法：今日振幅、今日最高与昨收差价、今日最低与昨收差价中的最大值，为真实波幅，求真实波幅的N日移动平均 
参数：N　天数，一般取14

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 ATR 值
MTR1,ATR1 = ATR(security_list1, check_date='2017-01-04', timeperiod=14)
print MTR1[security_list1]
print ATR1[security_list1]

# 输出 security_list2 的 ATR 值
MTR2,ATR2 = ATR(security_list2, check_date='2017-01-04', timeperiod=14)
for stock in security_list2:
    print MTR2[stock]
    print ATR2[stock]
BIAS-乖离率

BIAS(security_list,check_date, N1=6, N2=12, N3=24)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1: 统计的天数 N1
N2: 统计的天数 N2
N3: 统计的天数 N3
返回：

BIAS1, BIAS2, BIAS3 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 0.9012256669069999, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.064516129032250957, ‘601211.XSHG’: 0.285408490902611}, {‘000001.XSHE’: 1.4222302744813846, ‘603177.XSHG’: nan, ‘000002.XSHE’: -0.54106047853793771, ‘601211.XSHG’: 1.0015719739501157}, {‘000001.XSHE’: 1.8605285902742783, ‘603177.XSHG’: nan, ‘000002.XSHE’: -0.51514361883382098, ‘601211.XSHG’: 1.9332321011717053})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

1.本指标的乖离极限值随个股不同而不同，使用者可利用参考线设定，固定其乖离范围； 
2.当股价的正乖离扩大到一定极限时，股价会产生向下拉回的作用力； 
3.当股价的负乖离扩大到一定极限时，股价会产生向上拉升的作用力； 
4.本指标可设参考线。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 BIAS 值
BIAS11,BIAS12,BIAS13 = BIAS(security_list1,check_date='2017-01-04', N1=6, N2=12, N3=24)
print BIAS11[security_list1]
print BIAS12[security_list1]
print BIAS13[security_list1]

# 输出 security_list2 的 BIAS 值
BIAS21,BIAS22,BIAS23 = BIAS(security_list2,check_date='2017-01-04', N1=6, N2=12, N3=24)
for stock in security_list2:
    print BIAS21[stock]
    print BIAS22[stock]
    print BIAS23[stock]
BIAS_QL-乖离率_传统版

BIAS_QL(security_list, check_date, N = 6, M = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

BIAS和BIASMA 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 48.10992396473096, ‘603177.XSHG’: nan, ‘000002.XSHE’: 76.922476397442992, ‘601211.XSHG’: 42.883942027049542}, {‘000001.XSHE’: 44.033385880780266, ‘603177.XSHG’: nan, ‘000002.XSHE’: 79.616029960653222, ‘601211.XSHG’: 32.35472793345135})
备注：

返回结果与通达信和东方财富一致，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

因为BIAS_QL的计算公式与BIAS36相似，而常见的炒股软件中均没有找到BIAS_QL的用法注释，所以此处使用了BIAS36的用法注释；
本指标的乖离极限值随个股不同而不同，使用者可利用参考线设定，固定其乖离范围。※一般6-12BIAS信号的可靠度比3-6BIAS佳；
当股价的正乖离扩大到一定极限时，股价会产生向下拉回的作用力；
当股价的负乖离扩大到一定极限时，股价会产生向上拉升的作用力；
本指标可设参考线。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 BIAS_QL 值
BIAS1, BIASMA1 = BIAS_QL(security_list1, check_date = '2017-01-04', N = 6, M = 6)
print BIAS1[security_list1]
print BIASMA1[security_list1]

# 输出 security_list2 的 BIAS_QL 值
BIAS2, BIASMA2 = BIAS_QL(security_list2, check_date = '2017-01-04', N = 6, M = 6)
for stock in security_list2:
    print BIAS2[stock]
    print BIASMA2[stock]
BIAS36-三六乖离

BIAS36(security_list, check_date, M = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
M：统计的天数 M
返回：

BIAS36, BIAS612和MABIAS 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.021666666666666501, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.92333333333333201, ‘601211.XSHG’: -0.2083333333333357}, {‘000001.XSHE’: -0.054999999999999716, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.1916666666666735, ‘601211.XSHG’: -0.37666666666667226}, {‘000001.XSHE’: -0.020555555555556992, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.65916666666666279, ‘601211.XSHG’: -0.17138888888888873})
备注：

返回结果与通达信和东方财富一致，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

本指标的乖离极限值随个股不同而不同，使用者可利用参考线设定，固定其乖离范围。※一般6-12BIAS信号的可靠度比3-6BIAS佳；
当股价的正乖离扩大到一定极限时，股价会产生向下拉回的作用力；
当股价的负乖离扩大到一定极限时，股价会产生向上拉升的作用力；
本指标可设参考线。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 BIAS36 值
BIAS36_1, BIAS612_1, ABIAS_1 = BIAS_36(security_list1, check_date='2017-01-04', M = 6)
print BIAS36_1[security_list1]
print BIAS612_1[security_list1]
print ABIAS_1[security_list1]

# 输出 security_list2 的 BIAS36 值
BIAS36_2, BIAS612_2, ABIAS_2 = BIAS_36(security_list2, check_date='2017-01-04', M = 6)
for stock in security_list2:
    print BIAS36_2[stock]
    print BIAS612_2[stock]
    print ABIAS_2[stock]
CCI-商品路径指标

CCI(security_list, check_date, N=14)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

CCI 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 176.62274280137152, ‘603177.XSHG’: nan, ‘000002.XSHE’: -30.935837245695815, ‘601211.XSHG’: 98.68173258003705}
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

1.CCI 为正值时，视为多头市场；为负值时，视为空头市场； 
2.常态行情时，CCI 波动于±100 的间；强势行情，CCI 会超出±100 ； 
3.CCI>100 时，买进，直到CCI<100 时，卖出； 
4.CCI<-100 时，放空，直到CCI>-100 时，回补。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 CCI 值
CCI1 = CCI(security_list1, check_date='2017-01-04', N=14)
print CCI1[security_list1]

# 输出 security_list2 的 CCI 值
CCI2 = CCI(security_list2, check_date='2017-01-04', N=14)
for stock in security_list2:
    print CCI2[stock]
CYF-市场能量

CYF(security_list, check_date, N = 21)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

CYF 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 25.457927713284477, ‘603177.XSHG’: nan, ‘000002.XSHE’: 34.823659982605108, ‘601211.XSHG’: 47.605522169406555}
备注：

返回结果与通达信和东方财富均不一致，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
因本指标调用的API较多，该程序计算速度较慢
用法注释：

CYF反映了市场公众的状态和追涨热情,又称市场能量指标;
使用CYF判断股票的活跃程度, CYF小于10的股票是冷门股，CYF在20到40之间是活跃股，CYF大于50是热门股;
CYF与股价顶背离时,易形成反转.
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CYF 值
CYF1 = CYF(security_list1, check_date='2017-01-04', N = 21)
print CYF1[security_list1]

# 输出 security_list2 的 CYF 值
CYF2 = CYF(security_list2, check_date='2017-01-04', N = 21)
for stock in security_list2:
    print CYF2[stock]
DKX-多空线

DKX(security_list, check_date, M = 10)
参数：

security_list：股票列表
check_date：要查询数据的日期
M：统计的天数 M
返回：

DKX和MADKX 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.7320238095238096, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.6065, ‘601211.XSHG’: 18.081222222222227}, {‘000001.XSHE’: 8.7608388888888875, ‘603177.XSHG’: nan, ‘000002.XSHE’: 16.825250793650795, ‘601211.XSHG’: 18.38326587301588})
备注：

返回结果与通达信和东方财富一致，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

当多空线上穿其均线时为买入信号;
当多空线下穿其均线时为卖出信号。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 DKX 值
DKX1,MADKX1 = DKX(security_list1, check_date='2017-01-04', M = 10)
print DKX1[security_list1]
print MADKX1[security_list1]

# 输出 security_list2 的 DKX 值
DKX2,MADKX2 = DKX(security_list2, check_date='2017-01-04', M = 10)
for stock in security_list2:
    print DKX2[stock]
    print MADKX2[stock]
KD-随机指标KD

KD(security_list, check_date, N = 9, M1 = 3, M2 = 3)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M1：统计的天数 M1
M2：统计的天数 M2
返回：

K和D 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 76.634909558440839, ‘603177.XSHG’: nan, ‘000002.XSHE’: 31.205826728484286, ‘601211.XSHG’: 65.666306018342183}, {‘000001.XSHE’: 77.290976650878633, ‘603177.XSHG’: nan, ‘000002.XSHE’: 32.552242430383409, ‘601211.XSHG’: 64.593395785918702})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

KD的计算公式与SKDJ的不太大，而常见的炒股软件中均没有找到KD的用法注释，所以该处的用法注释使用的是公式SKDJ的；
指标>80 时，回档机率大；指标<20 时，反弹机率大；
K在20左右向上交叉D时，视为买进信号；
K在80左右向下交叉D时，视为卖出信号；
SKDJ波动于50左右的任何讯号，其作用不大。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 KD值
K1, D1 = KD(security_list1, check_date = '2017-01-04', N = 9, M1 = 3, M2 = 3)
print K1[security_list1]
print D1[security_list1]

# 输出 security_list2 的 KD 值
K2, D2 = KD(security_list2, check_date = '2017-01-04', N = 9, M1 = 3, M2 = 3)
for stock in security_list2:
    print K2[stock]
    print D2[stock]
KDJ-随机指标

KDJ(security_list, check_date, N =9, M1=3, M2=3) 
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M1：统计的天数 M1
M2：统计的天数 M2
返回：

K，D和J 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 89.145187806127595, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.523907534762358, ‘601211.XSHG’: 82.545216532766361}, {‘000001.XSHE’: 82.915346288340473, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.246652224886216, ‘601211.XSHG’: 80.903864946907802}, {‘000001.XSHE’: 101.60487084170185, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.078418154514644, ‘601211.XSHG’: 85.827919704483492})
备注：

返回结果与通达信、东方财富和同花顺结果一致
计算方式与通达信、东方财富和同花顺相同
用法注释：

1.指标>80 时，回档机率大；指标<20时，反弹机率大； 
2.K在20左右向上交叉D时，视为买进信号； 
3.K在80左右向下交叉D时，视为卖出信号； 
4.J>100 时，股价易反转下跌；J<0 时，股价易反转上涨； 
5.KDJ 波动于50左右的任何信号，其作用不大。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 KDJ 值
K1,D1,J1 = KDJ(security_list1, check_date='2017-01-04', N =9, M1=3, M2=3) 
print K1[security_list1]
print D1[security_list1]
print J1[security_list1]

# 输出 security_list2 的 KDJ 值
K2,D2,J2 = KDJ(security_list2, check_date='2017-01-04', N =9, M1=3, M2=3) 
for stock in security_list2:
    print K2[stock]
    print D2[stock]
    print J2[stock]
SKDJ-慢速随机指标

SKDJ(security_list, check_date, N = 9, M = 3)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

K和D 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 43.670179685638736, ‘603177.XSHG’: nan, ‘000002.XSHE’: 88.536829377842508, ‘601211.XSHG’: 11.706561251360608}, {‘000001.XSHE’: 39.385998813653607, ‘603177.XSHG’: nan, ‘000002.XSHE’: 83.231798914083683, ‘601211.XSHG’: 14.897182159244849})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

指标>80 时，回档机率大；指标<20 时，反弹机率大；
K在20左右向上交叉D时，视为买进信号；
K在80左右向下交叉D时，视为卖出信号；
SKDJ波动于50左右的任何讯号，其作用不大。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 SKDJ 值
K1, D1 = SKDJ(security_list1, check_date = '2017-01-04', N = 9, M = 3)
print K1[security_list1]
print D1[security_list1]

# 输出 security_list2 的 SKDJ 值
K2, D2 = SKDJ(security_list2, check_date = '2017-01-04', N = 9, M = 3)
for stock in security_list2:
    print K2[stock]
    print D2[stock]
MFI-资金流量指标

MFI(security_list, check_date, timeperiod=14)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数 N
返回：

MFI 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 49.042496052317411, ‘603177.XSHG’: nan, ‘000002.XSHE’: 82.747463608411636, ‘601211.XSHG’: 24.455594865835923}
备注：

返回结果与通达信、同花顺、东方财富结果一致
计算方式与同花顺、东方财富和通达信相同
用法注释：

1.MFI>80 为超买，当其回头向下跌破80 时，为短线卖出时机； 
2.MFI<20 为超卖，当其回头向上突破20 时，为短线买进时机； 
3.MFI>80，而产生背离现象时，视为卖出信号； 
4.MFI<20，而产生背离现象时，视为买进信号。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 MFI 值
MFI1 = MFI(security_list1,check_date='2017-01-04', timeperiod=14)
print MFI1[security_list1]

# 输出 security_list2 的 MFI 值
MFI2 = MFI(security_list2,check_date='2017-01-04', timeperiod=14)
for stock in security_list2:
    print MFI2[stock]
MTM-动量线

MTM(security_list, check_date, timeperiod=14)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数 N
返回：

MTM的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: -0.12999999999999901, ‘603177.XSHG’: nan, ‘000002.XSHE’: 5.9499999999999993, ‘601211.XSHG’: -1.2699999999999996}
备注：

返回结果与通达信、同花顺、东方财富结果一致
计算方式与通达信、同花顺和东方财富和相同
用法注释：

MTM线　:当日收盘价与N日前的收盘价的差； 
MTMMA线:对上面的差值求N日移动平均； 
参数：N 间隔天数，也是求移动平均的天数，一般取6用法： 
1.MTM从下向上突破MTMMA，买入信号； 
2.MTM从上向下跌破MTMMA，卖出信号； 
3.股价续创新高，而MTM未配合上升，意味上涨动力减弱； 
4.股价续创新低，而MTM未配合下降，意味下跌动力减弱； 
5.股价与MTM在低位同步上升，将有反弹行情；反之，从高位同步下降，将有回落走势。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 MTM 值
MTM1 = MTM(security_list1,check_date='2017-01-04', timeperiod=12)
print MTM1[security_list1]

# 输出 security_list2 的 MTM 值
MTM2= MTM(security_list2,check_date='2017-01-04', timeperiod=12)
for stock in security_list2:
    print MTM2[stock]
ROC-变动率指标

ROC(security_list, check_date, timeperiod=12)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数 N
返回：

ROC的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： {‘000001.XSHE’: -1.4557670772676223, ‘603177.XSHG’: nan, ‘000002.XSHE’: 33.999999999999986, ‘601211.XSHG’: -6.7302596714361336}
备注：

返回结果与通达信、同花顺和东方财富结果一致
计算方式与通达信、同花顺和东方财富相同
用法注释：

1.本指标的超买超卖界限值随个股不同而不同，使用者应自行调整； 
2.本指标的超买超卖范围，一般介于±6.5之间； 
3.本指标用法请参考MTM 指标用法； 
4.本指标可设参考线。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 ROC 值
ROC1 = ROC(security_list1,check_date='2017-01-04', timeperiod=12)
print ROC1[security_list1]

# 输出 security_list2 的 ROC 值
ROC2 = ROC(security_list2,check_date='2017-01-04', timeperiod=12)
for stock in security_list2:
    print ROC2[stock]
RSI-相对强弱指标

RSI(security_list, check_date, N1=6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数N1
返回：

RSI 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： {‘000001.XSHE’: 86.697784941552129, ‘603177.XSHG’: nan, ‘000002.XSHE’: 45.669839353084029, ‘601211.XSHG’: 65.952531344607962}
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

1.RSI>80 为超买，RSI<20 为超卖； 
2.RSI 以50为中界线，大于50视为多头行情，小于50视为空头行情； 
3.RSI 在80以上形成Ｍ头或头肩顶形态时，视为向下反转信号； 
4.RSI 在20以下形成Ｗ底或头肩底形态时，视为向上反转信号； 
5.RSI 向上突破其高点连线时，买进；RSI 向下跌破其低点连线时，卖出。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 RSI 值
RSI1 = RSI(security_list1, check_date='2017-01-04', N1=6)
print RSI1[security_list1]

# 输出 security_list2 的 RSI 值
RSI2 = RSI(security_list2, check_date='2017-01-04', N1=6)
for stock in security_list2:
    print RSI2[stock]
MARSI-相对强弱平均线

MARSI(security_list, check_date, M1 = 10, M2 = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
M1：统计的天数 M1
M2：统计的天数 M2
返回：

RSI10和RSI6 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 48.10992396473096, ‘603177.XSHG’: nan, ‘000002.XSHE’: 76.922476397442992, ‘601211.XSHG’: 42.883942027049542}, {‘000001.XSHE’: 44.033385880780266, ‘603177.XSHG’: nan, ‘000002.XSHE’: 79.616029960653222, ‘601211.XSHG’: 32.35472793345135})
备注：

返回结果与通达信一致，与同花顺和东方财富不一致
计算方式与通达信相同，与同花顺计算方式本质上相同，但参数不一致，东方财富没有该指标
用法注释：

RSI>20 为超买；RSI<20 为超卖；
RSI 以50为中界线，大于50视为多头行情，小于50视为空头行情；
RSI 在80以上形成Ｍ头或头肩顶形态时，视为向下反转信号；
RSI 在20以下形成Ｗ底或头肩底形态时，视为向上反转信号；
RSI 向上突破其高点连线时，买进；RSI 向下跌破其低点连线时，卖出。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 MARSI 值
RSI10_1, RSI6_1 = MARSI(security_list1, check_date = '2017-01-04', M1 = 10, M2 = 6)
print RSI10_1[security_list1]
print RSI6_1[security_list1]

# 输出 security_list2 的 MARSI 值
RSI10_2, RSI6_2 = MARSI(security_list2, check_date = '2017-01-04', M1 = 10, M2 = 6)
for stock in security_list2:
    print RSI10_2[stock]
    print RSI6_2[stock]
OSC-变动速率线

OSC(security_list, check_date, N = 20, M = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

OSC和MAOSC 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 7.3500000000001009, ‘603177.XSHG’: nan, ‘000002.XSHE’: -17.449999999998766, ‘601211.XSHG’: -5.150000000000432}, {‘000001.XSHE’: 10.992588074732661, ‘603177.XSHG’: nan, ‘000002.XSHE’: -6.6110853409889812, ‘601211.XSHG’: 8.2021191350369627})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

OSC 以100 为中轴线，OSC>100 为多头市场；OSC<100 为空头市场；
OSC 向上交叉其平均线时，买进；OSC 向下交叉其平均线时卖出；
OSC 在高水平或低水平与股价产生背离时，应注意股价随时有反转的可能；
OSC 的超买超卖界限值随个股不同而不同，使用者应自行调整
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 OSC 值
OSC1, MAOSC1 = OSC(security_list1, check_date = '2017-01-04', N = 20, M = 6)
print OSC1[security_list1]
print MAOSC1[security_list1]

# 输出 security_list2 的 OSC 值
OSC2, MAOSC2 = OSC(security_list2, check_date = '2017-01-04', N = 20, M = 6)
for stock in security_list2:
    print OSC2[stock]
    print MAOSC2[stock]
UDL-引力线

UDL(security_list, check_date, N1 = 3, N2 = 5, N3 = 10, N4 = 20, M = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数 N1
N2：统计的天数 N2
N3：统计的天数 N3
N4：统计的天数 N4
M：统计的天数 M
返回：

UDL和MAUDL 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 8.7100833333333352, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.746000000000006, ‘601211.XSHG’: 17.816458333333333}, {‘000001.XSHE’: 8.711291666666666, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.525548611111123, ‘601211.XSHG’: 18.064673611111122})
备注：

返回结果与通达信和同花顺一致，东方财富没有该指标
计算方式与通达信和同花顺相同，东方财富没有该指标
用法注释：

本指标的超买超卖界限值随个股不同而不同，使用者应自行调整；
使用时，可列出一年以上走势图，观察其常态性分布范围，然后用参考线设定其超买超卖范围。通常UDL 高于某个极限时，短期股价会下跌；UDL 低于某个极限时，短期股价会上涨；
本指标可设参考线。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 UDL 值
UDL1, MAUDL1 = UDL(security_list1, check_date = '2017-01-04', N1 = 3, N2 = 5, N3 = 10, N4 = 20, M = 6)
print UDL1[security_list1]
print MAUDL1[security_list1]

# 输出 security_list2 的 UDL 值
UDL2, MAUDL2 = UDL(security_list2, check_date = '2017-01-04', N1 = 3, N2 = 5, N3 = 10, N4 = 20, M = 6)
for stock in security_list2:
    print UDL2[stock]
    print MAUDL2[stock]
WR-威廉指标

WR(security_list, check_date, N = 10, N1 = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

WR和MAWR 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 57.50000000000005, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.0, ‘601211.XSHG’: 93.706293706293721}, {‘000001.XSHE’: 55.172413793103658, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.0, ‘601211.XSHG’: 88.157894736842152})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
方法注释：

WR波动于0 - 100，100置于顶部，0置于底部。
本指标以50为中轴线，高于50视为股价转强；低于50视为股价转弱
本指标高于20后再度向下跌破20，卖出；低于80后再度向上突破80，买进。
WR连续触底3 - 4次，股价向下反转机率大；连续触顶3 - 4次，股价向上反转机率大。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 WR 值
WR1, MAWR1 = WR(security_list1, check_date = '2017-01-04', N = 10, N1 = 6)
print WR1[security_list1]
print MAWR1[security_list1]

# 输出 security_list2 的 WR 值
WR2, MAWR2 = WR(security_list2, check_date = '2017-01-04', N = 10, N1 = 6)
for stock in security_list2:
    print WR2[stock]
    print MAWR2[stock]
LWR-LWR威廉指标

LWR(security_list, check_date, N = 9, M1 = 3, M2 = 3)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M1：统计的天数 M1
M2：统计的天数 M2
返回：

LWR1和LWR2 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 55.650573690335541, ‘603177.XSHG’: nan, ‘000002.XSHE’: 10.13678425444178, ‘601211.XSHG’: 87.916457180768532}, {‘000001.XSHE’: 58.489680228929586, ‘603177.XSHG’: nan, ‘000002.XSHE’: 16.390638110862337, ‘601211.XSHG’: 80.912153275638602})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

LWR2<30，超买；LWR2>70，超卖。
线LWR1向下跌破线LWR2，买进参考信号；线LWR1向上突破线LWR2，卖出参考信号。
线LWR1与线LWR2的交叉发生在30以下，70以上，才有效。
LWR指标不适于发行量小，交易不活跃的股票；
LWR指标对大盘和热门大盘股有极高准确性。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 LWR 值
LWR1, LWR2 = LWR(security_list1, check_date = '2017-01-04', N = 9, M1 = 3, M2 = 3)
print LWR1[security_list1]
print LWR2[security_list1]

# 输出 security_list2 的 LWR 值
LWR1, LWR2 = LWR(security_list2, check_date = '2017-01-04', N = 9, M1 = 3, M2 = 3)
for stock in security_list2:
    print LWR1[stock]
    print LWR2[stock]
TAPI-加权指数成交值

TAPI(index_stock, security_list, check_date, M=6)
参数：

security_list：股票列表
check_date：要查询数据的日期
M：统计的天数 M
返回：

TAPI和MATAPI 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 256244.00809560539, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2290672.9391872431, ‘601211.XSHG’: 295372.46021602425}, {‘000001.XSHE’: 305104.20587265556, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1682196.5742840525, ‘601211.XSHG’: 431300.71571008326})
备注：

返回结果与通达信和东方财富一致，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

先界定TAPI长期以来经常性的高低极限值，当TAPI触及顶端极限时，股价可能形成头部；当TAPI触及底端极限时，股价可能形成底部；
行情上涨，TAPI应伴随上涨；若不升反跌，则近期内将面临回档；
先前大盘量缩下跌，当其回升时，TAPI值却持续下跌，可视为买入信号。
示例：

# 大盘股票代码
index_stock = '399106.XSHE'
# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 TAPI 值
TAPI1,MATAPI1 = TAPI(index_stock, security_list1, check_date='2017-01-04', M=6)
print TAPI1[security_list1]
print MATAPI1[security_list1]

# 输出 security_list2 的 TAPI 值
TAPI2,MATAPI2 = TAPI(index_stock, security_list2, check_date='2017-01-04', M=6)
for stock in security_list2:
    print TAPI2[stock]
    print MATAPI2[stock]
FSL-分水岭

FSL(security_list, check_date)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

SWL和SWS 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.9778100759204698, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.894317966512268, ‘601211.XSHG’: 18.208534476715137}, {‘000001.XSHE’: 9.0214752948717933, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.072509500000002, ‘601211.XSHG’: 18.330323064102565})
备注：

返回结果与通达信和东方财富存在微小的差异，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

股价在分水岭之上为强势,反之为弱势.
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 FSL 值
SWL1,SWS1 = FSL(security_list1, check_date='2017-01-04')
print SWL1[security_list1]
print SWS1[security_list1]

# 输出 security_list2 的 FSL 值
SWL2,SWS2 = FSL(security_list2, check_date='2017-01-04')
for stock in security_list2:
    print SWL2[stock]
    print SWS2[stock]
趋势型

CHO-佳庆指标

CHO(security_list, check_date, N1 = 10, N2 = 20, M = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数 N1
N2: 统计的天数 N2
M: 统计的天数 M
返回：

CHO 和 MACHO 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: -2349.7877426190771, ‘603177.XSHG’: nan, ‘000002.XSHE’: 267047.22475180856, ‘601211.XSHG’: -1726.9088373843188}, {‘000001.XSHE’: -2304.8620185057907, ‘603177.XSHG’: nan, ‘000002.XSHE’: 292638.40931959258, ‘601211.XSHG’: -3050.487984994948})
备注：

返回结果与通达信、同花顺和东方财富结果均有不大于0.1的差异
计算方式与通达信、同花顺（交易量不是以手为单位）和东方财富相同
用法注释：

1.CHO 曲线产生急促的「凸起」时，代表行情即将向上或向下反转； 
2.股价>90 天平均线，CHO由负转正时，买进； 
3.股价<90 天平均线，CHO由正转负时，卖出； 
4.本指标也可设参考线，自定超买超卖的界限值； 
5.本指标须配合OBOS、ENVELOPE同时使用。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 CHO 值
CHO1,MACHO1 = CHO(security_list1,check_date='2017-01-04', N1 = 10, N2 = 20, M = 6)
print CHO1[security_list1]
print MACHO1[security_list1]

# 输出 security_list2 的 CHO 值
CHO2,MACHO2 = CHO(security_list2,check_date='2017-01-04', N1 = 10, N2 = 20, M = 6)
for stock in security_list2:
    print CHO2[stock]
    print MACHO2[stock]
CYE-市场趋势

CYE(security_list, check_date)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

CYEL和CYES的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.22946305644790699, ‘603177.XSHG’: nan, ‘000002.XSHE’: 4.3811058515459811, ‘601211.XSHG’: -0.38592508513052126}, {‘000001.XSHE’: 0.0057132410073656359, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.139178579978255, ‘601211.XSHG’: -0.26377299139325172})
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同，东方财富和同花顺没有该指标
用法注释：

CYE指标又叫趋势指标,是计算机模拟人的感觉用数值分析的方法对即日的K线进行一次拟合和趋势的判断;
CYE以 0轴为界，其上为上升趋势,否则为下降趋势.
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 CYE 值
CYEL1,CYES1 = CYE(security_list1,check_date='2017-01-04')
print CYEL1[security_list1]
print CYES1[security_list1]

# 输出 security_list2 的 CYE 值
CYEL2,CYES2 = CYE(security_list2,check_date='2017-01-04')
for stock in security_list2:
    print CYEL2[stock]
    print CYES2[stock]
DBQR-对比强弱

DBQR(index_stock, security_list, check_date, N = 5, M1 = 10, M2 = 20, M3 = 60)
参数：

index_stock:大盘股票代码
security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M1：统计的天数 M1
M2：统计的天数 M2
M3：统计的天数 M3
返回：

ZS, GG, MADBQR1, MADBQR2和MADBQR3的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.008962931388970025, ‘000002.XSHE’: 0.008962931388970025, ‘601211.XSHG’: 0.008962931388970025}, {‘000001.XSHE’: 0.011494252873563383, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.22774869109947632, ‘601211.XSHG’: -0.01895206243032329}, {‘000001.XSHE’: -0.0075263047885744793, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.11067285706112595, ‘601211.XSHG’: -0.031800418795617236}, {‘000001.XSHE’: 0.00045608985991743469, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.11198281967226727, ‘601211.XSHG’: -0.012823522774402763}, {‘000001.XSHE’: 0.00683851952397502, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.044647671789494942, ‘601211.XSHG’: 0.0081085126473629619})
备注：

返回结果与通达信一致（其中ZS值与用户选择的大盘股票代码直接相关），同花顺和东方财富没有该指标
计算方式与通达信相同，同花顺和东方财富没有该指标
用法注释：

对比强弱指标包含有两条指标线,一条是对应指数的强弱线。另外一条是个股的强弱线。当个股强弱线与指数强弱线发生金叉时，表明个股开始强过大盘，是买入时机。
当个股强弱线与指数强弱线发生死叉时，表明个股开始弱于大盘，是卖出时机。对比强弱指标是一个短线指标。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 DBQR 值
dbqr_zs, dbqr_gg, dbqr_madbqr1, dbqr_madbqr2, dbqr_madbqr3 = DBQR('000001.XSHG',security_list1,check_date='2017-01-04', N = 5, M1 = 10, M2 = 20, M3 = 60)
print dbqr_zs['000001.XSHG']
print dbqr_gg[security_list1]
print dbqr_madbqr1[security_list1]
print dbqr_madbqr2[security_list1]
print dbqr_madbqr3[security_list1]

# 输出 security_list2 的 DBQR 值
dbqr_zs, dbqr_gg, dbqr_madbqr1, dbqr_madbqr2, dbqr_madbqr3 = DBQR('000001.XSHG',security_list2,check_date='2017-01-04', N = 5, M1 = 10, M2 = 20, M3 = 60)
for stock in security_list2:
    print dbqr_zs['000001.XSHG']
    print dbqr_gg[stock]
    print dbqr_madbqr1[stock]
    print dbqr_madbqr2[stock]
    print dbqr_madbqr3[stock]
DMA-平均差

DMA(security_list, check_date, N1 = 10, N2 = 50, M = 10)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数 N1
N2: 统计的天数 N2
M: 统计的天数 M
返回：

DIF 和 DIFMA 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.10940000000000794, ‘603177.XSHG’: nan, ‘000002.XSHE’: 4.5221999999999927, ‘601211.XSHG’: 0.021799999999998931}, {‘000001.XSHE’: 0.20262000000000988, ‘603177.XSHG’: nan, ‘000002.XSHE’: 3.4217399999999927, ‘601211.XSHG’: 0.53958000000000261})
备注：

返回结果与通达信、同花顺（名为“新DMA”）和东方财富结果一致
计算方式与通达信、同花顺和东方财富相同
用法注释：

1.DMA 向上交叉其平均线时，买进； 
2.DMA 向下交叉其平均线时，卖出； 
3.DMA 的交叉信号比MACD、TRIX 略快； 
4.DMA 与股价产生背离时的交叉信号，可信度较高； 
5.DMA、MACD、TRIX 三者构成一组指标群，互相验证。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 DMA 值
DIF1,DIFMA1 = DMA(security_list1,check_date='2017-01-04', N1 = 10, N2 = 50, M = 10)
print DIF1[security_list1]
print DIFMA1[security_list1]

# 输出 security_list2 的 DMA 值
DIF2,DIFMA2 = DMA(security_list2,check_date='2017-01-04', N1 = 10, N2 = 50, M = 10)
for stock in security_list2:
    print DIF2[stock]
    print DIFMA2[stock]
DMI - 趋向指标

DMI(security_list, check_date, N=14,  MM = 6):
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
MM : 统计的天数 MM
返回：

PDI, MDI, ADX, ADXR的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 25.688830529080601, ‘603177.XSHG’: nan, ‘000002.XSHE’: 53.19815968968976, ‘601211.XSHG’: 18.761296151049379}, {‘000001.XSHE’: 12.721819718749906, ‘603177.XSHG’: nan, ‘000002.XSHE’: 4.3611435006995558, ‘601211.XSHG’: 25.554094733429896}, {‘000001.XSHE’: 25.604986954849515, ‘603177.XSHG’: nan, ‘000002.XSHE’: 74.405711362635628, ‘601211.XSHG’: 27.156295106705297}, {‘000001.XSHE’: 24.423375009809824, ‘603177.XSHG’: nan, ‘000002.XSHE’: 68.677055698186052, ‘601211.XSHG’: 30.275031367421029})
备注：

返回结果与通达信一致，与同花顺和东方财富不一致
计算方式与通达信相同，与同花顺和东方财富不同
用法注释：

用法：市场行情趋向明显时，指标效果理想。 
PDI(上升方向线) MDI(下降方向线) ADX(趋向平均值) 
1.PDI线从下向上突破MDI线，显示有新多头进场，为买进信号； 
2.PDI线从上向下跌破MDI线，显示有新空头进场，为卖出信号； 
3.ADX值持续高于前一日时，市场行情将维持原趋势； 
4.ADX值递减，降到20以下，且横向行进时，市场气氛为盘整； 
5.ADX值从上升倾向转为下降时，表明行情即将反转。 
参数：N　统计天数； M 间隔天数，一般为14、6

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 DMI 值
dmi_pdi, dmi_mdi, dmi_adx, dmi_adxr = DMI(security_list1,check_date='2017-01-04', N= 14, MM = 6)
print dmi_pdi[security_list1]
print dmi_mdi[security_list1]
print dmi_adx[security_list1]
print dmi_adxr[security_list1]

# 输出 security_list2 的 DMI 值
dmi_pdi, dmi_mdi, dmi_adx, dmi_adxr = DMI(security_list2,check_date='2017-01-04', N= 14, MM = 6)
for stock in security_list2:
    print dmi_pdi[stock]
    print dmi_mdi[stock]
    print dmi_adx[stock]
    print dmi_adxr[stock]
DPO-区间震荡线

DMI(security_list, check_date, N=20,  M = 6):
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M : 统计的天数 M
返回：

DPO 和 MADPO 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 0.035000000000000142, ‘603177.XSHG’: nan, ‘000002.XSHE’: 9.1530000000000129, ‘601211.XSHG’: -0.99149999999998784}, {‘000001.XSHE’: 0.0036666666666658188, ‘603177.XSHG’: nan, ‘000002.XSHE’: 6.5928333333333455, ‘601211.XSHG’: -0.79808333333332138})
备注：

返回结果与通达信一致，东方财富一致，与同花顺不一致
计算方式与通达信，东方财富相同，与同花顺不同
用法注释：

1.DOP>0 ，表示目前处于多头市场；DOP<0 ，表示目前处于空头市场； 
2.在0 轴上方设定一条超买线，当股价波动至超买线时，会形成短期高点； 
3.在0 轴下方设定一条超卖线，当股价波动至超卖线时，会形成短期低点； 
4.超买超卖的范围随个股不同而不同，使用者应自行调整； 
5.本指标可设参考线。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 DPO 值
DPO1,MADPO1 = DPO(security_list1,check_date='2017-01-04', N= 20, M = 6)
print DPO1[security_list1]
print MADPO1[security_list1]

# 输出 security_list2 的 DPO 值
DPO2,MADPO2 = DPO(security_list2,check_date='2017-01-04', N= 20, M = 6)
for stock in security_list2:
    print DPO2[stock]
    print MADPO2[stock]
EMV-简易波动指标

EMV(security_list, check_date, N = 14, M = 9)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

EMV和MAEMV的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: -0.19292255670566558, ‘603177.XSHG’: nan, ‘000002.XSHE’: 3.851095221636061, ‘601211.XSHG’: -0.75492717743004634}, {‘000001.XSHE’: -0.20164346999313121, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.0612852628683846, ‘601211.XSHG’: -0.72654134699455397})
备注：

返回结果与通达信、同花顺和东方财富结果一致
计算方式与通达信、同花顺和东方财富相同
用法注释：

1.EMV 由下往上穿越0 轴时，视为中期买进信号； 
2.EMV 由上往下穿越0 轴时，视为中期卖出信号； 
3.EMV 的平均线穿越0 轴，产生假信号的机会较少； 
4.当ADX 低于±DI时，本指标失去效用； 
5.须长期使用EMV 指标才能获得最佳利润。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 EMV 值
EMV1,MAEMV1 = EMV(security_list1,check_date='2017-01-04', N = 14, M = 9)
print EMV1[security_list1]
print MAEMV1[security_list1]

# 输出 security_list2 的 EMV 值
EMV2,MAEMV2 = EMV(security_list2,check_date='2017-01-04', N = 14, M = 9)
for stock in security_list2:
    print EMV2[stock]
    print MAEMV2[stock]
GDX-鬼道线

GDX(security_list, check_date, N = 30, M = 9)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

济安线、压力线和支撑线的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.579464236747615, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.274312299926329, ‘601211.XSHG’: 18.052914184896178}, {‘000001.XSHE’: 9.3516160180549015, ‘603177.XSHG’: nan, ‘000002.XSHE’: 23.1890004069197, ‘601211.XSHG’: 19.677676461536834}, {‘000001.XSHE’: 7.8073124554403304, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.359624192932959, ‘601211.XSHG’: 16.428151908255522})
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同，东方财富和同花顺没有该指标
用法注释：

通道理论公式，是一种用技术手段和经验判断来决定买卖股票的方法。该公式对趋势线做了平滑和修正处理，更精确的反应了股价运行规律。当股价上升到压力线时，投资者就卖出股票，而当股价下跌到支撑线时，投资者就进行相应的补进。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 GDX 值
gdx_jax, gdx_ylx, gdx_zcx = GDX(security_list1,check_date='2017-01-04', N = 30, M = 9)
print gdx_jax[security_list1]
print gdx_ylx[security_list1]
print gdx_zcx[security_list1]

# 输出 security_list2 的 GDX 值
gdx_jax, gdx_ylx, gdx_zcx = GDX(security_list2,check_date='2017-01-04', N = 30, M = 9)
for stock in security_list2:
    print gdx_jax[stock]
    print gdx_ylx[stock]
    print gdx_zcx[stock]
JLHB-绝路航标

JLHB(security_list, check_date, N = 7, M = 5)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

B, VAR2和绝路航标的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 62.675406125612177, ‘603177.XSHG’: nan, ‘000002.XSHE’: 50.248304902948838, ‘601211.XSHG’: 48.413005376201845}, {‘000001.XSHE’: 66.875000000000057, ‘603177.XSHG’: nan, ‘000002.XSHE’: 80.0, ‘601211.XSHG’: 43.800904977375581}, {‘000001.XSHE’: 0, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0, ‘601211.XSHG’: 0})
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同，同花顺和东方财富没有该指标
用法注释：

反趋势类选股指标。综合了动量观念、强弱指标与移动平均线的优点，在计算过程中主要研究高低价位与收市价的关系，反映价格走势的强弱和超买超卖现象。在市场短期超买超卖的预测方面又较敏感。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 JLHB 值
jlhb_b, jlhb_var2, jlhb_jlhb = JLHB(security_list1,check_date='2017-01-04', N = 7, M = 5)
print jlhb_b[security_list1]
print jlhb_var2[security_list1]
print jlhb_jlhb[security_list1]

# 输出 security_list2 的 JLHB 值
jlhb_b, jlhb_var2, jlhb_jlhb = JLHB(security_list2,check_date='2017-01-04', N = 7, M = 5)
for stock in security_list2:
    print jlhb_b[stock]
    print jlhb_var2[stock]
    print jlhb_jlhb[stock]
JS-加速线

JS(security_list, check_date, N = 5, M1 = 5, M2 = 10, M3 = 20)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M1：统计的天数 M1
M2：统计的天数 M2
M3：统计的天数 M3
返回：

JS, MAJS1, MAJS2和MAJS3 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.22988505747126764, ‘603177.XSHG’: nan, ‘000002.XSHE’: 4.5549738219895266, ‘601211.XSHG’: -0.37904124860646582}, {‘000001.XSHE’: 0.19895890422201745, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.7934335630385538, ‘601211.XSHG’: -0.42736705593419566}, {‘000001.XSHE’: -0.1505260957714892, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.2134571412225181, ‘601211.XSHG’: -0.63600837591234527}, {‘000001.XSHE’: 0.0091217971983490014, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.2396563934453453, ‘601211.XSHG’: -0.25647045548805508})
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同，同花顺和东方财富没有该指标
用法注释：

加速线指标是衡量股价涨速的工具,加速线指标上升表明股价上升动力增加,加速线指标下降表明股价下降压力增加。 
加速线适用于DMI表明趋势明显时(DMI.ADX大于20)使用： 
1.如果加速线在0值附近形成平台，则表明既不是最好的买入时机也不是最好的卖入时机； 
2.在加速线发生金叉后,均线形成底部是买入时机； 
3.在加速线发生死叉后,均线形成顶部是卖出时机；

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 JS 值
js_jsx, js_majsx1, js_majsx2, js_majsx3 = JS(security_list1,check_date='2017-01-04', N = 5, M1 = 5, M2 = 10, M3 = 20)
print js_jsx[security_list1]
print js_majsx1[security_list1]
print js_majsx2[security_list1]
print js_majsx3[security_list1]

# 输出 security_list2 的 JS 值
js_jsx, js_majsx1, js_majsx2, js_majsx3 = JS(security_list2,check_date='2017-01-04', N = 5, M1 = 5, M2 = 10, M3 = 20)
for stock in security_list2:
    print js_jsx[stock]
    print js_majsx1[stock]
    print js_majsx2[stock]
    print js_majsx3[stock]
MACD-平滑异同平均

MACD(security_list, check_date, SHORT = 12, LONG = 26, MID = 9)
参数：

security_list：股票列表
check_date：要查询数据的日期
SHORT：统计的天数 SHORT
LONG：统计的天数 LONG
MID：统计的天数 MID
返回：

DIF, DEA和MACD的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.024474457964069884, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.9534717416190936, ‘601211.XSHG’: -0.13735007291032986}, {‘000001.XSHE’: 0.031674925444633864, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.4784672678080988, ‘601211.XSHG’: -0.020490844872792721}, {‘000001.XSHE’: -0.014400934961127959, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.95000894762198973, ‘601211.XSHG’: -0.23371845607507427})
备注：

返回结果与通达信、东方财富和同花顺结果一致
计算方式与通达信、东方财富和同花顺相同
用法注释：

DIFF线　收盘价短期、长期指数平滑移动平均线间的差 
DEA线　 DIFF线的M日指数平滑移动平均线 
MACD线　DIFF线与DEA线的差，彩色柱状线 
参数：SHORT(短期)、LONG(长期)、M 天数，一般为12、26、9

用法： 
1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 
2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。 
3.DEA线与K线发生背离，行情反转信号。 
4.分析MACD柱状线，由红变绿(正变负)，卖出信号；由绿变红，买入信号

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 MACD 值
macd_dif, macd_dea, macd_macd = MACD(security_list1,check_date='2017-01-04', SHORT = 12, LONG = 26, MID = 9)
print macd_dif[security_list1]
print macd_dea[security_list1]
print macd_macd[security_list1]

# 输出 security_list2 的 MACD 值
macd_dif, macd_dea, macd_macd = MACD(security_list2,check_date='2017-01-04', SHORT = 12, LONG = 26, MID = 9)
for stock in security_list2:
    print macd_dif[stock]
    print macd_dea[stock]
    print macd_macd[stock]
QACD-快速异同平均

QACD(security_list, check_date, N1 = 12, N2 = 26, M = 9)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数 N1
N2：统计的天数 N2
M：统计的天数 M
返回：

DIF, MACD和DDIF的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.024474457258216731, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.9534717597632003, ‘601211.XSHG’: -0.13735007291033341}, {‘000001.XSHE’: 0.031674924406612889, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.4784672944906101, ‘601211.XSHG’: -0.020490844872803629}, {‘000001.XSHE’: -0.0072004671483961585, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.47500446527259022, ‘601211.XSHG’: -0.11685922803752978})
备注：

返回结果与通达信一致，与同花顺不同（原因在于同花顺的N2取值为6），东方财富没有该公式
计算方式与通达信和同花顺相同，东方财富没有该公式
用法注释：

1.DIF 向上交叉MACD，买进；DIF 向下交叉MACD，卖出； 
2.DIF 连续两次向下交叉MACD，将造成较大的跌幅； 
3.DIF 连续两次向上交叉MACD，将造成较大的涨幅； 
4.DIF 与股价形成背离时所产生的信号，可信度较高； 
5.DMA、MACD、TRIX 三者构成一组指标群，互相验证。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 QACD 值
qacd_dif, qacd_macd, qacd_ddif = QACD(security_list1,check_date='2017-01-04',  N1 = 12, N2 = 26, M = 9)
print qacd_dif[security_list1]
print qacd_macd[security_list1]
print qacd_ddif[security_list1]

# 输出 security_list2 的 QACD 值
qacd_dif, qacd_macd, qacd_ddif = QACD(security_list2,check_date='2017-01-04',  N1 = 12, N2 = 26, M = 9)
for stock in security_list2:
    print qacd_dif[stock]
    print qacd_macd[stock]
    print qacd_ddif[stock]
QR-强弱指标

QR(index_stock, security_list, check_date, N = 21)
参数：

index_stock:大盘股票代码
security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

个股，大盘和强弱指标的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.57142857142857961, ‘603177.XSHG’: nan, ‘000002.XSHE’: 68.462643678160916, ‘601211.XSHG’: -5.4779806659505876}, {‘000001.XSHE’: -0.60666287471217795, ‘000002.XSHE’: -0.60666287471217795, ‘601211.XSHG’: -0.60666287471217795}, {‘000001.XSHE’: 1.0486350432810712, ‘603177.XSHG’: nan, ‘000002.XSHE’: 62.726365293281042, ‘601211.XSHG’: -4.7928242094193871})
备注：

返回结果与通达信一致（其中ZS值与用户选择的大盘股票代码直接相关），同花顺和东方财富没有该指标
计算方式与通达信相同，同花顺和东方财富没有该指标
用法注释：

指标攀升表明个股走势渐强于大盘，后市看好；指标滑落表明个股走势弱于大盘，可择机换股。同时要结合大盘走势研判，应选择大盘转暖或走牛时出击。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 QR 值
qr_gg, qr_dp, qr_qrz = QR('000001.XSHG',security_list1,check_date='2017-01-04', N = 21)
print qr_gg[security_list1]
print qr_dp['000001.XSHG']
print qr_qrz[security_list1]

# 输出 security_list2 的 QR 值
qr_gg, qr_dp, qr_qrz = QR('000001.XSHG',security_list2,check_date='2017-01-04', N = 21)
for stock in security_list2:
    print qr_gg[stock]
    print qr_dp['000001.XSHG']
    print qr_qrz[stock]
TRIX-终极指标

TRIX(security_list, check_date, N = 12, M = 9)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

TRIX和MATRIX的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.025791210363593713, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.7583370989762825, ‘601211.XSHG’: -0.10625713971250776}, {‘000001.XSHE’: 0.069768190877912417, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.4324777288907538, ‘601211.XSHG’: 0.047380407660970618})
备注：

返回结果与通达信和东方财富相同，与同花顺不同（其中TRIX值大小相同，而MATRIX值与程序返回结果存在差异）
计算方式与通达信和东方财富相同，与同花顺不同（差异在于同花顺的M取值为20）
用法注释：

1.TRIX由下往上交叉其平均线时，为长期买进信号； 
2.TRIX由上往下交叉其平均线时，为长期卖出信号； 
3.DMA、MACD、TRIX 三者构成一组指标群，互相验证。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的TRIX值
TRIX1,MATRIX1 = TRIX(security_list1,check_date='2017-01-04', N = 12, M = 9)
print TRIX1[security_list1]
print MATRIX1[security_list1]

# 输出 security_list2 的 TRIX 值
TRIX2,MATRIX2 = TRIX(security_list2,check_date='2017-01-04', N = 12, M = 9)
for stock in security_list2:
    print TRIX2[stock]
    print MATRIX2[stock]
UOS-终极指标

UOS(security_list, check_date, N1 = 7, N2 = 14, N3 = 28, M = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数 N1
N2：统计的天数 N2
N3：统计的天数 N3
M：统计的天数 M
返回：

终极指标和MAUOS的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 57.771547164847973, ‘603177.XSHG’: nan, ‘000002.XSHE’: 70.504859217869893, ‘601211.XSHG’: 46.33057503226491}, {‘000001.XSHE’: 53.661130731923997, ‘603177.XSHG’: nan, ‘000002.XSHE’: 65.893320720410188, ‘601211.XSHG’: 46.940452580831135})
备注：

返回结果与通达信，东方财富和同花顺相同
计算方式与通达信，东方财富和同花顺相同
用法注释：

1.UOS 上升至50～70的间，而后向下跌破其Ｎ字曲线低点时，为短线卖点； 
2.UOS 上升超过70以上，而后向下跌破70时，为中线卖点； 
3.UOS 下跌至45以下，而后向上突破其Ｎ字曲线高点时，为短线买点； 
4.UOS 下跌至35以下，产生一底比一底高的背离现象时，为底部特征； 
5.以上各项数据会因个股不同而略有不同，请利用参考线自行修正。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的UOS值
uos_ultiInc, uos_mauos = UOS(security_list1,check_date='2017-01-04', N1 = 7, N2 = 14, N3 = 28, M = 6)
print uos_ultiInc[security_list1]
print uos_mauos[security_list1]

# 输出 security_list2 的 UOS 值
uos_ultiInc, uos_mauos = UOS(security_list2,check_date='2017-01-04', N1 = 7, N2 = 14, N3 = 28, M = 6)
for stock in security_list2:
    print uos_ultiInc[stock]
    print uos_mauos[stock]
VMACD-量平滑移动平均

VMACD(security_list, check_date, SHORT = 12, LONG = 26, MID = 9)
参数：

security_list：股票列表
check_date：要查询数据的日期
SHORT：统计的天数 SHORT
LONG：统计的天数 LONG
MID：统计的天数 MID
返回：

DIF, DEA和MACD 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: -29420.22472378047, ‘603177.XSHG’: nan, ‘000002.XSHE’: 246548.71517315158, ‘601211.XSHG’: -54288.764521957521}, {‘000001.XSHE’: -34871.616925081325, ‘603177.XSHG’: nan, ‘000002.XSHE’: 403729.04101507459, ‘601211.XSHG’: -60719.532041579558}, {‘000001.XSHE’: 5451.392201300856, ‘603177.XSHG’: nan, ‘000002.XSHE’: -157180.32584192301, ‘601211.XSHG’: 6430.7675196220371})
备注：

返回结果与通达信，东方财富均有不大于0.1的差异，与同花顺不一致（差别是同花顺的结果是返回结果的100倍）
计算方式与通达信，东方财富完全相同，与同花顺计算方式基本相同，差别在于同花顺的VOL是以交易量为单位，不是以手为单位
用法注释：

基于成交量的MACD算法。 
用法： 
1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 
2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。 
3.DEA线与K线发生背离，行情反转信号。 
4.分析MACD柱状线，由红变绿(正变负)，卖出信号；由绿变红，买入信号

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的VMACD值
vmacd_dif, vmacd_dea, vmacd_macd = VMACD(security_list1,check_date='2017-01-04', SHORT = 12, LONG = 26, MID = 9)
print vmacd_dif[security_list1]
print vmacd_dea[security_list1]
print vmacd_macd[security_list1]

# 输出 security_list2 的 VMACD 值
vmacd_dif, vmacd_dea, vmacd_macd = VMACD(security_list2,check_date='2017-01-04', SHORT = 12, LONG = 26, MID = 9)
for stock in security_list2:
    print vmacd_dif[stock]
    print vmacd_dea[stock]
    print vmacd_macd[stock]
VPT-量价曲线

VPT(security_list, check_date, N = 51, M = 6)
参数：

security_list: 股票列表
check_date: 要查询数据的日期
N: 统计的天数 N
M: 统计的天数 M
返回：

VPT 和 MAVPT 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 110162.20673868078, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2333294.6410979889, ‘601211.XSHG’: 213564.11670755409}, {‘000001.XSHE’: 109563.07430249352, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1968746.2352547429, ‘601211.XSHG’: 216122.67977483606})
备注：

返回结果与通达信有不大于0.1的差异，与东方财富不同，与同花顺不一致
计算方式与通达信相同，与东方财富相同（差别在于东方财富选取的N，M分别为24和5），与同花顺相同（差别在于同花顺的VOL是以交易量为单位，不是以手为单位）
用法注释：

1.VPT 由下往上穿越0 轴时，为买进信号； 
2.VPT 由上往下穿越0 轴时，为卖出信号； 
3.股价一顶比一顶高，VPT 一顶比一顶低时，暗示股价将反转下跌； 
4.股价一底比一底低，VPT 一底比一底高时，暗示股价将反转上涨； 
5.VPT 可搭配EMV 和WVAD指标使用效果更佳。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
VPT1 = VPT(security_list1,context.previous_date, N= 51, M = 6)
print VPT1[security_list1]

# 输出 security_list2 的 VPT 值
VPT2 = VPT(security_list2,context.previous_date, N= 51, M = 6)
for stock in security_list2:
    print VPT2[stock]
WVAD-威廉变异离散量

WVAD(security_list, check_date, N = 24, M = 6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

WVAD 和 MAWVAD的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 92.062648361186916, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2329.1965559178616, ‘601211.XSHG’: 3.1691529344278888}, {‘000001.XSHE’: 33.985407654779912, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1964.3494800488843, ‘601211.XSHG’: -25.500673953544354})
备注：

返回结果与通达信和东方财富一致，与同花顺不同
计算方式与通达信和东方财富相同，与同花顺不同
用法注释：

1.WVAD由下往上穿越0 轴时，视为长期买进信号； 
2.WVAD由上往下穿越0 轴时，视为长期卖出信号； 
3.当ADX 低于±DI时，本指标失去效用； 
4.长期使用WVAD指标才能获得最佳利润； 
5.本指标可与EMV 指标搭配使用。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 WVAD 值
wvad_wvad, wvad_mawvad = WVAD(security_list1,check_date='2017-01-04', N = 24, M = 6)
print wvad_wvad[security_list1]
print wvad_mawvad[security_list1]

# 输出 security_list2 的 WVAD 值
wvad_wvad, wvad_mawvad = WVAD(security_list2,check_date='2017-01-04', N = 24, M = 6)
for stock in security_list2:
    print wvad_wvad[stock]
    print wvad_mawvad[stock]
能量型

BRAR-情绪指标

BRAR(security_list, check_date, N=26)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

BR和AR 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 90.769230769230703, ‘603177.XSHG’: nan, ‘000002.XSHE’: 210.38812785388123, ‘601211.XSHG’: 81.198910081743762}, {‘000001.XSHE’: 92.349726775956157, ‘603177.XSHG’: nan, ‘000002.XSHE’: 283.66762177650412, ‘601211.XSHG’: 81.192660550459109})
备注：

返回结果与通达信和东方财富不一致，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

BR>400，暗示行情过热，应反向卖出；BR<40 ，行情将起死回生，应买进；
AR>180，能量耗尽，应卖出；AR<40 ，能量已累积爆发力，应买进；
BR 由300 以上的高点下跌至50以下的水平,低于AR 时,为绝佳买点；
BR、AR、CR、VR 四者合为一组指标群，须综合搭配使用。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 BRAR 值
BR1,AR1 = BRAR(security_list1, check_date='2017-01-04', N=26)
print BR1[security_list1]
print AR1[security_list1]

# 输出 security_list2 的 BRAR 值
BR2,AR2 = BRAR(security_list2, check_date='2017-01-04', N=26)
for stock in security_list2:
    print BR2[stock]
    print AR2[stock]
CR-带状能量线

CR(security_list, check_date, N=26, M1=10, M2=20, M3=40, M4=62)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M1：统计的天数 M1
M2：统计的天数 M2
M3：统计的天数 M3
M4：统计的天数 M4
返回：

CR和MA1，MA2，MA3，MA4 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 92.287917737788732, ‘603177.XSHG’: nan, ‘000002.XSHE’: 310.60606060606005, ‘601211.XSHG’: 65.852168601099407}, {‘000001.XSHE’: 140.86650665677868, ‘603177.XSHG’: nan, ‘000002.XSHE’: 263.61151123494176, ‘601211.XSHG’: 132.45402304938904}, {‘000001.XSHE’: 147.02494118319379, ‘603177.XSHG’: nan, ‘000002.XSHE’: 187.92520738936778, ‘601211.XSHG’: 138.9584146734295}, {‘000001.XSHE’: 98.715266031757878, ‘603177.XSHG’: nan, ‘000002.XSHE’: 116.68759448530741, ‘601211.XSHG’: 93.303386336228911}, {‘000001.XSHE’: 78.759338424450661, ‘603177.XSHG’: nan, ‘000002.XSHE’: 100.63420206110173, ‘601211.XSHG’: 78.912222905134882})
备注：

返回结果与通达信，同花顺和东方财富均不一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

CR>400时，其10日平均线向下滑落，视为卖出信号；CR<40买进；
CR 由高点下滑至其四条平均线下方时，股价容易形成短期底部；
CR 由下往上连续突破其四条平均线时，为强势买进点；
CR 除了预测价格的外，最大的作用在于预测时间；
BR、AR、CR、VR 四者合为一组指标群，须综合搭配使用。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CR 值
CR1, MA1, MA2, MA3, MA4 = CR(security_list1, check_date='2017-01-04', N=26, M1=10, M2=20, M3=40, M4=62)
print CR1[security_list1]
print MA1[security_list1]
print MA2[security_list1]
print MA3[security_list1]
print MA4[security_list1]

# 输出 security_list2 的 CR 值
CR1, MA1, MA2, MA3, MA4 = CR(security_list2, check_date='2017-01-04', N=26, M1=10, M2=20, M3=40, M4=62)
for stock in security_list2:
    print CR1[stock]
    print MA1[stock]
    print MA2[stock]
    print MA3[stock]
    print MA4[stock]
CYR-市场强弱

CYR(security_list, check_date, N = 13, M = 5)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

CYR 和 MACYR 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: -0.054093150941103563, ‘603177.XSHG’: nan, ‘000002.XSHE’: 3.2324567390829451, ‘601211.XSHG’: -0.39420121431832378}, {‘000001.XSHE’: -0.061359574639450187, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.7008273617957137, ‘601211.XSHG’: -0.35959378850023205})
备注：

返回结果与通达信和东方财富一致，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

CYR是成本均线派生出的指标,是13日成本均线的升降幅度;
使用CYR可以对股票的强弱进行排序,找出其中的强势和弱势股票。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CYR 值
CYR1,MACYR1 = CYR(security_list1, check_date='2017-01-04', N = 13, M = 5)
print CYR1[security_list1]
print MACYR1[security_list1]

# 输出 security_list2 的 CYR 值
CYR2,MACYR2 = CYR(security_list2, check_date='2017-01-04', N = 13, M = 5)
for stock in security_list2:
    print CYR2[stock]
    print MACYR2[stock]
MASS-梅斯线

MASS(security_list, check_date, N1=9, N2=25, M=6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数 N1
N2：统计的天数 N2
M：统计的天数 M
返回：

MASS和MAMASS 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 24.239711786446705, ‘603177.XSHG’: nan, ‘000002.XSHE’: 32.023209054655545, ‘601211.XSHG’: 23.609848955660624}, {‘000001.XSHE’: 23.894883731671456, ‘603177.XSHG’: nan, ‘000002.XSHE’: 31.687243323851508, ‘601211.XSHG’: 23.978558571459313})
备注：

返回结果与通达信，同花顺和东方财富均不一致，原因在于get_price获取的数据与炒股软件的不一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

MASS>27 后，随后又跌破26.5，此时股价若呈上涨状态，则卖出；
MASS<27 后，随后又跌破26.5，此时股价若呈下跌状态，则买进；
MASS<20 的行情，不宜进行投资。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 MASS 值
MASS1,MAMASS1 = MASS(security_list1, check_date='2017-01-04', N1=9, N2=25, M=6)
print MASS1[security_list1]
print MAMASS1[security_list1]

# 输出 security_list2 的 MASS 值
MASS2,MAMASS2 = MASS(security_list2, check_date='2017-01-04', N1=9, N2=25, M=6)
for stock in security_list2:
    print MASS2[stock]
    print MAMASS2[stock]
PCNT-幅度比

PCNT(security_list, check_date, M = 5)
参数：

security_list：股票列表
check_date：要查询数据的日期
M：统计的天数 M
返回：

PCNT 和 MAPCNT 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: -0.81775700934579765, ‘603177.XSHG’: nan, ‘000002.XSHE’: 9.1257995735607711, ‘601211.XSHG’: -0.17261219792866017}, {‘000001.XSHE’: -0.093375782685468367, ‘603177.XSHG’: nan, ‘000002.XSHE’: 5.1789530788938016, ‘601211.XSHG’: -0.6614506214203465})
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同，东方财富和同花顺没有该指标
用法注释：

PCNT 重视价格的涨跌幅度，排除观察涨跌跳动值；
较高的PCNT 值，表示该股波动幅度大；
较低的PCNT 值，表示该股波动幅度小。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 PCNT 值
PCNT1,MAPCNT1 = PCNT(security_list1, check_date='2017-01-04', M=5)
print PCNT1[security_list1]
print MAPCNT1[security_list1]

# 输出 security_list2 的 PCNT 值
PCNT2,MAPCNT2 = PCNT(security_list2, check_date='2017-01-04', M=5)
for stock in security_list2:
    print PCNT2[stock]
    print MAPCNT2[stock]
PSY-心理线

PSY(security_list, check_date, timeperiod=12)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数 N
返回：

PSY 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 50.0, ‘603177.XSHG’: nan, ‘000002.XSHE’: 58.333333333333336, ‘601211.XSHG’: 33.333333333333329}
备注：

返回结果与通达信、同花顺和东方财富结果均一致
计算方式与通达信、同花顺和东方财富相同
用法注释：

1.PSY>75，形成Ｍ头时，股价容易遭遇压力； 
2.PSY<25，形成Ｗ底时，股价容易获得支撑； 
3.PSY 与VR 指标属一组指标群，须互相搭配使用。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 PSY 值
PSY1 = PSY(security_list1,check_date='2017-01-04', timeperiod=14)
print PSY1[security_list1]

# 输出 security_list2 的 PSY 值
PSY2 = PSY(security_list2,check_date='2017-01-04', timeperiod=14)
for stock in security_list2:
    print PSY2[stock]
VR-成交量变异率

VR(security_list, check_date, N=26, M=6)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

VR和MAVR 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 131.42761741216233, ‘603177.XSHG’: nan, ‘000002.XSHE’: 213.15765431976482, ‘601211.XSHG’: 84.984239389082546}, {‘000001.XSHE’: 133.5803410407361, ‘603177.XSHG’: nan, ‘000002.XSHE’: 182.61022230207126, ‘601211.XSHG’: 117.87968865084336})
备注：

返回结果与通达信和东方财富一致，与同花顺不一致
计算方式与通达信和东方财富相同，与同花顺中的VR指标不同
用法注释：

VR>450，市场成交过热，应反向卖出；
VR<40 ，市场成交低迷，人心看淡的际，应反向买进；
VR 由低档直接上升至250，股价仍为遭受阻力，此为大行情的前兆；
VR 除了与PSY为同指标群外，尚须与BR、AR、CR同时搭配研判
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 VR 值
VR1,MAVR1 = VR(security_list1, check_date='2017-01-04', N=26, M=6)
print VR1[security_list1]
print MAVR1[security_list1]

# 输出 security_list2 的 VR 值
VR2,MAVR2 = VR(security_list2, check_date='2017-01-04', N=26, M=6)
for stock in security_list2:
    print VR2[stock]
    print MAVR2[stock]
成交量型

AMO-成交金额

AMO(security_list, check_date, M1 = 5, M2 = 10)
参数：

security_list：股票列表
check_date：要查询数据的日期
M1：统计的天数 M1
M2：统计的天数 M2
返回： 
- AMOW，AMO1和AMO2 的值

返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 42858.215500999999, ‘603177.XSHG’: nan, ‘000002.XSHE’: 528895.0784, ‘601211.XSHG’: 26720.7556}, {‘000001.XSHE’: 36852.956986600002, ‘603177.XSHG’: nan, ‘000002.XSHE’: 391033.63072000002, ‘601211.XSHG’: 30396.797399999999}, {‘000001.XSHE’: 40629.7649418, ‘603177.XSHG’: nan, ‘000002.XSHE’: 432376.88320000004, ‘601211.XSHG’: 36740.013179999994})
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同，东方财富和同花顺没有该指标
本函数未显示VOLSTICK，其在通达信中是柱状线的图形
用法注释：

成交金额大，代表交投热络，可界定为热门股；
底部起涨点出现大成交金额，代表攻击量；
头部地区出现大成交金额，代表出货量；
观察成交金额的变化，比观察成交手数更具意义，因为成交手数并未反应股价的涨跌的后所应支出的实际金额。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 AMO 值
AMOW,AMO1,AMO2 = AMO(security_list1, check_date='2017-01-04', M1 = 5, M2 = 10)
print AMOW[security_list1]
print AMO1[security_list1]
print AMO2[security_list1]

# 输出 security_list2 的 AMO 值
AMOW,AMO1,AMO2 = AMO(security_list2, check_date='2017-01-04', M1 = 5, M2 = 10)
for stock in security_list2:
    print AMOW[stock]
    print AMO1[stock]
    print AMO2[stock]
CCL-持仓量（适用于期货）

CCL(futures_list, check_date, M=5)
参数：

futures_list：股票列表
check_date：要查询数据的日期
M：统计的天数 M
返回：

CCL和MACCL 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘IF1712.CCFX’: 2533.0, ‘IF1803.CCFX’: nan, ‘IF1709.CCFX’: 9828.0, ‘IF1708.CCFX’: 1504.0}, {‘IF1712.CCFX’: 2500.0, ‘IF1803.CCFX’: nan, ‘IF1709.CCFX’: 9748.6000000000004, ‘IF1708.CCFX’: 1213.8})
备注：

返回结果与通达信一致，与东方财富不一致（原因在于参数M取值不同），同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

持仓量上升或下降的变化为图表分析师提供了判断价格走势的线索。
持仓量远不如价格信息重要，所以它主要用于印证市场走势。
示例：

# 定义金融期货代码列表
futures_list1 = 'IF1708.CCFX'
futures_list2 = ['IF1708.CCFX','IF1709.CCFX','IF1712.CCFX','IF1803.CCFX']

# 计算并输出 futures_list1 的 CCL 值
CCL1,MACCL1 = CCL(futures_list1, check_date='2017-07-04', M=5)
print CCL1[futures_list1]
print MACCL1[futures_list1]

# 输出 futures_list2 的 CCL 值
CCL2,MACCL2 = CCL(futures_list2, check_date='2017-07-04', M=5)
for stock in futures_list2:
    print CCL2[stock]
    print MACCL2[stock]
DBLB-对比量比

DBLB(index_stock, security_list, check_date, N=5, M=5)
参数：

index_stock: 大盘股票代码
security_list:股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

DBLB和MADBLB 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 2.1493659892493957, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.76166585836540168, ‘601211.XSHG’: 3.1383580528664869}, {‘000001.XSHE’: 1.310194821508738, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.82666969680671354, ‘601211.XSHG’: 1.3389363967102343})
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同
用法注释：

对比量比指标用于用于测度成交量放大程度或萎缩程度 
的指标。对比量比值越大，说明成交量较前期成交量放 
大程度越大，对比量比值越小，说明成交量较前期成交 
量萎缩程度越大，一般认为: 
对比量比大于20可以认为成交量极度放大；
对比量比大于3,可以认为成交量显著放大；
对比量比小于0.2,可以认为成交量极度萎缩；
对比量比小于0.4,可以认为成交量显著萎缩。
示例：

# 定义股票池列表
index_stock = '399106.XSHE'
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 DBLB 值
DBLB1,MADBLB1 = DBLB(index_stock, security_list1, check_date='2017-01-04', N=5, M=5)
print DBLB1[security_list1]
print MADBLB1[security_list1]

# 输出 security_list2 的 DBLB 值
DBLB2,MADBLB2 = DBLB(index_stock, security_list2, check_date='2017-01-04', N=5, M=5)
for stock in security_list2:
    print DBLB2[stock]
    print MADBLB2[stock]
DBQRV-对比强弱量

DBQRV(index_stock, security_list, check_date, N = 5)
参数：

index_stock: 大盘股票代码
security_list:股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

ZS和GG 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘399106.XSHE’: 0.6426864576400364}, {‘000001.XSHE’: 2.6501693742416115, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0.10023325347228342, ‘601211.XSHG’: 3.7644208422132119})（此次示例把深证综指（399106.XSHE）当做了大盘股票）
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同
用法注释：

对比强弱量指标包含有两条指标线,一条是对应指数量的 
强弱线。另外一条是个股成交量的强弱线。当个股强弱线 
与指数强弱线发生金叉时，表明个股成交活跃过大盘。当 
个股强弱线与指数强弱线发生死叉时，表明个股活跃度开 
始弱于大盘。对比强弱量指标也是一个短线指标。

注意：此指标使用到了大盘的数据，所以需要下载完整的 
日线数据,否则显示可能不正确

示例：

# 定义股票池列表
index_stock = '399106.XSHE'
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 DBQRV 值
ZS1,GG1 = DBQRV(index_stock, security_list1, check_date='2017-01-04', N = 5)
print ZS1[index_stock]
print GG1[security_list1]

# 输出 security_list2 的 DBQRV 值
ZS2,GG2 = DBQRV(index_stock, security_list2, check_date='2017-01-04', N = 5)
for stock in security_list2:
    print ZS2[index_stock]
    print GG2[stock]
HSL-换手线

HSL(security_list, check_date, N = 5)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

HSL和MAHSL 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 0.42388098152752657, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.4040782443554365, ‘601211.XSHG’: 1.0070272131147542}, {‘000001.XSHE’: 0.36486110275710459, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1.9485759345950888, ‘601211.XSHG’: 1.1303558950819672})
备注：

返回结果与通达信和同花顺有不大于0.01的差异，东方财富没有该指标
计算方式与通达信和同花顺相同，东方财富没有该指标
通达信中HSCOL指标的计算方式和结果与HSL完全相同，如果需要HSCOL，请以HSL做参考。
用法注释：

换手线是根据换手率绘制的曲线，使对于成交量的研判
不受股本变动的影响，更增加了成交量具有可比性。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 HSL 值
HSL1,MAHSL1 = HSL(security_list1, check_date='2017-01-04', N = 5)
print HSL1[security_list1]
print MAHSL1[security_list1]

# 输出 security_list2 的 HSL 值
HSL2,MAHSL2 = HSL(security_list2, check_date='2017-01-04', N = 5)
for stock in security_list2:
    print HSL2[stock]
    print MAHSL2[stock]
OBV-累积能量线

OBV(security_list, check_date, timeperiod=30)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数 N
返回：

OBV 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 7606250650.0, ‘603177.XSHG’: nan, ‘000002.XSHE’: 10161140224.0, ‘601211.XSHG’: 3422411336.0}
备注：

返回结果与通达信、同花顺、东方财富结果均不一致
用法注释：

1.股价一顶比一顶高，而OBV 一顶比一顶低，暗示头部即将形成； 
2.股价一底比一底低，而OBV 一底比一底高，暗示底部即将形成； 
3.OBV 突破其Ｎ字形波动的高点次数达5 次时，为短线卖点； 
4.OBV 跌破其Ｎ字形波动的低点次数达5 次时，为短线买点； 
5.OBV 与ADVOL、PVT、WAD、ADL同属一组指标群，使用时应综合研判。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 OBV 值
OBV1 = OBV(security_list1,check_date='2017-01-04', timeperiod=30)
print OBV1[security_list1]

# 输出 security_list2 的 OBV 值
OBV2 = OBV(security_list2,check_date='2017-01-04', timeperiod=30)
for stock in security_list2:
    print OBV2[stock]
VOL-成交量

VOL(security_list, check_date, M1=5, M2=10)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：统计的天数 M
返回：

VOL 和 MAVOL 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 500351.22999999998, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2333030.52, ‘601211.XSHG’: 153571.64999999999}, {‘000001.XSHE’: 430683.87, ‘603177.XSHG’: nan, ‘000002.XSHE’: 1890989.6699999999, ‘601211.XSHG’: 172379.274}, {‘000001.XSHE’: 474050.94499999995, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2246594.1269999999, ‘601211.XSHG’: 205083.77899999998})
备注：

返回结果与通达信，同花顺和东方财富均不一致，原因是get_price获取的源数据与炒股软件不一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

成交量大，代表交投热络，可界定为热门股；
底部起涨点出现大成交量(成交手数)，代表攻击量；
头部地区出现大成交量(成交手数)，代表出货量；
观察成交金额的变化，比观察成交手数更具意义，因为成交手数并未反应股价的涨跌的后所应支出的实际金额。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 VOL 值
VOL1,MAVOL11,MAVOL12 = VOL(security_list1, check_date='2017-01-04', M1=5, M2=10)
print VOL1[security_list1]
print MAVOL11[security_list1]
print MAVOL12[security_list1]

# 输出 security_list2 的 VOL 值
VOL2,MAVOL21,MAVOL22 = VOL(security_list2, check_date='2017-01-04', M1=5, M2=10)
for stock in security_list2:
    print VOL2[stock]
    print MAVOL21[stock]
    print MAVOL22[security_list1]
VRSI-相对强弱量

VRSI(security_list, check_date, N1=6, N2=12, N3=24)
参数：

security_list：股票列表
check_date：要查询数据的日期
N1：统计的天数 N1
N2：统计的天数 N2
N3：统计的天数 N3
返回：

RSI1，VRSI2和VRSI3 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 50.467938637493823, ‘603177.XSHG’: nan, ‘000002.XSHE’: 50.382520845028509, ‘601211.XSHG’: nan}, {‘000001.XSHE’: 49.322460708038193, ‘603177.XSHG’: nan, ‘000002.XSHE’: 51.166143930198224, ‘601211.XSHG’: nan}, {‘000001.XSHE’: 49.251191741159232, ‘603177.XSHG’: nan, ‘000002.XSHE’: 51.867549823141722, ‘601211.XSHG’: nan})
备注：

返回结果与通达信和同花顺一致，东方财富没有该指标
计算方式与通达信和同花顺相同，
用法注释：

VRSI>20 为超买；VRSI<20 为超卖；
VRSI 以50为中界线，大于50视为多头行情，小于50视为空头行情；
VRSI 在80以上形成Ｍ头或头肩顶形态时，视为向下反转信号；
VRSI 在20以下形成Ｗ底或头肩底形态时，视为向上反转信号；
VRSI 向上突破其高点连线时，买进；VRSI 向下跌破其低点连线时，卖出。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 VRSI 值
VRSI1,VRSI2,VRSI3  = VRSI(security_list1, check_date='2017-01-04', N1=6, N2=12, N3=24)
print VRSI1[security_list1]
print VRSI2[security_list1]
print VRSI3[security_list1]

# 输出 security_list2 的 VRSI 值
VRSI1,VRSI2,VRSI3 = VRSI(security_list2, check_date='2017-01-04', N1=6, N2=12, N3=24)
for stock in security_list2:
    print VRSI1[stock]
    print VRSI2[stock]
    print VRSI3[stock]
均线型

AMV-成本价均线

AMV(security_list, check_date, timeperiod = 13)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

AMV的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 8.2675000000000001, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.232499999999998, ‘601211.XSHG’: 16.314999999999998}
备注：

由于复权因子不同的原因，返回结果与通达信和同花顺结果有微小差异，东方财富没有该指标
计算方式与通达信，同花顺相同
用法注释：

成本价均线不同于一般移动平均线系统，成本价均线系统首次将成交量引入均线系统，充分提高均线系统的可靠性。同样对于成本价均线可以使用月均线系统(5,10,20,250)和季均线系统(20,40,60,250),另外成本价均线还可以使用自身特有的均线系统(5,13,34,250),称为市场平均建仓成本均线，简称成本价均线。在四个均线中参数为250的均线为年度均线,为行情支撑均线。成本均线不容易造成虚假信号或骗线，比如某日股价无量暴涨，移动均线会大幅拉升，但成本均线却不会大幅上升，因为在无量的情况下市场持仓成本不会有太大的变化。依据均线理论，当短期均线站在长期均线之上时叫多头排列，反之就叫空头排列。短期均线上穿长期均线叫金叉，短期均线下穿长期均线叫死叉。均线的多头排列是牛市的标志，空头排列是熊市的标志。均线系统一直是市场广泛认可的简单而可靠的分析指标，其使用要点是尽量做多头排列的股票，回避空头排列的股票。34日成本线是市场牛熊的重要的分水岭。一旦股价跌破34日成本线，则常常是最后的出逃机会。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 AMV 值
AMV1 = AMV(security_list1,check_date='2017-01-04', timeperiod=13)
print AMV1[security_list1]

# 输出 security_list2 的 AMV 值
AMV2 = AMV(security_list2,check_date='2017-01-04', timeperiod=13)
for stock in security_list2:
    print AMV2[stock]
ALLIGAT-鳄鱼线

ALLIGAT(security_list, check_date, timeperiod = 21)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

上唇 牙齿 下颚 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.2959999999999976, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.943000000000001, ‘601211.XSHG’: 16.442000000000004}, {‘000001.XSHE’: 8.3268749999999994, ‘603177.XSHG’: nan, ‘000002.XSHE’: 17.969375000000003, ‘601211.XSHG’: 16.434999999999999}, {‘000001.XSHE’: 8.4411538461538456, ‘603177.XSHG’: nan, ‘000002.XSHE’: 15.414615384615388, ‘601211.XSHG’: 16.79269230769231})
备注：

返回结果与通达信相同，同花顺和东方财富没有该指标
计算方式与通达信相同
用法注释：

鳄鱼线是运用分形几何学和非线性动力学的一组平均线（实际上就是一种比较特别的均线）。它分为蓝、红、绿三条。 
蓝线被称为鳄鱼的颚部，红线被称为鳄鱼的牙齿，绿色被称为鳄鱼的唇吻。 
它们的构造方法如下： 
颚部——13根价格线的平滑移动均线，并将数值向未来方向移动8根价格线； 
牙齿——8根价格线的平滑移动平均线，并将数值向未来方向移动5根价格线； 
唇吻——5根价格线的平滑移动均线，并将数值向未来方向移动3根价格线。 
鳄鱼线的基本使用方法是： 
当颚部、牙齿、唇吻纠缠在一起时，我们便进入了观望期（鳄鱼休息了） 
当唇吻(绿）在牙齿（红）以上，牙齿在颚部（蓝）以上时，我们便进入了多头市场（颚鱼要开始吃牛肉了） 
当唇吻在牙齿以下，牙齿在颚部以下时，我便进入了空头市场（鳄鱼要开始吃熊肉了）
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 ALLIGAT 值
up1, teeth1, down1 = ALLIGAT(security_list1,check_date='2017-01-04', timeperiod = 21)
print up1[security_list1]
print teeth1[security_list1]
print down1[security_list1]

# 输出 security_list2 的 ALLIGAT 值
up2, teeth2, down2 = ALLIGAT(security_list2,check_date='2017-01-04', timeperiod = 21)
for stock in security_list2:
    print up2[stock]
    print teeth2[stock]
    print down2[stock]
BBI-多空均线

BBI(security_list, check_date, timeperiod1=3, timeperiod2=6, timeperiod3=12, timeperiod4=24)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod1：统计的天数 N1
timeperiod2：统计的天数 N2
timeperiod3：统计的天数 N3
timeperiod4：统计的天数 N4
返回：

BBI 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： {‘000001.XSHE’: 9.223020833333333, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.7265625, ‘601211.XSHG’: 18.572187500000002}
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

1.股价位于BBI 上方，视为多头市场； 
2.股价位于BBI 下方，视为空头市场。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 BBI 值
BBI1 = BBI(security_list1, check_date='2017-01-04', timeperiod1=3, timeperiod2=6, timeperiod3=12, timeperiod4=24)
print BBI1[security_list1]

# 输出 security_list2 的 BBI 值
BBI2 = BBI(security_list2, check_date='2017-01-04', timeperiod1=3, timeperiod2=6, timeperiod3=12, timeperiod4=24)
for stock in security_list2:
    print BBI2[stock]
EXPMA-指数平均线

EXPMA(security_list, check_date, timeperiod = 12)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

EXPMA的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 8.3341666666666665, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.265000000000001, ‘601211.XSHG’: 16.537499999999998}
备注：

返回结果与通达信和同花顺和东方财富一致
计算方式与同花顺、东方财富和通达信相同
用法注释：

EXPMA 一般以观察12日和50日二条均线为主；
12日指数平均线向上交叉50日指数平均线时，买进；
12日指数平均线向下交叉50日指数平均线时，卖出；
EXPMA 是多种平均线计算方法的一；
EXPMA 配合MTM 指标使用，效果更佳。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 EXPMA 值
EXPMA1 = EXPMA(security_list1,check_date='2017-01-04', timeperiod=12)
print EXPMA1[security_list1]

# 输出 security_list2 的 EXPMA 值
EXPMA2 = EXPMA(security_list2,check_date='2017-01-04', timeperiod=12)
for stock in security_list2:
    print EXPMA2[stock]
BBIBOLL-多空布林线

BBIBOLL(security_list, check_date, N = 11, M = 6)
参数：

security_list：股票列表
check_date: 要查询数据的日期
N：统计的天数
M：统计的天数
返回：

BBIBOLL UPR DWN 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.3691666666666649, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.480520833333337, ‘601211.XSHG’: 16.675729166666663}, {‘000001.XSHE’: 8.5978513909597396, ‘603177.XSHG’: nan, ‘000002.XSHE’: 24.940210721576193, ‘601211.XSHG’: 17.285976571029227}, {‘000001.XSHE’: 8.1404819423735901, ‘603177.XSHG’: nan, ‘000002.XSHE’: 14.020830945090481, ‘601211.XSHG’: 16.065481762304099})
备注：

返回结果与通达信和同花顺一致，东方财富没有该指标
计算方式与通达信和同花顺相同
用法注释：

为BBI与BOLL的迭加；
高价区收盘价跌破BBI线，卖出信号；
低价区收盘价突破BBI线，买入信号；
BBI线向上，股价在BBI线之上，多头势强；
BBI线向下，股价在BBI线之下，空头势强。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 BBIBOLL 值
bbi1, upr1, dwn1 = BBIBOLL(security_list1,check_date='2017-01-04', N = 11, M = 6)
print bbi1[security_list1]
print upr1[security_list1]
print dwn1[security_list1]

# 输出 security_list2 的 BBIBOLL 值
bbi2, upr2, dwn2 = BBIBOLL(security_list2,check_date='2017-01-04', N = 11, M = 6)
for stock in security_list2:
    print bbi2[stock]
    print upr2[stock]
    print dwn2[stock]
MA-均线

MA(security_list, check_date, timeperiod=5)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数timeperiod
返回：

MA 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 9.2599999999999998, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.68, ‘601211.XSHG’: 18.704000000000001}
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

1.股价高于平均线，视为强势；股价低于平均线，视为弱势 
2.平均线向上涨升，具有助涨力道；平均线向下跌降，具有助跌力道； 
3.二条以上平均线向上交叉时，买进； 
4.二条以上平均线向下交叉时，卖出； 
5.移动平均线的信号经常落后股价，若以EXPMA 、VMA 辅助，可以改善。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 MA 值
MA1 = MA(security_list1, check_date='2017-01-04', timeperiod=5)
print MA1[security_list1]

# 输出 security_list2 的 MA 值
MA2 = MA(security_list2, check_date='2017-01-04', timeperiod=5)
for stock in security_list2:
    print MA2[stock]
HMA-高价平均线

HMA(security_list, check_date, timeperiod = 12)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

HMA的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 8.3641666666666676, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.754999999999999, ‘601211.XSHG’: 16.634166666666665}
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同
用法注释：

一般移动平均线以收盘价为计算基础，高价平均线是以每日最高价为计算基础。目前市场上许多投资人将其运用在空头市场，认为它的压力效应比传统平均线更具参考价值。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 HMA 值
HMA1 = HMA(security_list1,check_date='2017-01-04', timeperiod=12)
print HMA1[security_list1]

# 输出 security_list2 的 HMA 值
HMA2 = HMA(security_list2,check_date='2017-01-04', timeperiod=12)
for stock in security_list2:
    print HMA2[stock]
LMA-低价平均线

LMA(security_list, check_date, timeperiod = 12)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

LMA的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 8.2675000000000001, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.232499999999998, ‘601211.XSHG’: 16.314999999999998}
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同
用法注释：

一般移动平均线以收盘价为计算基础，低价平均线是以每日最低价为计算基础。目前市场上许多投资人将其运用在多头市场，认为它的支撑效应比传统平均线更具参考价值。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 LMA 值
LMA1 = LMA(security_list1,check_date='2017-01-04', timeperiod=12)
print LMA1[security_list1]

# 输出 security_list2 的 LMA 值
LMA2 = LMA(security_list2,check_date='2017-01-04', timeperiod=12)
for stock in security_list2:
    print LMA2[stock]
VMA-变异平均线

VMA(security_list, check_date, timeperiod = 12)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

VMA的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 8.3202083333333334, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.979166666666668, ‘601211.XSHG’: 16.474166666666669}
备注：

返回结果与通达信和同花顺一致，东方财富没有该指标
计算方式与通达信和同花顺相同
用法注释：

股价高于平均线，视为强势；股价低于平均线，视为弱势；
平均线向上涨升，具有助涨力道；平均线向下跌降，具有助跌力道；
二条以上平均线向上交叉时，买进；
二条以上平均线向下交叉时，卖出；
VMA 比一般平均线的敏感度更高，消除了部份平均线落后的缺陷。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 VMA 值
VMA1 = VMA(security_list1,check_date='2017-01-04', timeperiod=12)
print VMA1[security_list1]

# 输出 security_list2 的 VMA 值
VMA2 = VMA(security_list2,check_date='2017-01-04', timeperiod=12)
for stock in security_list2:
    print VMA2[stock]
路径型

BOLL-布林线

Bollinger_Bands(security_list, check_date, timeperiod=20, nbdevup=2, nbdevdn=2)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数timeperiod
nbdevup：统计的天数 nbdevup
nbdevdn：统计的天数 nbdevdn
返回：

上轨线UB 、中轨线MB、下轨线LB 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： ({‘000001.XSHE’: 9.2899945886169739, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.378028110909778, ‘601211.XSHG’: 18.846866409164456}, {‘000001.XSHE’: 9.1745000000000037, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.795500000000004, ‘601211.XSHG’: 18.423999999999999}, {‘000001.XSHE’: 9.0590054113830334, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.21297188909023, ‘601211.XSHG’: 18.001133590835543})
备注：

返回结果与通达信、东方财富和同花顺结果一致
计算方式与通达信、东方财富和同花顺相同
用法注释：

1.股价上升穿越布林线上限时，回档机率大； 
2.股价下跌穿越布林线下限时，反弹机率大； 
3.布林线震动波带变窄时，表示变盘在即； 
4.BOLL须配合BB 、WIDTH 使用；

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 BOLL 值
upperband, middleband, lowerband = Bollinger_Bands(security_list1, check_date='2017-01-04', timeperiod=20, nbdevup=2, nbdevdn=2)
print upperband[security_list1]
print middleband[security_list1]
print lowerband[security_list1]

# 输出 security_list2 的 BOLL 值
upperband, middleband, lowerband = Bollinger_Bands(security_list2, check_date='2017-01-04', timeperiod=20, nbdevup=2, nbdevdn=2)
for stock in security_list2:
    print upperband[stock]
    print middleband[stock]
    print lowerband[stock]
ENE-轨道线

ENE(security_list,check_date,N=25,M1=6,M2=6):
参数：

security_list：股票列表
check_date: 要查询数据的日期
N：统计的天数
M1：统计的天数
M2：统计的天数
返回：

UPPER LOWER ENE的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.9341039999999996, ‘603177.XSHG’: nan, ‘000002.XSHE’: 17.686311999999997, ‘601211.XSHG’: 17.851672000000001}, {‘000001.XSHE’: 7.9226959999999993, ‘603177.XSHG’: nan, ‘000002.XSHE’: 15.684087999999997, ‘601211.XSHG’: 15.830727999999999}, {‘000001.XSHE’: 8.4283999999999999, ‘603177.XSHG’: nan, ‘000002.XSHE’: 16.685199999999998, ‘601211.XSHG’: 16.841200000000001})
备注：

返回结果与通达信和东方财富一致，同花顺没有该指标
计算方式与东方财富和通达信相同
用法注释：

股价上升穿越轨道线上限时，回档机率大；
股价下跌穿越轨道线下限时，反弹机率大；
股价波动于轨道线内时，代表常态行情，此时，超买超卖指标可发挥效用；
股价波动于轨道线外时，代表脱轨行情，此时，应使用趋势型指标。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 ENE 值
up1, low1, ENE1 = ENE(security_list1,check_date='2017-01-04',N=25,M1=6,M2=6)
print up1[security_list1]
print low1[security_list1]
print ENE1[security_list1]

# 输出 security_list2 的 ENE 值
up2, low2, ENE2 = ENE(security_list2,check_date='2017-01-04',N=25,M1=6,M2=6)
for stock in security_list2:
    print up2[stock]
    print low2[stock]
    print ENE2[stock]
MIKE-麦克支撑压力

MIKE(security_list, check_date, timeperiod = 10)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

STOR MIDR WEKR WEKS MIDS STOS 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.6416666666666675, ‘603177.XSHG’: nan, ‘000002.XSHE’: 26.2775, ‘601211.XSHG’: 17.473333333333329}, {‘000001.XSHE’: 8.5164999999999988, ‘603177.XSHG’: nan, ‘000002.XSHE’: 23.604055555555551, ‘601211.XSHG’: 17.071111111111108}, {‘000001.XSHE’: 8.3913333333333338, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.930611111111112, ‘601211.XSHG’: 16.668888888888887}, {‘000001.XSHE’: 8.1854999999999993, ‘603177.XSHG’: nan, ‘000002.XSHE’: 15.899777777777777, ‘601211.XSHG’: 16.035555555555558}, {‘000001.XSHE’: 8.1048333333333336, ‘603177.XSHG’: nan, ‘000002.XSHE’: 13.542388888888889, ‘601211.XSHG’: 15.804444444444448}, {‘000001.XSHE’: 8.024166666666666, ‘603177.XSHG’: nan, ‘000002.XSHE’: 11.185, ‘601211.XSHG’: 15.573333333333336})
备注：

返回结果与通达信与东方财富一致，与同花顺不一致
计算方式与通达信和东方财富相同，与同花顺不同
用法注释：

MIKE指标共有六条曲线，上方三条压力线，下方三条支撑线；
当股价往压力线方向涨升时，其下方支撑线不具参考价值；
当股价往支撑线方向下跌时，其上方压力线不具参考价值；
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 MIKE 值
stor1, midr1, wekr1, weks1, mids1, stos1 = MIKE(security_list1,check_date='2017-01-04',timeperiod = 10)
print stor1[security_list1]
print midr1[security_list1]
print wekr1[security_list1]
print weks1[security_list1]
print mids1[security_list1]
print stos1[security_list1]

# 输出 security_list2 的 MIKE 值
stor2, midr2, wekr2, weks2, mids2, stos2 = MIKE(security_list2,check_date='2017-01-04', timeperiod = 10)
for stock in security_list2:
    print stor2[stock]
    print midr2[stock]
    print wekr2[stock]
    print weks2[stock]
    print mids2[stock]
    print stos2[stock]
PBX-瀑布线

PBX(security_list, check_date, timeperiod = 9):
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

PBX的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 8.4039531237966347, ‘603177.XSHG’: nan, ‘000002.XSHE’: 17.843806850286313, ‘601211.XSHG’: 16.843910079955958}
备注：

返回结果与通达信和同花顺一致，东方财富没有该指标
计算方式与通达信和同花顺相同
用法注释：

股价上升穿越轨道线上限时，回档机率大；
股价下跌穿越轨道线下限时，反弹机率大；
股价波动于轨道线内时，代表常态行情，此时，超买超卖指标可发挥效用；
股价波动于轨道线外时，代表脱轨行情，此时，应使用趋势型指标。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 PBX 值
PBX1 = PBX(security_list1,check_date='2017-01-04', timeperiod = 9)
print PBX1[security_list1]

# 输出 security_list2 的 PBX 值
PBX2 = PBX(security_list2,check_date='2017-01-04', timeperiod = 9)
for stock in security_list2:
    print PBX2[stock]
XS-薛斯通道

XS(security_list, check_date, timeperiod = 13)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

SUP SDN LUP LDN 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.919597907192415, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.023175426273021, ‘601211.XSHG’: 17.912385099606233}, {‘000001.XSHE’: 7.9098321063781789, ‘603177.XSHG’: nan, ‘000002.XSHE’: 16.869608396883621, ‘601211.XSHG’: 15.884567918518734}, {‘000001.XSHE’: 9.5082405240369283, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.585636157538445, ‘601211.XSHG’: 18.877898148622897}, {‘000001.XSHE’: 7.1728832023436473, ‘603177.XSHG’: nan, ‘000002.XSHE’: 16.283900960950056, ‘601211.XSHG’: 14.241221410364643})
备注：

返回结果与通达信一致，与东方财富不同，同花顺没有该指标
计算方式与通达信相同，与东方财富不同。
用法注释：

薛斯建立于薛斯的循环理论的基础上，属于短线指标。在薛斯通道中，股价实际上是被短期小通道包容着在长期大通道中上下运行，基本买卖策略是当短期小通道接近长期大通道时，预示着趋势的近期反转。在上沿接近时趋势向下反转，可扑捉短期卖点。在下沿接近时趋势向上反转，可捕捉短期买点。研究这个方法可以在每一波行情中成功地逃顶捉底，寻求最大限度的赢利。薛斯通道的研判法则: 
长期大通道是反映该股票的长期趋势状态，趋势有一定惯性，延伸时间较长，反映股票大周期，可以反握 股票整体趋势，适于中长线投资；
短期小通道反映该股票的短期走势状态，包容股票的涨跌起伏，有效地滤除股票走势中的频繁振动，但保留了股票价格在大通道内的上下波动，反映股票小周期，适于中短线炒作；
长期大通道向上，即大趋势总体向上 ，此时短期小通道触及（或接近长期大通道底部时，即买压增大，有反弹的可能。而短期小通道触及长期大通道顶部，既卖压增大，形态出现回调或盘整，有向长期大通道靠近的趋势。如果K线走势与短期小通道走势亦吻合得很好，那么更为有效；
长期大通道向上，而短期小通道触及长期大通道顶此时该股为强力拉长阶段，可适当观望，待短期转平转头向下时，为较好出货点，但穿透区为风险区应注意反转信号，随时出货；
长期大通道向下，即大趋势向下，此时短期小通道或价触顶卖压增加，有再次下跌趋势。而触底形态即买增大，有缓跌调整或止跌要求，同时价格运动将趋向近长期大通道上沿。回调宜慎重对待，待确认反转后方可买入；
长期大通道向下，而短期小通道向下穿透长期大通道线，此时多为暴跌过程，有反弹要求，但下跌过程会续，不宜立即建仓，应慎重，待长期大通道走平且有上趋势，短期小通道回头向上穿回时，是较好的低位仓机会；
当长期大通道长期横向走平时，为盘整行情，价格沿道上下震荡，此时为调整、建仓、洗盘阶段，预示着一轮行情的出现，短线炒家可逢高抛出，逢低买入。以短期小通道强力上穿长期大通道，且长期大通道转向，表明强劲上涨行情开始。若以短期小通道向下透长期大通道，且长期大通道向下转向，表明下跌将续。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 XS 值
sup1, sdn1, lup1, ldn1 = XS(security_list1,check_date='2017-01-04',timeperiod = 13)
print sup1[security_list1]
print sdn1[security_list1]
print lup1[security_list1]
print ldn1[security_list1]

# 输出 security_list2 的 XS 值
sup2, sdn2, lup2, ldn2 = XS(security_list2,check_date='2017-01-04', timeperiod = 13)
for stock in security_list2:
    print sup2[stock]
    print sdn2[stock]
    print lup2[stock]
    print ldn2[stock]
XS2-薛斯通道2

XS2(security_list, check_date, N = 102, M = 7)
参数：

security_list：股票列表
check_date: 要查询数据的日期
N：统计的天数
M：统计的天数
返回：

PASS1 PASS2 PASS3 PASS4 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.4950699999999948, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.858490000000007, ‘601211.XSHG’: 16.910580000000024}, {‘000001.XSHE’: 8.1619299999999946, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.040510000000005, ‘601211.XSHG’: 16.247420000000023}, {‘000001.XSHE’: 8.902368598745646, ‘603177.XSHG’: nan, ‘000002.XSHE’: 22.024829980205435, ‘601211.XSHG’: 18.300698543678497}, {‘000001.XSHE’: 7.7375727073209815, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.143076524851448, ‘601211.XSHG’: 15.9062146220757})
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信和相同。
用法注释：

特点:

根据通道形态找出波动的短周期,长周期是多少。
根据周期预测股票的后期走势。
股价的波动周期的各底是买入时机,股价的波动各顶是卖出时机。
用法:

当股价运行到短周期通道的下轨时是短线买入机会,当股价运行到短周期通道的上轨时是短线的卖出时机。
当股价运行到长周期的下轨时是中长线买入时机,而当股价运行到长周期的上轨时是中长线的卖出时机。
当短周期运行到长周期的下轨时，从下向上突破长周期的下轨时是买入时机，而当短周期运行到长周期的上轨时，从上向下突破长周期的上轨时为卖出时机。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 XS2 值
pass1, pass2, pass3, pass4 = XS2(security_list1,check_date='2017-01-04',N=102,M=7)
print pass1[security_list1]
print pass2[security_list1]
print pass3[security_list1]
print pass4[security_list1]

# 输出 security_list2 的 XS2 值
pass_1, pass_2, pass_3, pass_4 = XS2(security_list2,check_date='2017-01-04', N=102,M=7)
for stock in security_list2:
    print pass_1[stock]
    print pass_2[stock]
    print pass_3[stock]
    print pass_4[stock]
其他型

EMA-指数移动平均

EMA(security_list, check_date, timeperiod=30)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数timeperiod
返回：

EMA 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如： {‘000001.XSHE’: 9.2093998886039152, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.508006572807883, ‘601211.XSHG’: 18.477471693552996}
备注：

EMA(X,N)，求X的N日指数平滑移动平均。
通达信，同花顺和东方财富软件中没有独立的EMA指标，但在技术指标公式中很常见
用法注释：

返回指数移动平均

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 EMA 值
EMA1 = EMA(security_list1, check_date='2017-01-04', timeperiod=30)
print EMA1[security_list1]

# 输出 security_list2 的 EMA 值
EMA2 = EMA(security_list2, check_date='2017-01-04', timeperiod=30)
for stock in security_list2:
    print EMA2[stock]
SMA-移动平均

SMA(security_list, check_date, N = 7, M = 1)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
M：权重 M
返回：

SMA(X的 N 日移动平均) 的值。
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 9.2162678826932893, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.728620789626724, ‘601211.XSHG’: 18.560024926286996}
备注：

SMA(X, N, M)， 求X的N日移动平均，M为权重。
与EMA指标类似，通达信，同花顺和东方财富软件中都没有独立的SMA指标，但在技术指标公式中很常见
用法注释：

返回移动平均

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 SMA 值
SMA1 = SMA(security_list1, check_date='2017-01-04', N = 7, M = 1)
print SMA1[security_list1]

# 输出 security_list2 的 SMA 值
SMA2 = SMA(security_list2, check_date='2017-01-04', N = 7, M = 1)
for stock in security_list2:
    print SMA2[stock]
BDZX-波段之星

BDZX(security_list, check_date, timeperiod = 40)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

AK AD1 AJ AA BB CC BUY SELL的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 22.397881644648351, ‘603177.XSHG’: nan, ‘000002.XSHE’: 108.93248196853847, ‘601211.XSHG’: 18.728878312355658}, {‘000001.XSHE’: 15.461025692779121, ‘603177.XSHG’: nan, ‘000002.XSHE’: 105.76639666053059, ‘601211.XSHG’: 10.553105095800039}, {‘000001.XSHE’: 36.271593548386811, ‘603177.XSHG’: nan, ‘000002.XSHE’: 115.26465258455423, ‘601211.XSHG’: 35.080424745466892}, {‘000001.XSHE’: 100, ‘603177.XSHG’: nan, ‘000002.XSHE’: 100, ‘601211.XSHG’: 100}, {‘000001.XSHE’: 0, ‘603177.XSHG’: nan, ‘000002.XSHE’: 0, ‘601211.XSHG’: 0}, {‘000001.XSHE’: 80, ‘603177.XSHG’: nan, ‘000002.XSHE’: 80, ‘601211.XSHG’: 80}, {‘000001.XSHE’: 20, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20, ‘601211.XSHG’: 20}, {‘000001.XSHE’: 20, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20, ‘601211.XSHG’: 20})
备注：

由于复权因子不同的原因，返回结果与通达信结果有微小差异，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的BDZX值
ak1, ad11, aj1, aa1, bb1, cc1, buy1, sell1 = BDZX(security_list1,check_date='2017-01-04',timeperiod = 40)
print ak1[security_list1]
print ad11[security_list1]
print aj1[security_list1]
print aa1[security_list1]
print bb1[security_list1]
print cc1[security_list1]
print buy1[security_list1]
print sell1[security_list1]

# 输出 security_list2 的BDZX值
ak2, ad12, aj2, aa2, bb2, cc2, buy2, sell2 = BDZX(security_list2,check_date='2017-01-04',timeperiod = 40)
for stock in security_list2:
    print ak2[stock]
    print ad12[stock]
    print aj2[stock]
    print aa2[stock]
    print bb2[stock]
    print cc2[stock]
    print buy2[stock]
    print sell2[stock]
CDP-STD-逆势操作

CDP_STD(security_list, check_date, timeperiod = 2)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

CDP AH NH NL AL的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.2999999999999989, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.716666666666669, ‘601211.XSHG’: 16.420000000000002}, {‘000001.XSHE’: 8.3999999999999986, ‘603177.XSHG’: nan, ‘000002.XSHE’: 23.683333333333337, ‘601211.XSHG’: 16.839999999999996}, {‘000001.XSHE’: 8.3399999999999981, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.903333333333336, ‘601211.XSHG’: 16.580000000000002}, {‘000001.XSHE’: 8.2799999999999976, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.123333333333338, ‘601211.XSHG’: 16.320000000000004}, {‘000001.XSHE’: 8.2199999999999971, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.343333333333341, ‘601211.XSHG’: 16.060000000000006})
备注：

返回结果与通达信结果一致，东方财富和同花顺没有该指标
计算方式与通达信相同
用法注释：

在股价波动不是很大的情况下，即开盘价位在近高值与近低值之间时，通常交易者可以在近低值价位买进，而在近高值 
价位卖出，或在近高值价位卖出，近低值价位买进；
当开盘价开在最高值或最低值附近时，则意味着跳空开高跳空开低，是一个大行情发动的开始；
投资者可以在最高值的价位去追买，在最低值的价位去追。通常，一个跳空意味着强烈的涨跌，一般有相当利润。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CDP_STD 值
cdp1, ah1, nh1, nl1, al1 = CDP_STD(security_list1,check_date='2017-01-04',timeperiod = 2)
print cdp1[security_list1]
print ah1[security_list1]
print nh1[security_list1]
print nl1[security_list1]
print al1[security_list1]

# 输出 security_list2 的 CDP_STD 值
cdp2, ah2, nh2, nl2, al2 = CDP_STD(security_list2,check_date='2017-01-04',timeperiod = 2)
for stock in security_list2:
    print cdp2[stock]
    print ah2[stock]
    print nh2[stock]
    print nl2[stock]
    print al2[stock]
CJDX-超级短线

CJDX(security_list, check_date, timeperiod = 16)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

J D X 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.11002480230239936, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.6556460504346004, ‘601211.XSHG’: 0.29901270180941614}, {‘000001.XSHE’: -0.01320344720107162, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.1633636400906964, ‘601211.XSHG’: 0.077664343546118675}, {‘000001.XSHE’: 0.11002480230239936, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.6556460504346004, ‘601211.XSHG’: 0.29901270180941614})
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CJDX 值
j1, d1, x1 = CJDX(security_list1,check_date='2017-01-04',timeperiod = 16)
print j1[security_list1]
print d1[security_list1]
print x1[security_list1]

# 输出 security_list2 的 CJDX 值
j2, d2, x2 = CJDX(security_list2,check_date='2017-01-04', timeperiod = 16)
for stock in security_list2:
    print j2[stock]
    print d2[stock]
    print x2[stock]
CYHT-财运亨通

CYHT(security_list, check_date, timeperiod = 60)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

高抛 SK SD 低吸 强弱分界 卖出 买进的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 80, ‘603177.XSHG’: nan, ‘000002.XSHE’: 80, ‘601211.XSHG’: 80}, {‘000001.XSHE’: 17.929490206459231, ‘603177.XSHG’: nan, ‘000002.XSHE’: 83.601127541849465, ‘601211.XSHG’: 12.914568429828984}, {‘000001.XSHE’: 17.146097465013412, ‘603177.XSHG’: nan, ‘000002.XSHE’: 82.349398031667931, ‘601211.XSHG’: 11.993894956959814}, {‘000001.XSHE’: 20, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20, ‘601211.XSHG’: 20}, {‘000001.XSHE’: 50, ‘603177.XSHG’: nan, ‘000002.XSHE’: 50, ‘601211.XSHG’: 50}, {‘000001.XSHE’: 78, ‘603177.XSHG’: nan, ‘000002.XSHE’: 78, ‘601211.XSHG’: 78}, {‘000001.XSHE’: 40, ‘603177.XSHG’: nan, ‘000002.XSHE’: 22, ‘601211.XSHG’: 40})
备注：

返回结果与通达信结果一致，东方财富和同花顺没有该指标
计算方式与通达信相同
用法注释：

无
示例：

security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CYHT 值
h_throw1, sk1, sd1, weak1, bound1, sell1, buy1 = CYHT(security_list1,check_date='2017-07-03', timeperiod = 60)
print h_throw1[security_list1]
print sk1[security_list1]
print sd1[security_list1]
print weak1[security_list1]
print bound1[security_list1]
print sell1[security_list1]
print buy1[security_list1]

# 输出 security_list2 的 CYHT 值
h_throw2, sk2, sd2, weak2, bound2, sell2, buy2 = CYHT(security_list2,check_date='2016-01-04', timeperiod = 60)
for stock in security_list2:
    print h_throw2[stock]
    print sk2[stock]
    print sd2[stock]
    print weak2[stock]
    print bound2[stock]
    print sell2[stock]
    print buy2[stock]
JAX-济安线

JAX(security_list, check_date, timeperiod = 30)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

JAX的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8.5740591143944016, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.897541170540642, ‘601211.XSHG’: 17.019535303955521}, {‘000001.XSHE’: 8.5740591143944016, ‘603177.XSHG’: nan, ‘000002.XSHE’: nan, ‘601211.XSHG’: 17.019535303955521}, {‘000001.XSHE’: 8.308706269396076, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.390565309524611, ‘601211.XSHG’: 16.648839215213961}, {‘000001.XSHE’: 8.308706269396076, ‘603177.XSHG’: nan, ‘000002.XSHE’: nan, ‘601211.XSHG’: 16.648839215213961})
备注：

返回结果与通达信相同，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

随行情自动调整参数，在济安线上面做多，重心价低于济安线做空。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 JAX 值
jax1, j1, a1, x1 = JAX(security_list1,check_date='2017-01-04',timeperiod = 30)
print jax1[security_list1]
print j1[security_list1]
print a1[security_list1]
print x1[security_list1]

# 输出 security_list2 的 JAX 值
jax2, j2, a2, x2 = JAX(security_list2,check_date='2017-01-04', timeperiod = 30)
for stock in security_list2:
    print jax2[stock]
    print j2[stock]
    print a2[stock]
    print x2[stock]
JFZX-飓风智能中线

JFZX(security_list, check_date, timeperiod = 30)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

多头力量 空头力量 多空平衡的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 51.561349115382981, ‘603177.XSHG’: nan, ‘000002.XSHE’: 74.378474653808553, ‘601211.XSHG’: 45.557918745746676}, {‘000001.XSHE’: 48.438650884617019, ‘603177.XSHG’: nan, ‘000002.XSHE’: 25.621525346191447, ‘601211.XSHG’: 54.442081254253324}, {‘000001.XSHE’: 50, ‘603177.XSHG’: nan, ‘000002.XSHE’: 50, ‘601211.XSHG’: 50})
备注：

返回结果与通达信一致，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 JFZX 值
most1, empty1, balance1 = JFZX(security_list1,check_date='2017-01-04',timeperiod = 30)
print most1[security_list1]
print empty1[security_list1]
print balance1[security_list1]
# 输出 security_list2 的 JFZX 值
most2, empty2, balance2 = JFZX(security_list2,check_date='2017-01-04', timeperiod = 30)
for stock in security_list2:
    print most2[stock]
    print empty2[stock]
    print balance2[stock]
JYJL-交易参考均量

JYJL(security_list, check_date, N = 120, M = 5)
参数：

security_list：股票列表
check_date: 要查询数据的日期
N：统计的天数
M：统计的天数
返回：

单位时间总量 单位时间内均量的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 7182321907.0, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21805306577.0, ‘601211.XSHG’: 4912822384.0}, {‘000001.XSHE’: 299263412.79166663, ‘603177.XSHG’: nan, ‘000002.XSHE’: 908554440.70833337, ‘601211.XSHG’: 204700932.66666666})
备注：

由于复权因子不同的原因，返回结果与通达信结果有微小差异，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 JYJL 值
com1, per1 = JYJL(security_list1,check_date='2017-01-04',N = 120, M = 5)
print com1[security_list1]
print per1[security_list1]
# 输出 security_list2 的 JYJL 值
com2, per2 = JYJL(security_list2,check_date='2017-01-04', N = 120, M = 5)
for stock in security_list2:
    print com2[stock]
    print per2[stock]
LHXJ-猎狐先觉

LHXJ(security_list, check_date, timeperiod = 100)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

弃盘 控盘 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: -0.078954910995084795, ‘603177.XSHG’: nan, ‘000002.XSHE’: -2.4117024942960295, ‘601211.XSHG’: -0.55041969706332594}, {‘000001.XSHE’: 0.078954910995084795, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.4117024942960295, ‘601211.XSHG’: 0.55041969706332594})
备注：

返回结果与通达信相同，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 LHXJ 值
give_up1, control1 = LHXJ(security_list1,check_date='2017-01-04',timeperiod = 100)
print give_up1[security_list1]
print control1[security_list1]
# 输出 security_list2 的 LHXJ 值
give_up2, control2 = LHXJ(security_list2,check_date='2017-01-04', timeperiod = 100)
for stock in security_list2:
    print give_up2[stock]
    print control2[stock]
LYJH-猎鹰歼狐

LYJH(security_list, check_date, M = 80, M1 = 50)
参数：

security_list：股票列表
check_date: 要查询数据的日期
M：统计的天
M1：统计的天数
返回：

EMPTY MOST LH LH1的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 70.233318935447187, ‘603177.XSHG’: nan, ‘000002.XSHE’: 3.3460592852753157, ‘601211.XSHG’: 75.765157023322814}, {‘000001.XSHE’: 41.673107311405985, ‘603177.XSHG’: nan, ‘000002.XSHE’: 77.29146032043505, ‘601211.XSHG’: 43.650685322144895}, {‘000001.XSHE’: 80, ‘603177.XSHG’: nan, ‘000002.XSHE’: 80, ‘601211.XSHG’: 80}, {‘000001.XSHE’: 50, ‘603177.XSHG’: nan, ‘000002.XSHE’: 50, ‘601211.XSHG’: 50})
备注：

返回结果与通达信结果有微小差异，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 LYJH 值
empty1, most1, lh1, lh11 = LYJH(security_list1,check_date='2017-01-04',M = 80, M1 = 50)
print empty1[security_list1]
print most1[security_list1]
print lh1[security_list1]
print lh11[security_list1]

# 输出 security_list2 的 LYJH 值
empty2, most2, lh2, lh12 = LYJH(security_list2,check_date='2017-01-04',M = 80, M1 = 50)
for stock in security_list2:
    print empty2[stock]
    print most2[stock]
    print lh2[stock]
    print lh12[stock]
TBP-STD-趋势平衡点

TBP_STD(security_list, check_date, timeperiod=30)
参数：

security_list：股票列表
check_date：要查询数据的日期
timeperiod：统计的天数
返回：

tbp，多头获利，多头停损，空头回补和空头停损的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 7.6199999999999992, ‘603177.XSHG’: nan, ‘000002.XSHE’: 19.489999999999998, ‘601211.XSHG’: 14.91}, {‘000001.XSHE’: 7.9133333333333331, ‘603177.XSHG’: nan, ‘000002.XSHE’: 21.903333333333336, ‘601211.XSHG’: 15.940000000000001}, {‘000001.XSHE’: 7.4466666666666663, ‘603177.XSHG’: nan, ‘000002.XSHE’: 18.786666666666669, ‘601211.XSHG’: 14.67}, {‘000001.XSHE’: nan, ‘603177.XSHG’: nan, ‘000002.XSHE’: nan, ‘601211.XSHG’: nan}, {‘000001.XSHE’: nan, ‘603177.XSHG’: nan, ‘000002.XSHE’: nan, ‘601211.XSHG’: nan})
备注：

返回结果与通达信一致，没有该指标
计算方式与通达信
用法注释：

一.开始进场 
当收盘价高于TBP时，在收盘的那一刻，应该进场买入股票；
当收盘价低于TBP时，在收盘的那一刻，应该卖出股票出场或融券放空；
二.市况反转（股价未触及了结点或停损点时） 
当收盘价高于TBP时，在收盘的那一刻，应该把空头交易改为多头交易；
当收盘价低于TBP时，在收盘的那一刻，应该把多头交易改为空头交易；
三.出场 
当股价抵达了结点时，应获利了结出场，但不能反转；
当股价碰触停损点时，应停损出场，但不能反转；
四.重新进场 
出场后，须依据收盘时的TBP来决定是否重新进场；
五.决定明天的TBP 
如果市况是多头，则先挑出前两天速量因子中较小者，然后，再与昨天的收盘价相加，即可求出明天的TBP；
如果市况是空头，则先挑出前两天速量加子中较大者，然后，再与昨天的收盘 价相加，即可求出明天的TBP。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 TBP-STD 值
tbp,dthl,dtts,kthb,ktts = TBP_STD(security_list1, check_date='2017-01-04', timeperiod=30)
print tbp[security_list1]
print dthl[security_list1]
print dtts[security_list1]
print dthb[security_list1]
print dtts[security_list1]
# 输出 security_list2 的 TBP-STD 值
tbp,dthl,dtts,kthb,ktts = TBP_STD(security_list1, check_date='2017-01-04', timeperiod=30)
for stock in security_list2:
    print tbp[stock]
    print dthl[stock]
    print dtts[stock]
    print dthb[stock]
    print dtts[stock]
ZBCD-准备抄底

ZBCD(security_list, check_date, timeperiod = 10)
参数：

security_list：股票列表
check_date: 要查询数据的日期
timeperiod：统计的天数
返回：

抄底 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 2.2391834797025112, ‘603177.XSHG’: nan, ‘000002.XSHE’: 22.322622024365632, ‘601211.XSHG’: 4.8837093022246734}
备注：

返回结果与通达信结果有微小差异，东方财富和同花顺没有该指标
计算方式与通达信相同。
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 ZBCD 值
cd1 = ZBCD(security_list1,check_date='2017-01-04',timeperiod = 10)
print cd1[security_list1]

# 输出 security_list2 的 ZBCD 值
cd2 = ZBCD(security_list2,check_date='2017-01-04', timeperiod = 10)
for stock in security_list2:
    print cd2[stock]
神系

SG-SMX-生命线

SG_SMX(index_stock, security_list, check_date, N = 50)
参数：

index_stock: 大盘股票代码
security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

ZY1, ZY2 和 ZY3 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 1.8249767841949445, ‘603177.XSHG’: nan, ‘000002.XSHE’: 4.1215983992887697, ‘601211.XSHG’: 3.6984717987521352}, {‘000001.XSHE’: 1.8127958869845739, ‘603177.XSHG’: nan, ‘000002.XSHE’: 4.1584984587193548, ‘601211.XSHG’: 3.6942602296341875}, {‘000001.XSHE’: 1.7890675015767712, ‘603177.XSHG’: nan, ‘000002.XSHE’: 4.2813808808869398, ‘601211.XSHG’: 3.6389978817776334})
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同
没有计算通达信公式中跟输出结果无关的数据
用法注释：

无
示例：

# 定义股票池列表
index_stock = '399001.XSHE'
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 SMX 值
ZY1, ZY2, ZY3 = SG_SMX(index_stock, security_list1, check_date='2017-01-04', N = 50)
print ZY1[security_list1]
print ZY2[security_list1]
print ZY3[security_list1]

# 输出 security_list2 的 SMX 值
ZY1, ZY2, ZY3 = SG_SMX(index_stock, security_list2, check_date='2017-01-04', N = 50)
for stock in security_list2:
    print ZY1[stock]
    print ZY2[stock]
    print ZY3[stock]
SG-LB-量比

SG_LB(index_stock, security_list, check_date)
参数：

index_stock: 大盘股票代码
security_list：股票列表
check_date：要查询数据的日期
返回：

SG_LB,MA5和MA10 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 10.109096220368592, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.7192841800000771, ‘601211.XSHG’: 4.0452705438643175}, {‘000001.XSHE’: 8.6241703174432391, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.9900942255843939, ‘601211.XSHG’: 4.4009642301227458}, {‘000001.XSHE’: 9.0082294808292254, ‘603177.XSHG’: nan, ‘000002.XSHE’: 3.9101232166994464, ‘601211.XSHG’: 4.6234315070278713})
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同
用法注释：

无
示例：

# 定义股票池列表
index_stock = '399106.XSHE'
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 SG-LB 值
LB,MA5,MA10 = SG_LB(index_stock, security_list1, check_date='2017-01-04')
print LB[security_list1]
print MA5[security_list1]
print MA10[security_list1]

# 输出 security_list2 的 SG-LB 值
LB,MA5,MA10 = SG_LB(index_stock, security_list2, check_date='2017-01-04')
for stock in security_list2:
    print LB[stock]
    print MA5[stock]
    print MA10[stock]
SG-PF-强势股评分

SG_PF(index_stock, security_list, check_date)
参数：

index_stock：大盘股票代码
security_list：股票列表
check_date：要查询数据的日期
返回：

强势股评分 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 20, ‘603177.XSHG’: nan, ‘000002.XSHE’: 15, ‘601211.XSHG’: 10}
备注：

返回结果与通达信和同花顺不一致，东方财富没有该指标
计算方式与通达信和同花顺不完全一致
对公式有修改，将计算A1,A2,A3,A4的公式（如 A1:IF(ZY1>HHV(ZY1,3),10,0);）修改为A1:IF(ZY1>=HHV(ZY1,3),10,0)，原因在于条件ZY1>HHV(ZY1,3)永不成立，就没有存在的意义，且考虑到公式是求一支股票的强势程度，即今天的ZY1是N日内的最大值，所以加了等于号
用法注释：

无
示例：

# 定义股票池列表
index_stock = '399001.XSHE'
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 SG-PF 值
PF1 = SG_PF(index_stock, security_list1, check_date='2017-01-04')
print PF1[security_list1]

# 输出 security_list2 的 SG-PF 值
PF2 = SG_PF(index_stock, security_list2, check_date='2017-01-04')
for stock in security_list2:
    print PF2[stock]
XDT-心电图

XDT(index_stock,security_list, check_date, P1 = 5, P2 = 10)
参数：

security_list：股票列表
check_date：要查询数据的日期
P1：统计的天数 P1
P2：统计的天数 P2
返回：

QR,MAQR1和MAQR2 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 0.91082877183074495, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.0548217717445239, ‘601211.XSHG’: 1.8365403667306197}, {‘000001.XSHE’: 0.91460263585968915, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.0651657576824887, ‘601211.XSHG’: 1.8592000444660219}, {‘000001.XSHE’: 0.91681359839247212, ‘603177.XSHG’: nan, ‘000002.XSHE’: 2.0851497017887906, ‘601211.XSHG’: 1.8742782030819618})
备注：

返回结果与通达信，同花顺和东方财富一致
计算方式与通达信，同花顺和东方财富相同
用法注释：

无
示例：

# 定义股票池列表
index_stock = '399001.XSHE'
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 XDT 值
QR1,MAQR11,MAQR12 = XDT(index_stock, security_list1, check_date='2017-01-04', P1 = 5, P2 = 10)
print QR1[security_list1]
print MAQR11[security_list1]
print MAQR12[security_list1]

# 输出 security_list2 的 XDT 值
QR2,MAQR21,MAQR22 = XDT(index_stock, security_list2, check_date='2017-01-04', P1 = 5, P2 = 10)
for stock in security_list2:
    print QR2[stock]
    print MAQR21[stock]
    print MAQR22[stock]
龙系

ZLMM-主力买卖

ZLMM(security_list, check_date)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

MMS, MMM和MML 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 81.84073256710262, ‘603177.XSHG’: 100.0, ‘000002.XSHE’: 55.243339562598599, ‘601211.XSHG’: 66.72863363565412}, {‘000001.XSHE’: 77.146636073746109, ‘603177.XSHG’: 100.0, ‘000002.XSHE’: 49.409986856429853, ‘601211.XSHG’: 63.28540263029231}, {‘000001.XSHE’: 56.074044372334619, ‘603177.XSHG’: 100.00000000000001, ‘000002.XSHE’: 37.402631031296416, ‘601211.XSHG’: 53.621023102642006})
备注：

返回结果与通达信和东方财富存在微小差异，同花顺没有该指标
计算方式与通达信和东方财富相同，同花顺没有该指标
用法注释：

白线为短期趋势线，黄线为中期趋势线，紫线为长期趋势线。 
1. 主力买卖与主力进出配合使用时准确率极高。 
2. 当底部构成发出信号，且主力进出线向上时判断买点，准确率极高。 
3. 当短线上穿中线及长线时，形成最佳短线买点交叉形态（如底部构成已发出信号或主力进出线也向上且短线乖离率不大时）。 
4. 当短线、中线均上穿长线，形成中线最佳买点形态（如底部构成已发出信号或主力进出线也向上且三线均向上时）。 
5. 当短线下穿中线，且短线与长线正乖离率太大时，形成短线最佳卖点交叉形态。 
6. 当短线、中线下穿长线，且是主力进出已走平或下降时，形成中线最佳卖点交叉形态。 
7. 在上升途中，短、中线回落受长线支撑再度上行之时，为较佳的买入时机。 
8. 指标在0以上表明个股处于强势，指标跌穿0线表明该股步入弱势。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 ZLMM 值
MMS1,MMM1,MML1 = ZLMM(security_list1, check_date='2017-01-04')
print MMS1[security_list1]
print MMM1[security_list1]
print MML1[security_list1]

# 输出 security_list2 的 ZLMM 值
MMS2,MMM2,MML2 = ZLMM(security_list2, check_date='2017-01-04')
for stock in security_list2:
    print MMS2[stock]
    print MMM2[stock]
    print MML2[stock]
RAD-威力雷达

RAD(index_stock, security_list, check_date, D=3, S=30, M=30)
参数：

index_stock:大盘股票代码
security_list:股票列表
check_date：要查询数据的日期
D：统计的天数 D
S：统计的天数 S
M：统计的天数 M
返回：

RADER1和RADERMA 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 41.007798368877012, ‘603177.XSHG’: nan, ‘000002.XSHE’: -124.32686046196363, ‘601211.XSHG’: 31.098497424710864}, {‘000001.XSHE’: 61.801642266353412, ‘603177.XSHG’: nan, ‘000002.XSHE’: -145.61770337759745, ‘601211.XSHG’: 89.416830374282384})
备注：

返回结果中RADER1与通达信、同花顺和东方财富均相同，而RADERMA与通达信存在不大于1的差异，与另外两者结果不一致；三家炒股软件的RADERMA值也各不相同，应该是在计算RADERMA时设置的RADER1数据的长度不同造成的
计算方式与通达信和东方财富相同，与同花顺不相同
用法注释：

RAD 曲线往上跷升越陡者，代表该股为强势股。
RAD 指标选择强势股的效果相当良好，请多多利用。
示例：

# 定义股票池列表
index_stock = '399001.XSHE'
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 RAD 值
RAD1,MARAD1 = RAD(index_stock, security_list1, check_date='2017-01-04', D=3, S=30, M=30)
print RAD1[security_list1]
print MARAD1[security_list1]

# 输出 security_list2 的 RAD 值
RAD2,MARAD2 = RAD(index_stock, security_list2, check_date='2017-01-04', D=3, S=30, M=30)
for stock in security_list2:
    print RAD2[stock]
    print MARAD2[stock]
SHT-龙系短线

SHT(security_list, check_date, N=5)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

SHT和SHTMA 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 1.9308833356099495, ‘603177.XSHG’: nan, ‘000002.XSHE’: -0.47615239234731388, ‘601211.XSHG’: 2.0635067459722265}, {‘000001.XSHE’: 1.2099901505545463, ‘603177.XSHG’: nan, ‘000002.XSHE’: -0.46395687264301505, ‘601211.XSHG’: 1.9891297585929468})
备注：

返回结果与通达信和东方财富存在微小差异，同花顺没有该指标
计算方式与通达信和东方财富（指标名称为SHO）相同
计算公式中MY和SHT值相同，只输出了SHT
用法注释：

当指标曲线向上交叉其平均线时，视为短线买进信号。
当指标曲线向下交叉其平均线时，视为短线卖出信号。
本指标可搭配KDJ、DMA指标使用。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 SHT 值
SHT1,MASHT1 = SHT(security_list1, check_date='2017-01-04', N=5)
print SHT1[security_list1]
print MASHT1[security_list1]

# 输出 security_list2 的 SHT 值
SHT2,MASHT2 = SHT(security_list2, check_date='2017-01-04', N=5)
for stock in security_list2:
    print SHT2[stock]
    print MASHT2[stock]
鬼系

CYW-主力控盘

CYW(security_list, check_date)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

主力控盘 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 156.19960836507815, ‘603177.XSHG’: nan, ‘000002.XSHE’: -1.0073386373887827, ‘601211.XSHG’: 128.07126639142004}
备注：

返回结果与通达信和东方财富不一致，同花顺没有该指标
计算方式与通达信和东方财富相同
用法注释：

无
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CYW 值
CYW1 = CYW(security_list1, check_date='2017-01-04')
print CYW1[security_list1]

# 输出 security_list2 的 CYW 值
CYW2 = CYW(security_list2, check_date='2017-01-04')
for stock in security_list2:
    print CYW2[stock]
CYS-市场盈亏

CYS(security_list, check_date)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

市场盈亏 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：{‘000001.XSHE’: 1.3988916898194301, ‘603177.XSHG’: nan, ‘000002.XSHE’: -1.0261207332078812, ‘601211.XSHG’: 1.0911602313875552}
备注：

返回结果与通达信，同花顺和东方财富结果不一致
计算方式与通达信和东方财富相同，与同花顺本质上相同
用法注释：

CYS指标主要用于捕捉超跌股，CYS13<-16为短线超跌，CYS34<-22为中线超跌。一般情况下，买入超跌股，获得一个小额赢利概率较大。
注意区分某一个股超跌与大盘下跌时形成的个股超跌的差别，若大盘表现不错，但某些个股出现超跌，则这种超跌的原因是个股基本面的崩溃，风险较大，但当大盘出现调整时，部分个股调整过度，呈现出超跌状态，则是较佳的短线品种，可进行关注。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CYS 值
CYS1 = CYS(security_list1, check_date='2017-01-04')
print CYS1[security_list1]

# 输出 security_list2 的 CYS 值
CYS2 = CYS(security_list2, check_date='2017-01-04')
for stock in security_list2:
    print CYS2[stock]
特色型

AROON-阿隆指标

AROON(security_list, check_date, N = 25)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

上轨和下轨 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 8, ‘603177.XSHG’: 16, ‘000002.XSHE’: 4, ‘601211.XSHG’: 52}, {‘000001.XSHE’: 76, ‘603177.XSHG’: 68, ‘000002.XSHE’: 100, ‘601211.XSHG’: 72})
备注：

返回结果与通达信一致, 同花顺和东方财富没有该指标
计算方式与通达信相同
用法注释：

在分析Aroon指标时,主要观察三种状态:
极值0和100，当UP线达到100时，市场处于强势；如果维持在70~100之间，表示一个上升趋势。同样，如果Down线达到0，表示处于弱势，如果维持在0~30之间，表示处于下跌趋势。如果两条线同处于极值水平，则表明一个更强的趋势。
平行运动，如果两条线平行运动时，表明市场趋势被打破。可以预期该状况将持续下去，只到由极值水平或交叉穿行时为止。 　　
交叉穿行，当下行线上穿上行线时，表明潜在弱势，预期价格开始趋于下跌。反之，表明潜在强势，预期价格趋于走高。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 AROON 值
SG1,XG1 = AROON(security_list1, check_date='2017-01-04', N = 25)
print SG1[security_list1]
print XG1[security_list1]

# 输出 security_list2 的 AROON 值
SG2,XG2 = AROON(security_list2, check_date='2017-01-04', N = 25)
for stock in security_list2:
    print SG2[stock]
    print XG2[stock]
CFJT-财富阶梯

CFJT(security_list, check_date, MM = 200)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

突破，A1X，多方和空方 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 9.091020360179682, ‘603177.XSHG’: nan, ‘000002.XSHE’: 20.803750806335895, ‘601211.XSHG’: 18.557344251180741}, {‘000001.XSHE’: 0.30048617213779022, ‘603177.XSHG’: nan, ‘000002.XSHE’: -0.35335749810512884, ‘601211.XSHG’: 0.10620817622332195}, {‘000001.XSHE’: 9.0220919736614977, ‘603177.XSHG’: nan, ‘000002.XSHE’: None, ‘601211.XSHG’: 18.29222867039314}, {‘000001.XSHE’: None, ‘603177.XSHG’: nan, ‘000002.XSHE’: 26.722071885395618, ‘601211.XSHG’: None})
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同
只输出通达信公式中的赋值数据，没有画图
MM 取值200，是因为各支股票的在某些阶段的BARSLAST(CROSS(A1X,0))(即上次A1X上穿0距今天数)不一致，有的会是50左右（出现次数较多），有的是100左右（出现次数较少），在兼顾考虑程序运行占用内存的情况下，本函数选择获取MM(200)天的数据来计算，来使其尽量适用于任何股票，同时用户可以自己设置MM的取值。
用法注释：

在红色阶梯内做多，在绿色阶梯内做空。（来自新浪博客）
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 CFJT 值
TP1,A1X1,DF1,KF1 = CFJT(security_list1, check_date='2017-01-04', MM = 200)
print TP1[security_list1]
print A1X1[security_list1]
print DF1[security_list1]
print KF1[security_list1]
# 输出 security_list2 的 CFJT 值
TP2,A1X2,DF2,KF2 = CFJT(security_list1, check_date='2017-01-04', MM = 200)
for stock in security_list2:
    print TP2[stock]
    print A1X2[stock]
    print DF2[stock]
    print KF2[stock]
ZSDB-指数对比

ZSDB(index_stock, check_date)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

A和指数涨幅 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘399001.XSHE’: 10004.844999999999}, {‘399001.XSHE’: 0.73852218600089092})
备注：

返回结果与通达信一致，同花顺和东方财富没有该指标
计算方式与通达信相同
公式中需要画图部分未输出
用法注释：

无
示例：

# 定义大盘股票
index_stock = '399001.XSHE'

# 计算并输出 index_stock 的 ZSDB 值
A1,ZSZF1 = ZSDB(index_stock, check_date='2017-01-04')
print A1[index_stock]
print ZSZF1[index_stock]
图表型

ZX-重心线

ZX(security_list, check_date)
参数：

security_list：股票列表
check_date：要查询数据的日期
返回：

AV 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: -2349.7877426190771, ‘603177.XSHG’: nan, ‘000002.XSHE’: 267047.22475180856, ‘601211.XSHG’: -1726.9088373843188}, {‘000001.XSHE’: 2304.8620185057907, ‘603177.XSHG’: nan, ‘000002.XSHE’: 292638.40931959258, ‘601211.XSHG’: -3050.487984994948})
备注：

由于复权方式的不同，返回结果与通达信和同花顺均存在微小的差异，东方财富没有该指标
计算方式与通达信和同花顺相同，东方财富没有该指标
用法注释：

重心线指标，重心线是由重心价连接而成的曲线，反映历史平均价位， 
对于指数计算公式为: 
    ZX = 成交金额/成交量。 
对个股而言: 
    ZX = (最高指数＋最低指数＋收盘指数) / 3 
类似于不加权平均指数。

示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 ZX 值
AV1 = ZX(security_list1, check_date='2017-01-04')
print AV1[security_list1]

# 输出 security_list2 的 ZX 值
AV2 = ZX(security_list2, check_date='2017-01-04')
for stock in security_list2:
    print AV2[stock]
PUCU-逆时钟曲线

PUCU(security_list, check_date, N=24)
参数：

security_list：股票列表
check_date：要查询数据的日期
N：统计的天数 N
返回：

PU 和 CU 的值
返回结果类型：

字典(dict)：键(key)为股票代码，值(value)为数据。
如：({‘000001.XSHE’: 9.193749999999998, ‘603177.XSHG’: nan, ‘000002.XSHE’: 23.042083333333334, ‘601211.XSHG’: 18.68916666666667}, {‘000001.XSHE’: 631259.65249999997, ‘603177.XSHG’: nan, ‘000002.XSHE’: 540794.70458333334, ‘601211.XSHG’: 580351.75625000009})
备注：

因为复权的原因，返回结果与通达信不一致，同花顺和东方财富没有该指标
计算方式与通达信相同，同花顺和东方财富没有该指标
用法注释：

图表的曲线上有一个箭头，该处代表目前价量的位置；
曲线由绿变成红色时，视为买进信号；
曲线由红变成绿色时，视为卖出信号。
示例：

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']
# 计算并输出 security_list1 的 PUCU 值
PU1,CU1 = PUCU(security_list1, check_date='2017-01-04', N=24)
print PU1[security_list1]
print CU1[security_list1]

# 输出 security_list2 的 PUCU 值
PU2,CU2 = PUCU(security_list2, check_date='2017-01-04', N=24)
for stock in security_list2:
    print PU2[stock]
    print CU2[stock]