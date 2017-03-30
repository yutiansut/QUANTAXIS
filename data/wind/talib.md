函数名：AD
名称：Chaikin A/D Line 累积/派发线（Accumulation/Distribution Line）
简介：Marc Chaikin提出的一种平衡交易量指标，以当日的收盘价位来估算成交流量，用于估定一段时间内该证券累积的资金流量。
计算公式：A/D = 昨日A/D + 多空对比 * 今日成交量
               多空对比 = [（收盘价- 最低价） - （最高价 - 收盘价）] / （最高价 - 最低价）
               若最高价等于最低价： 多空对比 = （收盘价 / 昨收盘） - 1
研判：1、A/D测量资金流向，向上的A/D表明买方占优势，而向下的A/D表明卖方占优势
　　   2、A/D与价格的背离可视为买卖信号，即底背离考虑买入，顶背离考虑卖出
　   　3、应当注意A/D忽略了缺口的影响，事实上，跳空缺口的意义是不能轻易忽略的
　　        A/D指标无需设置参数，但在应用时，可结合指标的均线进行分析
例子：real = AD(high, low, close, volume)


函数名：ADOSC
名称：Chaikin A/D Oscillator Chaikin震荡指标
简介：将资金流动情况与价格行为相对比，检测市场中资金流入和流出的情况
计算公式：fastperiod A/D - slowperiod A/D
研判：1、交易信号是背离：看涨背离做多，看跌背离做空
         2、股价与90天移动平均结合，与其他指标结合
         3、由正变负卖出，由负变正买进
例子：real = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)

函数名：OBV
名称：On Balance Volume 能量潮
简介：Joe Granville提出，通过统计成交量变动的趋势推测股价趋势
计算公式：以某日为基期，逐日累计每日上市股票总成交量，若隔日指数或股票上涨，则基期OBV加上本日成交量为本日OBV。隔日指数或股票下跌，则基期OBV减去本日成交量为本日OBV
研判：1、以“N”字型为波动单位，一浪高于一浪称“上升潮”，下跌称“跌潮”；上升潮买进，跌潮卖出
         2、须配合K线图走势
         3、用多空比率净额法进行修正，但不知TA-Lib采用哪种方法
              多空比率净额= [（收盘价－最低价）－（最高价-收盘价）] ÷（ 最高价－最低价）×成交量
例子：real = OBV(close, volume)



函数名：CDL2CROWS

名称：Two Crows 两只乌鸦

简介：三日K线模式，第一天长阳，第二天高开收阴，第三天再次高开继续收阴，收盘比前一日收盘价低，预示股价下跌。

例子：integer = CDL2CROWS(open, high, low, close)



函数名：CDL3BLACKCROWS

名称：Three Black Crows 三只乌鸦

简介：三日K线模式，连续三根阴线，每日收盘价都下跌且接近最低价，每日开盘价都在上根K线实体内，预示股价下跌。

例子：integer = CDL3BLACKCROWS(open, high, low, close)



函数名：CDL3INSIDE

名称： Three Inside Up/Down 三内部上涨和下跌

简介：三日K线模式，母子信号+长K线，以三内部上涨为例，K线为阴阳阳，第三天收盘价高于第一天开盘价，第二天K线在第一天K线内部，预示着股价上涨。

例子：integer = CDL3INSIDE(open, high, low, close)



函数名：CDL3LINESTRIKE

名称： Three-Line Strike 三线打击

简介：四日K线模式，前三根阳线，每日收盘价都比前一日高，开盘价在前一日实体内，第四日市场高开，收盘价低于第一日开盘价，预示股价下跌。

例子：integer = CDL3LINESTRIKE(open, high, low, close)



函数名：CDL3OUTSIDE

名称：Three Outside Up/Down 三外部上涨和下跌

简介：三日K线模式，与三内部上涨和下跌类似，K线为阴阳阳，但第一日与第二日的K线形态相反，以三外部上涨为例，第一日K线在第二日K线内部，预示着股价上涨。

例子：integer = CDL3OUTSIDE(open, high, low, close)



函数名：CDL3STARSINSOUTH

名称：Three Stars In The South 南方三星

