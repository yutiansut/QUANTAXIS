# QUANTAXIS-Strategy

CTA Strategy Framework Review | 策略框架综述
=====



<!-- TOC -->

- [QUANTAXIS-Strategy](#quantaxis-strategy)
- [趋势策略](#趋势策略)
    - [日内趋势策略(tick级别的回测)](#日内趋势策略tick级别的回测)
        - [菲阿里四价策略](#菲阿里四价策略)
            - [参数设置](#参数设置)
            - [交易逻辑](#交易逻辑)
        - [横盘突破策略](#横盘突破策略)
        - [唐奇安通道策略](#唐奇安通道策略)
        - [R-Breaker策略](#r-breaker策略)
            - [参数设置](#参数设置-1)
            - [交易逻辑](#交易逻辑-1)
        - [Dual Thrust策略](#dual-thrust策略)
            - [参数设置](#参数设置-2)
            - [交易逻辑](#交易逻辑-2)
        - [ATR策略](#atr策略)
            - [参数设置](#参数设置-3)
            - [交易逻辑](#交易逻辑-3)
        - [King-keltner策略](#king-keltner策略)
            - [参数设置](#参数设置-4)
            - [交易逻辑](#交易逻辑-4)
        - [实证检验部分](#实证检验部分)
            - [不同商品期货的单边回测结果](#不同商品期货的单边回测结果)
            - [组合策略的相关性与回测表现](#组合策略的相关性与回测表现)
    - [日间交易策略](#日间交易策略)
        - [均线策略](#均线策略)
        - [MACD策略](#macd策略)
        - [布林带通道策略](#布林带通道策略)
        - [布林策略Bollinger Bandit](#布林策略bollinger-bandit)
            - [参数设置](#参数设置-5)
            - [交易逻辑](#交易逻辑-5)
- [套利策略](#套利策略)
    - [关联套利](#关联套利)
        - [农产品跨品种套利](#农产品跨品种套利)
        - [基本金属跨品种套利](#基本金属跨品种套利)
        - [金融衍生品跨市跨品种套利](#金融衍生品跨市跨品种套利)
    - [内因套利](#内因套利)
        - [期现套利](#期现套利)
        - [同一品种的跨期套利](#同一品种的跨期套利)
        - [同一品种的跨市场套利](#同一品种的跨市场套利)
        - [产业链套利](#产业链套利)
            - [黑色产业链](#黑色产业链)
                - [钢产业 (螺纹钢，铁矿，焦炭)](#钢产业-螺纹钢铁矿焦炭)
                    - [套利逻辑](#套利逻辑)
                    - [策略设置](#策略设置)
                - [炼焦产业 (焦煤，焦炭)](#炼焦产业-焦煤焦炭)
                    - [套利逻辑](#套利逻辑-1)
                    - [策略设置](#策略设置-1)
            - [能源化工产业链](#能源化工产业链)
                - [甲醇制PP利润套利 (甲醇，聚丙烯)](#甲醇制pp利润套利-甲醇聚丙烯)
                    - [套利逻辑](#套利逻辑-2)
                    - [策略设置](#策略设置-2)
            - [农产品期货产业链](#农产品期货产业链)
                - [大豆提油套利 (大豆，豆粕，豆油)](#大豆提油套利-大豆豆粕豆油)
                    - [套利逻辑](#套利逻辑-3)
                - [鸡蛋利润套利 (鸡蛋，豆粕，玉米)](#鸡蛋利润套利-鸡蛋豆粕玉米)
                    - [套利逻辑](#套利逻辑-4)
                    - [策略设置](#策略设置-3)
- [风险控制](#风险控制)
    - [止损策略](#止损策略)
        - [技术指标](#技术指标)
        - [成本损失](#成本损失)
        - [趋势研判](#趋势研判)
    - [策略组合和资金曲线](#策略组合和资金曲线)
        - [马科维茨的均值方差分析](#马科维茨的均值方差分析)
        - [策略相关性以及风险收益比](#策略相关性以及风险收益比)
- [机器学习的应用](#机器学习的应用)
    - [参数优化](#参数优化)
        - [群参数优化算法](#群参数优化算法)
            - [PSO粒子群优化算法](#pso粒子群优化算法)
            - [GA遗传算法](#ga遗传算法)
            - [蚁群算法](#蚁群算法)
            - [果蝇算法](#果蝇算法)
    - [分类器](#分类器)
        - [SVM支持向量机](#svm支持向量机)
            - [原理](#原理)
            - [算法](#算法)
            - [应用](#应用)
                - [分类](#分类)
                - [预测](#预测)
        - [神经网络以及深度学习](#神经网络以及深度学习)
        - [分类树算法C5.0以及随机森林](#分类树算法c50以及随机森林)
        - [聚类算法](#聚类算法)
    - [信号分解算法](#信号分解算法)
        - [小波分析](#小波分析)
        - [EMD算法](#emd算法)
    - [迁移学习和增量算法](#迁移学习和增量算法)
    - [增强学习Reinforcements](#增强学习reinforcements)

<!-- /TOC -->

# 趋势策略

## 日内趋势策略(tick级别的回测)
日内交易策略要求所有开仓头寸都必须在日内交易时段结束前平仓出局,这种策略下资金暴露在风险中的时间最短,能获得稳定的利润收益,但也要求所选择的投资品种在日内有着较大的波动和成交量,这种策略更多应用于豆粕,螺纹钢,橡胶等商品
### 菲阿里四价策略
菲阿里四价策略是一种通道突破方法,用过计算四个核心价格作为两条通道线的支撑,前一交易日最低价,前一交易日最高价,前一交易日收盘价和当前开盘价.

#### 参数设置
上轨:上一交易日最高价
下轨:上一交易日最低价

#### 交易逻辑

当价格突破上轨时,买入开仓,当价格突破下轨时,卖出开仓

这种交易策略会遇到一定程度的假突破问题，由于多空的博弈，在突破位会出现很大的阻力，有一定程度的随机回落的可能。需要进行一定的止盈止损策略进行限制

### 横盘突破策略
横盘是指价格波动幅度较小,没有明显的上涨或者下跌趋势,这时候市场的多空力量大致均衡.当出现横盘突破,及多空力量被打破的时候,表示一方动能较强,后市价格继续朝突破方向运动的趋势性更强.

当价格在过去30根K线的高低点围绕中轴上下0.5%的范围内波动时:
上轨=过去30根K线的最高价
下轨=过去30根K线的最低价

如果价格突破上下轨则表示当前价格波动较大,形成一个入场信号,也就是说:
当价格突破上轨时,买入开仓
当价格突破下轨时,卖出开仓

### 唐奇安通道策略
唐奇安的主要思想是寻找一定时间(X)内出现的最高价和最低价
上轨:过去X天内的最高点
下轨:过去X天内的最低嗲
如果价格突破上下轨则表示价格运动较为强势,释放入场信号
当价格突破上轨时,买入开仓
当价格突破下轨时,卖出开仓

### R-Breaker策略
R-B是一个结合了日内趋势追踪和反转的策略,核心是通过前一交易日的最高.最低,收盘价计算出6个重要的价格指标.及突破买入价,观察卖出价,反转卖出价,反转买入价,观察买入价,突破卖出价.

#### 参数设置
观察卖出价=最高价+0.35*(收盘价-最低价)

观察买入价=最低价-0.35*(最高价-收盘价)

反转卖出价=1.07/2*(最高价+最低价)-0.07*最低价

反转买入价=1.07/2*(最高价+最低价)-0.07*最高价

突破买入价=观察卖出价+0.25*(观察卖出价-观察买入价)

突破卖出价=观察买入价-0.25*(观察卖出价-观察买入价)



#### 交易逻辑
1. 空仓情况下,盘中价格跌破突破卖出价,采取趋势策略,即在该点做空.
2. 空仓情况下,盘中价格超过突破买入价,采取趋势策略,即在该点做多.
3. 持多单时,当日最高价超过观察卖出价后,盘中价格回落并且跌破发转卖出价,采取反转策略,即在该点反手做空
4. 持空单时,当日最低价低于观察买入价后,盘中价格反弹并且超过反转买入价,采取反转策略,即在该点反手做多.
5. 设定止盈止损条件
6. 收盘前进行平仓

### Dual Thrust策略
在开盘价的基础上,确定一个非对称的上下轨道，利用前N日的最高，最低和收盘价格去确定一个合理的震荡区间，将上下轨到开盘价的距离设置为震荡区间的一定比例，一旦当前价格突破了这个比例，则产生入场或离场信号。

#### 参数设置
记前N日的最高价的最大值为HH,前N日的最低价的最小值为LL

记前N日的收盘价的最大值为HC,前N日的收盘价的最小值为LC

震荡区间为Range

Range = MAX{HH-LC,HC-LL};

BuyLine = Open + K_s×Range;

SellLine = Open - K_x*Range;

#### 交易逻辑

当价格突破上轨BuyLine时：买多开仓|平空反向做多

当价格突破下轨SellLine时,买空开仓|平多反向做空


Dual Thrust 策略中震荡区间的选取为前 N 日的最值,使得其在一定时期内保持相对稳定,参数K_s 和K_x 用来调节多头和空头触发条件难易。当K_s 较大时,空头较容易被触发;当K_x 较大时,多头较容易被触发。参数的调节可以通过参考数据测试得到的最优参数并结合主观分析得到。

### ATR策略

Average True Range 真实波动范围指标，用于衡量市场波动的程度，是显示市场变化率的指标。目前，主要用于衡量价格的波动，并不能直接反应价格走向以及趋势的稳定性，仅仅表明价格波动的程度。

#### 参数设置
- X1: 当前交易日的价差 PriceMax-PirceMin
- X2: 前一个交易日收盘价与当前交易日的最高价的波幅
- X3: 前一交易日的收盘价与当前交易日的最低价的波幅

 真实波幅TR=MAX{X1,X2,X3}

 TR=MAX{Max(High-Low),Abs(Ref(Close,1)-High),Abs(Ref(Close,1)-Low)}

 ATR 是TR的N日移动平均  AR=MA(TR)

 一般而言，N=14

#### 交易逻辑

- 日内平仓
- 日内ATR突破基于当
- 价格突破上轨，买入开仓
- 价格跌穿下轨，卖出开仓


### King-keltner策略

#### 参数设置

- 中心价=MA((H+L+C)/3,40)  中心价是最高价，最低价，收盘价三者平均后的40日移动平均线

- 计算真实价格区间（TrueRange），等于本日最高价-本日最低价，本日最高价-昨日收盘价，本日最低价-昨日收盘价的三者的最大值

   TR=MAX{Max(High-Low),Abs(Ref(Close,1)-High),Abs(Ref(Close,1)-Low)}

- 计算价格上下轨(upBand,dnBand),其中multi为固定参数，可设置初始值为1

  上轨=中心价+multi× MA(TR,40)

  下轨=中心价-multi× MA(TR,40)

- 平仓价格=中心价

#### 交易逻辑

- 买入开仓：今日中心价大于昨日中心价，且价格突破上轨

- 卖出开仓：今日中心价小于昨日中心价，且价格突破下轨

- 买入平仓：今日价格向下突破平仓价格

- 卖出平仓：今日价格向上突破平仓价格

  ​


其中，平仓条件既是止损条件，也是止盈条件 （移动止盈）



该策略的核心是对于multi参数和MA的天数的优化问题，风险在于，震荡时期的频繁交易会因为止损过多而导致较大回撤



### 实证检验部分

#### 不同商品期货的单边回测结果

#### 组合策略的相关性与回测表现


## 日间交易策略

### 均线策略

均线策略的内在思想是短期和长期趋势不同的涨跌变化对交易有不同的指导意义。均线策略中的均线体现了价格的变化,常用的均线有简单移动平均、加权移动平均、指数移动平均

### MACD策略



### 布林带通道策略

### 布林策略Bollinger Bandit

#### 参数设置

- 计算布林带的上下边界，等于收盘价的50日移动平均价加减1.25倍标准差

  - 上边界=MA(收盘价,50)+StdDev(收盘价,50)×1.25
  - 下边界=MA(收盘价,50)-StdDev(收盘价,50)×1.25

- 计算计步器，等于当日收盘价-30日前收盘价

  - 如果今日未平仓，则计算天数-1，直到递减到10
  - 如果今日平仓，将计算天数还原到50

- 计算止损价，等于收盘价的移动平均，计算天数初始值为50

  止损价=MA(收盘价，计算天数)

#### 交易逻辑

- 买入开仓：计步器大于0，当前价格大于上边界
- 卖出开仓：计步器小于0，且当前价格小于下边界
- 卖出平仓：当止损价大于上边界且当前价格小于止损价
- 买入平仓：当止损价小于下边界且当前价格大于止损价

# 套利策略



我们并没有使用传统的跨期套利，跨品种套利和跨市场套利去对套利算法进行区分，而是使用关联套利和内因套利去区分这几种套利方法。
## 关联套利
关联套利是指套利对象之间没有必然的内因约束，但价格受共同因素所主导，但受影响的程度不同，通过两种对象对同一影响因素表现不同而建立的套利关系称之为关联套利

关联套利：套利对象之间基差的大小不对买卖力量产生负反馈作用,多数的情况下形成一个发散性的蛛网.

盈利原理：通过追逐比价(或差价)趋势的办法，将错误操作的损失通过止损控制在一定的限度之内，将正确操作的利润尽量放大,从而达到“赚多赔少”的总体目标

关联套利理论基础:

1.供需关系决定了商品的价格趋势;供需关系紧张的程度决定了价格趋势的强度.

2.价格趋势在没有受到新的力量作用时,会保持原来的方向.（牛顿第一定律）

3.基本面不会在一天之内改变.(如农产品供应的年周期性和消费的广泛性;对于工业品而言,也存在一个较长的生产周期)

### 农产品跨品种套利

[替代性品种，并无内因关系，只是供求关系]

大豆与玉米、玉米与小麦之间、不同油脂类品种之间

### 基本金属跨品种套利

铜、铝、锌之间的套利
### 金融衍生品跨市跨品种套利
不同国家的股票指数套利



## 内因套利
内因套利是指当商品期货投资对象间价格关系因某种原因过分背离时，通过内在纠正力量而产生的套利行为。 

内因套利：套利对象之间基差的大小负反馈于买卖力量,形成一个收敛性的蛛网.

盈利原理：谨慎选择有限波动差价(或比价)两端的极端机会，提高胜算率来保证交易的成功，即使出现意外，也可以能够通过现货处理、向后延期等办法来抑制亏损

1.存在基差收缩的机制(内因)

2.市场是有效的(特别是期货市场)


核心要点：

1 寻找导致目前价格关系过分背离的原因。

2 分析未来能够纠正价格关系恢复的内在因素。


步骤：

第一步:选择经过有效性检验的、并且有内因约束的套利对象，确定套利追踪目标。

比如:大豆期现套利;大豆,豆粕,豆油的远近合约套利;大豆与豆粕,豆油三者的压榨套利;连豆和CBOT黄大豆之间跨市套利等等.

第二步:建立上述套利对象的历史比价（差价）数据库，并每日更新。

第三步:将当前比价（差价）分别导入各套利对象的比价（差价）区间，用数理的方法鉴别出当前比价（差价）在区间中所处位置，并计算该比价（差价）在历史上所出现的概率。

第四步:通过数理分择,判定基差偏离程度和套利机会的大小.

第五步:内因佐证分析. 建立各影响因子的数据资料库,通过多因素分析方法来分析寻找导致目前价格关系过分背离的原因,分析未来能够纠正价格关系恢复的内在因素。

- 进口成本
- 现货走势图
- 运费变化图
- 升贴水变化图
- 仓单变化
- 压榨利润
- 政策因素
- 需求方面
- 供给方面
- 经济周期
- 政治因素
- 自然因素
- 金融因素

第六步:按照内因套利的五大原则,对套利外部环境进行评估，再次鉴别市场的有效性以及头寸的可持续性。

第七步:进入资金管理和风险控制的实际操作阶段。

### 期现套利

期现套利（Arbitrage）是利用同一种商品在期货市场与现货市场之间的不合理的价差进行的套利行为。

两个投资组合，若其未来现金流完全相同，则现值一定相等，否则将出现套利机会：买入现值较低的投资组合，同时卖出较高的投资组合，并持有到期，必定可获得无风险利润。

同一种商品的期货合约价格与其现货价格之间存在着无套利机会的定价关系，这种关系通常称为持有成本定价。所谓持有成本，是指商品的储藏成本加上为资产融资所需支付的利息再扣掉持有资产带来的收入。  

### 同一品种的跨期套利
单一农产品品种的跨期套利

同一种商品的不同交割月份的期货合约价格之间也存在着无套利机会的定价关系。当远期合约的价格超过无套利区间的上边界时，可以从事正向套利操作；而跌过无套利区间的下边界时，可以从事反向套利操作。

套利步骤：

1。通过计算无套利区间，建立套利机会每日跟踪系统。
相邻合约间跨期套利的持仓成本＝间隔期内的商品仓储费用＋交易交割手续费＋套利期内资金占压成本（贷款利息）＋增值税（（交割结算价－买入价格）×税率）


2。当满足套利条件时，开始做市场有效性检验，比如，具备不具备逼仓条件，市场容量，交易群体调查等等。

3。展期条件和展期收益评估。

4。风险评估和风险预警措施制定。

5。实施操作。

### 同一品种的跨市场套利
国内外大豆进口套利

>套利公式：

>进口利润=国内大豆价格-进口成本价

>进口成本=（CBOT期价+海岸升水+海运费）×汇率+港杂费

>进口大豆关税1%，增值税13%。

>港杂费100元/吨左右。

单位换算：

1蒲式耳大豆=60磅=60×0.4536公斤=27.216公斤=0.027216吨

1美分/蒲式耳=0.01美元/0.027216吨=0.36743美元/吨；
### 产业链套利
#### 黑色产业链
##### 钢产业 (螺纹钢，铁矿，焦炭)
炼钢生产的成本主要是生铁，废钢，合金，电极，耐火材料，辅助材料，电能，维护检修和其他费用。中国目前主要的炼钢设备为转炉和电炉，基于冶炼原理的不同，转炉和电炉在主要的原料（生铁、废钢）配比有一定的差异，转炉工艺一般需配置10%的废钢，而电炉工艺废钢的使用量则占到80％。 

结合国内钢铁企业的平均情况，炼铁工艺中影响总成本的主要因素是原料（铁矿石、焦炭）成本，而包括辅料、燃料、人工费用在内的其他费用与副产品回收进行冲抵后仅占总成本的10%左右，而炼钢工艺中因为耗电量的增加、合金的加入以及维检费用的上升使得除主要原料外的其他费用占到炼钢总成本的18％左右。炼铁、炼钢工艺中的其他费用波动不大。 

###### 套利逻辑

> 钢成本/吨=1.6吨铁精粉+0.5吨焦炭+生铁费+钢胚费+轧材费+其他费用

> 螺纹钢期货价格=1.6×铁矿石期货价格+0.5×焦炭期货价格+其他成本


在实际的期货市场上，由于价格的波动，出现了无套利等式左右不等的情况，此时的价差及为钢厂的利润，这也是内因策略的利润核心。跟随钢厂利润，我们可以认为，当钢厂利润较高，钢厂就会进行产量的调整，提高开工率并且在原材料市场上进行大量购买，导致原材料市场的供小于求，铁矿石和焦炭价格上涨，导致钢厂的利润下降；反之，如果钢厂利润下降，钢厂会动态调整最优产量从而影响了上下游产业的价格，铁矿石和焦炭价格也会下降，同时在产品市场上，由于钢厂的供给减少，钢材的价格也会上升，恢复了钢厂的利润平衡。

![炼钢利润波动](http://p1.bpimg.com/1949/c96b104b674b30c9.png)

| 期货品种   | 螺纹钢   | 铁矿石    | 焦炭     |
| ------ | ----- | ------ | ------ |
| 保证金    | 9%    | 10%    | 15%    |
| 合约乘数   | 10吨/手 | 100吨/手 | 100吨   |
| 最小变动单位 | 1元/吨  | 0.5元/吨 | 0.5元/吨 |

###### 策略设置
- 开仓条件：价差在[10日均值+标准差，10日均值+1.2×标准差],有回归趋势
- 平仓条件：回归到十日均值进行平仓
- 止损： 5%，止损后10日内不开仓
- 换仓： 主力合约一般是1,5,9 在主力合约到来的前一个月进行换仓
- 滑点： 一个最小变动价位




##### 炼焦产业 (焦煤，焦炭)

煤焦加工套利包括三种模式，分别为独立焦化企业模式、煤矿企业模式以及自有焦化厂的钢铁企业模式。煤焦加工套利的难点在于配煤炼焦工艺的确定、产成品质量及升贴水的确定、以及副产品构成及其价值的确定。一级冶炼焦的配煤比例是主焦煤占比 35%、1/3 焦煤占比 25%、气煤占比 12%、肥煤占比 18%、瘦煤占比 10%。企业为了降低炼焦的成本，一般是提高价格较低的瘦煤的比重而降低主焦煤比重，因此企业为了应对市场变化带来的成本压力会改变原料的配比，那么炼焦成本也是在变化的，配煤的比例是动态变化的，并不是固定的。

###### 套利逻辑

参考一般的炼焦工艺，平均 1.3 吨炼焦煤加工产生 1 吨焦炭和若干副产品。自焦煤期货上市以来，期货焦炭指数/焦煤指数的比价均值却高达 1.37，同时较长时间维在 1.38 以上，指数最高比价曾达到 1.45。因此，我们最终确定炼焦利润的公式为：
炼焦利润=焦炭期货价格-1.4*焦煤期货价格-其他成本



上述等式的系数是参考基本面的逻辑来确定的，与钢厂利润套利类似，等式中固定的系数与实际生产的系数存在差异，实际生产的系数也难以把握，因此通过量化的手段来确定各品种之间的关系也是一种备选方案。

![炼焦利润波动](http://p1.bpimg.com/1949/cfecf31d5c0aa617.png)

| 期货合约   | 焦煤     | 焦炭     |
| ------ | ------ | ------ |
| 保证金    | 15%    | 15%    |
| 合约乘数   | 60吨/手  | 100吨/手 |
| 最小变动单位 | 0.5元/吨 | 0.5元/吨 |



###### 策略设置

开仓条件：价差在 10 日均值加 1 倍标准差和 1.2 倍标准差之间，且有回归趋势开仓。
平仓条件：回归到 10 日均值进行平仓。
止损：设置的止损为 2%，止损后 10 天内不开仓。
换仓：主力合约一般为 1,5,9 月份，因此我们在主力合约到期前一个多月进行主力合约的换仓。
滑点：一个最小变动价位

#### 能源化工产业链

##### 甲醇制PP利润套利 (甲醇，聚丙烯)

###### 套利逻辑

甲醇既可自用又可外售的特征是甲醇制 PP 套利可行的重要原因。根据理论生产成本，3 吨甲醇另加 800 元加工费用可制得 1 吨聚丙烯。具体到期货价格的层面，在无套利机会的情况下可以得到如下等式：
聚丙烯期货价格=3*甲醇期货价格+800

![甲醇制PP利润](http://p1.bpimg.com/1949/5c64627310ac00fd.png)



| 期货品种   | 甲醇    | 聚丙烯PP |
| ------ | ----- | ----- |
| 保证金    | 7%    | 7%    |
| 合约乘数   | 10吨/手 | 5吨    |
| 最小变动单位 | 1元/吨  | 1元/吨  |

###### 策略设置

开仓条件：价差超越 5 日均值加 1 倍标准差进行开仓。
平仓条件：回归到 5 日均值进行平仓。
止损：设置的止损为 5%，止损后 10 天内不开仓。
换仓：主力合约一般为 1,5,9 月份，因此我们在主力合约到期前一个多月进行主力合约的换仓。
滑点：一个最小变动价位。

#### 农产品期货产业链

##### 大豆提油套利 (大豆，豆粕，豆油)

###### 套利逻辑

大豆提油套利的模式主要是在美豆和国内豆粕豆油间展开，具体的路径是进口美豆后在国内压榨出售。因此要关注的点是美豆成本、豆粕价格和豆油价格。美豆的成本涉及到增值税、关税、汇率、港杂费和运费等因素。计算美豆到厂成本主要公式
如下：

大船舱底完税价格=到岸价格*（1+增值税）*（1+关税）*美元兑人民币汇率

进口大豆到厂成本=大船舱底完税价格+港杂费+运费

进口大豆到厂成本即为美豆的成本。相对于煤焦钢产业链，大豆压榨的技术参数较为稳定，国内的大豆压榨工艺显示大豆压榨时油粕产出比例存在如下的关系：

100%进口大豆=19.2%豆油+78.6%豆粕+2.2.%损耗

因此，进口大豆压榨的利润公式可以根据美豆成本以及压榨的技术参数得出。

进口大豆压榨利润=豆粕价格*78.6%+豆油价格*19.2%-进口大豆到厂成本-其他费用

![Markdown](http://p1.bpimg.com/1949/7e6c02eb4beb1d17.png)





##### 鸡蛋利润套利 (鸡蛋，豆粕，玉米)

###### 套利逻辑

鸡蛋作为日常消费品，需求比较稳定。一般，每年在端午节（5 月）和中秋节（9 月）会出现两个需求小高峰，春节前后（2 月）会出现需求低谷。最近几年由于集约养殖比例增大以及鸡蛋期货上市，鸡蛋价格的季节性波动已经越来越不明显。鉴于鸡蛋需求稳定的特征，鸡蛋价格一般由产蛋成本决定。
蛋鸡养殖的主要成本包括鸡苗、饲料、水、电、人工和防疫等费用。需要注意的是，除了鸡蛋出售收入，还有鸡粪以及蛋鸡淘汰以后变卖的收入。一只蛋鸡从鸡苗到产蛋到退役，整个过程经历 17 个月。蛋鸡在生命周期内产蛋 37.5 斤，消耗饲料约 122.7 斤，鸡苗成本约 3 元，防疫费支出 3 元，水电费支出 0.5 元，鸡粪获利 3.4 元，淘汰鸡出售约 16.4 元。
据此，我们测算出：

鸡蛋盈亏平衡点=(饲料费用+鸡苗成本+防疫费+水电费-鸡粪收入-淘汰鸡收入)/37.5

上式中鸡苗成本、防疫费、水电费、鸡粪收入和淘汰鸡收入变化不大，可以使用常数替代，主要的变量是饲料价格。蛋鸡饲料的典型配方是 62%的玉米、31%的豆粕和 7%的预混料(麦麸、磷酸氢钙、石粉、食盐、其他添加剂等)，预混料价格大约在 2.5 元/斤。那么，饲料价格的公式可以表示为：

一斤饲料的价格=0.62*玉米价格 + 0.31*豆粕价格+ 0.175

依据鸡蛋的盈亏平衡点计算公式和饲料价格的公式，可以得出联系期货价格的等式。

鸡蛋盈亏平衡点(元/吨) = 2.02864*玉米(元/吨) + 1.01432*豆粕(元/吨) + 437.2

![鸡蛋利润](http://p1.bpimg.com/1949/20d0d108868848bc.png)

鸡蛋的利润波动曲线回归周期仍然比较长,并且没有明显的周期性规律,总体来看,价差要经历差不多一年的时间才会恢复到 0 附近的水平。因此如果设定固定价差来进行套利,开仓次数将很有限,而且价差设置越大开仓次数越少。如果价差设置过小,则需要很长时间才会回归,并且会有很大的回撤。因此我们仍然采用之前的在均值上加减标准差的方式进行开仓,在价差恢复到均
值时进行平仓。

###### 策略设置
开仓条件:价差超越 10 日均值加 2 倍标准差进行开仓。
平仓条件:回归到 10 日均值进行平仓。
止损:设置的止损为 5%,止损后 10 天内不开仓。
换仓:主力合约一般为 1,5,9 月份,因此我们在主力合约到期前一个多月进行主力合约的换仓。
滑点:一个最小变动价位。

# 风险控制
## 止损策略
### 技术指标
### 成本损失
### 趋势研判


## 策略组合和资金曲线
### 马科维茨的均值方差分析

### 策略相关性以及风险收益比

# 机器学习的应用
## 参数优化
### 群参数优化算法
#### PSO粒子群优化算法
通过群体中个体之间的协作和信息共享来寻找最优解．

鸟被抽象为没有质量和体积的微粒(点)，并延伸到N维空间，粒子i在N维空间的位置表示为矢量Xi＝(x1，x2，…，xN)，飞行速度表示为矢量Vi＝(v1，v2，…，vN)。每个粒子都有一个由目标函数决定的适应值(fitness value)，并且知道自己到目前为止发现的最好位置(pbest)和现在的位置Xi。这个可以看作是粒子自己的飞行经验。除此之外，每个粒子还知道到目前为止整个群体中所有粒子发现的最好位置(gbest)(gbest是pbest中的最好值)，这个可以看作是粒子同伴的经验。粒子就是通过自己的经验和同伴中最好的经验来决定下一步的运动。 
  PSO初始化为一群随机粒子(随机解)。然后通过迭代找到最优解。在每一次的迭代中，粒子通过跟踪两个“极值”(pbest，gbest)来更新自己。在找到这两个最优值后，粒子通过下面的公式来更新自己的速度和位置。


$$ v_{i}=v_{i} + c_{1} * rand()*(pbest_{i} -x_{i}) +c_{2}*rand()*(gbest_{i}-x_i)   (1)$$
$$x_{i}=x_{i}+v_{i}     (2)$$

> 在公式（1），（2）中，i=1,2,3,...,N是此群中粒子的总数

$$ v_{i} 是粒子的速度$$

$$ rand() 介于（0,1）的随机数$$
$$ x_{i}粒子的当前位置$$
$$ c_{1},c_{2} 学习因子  一般设置为2$$
$$ v_{i}的最大值为 V_{max} $$ 

公式(1)的第一部分称为【记忆项】，表示上次速度大小和方向的影响；公式(1)的第二部分称为【自身认知项】，是从当前点指向粒子自身最好点的一个矢量，表示粒子的动作来源于自己经验的部分；公式(1)的第三部分称为【群体认知项】，是一个从当前点指向种群最好点的矢量，反映了粒子间的协同合作和知识共享。粒子就是通过自己的经验和同伴中最好的经验来决定下一步的运动。

以上面两个公式为基础，形成了PSO的标准形式。

​     
$$v_{i}=\omega *v_{i}+c_{i}*rand()*(pbest_{i}-x_{i})+c_2×rand()*(gbest_{i}-x_{i}) (3)$$   
$$ \omega 为惯性因子 值为非负$$

公式(2)和 公式(3)被视为标准PSO算法。

标准PSO算法流程

    1）初始化一群微粒(群体规模为N)，包括随机位置和速度；

    2）评价每个微粒的适应度；

    3）对每个微粒，将其适应值与其经过的最好位置pbest作比较，如果较好，则将其作为当前的最好位置pbest；

    4）对每个微粒，将其适应值与其经过的最好位置gbest作比较，如果较好，则将其作为当前的最好位置gbest；

    5）根据公式(2)、(3)调整微粒速度和位置；

    6）未达到结束条件则转第2）步

迭代终止条件根据具体问题一般选为最大迭代次数Gk或(和)微粒群迄今为止搜索到的最优位置满足预定最小适应阈值。

公式(2)和(3)中pbest和gbest分别表示微粒群的局部和全局最优位置。

当C1＝0时，则粒子没有了认知能力，变为只有社会的模型(social-only)：

​     

被称为全局PSO算法。粒子有扩展搜索空间的能力，具有较快的收敛速度，但由于缺少局部搜索，对于复杂问题比标准PSO 更易陷入局部最优。

当C2＝0时，则粒子之间没有社会信息，模型变为只有认知(cognition-only)模型：

​     

被称为局部PSO算法。由于个体之间没有信息的交流，整个群体相当于多个粒子进行盲目的随机搜索，收敛速度慢，因而得到最优解的可能性小。

参数分析
参数：群体规模N，惯性因子 ，学习因子c1和c2，最大速度Vmax，最大迭代次数Gk。

群体规模N：一般取20～40，对较难或特定类别的问题可以取到100～200。

最大速度Vmax：决定当前位置与最好位置之间的区域的分辨率(或精度)。如果太快，则粒子有可能越过极小点；如果太慢，则粒子不能在局部极小点之外进行足够的探索，会陷入到局部极值区域内。这种限制可以达到防止计算溢出、决定问题空间搜索的粒度的目的。

权重因子：包括惯性因子和学习因子c1和c2。使粒子保持着运动惯性，使其具有扩展搜索空间的趋势，有能力探索新的区域。c1和c2代表将每个粒子推向pbest和gbest位置的统计加速项的权值。较低的值允许粒子在被拉回之前可以在目标区域外徘徊，较高的值导致粒子突然地冲向或越过目标区域。

参数设置：

1) 如果令c1＝c2＝0，粒子将一直以当前速度的飞行，直到边界。很难找到最优解。
2) 如果＝0，则速度只取决于当前位置和历史最好位置，速度本身没有记忆性。假设一个粒子处在全局最好位置，它将保持静止，其他粒子则飞向它的最好位置和全局最好位置的加权中心。粒子将收缩到当前全局最好位置。在加上第一部分后，粒子有扩展搜索空间的趋势，这也使得的作用表现为针对不同的搜索问题，调整算法的全局和局部搜索能力的平衡。较大时，具有较强的全局搜索能力；较小时，具有较强的局部搜索能力。

3) 通常设c1＝c2＝2。Suganthan的实验表明：c1和c2为常数时可以得到较好的解，但不一定必须等于2。Clerc引入收敛因子(constriction factor) K来保证收敛性。


​       
通常取为4.1,则K＝0.729.实验表明，与使用惯性权重的PSO算法相比，使用收敛因子的PSO有更快的收敛速度。其实只要恰当的选取和c1、c2，两种算法是一样的。因此使用收敛因子的PSO可以看作使用惯性权重PSO的特例。

恰当的选取算法的参数值可以改善算法的性能。
​         

```python
class bird:
"""
speed:速度
position:位置
fit:适应度
lbestposition:经历的最佳位置
lbestfit:经历的最佳的适应度值
"""
def __init__(self, speed, position, fit, lBestPosition, lBestFit):
    self.speed = speed
    self.position = position
    self.fit = fit
    self.lBestFit = lBestPosition
    self.lBestPosition = lPestFit

```

```python
import random

class PSO:
    """
    fitFunc:适应度函数
    birdNum:种群规模
    w:惯性权重
    c1,c2:个体学习因子，社会学习因子
    solutionSpace:解空间，列表类型：[最小值，最大值]
    """
    def __init__(self, fitFunc, birdNum, w, c1, c2, solutionSpace):
        self.fitFunc = fitFunc
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.birds, self.best = self.initbirds(birdNum, solutionSpace)

    def initbirds(self, size, solutionSpace):
        birds = []
        for i in range(size):
            position = random.uniform(solutionSpace[0], solutionSpace[1])
            speed = 0
            fit = self.fitFunc(position)
            birds.append(bird(speed, position, fit, position, fit))
        best = birds[0]
        for bird in birds:
            if bird.fit > best.fit:
                best = bird
        return birds,best

    def updateBirds(self):
        for bird in self.birds:
            # 更新速度
            bird.speed = self.w * bird.speed + self.c1 * random.random() * (bird.lBestPosition - bird.position) + self.c2 * random.random() * (self.best.position - bird.position)
            # 更新位置
            bird.position = bird.position + bird.speed
            # 跟新适应度
            bird.fit = self.fitFunc(bird.position)
            # 查看是否需要更新经验最优
            if bird.fit > bird.lBestFit:
                bird.lBestFit = bird.fit
                bird.lBestPosition = bird.position

    def solve(self, maxIter):
        # 只考虑了最大迭代次数，如需考虑阈值，添加判断语句就好
        for i in range(maxIter):
            # 更新粒子
            self.updateBirds()
            for bird in self.birds:
                # 查看是否需要更新全局最优
                if bird.fit > self.best.fit:
                    self.best = bird

```
#### GA遗传算法

GA遗传算法:
```python

from __future__ import division
import numpy as np
import random
import math
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
import time


class GA(object):
    def __init__(self, maxiter, sizepop, lenchrom, pc, pm, dim, lb, ub, Fobj):
        """
        maxiter：最大迭代次数
        sizepop：种群数量
        lenchrom：染色体长度
        pc：交叉概率
        pm：变异概率
        dim：变量的维度
        lb：最小取值
        ub：最大取值
        Fobj：价值函数
        """
        self.maxiter = maxiter
        self.sizepop = sizepop
        self.lenchrom = lenchrom
        self.pc = pc
        self.pm = pm
        self.dim = dim
        self.lb = lb
        self.ub = ub
        self.Fobj = Fobj

    # 初始化种群：返回一个三维数组，第一维是种子，第二维是变量维度，第三维是编码基因
    def Initialization(self):
        pop = []
        for i in range(self.sizepop):
            temp1 = []
            for j in range(self.dim):
                temp2 = []
                for k in range(self.lenchrom):
                    temp2.append(random.randint(0, 1))
                temp1.append(temp2)
            pop.append(temp1)
        return pop

    # 将二进制转化为十进制
    def b2d(self, pop_binary):
        pop_decimal = []
        for i in range(len(pop_binary)):
            temp1 = []
            for j in range(self.dim):
                temp2 = 0
                for k in range(self.lenchrom):
                    temp2 += pop_binary[i][j][k] * math.pow(2, k)
                temp2 = temp2 * (self.ub[j] - self.lb[j]) / (math.pow(2, self.lenchrom) - 1) + self.lb[j]
                temp1.append(temp2)
            pop_decimal.append(temp1)
        return pop_decimal

    # 轮盘赌模型选择适应值较高的种子
    def Roulette(self, fitness, pop):
        # 适应值按照大小排序
        sorted_index = np.argsort(fitness)
        sorted_fitness, sorted_pop = [], []
        for index in sorted_index:
            sorted_fitness.append(fitness[index])
            sorted_pop.append(pop[index])

        # 生成适应值累加序列
        fitness_sum = sum(sorted_fitness)
        accumulation = [None for col in range(len(sorted_fitness))]
        accumulation[0] = sorted_fitness[0] / fitness_sum
        for i in range(1, len(sorted_fitness)):
            accumulation[i] = accumulation[i - 1] + sorted_fitness[i] / fitness_sum

        # 轮盘赌
        roulette_index = []
        for j in range(len(sorted_fitness)):
            p = random.random()
            for k in range(len(accumulation)):
                if accumulation[k] >= p:
                    roulette_index.append(k)
                    break
        temp1, temp2 = [], []
        for index in roulette_index:
            temp1.append(sorted_fitness[index])
            temp2.append(sorted_pop[index])
        newpop = [[x, y] for x, y in zip(temp1, temp2)]
        newpop.sort()
        newpop_fitness = [newpop[i][0] for i in range(len(sorted_fitness))]
        newpop_pop = [newpop[i][1] for i in range(len(sorted_fitness))]
        return newpop_fitness, newpop_pop

    # 交叉繁殖：针对每一个种子，随机选取另一个种子与之交叉。
    # 随机取种子基因上的两个位置点，然后互换两点之间的部分
    def Crossover(self, pop):
        newpop = []
        for i in range(len(pop)):
            if random.random() < self.pc:
                # 选择另一个种子
                j = i
                while j == i:
                    j = random.randint(0, len(pop) - 1)
                cpoint1 = random.randint(1, self.lenchrom - 1)
                cpoint2 = cpoint1
                while cpoint2 == cpoint1:
                    cpoint2 = random.randint(1, self.lenchrom - 1)
                cpoint1, cpoint2 = min(cpoint1, cpoint2), max(cpoint1, cpoint2)
                newpop1, newpop2 = [], []
                for k in range(self.dim):
                    temp1, temp2 = [], []
                    temp1.extend(pop[i][k][0:cpoint1])
                    temp1.extend(pop[j][k][cpoint1:cpoint2])
                    temp1.extend(pop[i][k][cpoint2:])
                    temp2.extend(pop[j][k][0:cpoint1])
                    temp2.extend(pop[i][k][cpoint1:cpoint2])
                    temp2.extend(pop[j][k][cpoint2:])
                    newpop1.append(temp1)
                    newpop2.append(temp2)
                newpop.extend([newpop1, newpop2])
        return newpop

    # 变异：针对每一个种子的每一个维度，进行概率变异，变异基因为一位
    def Mutation(self, pop):
        newpop = copy.deepcopy(pop)
        for i in range(len(pop)):
            for j in range(self.dim):
                if random.random() < self.pm:
                    mpoint = random.randint(0, self.lenchrom - 1)
                    newpop[i][j][mpoint] = 1 - newpop[i][j][mpoint]
        return newpop

    # 绘制迭代-误差图
    def Ploterro(self, Convergence_curve):
        mpl.rcParams['font.sans-serif'] = ['Courier New']
        mpl.rcParams['axes.unicode_minus'] = False
        fig = plt.figure(figsize=(10, 6))
        x = [i for i in range(len(Convergence_curve))]
        plt.plot(x, Convergence_curve, 'r-', linewidth=1.5, markersize=5)
        plt.xlabel(u'Iter', fontsize=18)
        plt.ylabel(u'Best score', fontsize=18)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.xlim(0, )
        plt.grid(True)
        plt.show()

    def Run(self):
        pop = self.Initialization()
        errolist = []
        for Current_iter in range(self.maxiter):
            print("Iter = " + str(Current_iter))
            pop1 = self.Crossover(pop)
            pop2 = self.Mutation(pop1)
            pop3 = self.b2d(pop2)
            fitness = []
            for j in range(len(pop2)):
                fitness.append(self.Fobj(pop3[j]))
            sorted_fitness, sorted_pop = self.Roulette(fitness, pop2)
            best_fitness = sorted_fitness[-1]
            best_pos = self.b2d([sorted_pop[-1]])[0]
            pop = sorted_pop[-1:-(self.sizepop + 1):-1]
            errolist.append(1 / best_fitness)
            if 1 / best_fitness < 0.0001:
                print("Best_score = " + str(round(1 / best_fitness, 4)))
                print("Best_pos = " + str([round(a, 4) for a in best_pos]))
                break
        return best_fitness, best_pos, errolist


if __name__ == "__main__":
    # 价值函数，求函数最小值点 -> [1, -1, 0, 0]
    def Fobj(factor):
        cost = (factor[0] - 1) ** 2 + (factor[1] + 1) ** 2 + factor[2] ** 2 + factor[3] ** 2
        return 1 / cost
    starttime = time.time()
    a = GA(100, 50, 10, 0.8, 0.01, 4, [-1, -1, -1, -1], [1, 1, 1, 1], Fobj)
    Best_score, Best_pos, errolist = a.Run()
    endtime = time.time()
    print("Runtime = " + str(endtime - starttime))
    a.Ploterro(errolist)
```

#### 蚁群算法

#### 果蝇算法
## 分类器
### SVM支持向量机

#### 原理

支持向量机的原理大致可以理解为特征在无穷维度的线性分类，通过核函数映射，我们不断的增加特征将其分开并进行还原。

#### 算法

```python
# -*- coding: utf-8 -*-
"""
SVC
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model,cross_validation,svm

def load_data_classfication():
    '''
    加载用于分类问题的数据集

    :return: 一个元组，用于分类问题。元组元素依次为：训练样本集、测试样本集、训练样本集对应的标记、测试样本集对应的标记
    '''
    iris=datasets.load_iris()# 使用 scikit-learn 自带的 iris 数据集
    X_train=iris.data
    y_train=iris.target
    return cross_validation.train_test_split(X_train, y_train,test_size=0.25,
		random_state=0,stratify=y_train) # 分层采样拆分成训练集和测试集，测试集大小为原始数据集大小的 1/4

def test_SVC_linear(*data):
    '''
    测试 SVC 的用法。这里使用的是最简单的线性核

    :param data:  可变参数。它是一个元组，这里要求其元素依次为：训练样本集、测试样本集、训练样本的标记、测试样本的标记
    :return: None
    '''
    X_train,X_test,y_train,y_test=data
    cls=svm.SVC(kernel='linear')
    cls.fit(X_train,y_train)
    print('Coefficients:%s, intercept %s'%(cls.coef_,cls.intercept_))
    print('Score: %.2f' % cls.score(X_test, y_test))
def test_SVC_poly(*data):
    '''
    测试多项式核的 SVC 的预测性能随 degree、gamma、coef0 的影响.

    :param data:  可变参数。它是一个元组，这里要求其元素依次为：训练样本集、测试样本集、训练样本的标记、测试样本的标记
    :return: None
    '''
    X_train,X_test,y_train,y_test=data
    fig=plt.figure()
    ### 测试 degree ####
    degrees=range(1,20)
    train_scores=[]
    test_scores=[]
    for degree in degrees:
        cls=svm.SVC(kernel='poly',degree=degree)
        cls.fit(X_train,y_train)
        train_scores.append(cls.score(X_train,y_train))
        test_scores.append(cls.score(X_test, y_test))
    ax=fig.add_subplot(1,3,1) # 一行三列
    ax.plot(degrees,train_scores,label="Training score ",marker='+' )
    ax.plot(degrees,test_scores,label= " Testing  score ",marker='o' )
    ax.set_title( "SVC_poly_degree ")
    ax.set_xlabel("p")
    ax.set_ylabel("score")
    ax.set_ylim(0,1.05)
    ax.legend(loc="best",framealpha=0.5)

    ### 测试 gamma ，此时 degree 固定为 3####
    gammas=range(1,20)
    train_scores=[]
    test_scores=[]
    for gamma in gammas:
        cls=svm.SVC(kernel='poly',gamma=gamma,degree=3)
        cls.fit(X_train,y_train)
        train_scores.append(cls.score(X_train,y_train))
        test_scores.append(cls.score(X_test, y_test))
    ax=fig.add_subplot(1,3,2)
    ax.plot(gammas,train_scores,label="Training score ",marker='+' )
    ax.plot(gammas,test_scores,label= " Testing  score ",marker='o' )
    ax.set_title( "SVC_poly_gamma ")
    ax.set_xlabel(r"$\gamma$")
    ax.set_ylabel("score")
    ax.set_ylim(0,1.05)
    ax.legend(loc="best",framealpha=0.5)
    ### 测试 r ，此时 gamma固定为10 ， degree 固定为 3######
    rs=range(0,20)
    train_scores=[]
    test_scores=[]
    for r in rs:
        cls=svm.SVC(kernel='poly',gamma=10,degree=3,coef0=r)
        cls.fit(X_train,y_train)
        train_scores.append(cls.score(X_train,y_train))
        test_scores.append(cls.score(X_test, y_test))
    ax=fig.add_subplot(1,3,3)
    ax.plot(rs,train_scores,label="Training score ",marker='+' )
    ax.plot(rs,test_scores,label= " Testing  score ",marker='o' )
    ax.set_title( "SVC_poly_r ")
    ax.set_xlabel(r"r")
    ax.set_ylabel("score")
    ax.set_ylim(0,1.05)
    ax.legend(loc="best",framealpha=0.5)
    plt.show()
def test_SVC_rbf(*data):
    '''
    测试 高斯核的 SVC 的预测性能随 gamma 参数的影响

    :param data:  可变参数。它是一个元组，这里要求其元素依次为：训练样本集、测试样本集、训练样本的标记、测试样本的标记
    :return: None
    '''
    X_train,X_test,y_train,y_test=data
    gammas=range(1,20)
    train_scores=[]
    test_scores=[]
    for gamma in gammas:
        cls=svm.SVC(kernel='rbf',gamma=gamma)
        cls.fit(X_train,y_train)
        train_scores.append(cls.score(X_train,y_train))
        test_scores.append(cls.score(X_test, y_test))
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(gammas,train_scores,label="Training score ",marker='+' )
    ax.plot(gammas,test_scores,label= " Testing  score ",marker='o' )
    ax.set_title( "SVC_rbf")
    ax.set_xlabel(r"$\gamma$")
    ax.set_ylabel("score")
    ax.set_ylim(0,1.05)
    ax.legend(loc="best",framealpha=0.5)
    plt.show()
def test_SVC_sigmoid(*data):
    '''
    测试 sigmoid 核的 SVC 的预测性能随 gamma、coef0 的影响.

    :param data:  可变参数。它是一个元组，这里要求其元素依次为：训练样本集、测试样本集、训练样本的标记、测试样本的标记
    :return: None
    '''
    X_train,X_test,y_train,y_test=data
    fig=plt.figure()

    ### 测试 gamma ，固定 coef0 为 0 ####
    gammas=np.logspace(-2,1)
    train_scores=[]
    test_scores=[]

    for gamma in gammas:
        cls=svm.SVC(kernel='sigmoid',gamma=gamma,coef0=0)
        cls.fit(X_train,y_train)
        train_scores.append(cls.score(X_train,y_train))
        test_scores.append(cls.score(X_test, y_test))
    ax=fig.add_subplot(1,2,1)
    ax.plot(gammas,train_scores,label="Training score ",marker='+' )
    ax.plot(gammas,test_scores,label= " Testing  score ",marker='o' )
    ax.set_title( "SVC_sigmoid_gamma ")
    ax.set_xscale("log")
    ax.set_xlabel(r"$\gamma$")
    ax.set_ylabel("score")
    ax.set_ylim(0,1.05)
    ax.legend(loc="best",framealpha=0.5)
    ### 测试 r，固定 gamma 为 0.01 ######
    rs=np.linspace(0,5)
    train_scores=[]
    test_scores=[]

    for r in rs:
        cls=svm.SVC(kernel='sigmoid',coef0=r,gamma=0.01)
        cls.fit(X_train,y_train)
        train_scores.append(cls.score(X_train,y_train))
        test_scores.append(cls.score(X_test, y_test))
    ax=fig.add_subplot(1,2,2)
    ax.plot(rs,train_scores,label="Training score ",marker='+' )
    ax.plot(rs,test_scores,label= " Testing  score ",marker='o' )
    ax.set_title( "SVC_sigmoid_r ")
    ax.set_xlabel(r"r")
    ax.set_ylabel("score")
    ax.set_ylim(0,1.05)
    ax.legend(loc="best",framealpha=0.5)
    plt.show()
if __name__=="__main__":
    X_train,X_test,y_train,y_test=load_data_classfication() # 生成用于分类问题的数据集
    test_SVC_linear(X_train,X_test,y_train,y_test) # 调用 test_SVC_linear
    # test_SVC_poly(X_train,X_test,y_train,y_test) # 调用 test_SVC_poly
    # test_SVC_rbf(X_train,X_test,y_train,y_test) # 调用 test_SVC_rbf
    # test_SVC_sigmoid(X_train,X_test,y_train,y_test) # test_SVC_sigmoid test_SVC_linear
```





#### 应用

##### 分类

通过支持向量机，我们可以对于日内策略进行一个简单的改进DEMO：

在日内策略中，很重要的一个问题就是如何识别真实突破：

很多时候，如DualHurst策略，R-breaker策略等等，对于突破的识别仅限于价格的简单关系，并没有理论的支撑，经常会出现一些由于价格波动导致的假突破而发生错误的交易信号。

支持向量机可以对于小样本的多维度向量进行快速的分析和分类，由于基于非线性的高维空间分类的方法，其分类精度超过了传统的分类方法，并可以对于非线性数据有着较好的适应度。

![简单的支持向量机原理示意](http://p1.bpimg.com/1949/3061ab9644fb00d7.gif)

[简单的支持向量机原理示意]

我们可以通过对于前N日的开高收低，量，大单持仓等进行维度建模，先进行数据分解，再进行标准化，最后进行合成信号进行分类。

首先对于数据进行小波或者EMD分解，找到特定的周期特征部分，然后对于其特征部分进行前向标准化，放入维度矩阵，进行样本内训练，之后进行分类。



关于迁移学习，对于不同的商品期货品种进行训练，从而达到迁移学习的效果

##### 预测

### 神经网络以及深度学习

### 分类树算法C5.0以及随机森林
### 聚类算法
## 信号分解算法

### 小波分析
### EMD算法
## 迁移学习和增量算法
## 增强学习Reinforcements