# 接口代码
## get_financial(symbol)	
财务数据：var=tt.get_financial('600100') ,返回值是3个DataFrame的LIST，对应3大财务报表。
## get_ipo()	
IPO新股上市数据：最新的IPO数据。
## get_tfp(Date)	
停牌复牌信息：var=tt.get_tfp('2016-10-21') ,返回值是2个DataFrame的LIST，对应停牌和复牌。
## get_brief(symbol_list)	
上市公司基础资料：symbol_list = ['600100','600000','600030','000002','300314'] 参数为LIST
## get_lastest(symbol_list)
股本，财务简报等最新数据：symbol_list = ['600100','600000','600030','000002','300314'] 参数为LIST
## get_dividend(symbol)	
分红数据：var=tt.get_dividend('600100') ,返回值是上市以来所有分红数据。
## get_allotment(symbol)	
配股数据：var=tt.get_allotment('600100') ,返回值是上市以来所有配股数据。
## get_fh_all()	
当年全部股票的分红资料：返回值可以用来给分钟K除权，也可以作为是否更新分红数据的依据。
## get_stocklist()
全部A股列表：其中包含停牌的股票 ，没有B股，这个数据其实也是截面数据，盘中可以实时刷新。
## get_last_daybar(symbol_list)	
截面数据：symbol_list = ['600100','600000','600030','000002','300314'] 参数为LIST
## get_last_tick(symbol_list)	
TICK截面数据：symbol_list = ['600100','600000','600030','000002','300314'] 参数为LIST
## get_last100_ticks(symbol_list)	
最新100条TICK：symbol_list = ['600100','600000','600030','000002','300314']返回5个DataFrame
## get_all_ticks(symbol_list)	
开盘来全部TICK：symbol_list = ['600100','600000','600030','000002','300314']返回5个DataFrame
## get_moneyflow(symbol_list)
当日资金流量截面数据：symbol_list = ['600100','600000','600030','000002','300314'] 1个DataFrame
## get_money_on_minute(symbol)	
当日资金流量每分钟数据：var=tt.get_money_on_minute('600100') ,返回值是资金流量数据
## get_money_30days(symbol)	
30天的资金流量数据：各大财经网站资金流量数据都不一样，东财的资金公式跟益盟操盘手一样。
## get_tick_history(symbol,Date)	
历史TICK接口：2009年以前的数据有缺失，建议下载2009年开始的数据。
## get_fjb(tick)	
分价表：参数为TICK数据，返回值就是股票软件中的筹码峰。可以把N天的TICK数据合并在一起，然后计算分价表。
## tick_to_min(tick,n)	
tick转分钟K：参数tick为某一天的tick数据，只能1天的tick数据，n为能被120整除的分钟数，例如：1,2,3,4,5,6,8,12,15,30,60等
## get_last_n_daybar(symbol,n,Type)	
最近N个日K：Type参数（前复权：'qfq'，后复权：'hfq'，不复权：'bfq'）。不包含当日K，属于历史数据。
## get_yearlist(symbol):	
K线数量按年列表：返回值为LIST，上市以来每年的K线数量。用于计算N个日K需要取的年份。跟上下2个接口有关联。
## get_daybar_year(symbol,year,Type)	
按年提取日K：Type参数（前复权：'qfq'，后复权：'hfq'，不复权：'bfq'）。不包含当日K，属于历史数据。
## get_all_daybar(symbol,Type)	
全部日K：Type参数（前复权：'qfq'，后复权：'hfq'，不复权：'bfq'）。不包含当日K，属于历史数据。
## get_stock_bar(symbol,Type)	
证券实时行情接口：Type参数（5分钟:1,15分钟：2,30分钟：3,60分钟：4，日K：5，周K：6）
## get_future_list(id)	
期货分类数据：id参数（id = 'dce'，得到全部品种的LIST， 或者 id = 'dce.c'，得到玉米的全部合约，返回值为LIST[0])
## get_future_symbol(id)	
某个品种的全部合约代码：id ='dce.c',返回值是玉米品种的合约代码
## get_zhuli()	
4大期货交易所的主力合约：删除了一些很不活跃的品种。
## get_future_bars(symbol,Type)
期货实时行情接口：Type参数5分钟:1,15分钟：2,30分钟：3,60分钟：4，日K：5，周K：6）,var=get_future_bars('DCE.C1701',3)
## get_future_info(symbol)	
期货合约基本信息：上市日期，交割日期，保证金，交易单位，最小变动单位等等。。。。
## get_future_tick(symbol)	
期货TICK数据：只能取到最近10分钟左右的数据，没什么用处，先放着。
## get_calendar(starttime,endtime)	
交易日历：是跟交易所有关，不是某个股票的交易日历，主要用于回测，在个股停牌期间的计算。
NOTE 蓝色接口代码链接的是数据样本，由 pandas.DataFrame.to_html 对象生成。 生成样本数据的示例代码

# 掘金量化行情数据
转换DataFrame接口列表（需要在掘金 注册个人免费版账户）