简介：三日K线模式，与大敌当前相反，三日K线皆阴，第一日有长下影线，第二日与第一日类似，K线整体小于第一日，第三日无下影线实体信号，成交价格都在第一日振幅之内，预示下跌趋势反转，股价上升。

例子：integer = CDL3STARSINSOUTH(open, high, low, close)



函数名：CDL3WHITESOLDIERS

名称：Three Advancing White Soldiers 三个白兵

简介：三日K线模式，三日K线皆阳，每日收盘价变高且接近最高价，开盘价在前一日实体上半部，预示股价上升。

例子：integer = CDL3WHITESOLDIERS(open, high, low, close)



函数名：CDLABANDONEDBABY

名称：Abandoned Baby 弃婴

简介：三日K线模式，第二日价格跳空且收十字星（开盘价与收盘价接近，最高价最低价相差不大），预示趋势反转，发生在顶部下跌，底部上涨。

例子：integer = CDLABANDONEDBABY(open, high, low, close, penetration=0)



函数名：CDLADVANCEBLOCK

名称：Advance Block 大敌当前

简介：三日K线模式，三日都收阳，每日收盘价都比前一日高，开盘价都在前一日实体以内，实体变短，上影线变长。

例子：integer = CDLADVANCEBLOCK(open, high, low, close)



函数名：CDLBELTHOLD

名称：Belt-hold 捉腰带线

简介：两日K线模式，下跌趋势中，第一日阴线，第二日开盘价为最低价，阳线，收盘价接近最高价，预示价格上涨。

例子：integer = CDLBELTHOLD(open, high, low, close)



函数名：CDLBREAKAWAY

名称：Breakaway 脱离

简介：五日K线模式，以看涨脱离为例，下跌趋势中，第一日长阴线，第二日跳空阴线，延续趋势开始震荡，第五日长阳线，收盘价在第一天收盘价与第二天开盘价之间，预示价格上涨。

例子：integer = CDLBREAKAWAY(open, high, low, close)



函数名：CDLCLOSINGMARUBOZU

名称：Closing Marubozu 收盘缺影线

简介：一日K线模式，以阳线为例，最低价低于开盘价，收盘价等于最高价，预示着趋势持续。

例子：integer = CDLCLOSINGMARUBOZU(open, high, low, close)



函数名：CDLCONCEALBABYSWALL

名称： Concealing Baby Swallow 藏婴吞没

简介：四日K线模式，下跌趋势中，前两日阴线无影线，第二日开盘、收盘价皆低于第二日，第三日倒锤头，第四日开盘价高于前一日最高价，收盘价低于前一日最低价，预示着底部反转。

例子：integer = CDLCONCEALBABYSWALL(open, high, low, close)



函数名：CDLCOUNTERATTACK

名称：Counterattack 反击线

简介：二日K线模式，与分离线类似。

例子：integer = CDLCOUNTERATTACK(open, high, low, close)



函数名：CDLDARKCLOUDCOVER

名称：Dark Cloud Cover 乌云压顶

简介：二日K线模式，第一日长阳，第二日开盘价高于前一日最高价，收盘价处于前一日实体中部以下，预示着股价下跌。

例子：integer = CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)



函数名：CDLDOJI

名称：Doji 十字

简介：一日K线模式，开盘价与收盘价基本相同。

例子：integer = CDLDOJI(open, high, low, close)



函数名：CDLDOJISTAR

名称：Doji Star 十字星

简介：一日K线模式，开盘价与收盘价基本相同，上下影线不会很长，预示着当前趋势反转。

例子：integer = CDLDOJISTAR(open, high, low, close)



函数名：CDLDRAGONFLYDOJI

名称：Dragonfly Doji 蜻蜓十字/T形十字

简介：一日K线模式，开盘后价格一路走低，之后收复，收盘价与开盘价相同，预示趋势反转。

例子：integer = CDLDRAGONFLYDOJI(open, high, low, close)



函数名：CDLENGULFING

名称：Engulfing Pattern 吞噬模式

简介：两日K线模式，分多头吞噬和空头吞噬，以多头吞噬为例，第一日为阴线，第二日阳线，第一日的开盘价和收盘价在第二日开盘价收盘价之内，但不能完全相同。

例子：integer = CDLENGULFING(open, high, low, close)



函数名：CDLEVENINGDOJISTAR

名称：Evening Doji Star 十字暮星

简介：三日K线模式，基本模式为暮星，第二日收盘价和开盘价相同，预示顶部反转。

例子：integer = CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)



函数名：CDLEVENINGSTAR

名称：Evening Star 暮星

简介：三日K线模式，与晨星相反，上升趋势中，第一日阳线，第二日价格振幅较小，第三日阴线，预示顶部反转。

例子：integer = CDLEVENINGSTAR(open, high, low, close, penetration=0)



函数名：CDLGAPSIDESIDEWHITE

名称：Up/Down-gap side-by-side white lines 向上/下跳空并列阳线

简介：二日K线模式，上升趋势向上跳空，下跌趋势向下跳空，第一日与第二日有相同开盘价，实体长度差不多，则趋势持续。

例子：integer = CDLGAPSIDESIDEWHITE(open, high, low, close)



函数名：CDLGRAVESTONEDOJI

名称：Gravestone Doji 墓碑十字/倒T十字

简介：一日K线模式，开盘价与收盘价相同，上影线长，无下影线，预示底部反转。

例子：integer = CDLGRAVESTONEDOJI(open, high, low, close)



函数名：CDLHAMMER

名称：Hammer 锤头

简介：一日K线模式，实体较短，无上影线，下影线大于实体长度两倍，处于下跌趋势底部，预示反转。

例子：integer = CDLHAMMER(open, high, low, close)



函数名：CDLHANGINGMAN

名称：Hanging Man 上吊线

简介：一日K线模式，形状与锤子类似，处于上升趋势的顶部，预示着趋势反转。

例子：integer = CDLHANGINGMAN(open, high, low, close)



函数名：CDLHARAMI

名称：Harami Pattern 母子线

简介：二日K线模式，分多头母子与空头母子，两者相反，以多头母子为例，在下跌趋势中，第一日K线长阴，第二日开盘价收盘价在第一日价格振幅之内，为阳线，预示趋势反转，股价上升。

例子：integer = CDLHARAMI(open, high, low, close)



函数名：CDLHARAMICROSS

名称：Harami Cross Pattern 十字孕线

简介：二日K线模式，与母子县类似，若第二日K线是十字线，便称为十字孕线，预示着趋势反转。

例子：integer = CDLHARAMICROSS(open, high, low, close)



函数名：CDLHIGHWAVE

名称：High-Wave Candle 风高浪大线

简介：三日K线模式，具有极长的上/下影线与短的实体，预示着趋势反转。

例子：integer = CDLHIGHWAVE(open, high, low, close)



函数名：CDLHIKKAKE

名称：Hikkake Pattern 陷阱

简介：三日K线模式，与母子类似，第二日价格在前一日实体范围内，第三日收盘价高于前两日，反转失败，趋势继续。

例子：integer = CDLHIKKAKE(open, high, low, close)



函数名：CDLHIKKAKEMOD

名称：Modified Hikkake Pattern 修正陷阱

简介：三日K线模式，与陷阱类似，上升趋势中，第三日跳空高开；下跌趋势中，第三日跳空低开，反转失败，趋势继续。

例子：integer = CDLHIKKAKEMOD(open, high, low, close)



函数名：CDLHOMINGPIGEON

名称：Homing Pigeon 家鸽

简介：二日K线模式，与母子线类似，不同的的是二日K线颜色相同，第二日最高价、最低价都在第一日实体之内，预示着趋势反转。

例子：integer = CDLHOMINGPIGEON(open, high, low, close)



函数名：CDLIDENTICAL3CROWS

名称：Identical Three Crows 三胞胎乌鸦

简介：三日K线模式，上涨趋势中，三日都为阴线，长度大致相等，每日开盘价等于前一日收盘价，收盘价接近当日最低价，预示价格下跌。

例子：integer = CDLIDENTICAL3CROWS(open, high, low, close)



函数名：CDLINNECK

名称：In-Neck Pattern 颈内线

简介：二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低，收盘价略高于第一日收盘价，阳线，实体较短，预示着下跌继续。

例子：integer = CDLINNECK(open, high, low, close)



函数名：CDLINVERTEDHAMMER