接口代码	接口说明
## get_shse()	
上交所的股票列表，包含B股。
## get_szse()	
深交所的股票列表，包含B股。
## get_dce()	
大连期货交易所的上市品种列表
## get_czce()
郑州期货交易所的上市品种列表
## get_shfe()	
上海期货交易所的上市品种列表
## get_cffex()	
中国金融期货交易所的上市品种列表
## get_constituents(index_symbol)	
指数权重数据，提供了大部分重要的大盘指数成分股权重数据，index_symbol =‘SHSE.000300’,注意指数代码格式
## get_etf()	
上证50ETF期权
## get_fund()	
沪深基金数据
## get_index()	
沪深指数列表
## get_instruments_by_name(name)	
期货接口-这里注意代码大小写，大写是连续合约，小写是具体的合约 name ='cu'( 返回值说明)
## get_financial_index(symbol, t_begin, t_end)	
财务简报( 返回值说明)：symbol = 'SHSE.600100',t_begin = '2015-01-01',t_end = '2016-10-21'
## get_last_financial_index(symbol_list)	
最新财务简报( 返回值说明)：symbol_list=['SHSE.600100','SHSE.600000','SHSE.600030','SZSE.000002','SZSE.300124']
## get_share_index(symbol_list)	
股本指标：( 返回值说明)：symbol_list=['SHSE.600100','SHSE.600000','SHSE.600030','SZSE.000002','SZSE.300124']
## get_market_index(symbol_list):	
市场指标：( 返回值说明)：symbol_list=['SHSE.600100','SHSE.600000','SHSE.600030','SZSE.000002','SZSE.300124']
## get_ticks(symbol, begin_time, end_time):	
掘金量化大概保存有10天左右的TICK。证券期货通用。begin = '2016-10-20 08:00:00'，end= '2016-10-21 15:00:00'
## get_last_ticks(symbol_list):	
TICK截面：symbol_list=['SHSE.600100','SHSE.600000','SHSE.600030','SZSE.000002','SZSE.300124']
## get_last_n_ticks(symbol, n)	
N个TICK数据：
## get_bars(symbol, bar_type, begin_time, end_time)	
掘金量化保存自2015年以来的所有分钟K，注意参数bar_type(min1:1*60,min5:5*60...min60=60*60)
## get_last_bars(symbol_list, bar_type)	
最后一个分钟K ：symbol_list=['SHSE.600100','SHSE.600000','SHSE.600030','SZSE.000002','SZSE.300124']
## get_last_n_bars(symbol, bar_type, n)	
N个分钟K ：分钟K也是历史K，不包含最后一根没有成型的K。
## get_dailybars(symbol, begin_time, end_time)	
日线历史数据:返回值中ADJ是复权因子，复权因子是简化算法，请谨慎使用。精确的算法是按照分红除权数据重新计算。
## get_last_dailybars(symbol_list)
最后一个日线BAR：
## get_last_n_dailybars(symbol, n)
N个日线K： 属于历史数据
NOTE 蓝色接口代码链接的是数据样本，由 pandas.DataFrame.to_html 对象生成。 生成样本数据的示例代码

# Formula
## MA(DF, N)	
var =pd.read_pickle('600100') #K线数据赋值,C= var['close']#声明C是‘close’收盘价，切片，MA30 = MA(C,30)
## EMA(DF, N)	
同上
## SMA(DF,N,M)	
pandas 没有提供SMA算法，这个函数是就是自己写的。
## ATR(DF,N)	
## HHV(DF,N)
## LLV(DF,N)
## SUM (DF,N)
## ABS (DF)
## MAX (A,B)
## IF (COND,V1,V2)
## REF(DF,N)
## STD(DF,N)
## MACD(DF,FAST,SLOW,MID)
## KDJ(DF,N,M1,M2)
## OSC(DF,N,M):	
变动速率线
## BBI(DF,N1,N2,N3,N4)
多空指标
## BBIBOLL(DF,N1,N2,N3,N4,N,M)
多空布林线
## PBX(DF,N1,N2,N3,N4,N5,N6)
瀑布线
## BOLL(DF,N)
布林线
## ROC(DF,N,M)
变动率指标
## MTM(DF,N,M)	
动量线
## MFI(DF,N)	
资金指标
## SKDJ(DF,N,M):
## WR(DF,N,N1)	
威廉指标
## BIAS(DF,N1,N2,N3)	
乖离率
## RSI(DF,N1,N2,N3)	
相对强弱指标
## ADTM(DF,N,M)	
动态买卖气指标
## DDI(DF,N,N1,M,M1):	
方向标准离差指数

以上公式都是数组运算，计算最后一个BAR的指标可以换个方法。

例子：计算MA30：

var =pd.read_pickle('600100')#取K线数据

C= var['close']#切片收盘价

C30 = C.tail(30)#取最后30个收盘价数据

MA30 = C30.mean()#均值

可以写在一起：MA30 = pd.read_pickle('600100')['close'].tail(30).mean()