名称：Inverted Hammer 倒锤头

简介：一日K线模式，上影线较长，长度为实体2倍以上，无下影线，在下跌趋势底部，预示着趋势反转。

例子：integer = CDLINVERTEDHAMMER(open, high, low, close)



函数名：CDLKICKING

名称：Kicking 反冲形态

简介：二日K线模式，与分离线类似，两日K线为秃线，颜色相反，存在跳空缺口。

例子：integer = CDLKICKING(open, high, low, close)



函数名：CDLKICKINGBYLENGTH

名称：Kicking - bull/bear determined by the longer marubozu 由较长缺影线决定的反冲形态

简介：二日K线模式，与反冲形态类似，较长缺影线决定价格的涨跌。

例子：integer = CDLKICKINGBYLENGTH(open, high, low, close)



函数名：CDLLADDERBOTTOM

名称：Ladder Bottom 梯底

简介：五日K线模式，下跌趋势中，前三日阴线，开盘价与收盘价皆低于前一日开盘、收盘价，第四日倒锤头，第五日开盘价高于前一日开盘价，阳线，收盘价高于前几日价格振幅，预示着底部反转。

例子：integer = CDLLADDERBOTTOM(open, high, low, close)



函数名：CDLLONGLEGGEDDOJI

名称：Long Legged Doji 长脚十字

简介：一日K线模式，开盘价与收盘价相同居当日价格中部，上下影线长，表达市场不确定性。

例子：integer = CDLLONGLEGGEDDOJI(open, high, low, close)



函数名：CDLLONGLINE

名称：Long Line Candle 长蜡烛

简介：一日K线模式，K线实体长，无上下影线。

例子：integer = CDLLONGLINE(open, high, low, close)



函数名：CDLMARUBOZU

名称：Marubozu 光头光脚/缺影线

简介：一日K线模式，上下两头都没有影线的实体，阴线预示着熊市持续或者牛市反转，阳线相反。

例子：integer = CDLMARUBOZU(open, high, low, close)



函数名：CDLMATCHINGLOW

名称：Matching Low 相同低价

简介：二日K线模式，下跌趋势中，第一日长阴线，第二日阴线，收盘价与前一日相同，预示底部确认，该价格为支撑位。

例子：integer = CDLMATCHINGLOW(open, high, low, close)



函数名：CDLMATHOLD

名称：Mat Hold 铺垫

简介：五日K线模式，上涨趋势中，第一日阳线，第二日跳空高开影线，第三、四日短实体影线，第五日阳线，收盘价高于前四日，预示趋势持续。

例子：integer = CDLMATHOLD(open, high, low, close, penetration=0)



函数名：CDLMORNINGDOJISTAR

名称：Morning Doji Star 十字晨星

简介：三日K线模式，基本模式为晨星，第二日K线为十字星，预示底部反转。

例子：integer = CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)



函数名：CDLMORNINGSTAR

名称：Morning Star 晨星

简介：三日K线模式，下跌趋势，第一日阴线，第二日价格振幅较小，第三天阳线，预示底部反转。

例子：integer = CDLMORNINGSTAR(open, high, low, close, penetration=0)



函数名：CDLONNECK

名称：On-Neck Pattern 颈上线

简介：二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低，收盘价与前一日最低价相同，阳线，实体较短，预示着延续下跌趋势。

例子：integer = CDLONNECK(open, high, low, close)



函数名：CDLPIERCING

名称：Piercing Pattern 刺透形态

简介：两日K线模式，下跌趋势中，第一日阴线，第二日收盘价低于前一日最低价，收盘价处在第一日实体上部，预示着底部反转。

例子：integer = CDLPIERCING(open, high, low, close)



函数名：CDLRICKSHAWMAN

名称：Rickshaw Man 黄包车夫

简介：一日K线模式，与长腿十字线类似，若实体正好处于价格振幅中点，称为黄包车夫。

例子：integer = CDLRICKSHAWMAN(open, high, low, close)



函数名：CDLRISEFALL3METHODS

名称：Rising/Falling Three Methods 上升/下降三法

简介： 五日K线模式，以上升三法为例，上涨趋势中，第一日长阳线，中间三日价格在第一日范围内小幅震荡，第五日长阳线，收盘价高于第一日收盘价，预示股价上升。

例子：integer = CDLRISEFALL3METHODS(open, high, low, close)



函数名：CDLSEPARATINGLINES

名称：Separating Lines 分离线

简介：二日K线模式，上涨趋势中，第一日阴线，第二日阳线，第二日开盘价与第一日相同且为最低价，预示着趋势继续。

例子：integer = CDLSEPARATINGLINES(open, high, low, close)



函数名：CDLSHOOTINGSTAR

名称：Shooting Star 射击之星

简介：一日K线模式，上影线至少为实体长度两倍，没有下影线，预示着股价下跌

例子：integer = CDLSHOOTINGSTAR(open, high, low, close)



函数名：CDLSHORTLINE

名称：Short Line Candle 短蜡烛

简介：一日K线模式，实体短，无上下影线。

例子：integer = CDLSHORTLINE(open, high, low, close)



函数名：CDLSPINNINGTOP

名称：Spinning Top 纺锤

简介：一日K线，实体小。

例子：integer = CDLSPINNINGTOP(open, high, low, close)



函数名：CDLSTALLEDPATTERN

名称：Stalled Pattern 停顿形态

简介：三日K线模式，上涨趋势中，第二日长阳线，第三日开盘于前一日收盘价附近，短阳线，预示着上涨结束。

例子：integer = CDLSTALLEDPATTERN(open, high, low, close)



函数名：CDLSTICKSANDWICH

名称：Stick Sandwich 条形三明治

简介：三日K线模式，第一日长阴线，第二日阳线，开盘价高于前一日收盘价，第三日开盘价高于前两日最高价，收盘价于第一日收盘价相同。

例子：integer = CDLSTICKSANDWICH(open, high, low, close)



函数名：CDLTAKURI

名称：Takuri (Dragonfly Doji with very long lower shadow) 探水竿

简介：一日K线模式，大致与蜻蜓十字相同，下影线长度长。

例子：integer = CDLTAKURI(open, high, low, close)



函数名：CDLTASUKIGAP

名称：Tasuki Gap 跳空并列阴阳线

简介：三日K线模式，分上涨和下跌，以上升为例，前两日阳线，第二日跳空，第三日阴线，收盘价于缺口中，上升趋势持续。

例子：integer = CDLTASUKIGAP(open, high, low, close)



函数名：CDLTHRUSTING

名称：Thrusting Pattern 插入

简介：二日K线模式，与颈上线类似，下跌趋势中，第一日长阴线，第二日开盘价跳空，收盘价略低于前一日实体中部，与颈上线相比实体较长，预示着趋势持续。

例子：integer = CDLTHRUSTING(open, high, low, close)



函数名：CDLTRISTAR

名称：Tristar Pattern 三星

简介：三日K线模式，由三个十字组成，第二日十字必须高于或者低于第一日和第三日，预示着反转。

例子：integer = CDLTRISTAR(open, high, low, close)



函数名：CDLUNIQUE3RIVER

名称：Unique 3 River 奇特三河床

简介：三日K线模式，下跌趋势中，第一日长阴线，第二日为锤头，最低价创新低，第三日开盘价低于第二日收盘价，收阳线，收盘价不高于第二日收盘价，预示着反转，第二日下影线越长可能性越大。

例子：integer = CDLUNIQUE3RIVER(open, high, low, close)



函数名：CDLUPSIDEGAP2CROWS

名称：Upside Gap Two Crows 向上跳空的两只乌鸦

简介：三日K线模式，第一日阳线，第二日跳空以高于第一日最高价开盘，收阴线，第三日开盘价高于第二日，收阴线，与第一日比仍有缺口。

例子：integer = CDLUPSIDEGAP2CROWS(open, high, low, close)



函数名：CDLXSIDEGAP3METHODS

名称：Upside/Downside Gap Three Methods 上升/下降跳空三法

简介：五日K线模式，以上升跳空三法为例，上涨趋势中，第一日长阳线，第二日短阳线，第三日跳空阳线，第四日阴线，开盘价与收盘价于前两日实体内，第五日长阳线，收盘价高于第一日收盘价，预示股价上升。

例子：integer = CDLXSIDEGAP3METHODS(open, high, low, close)