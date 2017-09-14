
订单状态。
``` python
    OrderStatus_New = 1,                        #已报
    OrderStatus_PartiallyFilled = 2,            #部成
    OrderStatus_Filled = 3,                     #已成
    OrderStatus_DoneForDay = 4,                 #
    OrderStatus_Canceled = 5,                   #已撤
    OrderStatus_PendingCancel = 6,              #待撤
    OrderStatus_Stopped = 7,                    #停止
    OrderStatus_Rejected = 8,                   #已拒绝
    OrderStatus_Suspended = 9,                  #挂起
    OrderStatus_PendingNew = 10,                #待报
    OrderStatus_Calculated = 11,                #计算
    OrderStatus_Expired = 12,                   #已过期
    OrderStatus_AcceptedForBidding = 13,        #接受竞价
    OrderStatus_PendingReplace = 14             #待修改
```
OrderRejectReason

订单拒绝原因。
``` python
    OrderRejectReason_UnknownReason = 1,                #未知原因
    OrderRejectReason_RiskRuleCheckFailed = 2,          #不符合风控规则
    OrderRejectReason_NoEnoughCash = 3,                 #资金不足
    OrderRejectReason_NoEnoughPosition = 4,             #仓位不足
    OrderRejectReason_IllegalStrategyID = 5,            #非法策略ID
    OrderRejectReason_IllegalSymbol = 6,                #非法交易标的
    OrderRejectReason_IllegalVolume = 7,                #非法委托量
    OrderRejectReason_IllegalPrice = 8,                 #非法委托价
    OrderRejectReason_NoMatchedTradingChannel = 9,      #没有匹配的交易通道
    OrderRejectReason_AccountForbidTrading = 10,        #交易账号被禁止交易
    OrderRejectReason_TradingChannelNotConnected = 11,  #交易通道未连接
    OrderRejectReason_StrategyForbidTrading = 12,       #策略不允许交易
    OrderRejectReason_NotInTradingSession = 13          #非交易时段
    CancelOrderRejectReason_OrderFinalized = 101        #订单已是最终状态
    CancelOrderRejectReason_UnknownOrder = 102          #未知订单
    CancelOrderRejectReason_BrokerOption = 103          #柜台拒绝
    CancelOrderRejectReason_AlreadyInPendingCancel = 104        #重复撤单
```
OrderSide

订单方向。
``` python
    OrderSide_Bid = 1  ## 多方向
    OrderSide_Ask = 2  ## 空方向
```
OrderType

订单类型。

    OrderType_LMT = 0,       ## 限价委托(limit)                        
    OrderType_BOC = 1,       ## 对方最优价格(best of counterparty)     
    OrderType_BOP = 2,       ## 己方最优价格(best of party)            
    OrderType_B5TC = 3,      ## 最优五档剩余撤销(best 5 then cancel)   
    OrderType_B5TL = 4,      ## 最优五档剩余转限价(best 5 then limit)  
    OrderType_IOC = 5,       ## 即时成交剩余撤销(immediately or cancel)
    OrderType_FOK = 6,       ## 即时全额成交或撤销(fill or kill)       
    OrderType_AON = 7,       ## 全额成交或不成交(all or none)          
    OrderType_MTL = 8,       ## 市价剩余转限价(market then limit)      
    OrderType_EXE = 9        ## 期权行权(option execute)  
ExecType

订单执行回报类型。

    ExecType_New = 1                ## 交易所已接受订单
    ExecType_DoneForDay = 4
    ExecType_Canceled = 5           ## 已撤
    ExecType_PendingCancel = 6      ## 待撤
    ExecType_Stopped = 7            ## 已停
    ExecType_Rejected = 8           ## 已拒绝
    ExecType_Suspended = 9          ## 暂停
    ExecType_PendingNew = 10        ## 待接受
    ExecType_Calculated = 11        ## 已折算
    ExecType_Expired = 12           ## 过期
    ExecType_Restated = 13          ## 重置
    ExecType_PendingReplace = 14    ## 待修改
    ExecType_Trade = 15             ## 交易
    ExecType_TradeCorrect = 16      ## 交易更正
    ExecType_TradeCancel = 17       ## 交易取消
    ExecType_OrderStatus = 18       ## 更新订单状态
    ExecType_CancelRejected = 19    ## 撤单被拒绝
PositionEffect

开平仓类型。

    PositionEffect_Open = 1             ## 开仓
    PositionEffect_Close = 2            ## 平仓
    PositionEffect_CloseToday = 3       ## 平今仓
    PositionEffect_CloseYesterday = 4   ## 平昨仓
交易数据类型

交易数据类型主要包括委托，执行回报，资金，持仓，绩效等数据类型。

Order

委托订单。

class Order(object):

    def __init__(self):
        self.strategy_id = ''                 ## 策略ID
        self.account_id = ''                  ## 交易账号

        self.cl_ord_id = ''                   ## 客户端订单ID
        self.order_id = ''                    ## 柜台订单ID
        self.ex_ord_id = ''                   ## 交易所订单ID

        self.exchange = ''                    ## 交易所代码
        self.sec_id = ''                      ## 证券ID

        self.position_effect = 0              ## 开平标志
        self.side = 0                         ## 买卖方向
        self.order_type = 0                   ## 订单类型
        self.order_src = 0                    ## 订单来源
        self.status = 0                       ## 订单状
        self.ord_rej_reason = 0               ## 订单拒绝原因
        self.ord_rej_reason_detail = ''       ## 订单拒绝原因描述

        self.price = 0.0                      ## 委托价
        self.stop_price = 0.0;                ## 止损价
        self.volume = 0.0                     ## 委托量
        self.filled_volume = 0.0              ## 已成交量
        self.filled_vwap = 0.0                ## 已成交均价
        self.filled_amount = 0.0              ## 已成交额

        self.sending_time = 0.0               ## 委托下单时间
        self.transact_time = 0.0              ## 最新一次成交时间
ExecRpt

委托执行回报。

class ExecRpt(object):

    def __init__(self):
        self.strategy_id = ''                 ## 策略ID

        self.cl_ord_id = ''                   ## 客户端订单ID
        self.order_id = ''                    ## 交易所订单ID
        self.exec_id = ''                     ## 订单执行回报ID

        self.exchange = ''                    ## 交易所代码
        self.sec_id = ''                      ## 证券ID

        self.position_effect = 0              ## 开平标志
        self.side = 0                         ## 买卖方向
        self.ord_rej_reason = 0               ## 订单拒绝原因
        self.ord_rej_reason_detail = ''       ## 订单拒绝原因描述
        self.exec_type = 0                    ## 订单执行回报类型

        self.price = 0.0                      ## 成交价
        self.volume = 0.0                     ## 成交量
        self.amount = 0.0                     ## 成交额

        self.transact_time = 0.0              ## 交易时间
Cash

资金。

class Cash(object):

    def __init__(self):
        self.strategy_id = ''           ## 策略ID
        self.account_id = ''            ## 账户id
        self.currency = 0               ## 币种

        self.nav = 0.0                  ## 资金余额
        self.fpnl = 0.0                 ## 浮动收益
        self.pnl = 0.0                  ## 净收益
        self.profit_ratio = 0.0         ## 收益率
        self.frozen = 0.0               ## 持仓冻结金额
        self.order_frozen = 0.0         ## 挂单冻结金额
        self.available = 0.0            ## 可用资金

        self.cum_inout = 0.0            ## 累计出入金
        self.cum_trade = 0.0            ## 累计交易额
        self.cum_pnl = 0.0              ## 累计收益
        self.cum_commission = 0.0       ## 累计手续费

        self.last_trade = 0.0           ## 最新一笔交易额
        self.last_pnl = 0.0             ## 最新一笔交易收益
        self.last_commission = 0.0      ## 最新一笔交易手续费
        self.last_inout = 0.0           ## 最新一次出入金
        self.change_reason = 0          ## 变动原因

        self.transact_time = 0.0        ## 交易时间

Position

持仓。

class Position(object):

    def __init__(self):
        self.strategy_id = ''           ## 策略ID
        self.account_id = ''            ## 账户id
        self.exchange = ''              ## 交易所代码
        self.sec_id = ''                ## 证券ID
        self.side = 0                   ## 买卖方向
        self.volume = 0.0               ## 持仓量
        self.volume_today = 0.0         ## 今仓量
        self.amount = 0.0               ## 持仓额
        self.vwap = 0.0                 ## 持仓均价

        self.price = 0.0                ## 当前行情价格
        self.fpnl = 0.0                 ## 持仓浮动盈亏
        self.cost = 0.0                 ## 持仓成本
        self.order_frozen = 0.0         ## 挂单冻结仓位
        self.available = 0.0            ## 可平仓位
        self.available_today = 0.0      ## 可平今仓位(volume_today-order_frozen_today)
        self.available_yesterday = 0.0  ## 可平昨仓位(available - available_today)
        self.order_frozen_today = 0.0   ## 挂单冻结今仓
        self.last_price = 0.0           ## 上一笔成交价
        self.last_volume = 0.0          ## 上一笔成交量
        self.init_time = 0.0            ## 初始建仓时间
        self.transact_time = 0.0        ## 上一仓位变更时间

Indicator

绩效。

class Indicator(object):

    def __init__(self):
        self.strategy_id = ''                       ## 策略ID
        self.account_id = ''                        ## 账号ID

        self.nav = 0.0                              ## 净值(cum_inout + cum_pnl + fpnl - cum_commission)
        self.pnl = 0.0                              ## 净收益(nav-cum_inout)
        self.profit_ratio = 0.0                     ## 收益率(pnl/cum_inout)
        self.profit_ratio_bench = 0.0               ## 基准收益率
        self.sharp_ratio = 0.0                      ## 夏普比率
        self.risk_ratio = 0.0                       ## 风险比率
        self.trade_count = 0                        ## 交易次数
        self.win_count = 0                          ## 盈利次数
        self.lose_count = 0                         ## 亏损次数
        self.win_ratio = 0.0                        ## 胜率
        self.max_profit = 0.0                       ## 最大收益
        self.min_profit = 0.0                       ## 最小收益
        self.max_single_trade_profit = 0.0          ## 最大单次交易收益
        self.min_single_trade_profit = 0.0          ## 最小单次交易收益
        self.daily_max_single_trade_profit = 0.0    ## 今日最大单次交易收益
        self.daily_min_single_trade_profit = 0.0    ## 今日最小单次交易收益
        self.max_position_value = 0.0               ## 最大持仓市值或权益
        self.min_position_value = 0.0               ## 最小持仓市值或权益
        self.max_drawdown = 0.0                     ## 最大回撤
        self.daily_pnl = 0.0                        ## 今日收益
        self.daily_return = 0.0                     ## 今日收益率
        self.annual_return = 0.0                    ## 年化收益率

        self.cum_inout = 0.0                        ## 累计出入金
        self.cum_trade = 0.0                        ## 累计交易额
        self.cum_pnl = 0.0                          ## 累计平仓收益(没扣除手续费)
        self.cum_commission = 0.0                   ## 累计手续费

        self.transact_time = 0.0                    ## 指标计算时间

BrokerAccount

柜台账户

class BrokerAccount(object):

    def __init__(self):
        self.account_id = ''                         # 柜台账号ID
        self.username = ''                           # 柜台账号
        self.permissible = 0                         # 允许交易
        self.status = 0                              # 账号当前状态
StrategyParameter

策略参数

class StrategyParameter(object):

    def __init__(self):
        self.name = ''                              # 参数名
        self.value = 0.0                            # 参数值
        self.min = 0.0                              # 可设置的最小值
        self.max = 0.0                              # 可设置的最大值
        self.readonly = false                       # 是否只读
        self.group = ''                             # 组名
        self.intro = ''                             # 参数说明
StrategySymbol

策略交易标的

class StrategySymbol(object):

    def __init__(self):
        self.symbol = ''                               # 交易代码
        self.exchange = ''                            # 交易所代码
        self.sec_id = ''                              # 证券ID
行情数据类型

行情数据类型有Tick，Bar，DailyBar。

Tick

逐笔行情数据。

class Tick(object):

    def __init__(self):
        self.exchange = ''          ## 交易所代码
        self.sec_id = ''            ## 证券ID
        self.utc_time = 0.0         ## 行情时间戳
        self.strtime = ''           ## 可视化时间
        self.last_price = 0.0       ## 最新价
        self.open = 0.0             ## 开盘价
        self.high = 0.0             ## 最高价
        self.low = 0.0              ## 最低价

        self.cum_volume = 0.0       ## 成交总量/最新成交量,累计值
        self.cum_amount = 0.0       ## 成交总金额/最新成交额,累计值
        self.cum_position = 0.0L    ## 合约持仓量(期),累计值
        self.last_volume = 0        ## 瞬时成交量(中金所提供)
        self.last_amount = 0.0      ## 瞬时成交额

        self.upper_limit = 0.0      ## 涨停价
        self.lower_limit = 0.0      ## 跌停价
        self.settle_price = 0.0     ## 今日结算价
        self.trade_type = 0         ## 1:'双开', 2: '双平', 3: '多开', 4:'空开', 5: '空平', 6:'多平', 7:'多换', 8:'空换'
        self.pre_close = 0.0        ## 昨收价

        self.bids = []  ## [(price, volume), (price, volume), ...] ## 1-5档买价,量
        self.asks = []  ## [(price, volume), (price, volume), ...] ## 1-5档卖价,量
Bar

各种周期的Bar数据。

class Bar(object):

    def __init__(self):
        self.exchange = ''       ## 交易所代码
        self.sec_id = ''         ## 证券ID

        self.bar_type = 0        ## bar类型，以秒为单位，比如1分钟bar, bar_type=60
        self.strtime = ''        ## Bar开始时间
        self.utc_time = 0.0      ## Bar开始时间
        self.strendtime = ''     ## Bar结束时间
        self.utc_endtime = 0.0   ## Bar结束时间
        self.open = 0.0          ## 开盘价
        self.high = 0.0          ## 最高价
        self.low = 0.0           ## 最低价
        self.close = 0.0         ## 收盘价
        self.volume = 0.0        ## 成交量
        self.amount = 0.0        ## 成交额
        self.pre_close           ## 前收盘价
        self.position;           ## 持仓量
        self.adj_factor          ## 复权因子
        self.flag                ## 除权出息标记
DailyBar

日频数据，在Bar数据的基础上，还包含结算价，涨跌停价等静态数据。


class Dailybar(object):

    def __init__(self):
        self.exchange = ''          ## 交易所代码
        self.sec_id = ''            ## 证券ID

        self.bar_type = 0           ## bar类型
        self.strtime = ''           ## 可视化时间
        self.utc_time = 0.0         ## 行情时间戳

        self.open = 0.0             ## 开盘价
        self.high = 0.0             ## 最高价
        self.low = 0.0              ## 最低价
        self.close = 0.0            ## 收盘价
        self.volume = 0.0           ## 成交量
        self.amount = 0.0           ## 成交额

        self.position = 0.0L        ## 仓位
        self.settle_price = 0.0     ## 结算价
        self.upper_limit = 0.0      ## 涨停价
        self.lower_limit = 0.0      ## 跌停价
        self.pre_close              ## 前收盘价
        self.adj_factor             ## 复权因子
        self.flag                   ## 除权出息，停牌等标记
Instrument

交易代码数据类型


class Instrument(object):

    def __init__(self):
        self.symbol = ''                ## 交易代码
        self.sec_type = 0               ## 代码类型
        self.sec_name = ''              ## 代码名称
        self.multiplier = 0.0           ## 合约乘数
        self.margin_ratio = 0.0         ## 保证金比率
        self.price_tick = 0.0           ## 价格最小变动单位
        self.upper_limit = 0.0          ## 当天涨停板
        self.lower_limit = 0.0          ## 当天跌停板
        self.is_active = 0              ## 当天是否交易
        self.update_time = ''           ## 更新时间
Constituent

成份股数据类型


class Constituent(object):

    def __init__(self):
        self.symbol = ''                ## 交易代码
        self.weight = 0.0               ## 代码权重
FinancialIndex

财务指标


class FinancialIndex(object):

    def __init__(self):
        self.symbol = ''                         #股票代码
        self.pub_date = ''                       #公告日期    
        self.eps = 0.0                           #每股收益    
        self.bvps = 0.0                          #每股净资产  
        self.cfps = 0.0                          #每股现金流  
        self.afps = 0.0                          #每股公积金  
        self.total_asset = 0.0                   #总资产      
        self.current_asset = 0.0                 #流动资产    
        self.fixed_asset = 0.0                   #固定资产    
        self.liability = 0.0                     #负债合计    
        self.current_liability = 0.0             #流动负债
        self.longterm_liability = 0.0            #长期负债
        self.equity = 0.0                        #所有者权益
        self.income = 0.0                        #主营业务收入
        self.operating_profit = 0.0              #主营业务利润
        self.net_profit = 0.0                    #净利润
ShareIndex

股本指标

class ShareIndex(Object):

    def __init__(self):
        self.symbol = ''                          #股票代码
        self.pub_date = ''                        #公告日期
        self.total_share = 0.0                    #总股本
        self.flow_a_share = 0.0                   #流通A股
        self.nonflow_a_share = 0.0                #限售流通A股
MarketIndex

市场指标

class MarketIndex(Object):

    def __init__(self):
        self.symbol = ''               #股票代码
        self.pub_date = ''             #公告日期
        self.pe_ratio = 0.0            #市盈率
        self.pb_ratio = 0.0            #市净率
        self.ps_ratio = 0.0            #市销率
        self.market_value = 0.0        #市值
        self.market_value_flow = 0.0   #流通市值
TradeDate

交易日类型


class TradeDate(object):

    def __init__(self):
        self.utc_time = 0.0                 ## UTC时间戳[带毫秒]
        self.strtime = ''                   ## 交易日
StockAdjustFactor

复权因子


class StockAdjustFactor(object):

    def __init__(self):
         self.symbol         ##股票代码
         self.trade_date     ##交易日
         self.adj_factor     ##复权因子
StockDivident

分红送股事件明细


class StockDivident(object):

    def __init__(self):
        self.symbol                     ##股票代码
        self.div_date                   ##除权除息日
        self.cash_div                   ##每股派现
        self.share_div_ratio            ##每股送股比例
        self.share_trans_ratio          ##每股转增股比例
        self.allotment_ratio            ##每股配股比例
        self.allotment_price            ##配股价
VirtualContract

虚拟合约明细


class VirtualContract(object):

    def __init__(self):
         self.vsymbol        ##主力合约或连接合约代码
         self.symbol         ##真实symbol
         self.trade_date     ##交易日
策略初始化方法

init

初始化策略，设置服务地址，账号密码，策略ID，以及需要订阅的symbol列表。策略自动连接服务，并登陆，订阅对应的行情，准备好运行。

函数原型：

__init__(self,
         username, 
         password, 
         strategy_id, 
         subscribe_symbols='', 
         mode=2, 
         td_addr='',
         config_file=None,
         config_file_encoding='utf-8')
参数：

参数名	类型	说明
username	string	掘金终端账号
password	string	掘金终端密码
strategy_id	string	策略ID
subscribe_symbols	string	行情订阅的代码列表
mode	int	枚举类型，行情模式
td_addr	string	交易服务器uri, 如设置为localhost:8001，则终端用户指向本地客户端 , 如果设置为空, 则使用掘金云端服务
返回值：

返回值编码

示例：

初始化时订阅上交所浦发银行的tick和1min bar实时行情

ret = Strategy("your user name", 
               "your password", 
               "strategy id", 
               "SHSE.600000.tick,SHSE.600000.bar.60",
               2,
               "localhost:8001")
注意项：

symbol_list 订阅代码表,参数格式如下:

订阅串有三节或四节组成,用'.'分隔，格式：

对应交易所exchange.代码code.数据类型data_type.周期类型bar_type

只有订阅bar数据时, 才用到第四节, 周期类型才有作用 交易所exchange统一四个字节:

CFFEX-中金所 SHFE-上期所 DCE-大商所 CZCE-郑商所 SHSE-上交所 SZSE-深交所

支持6种格式的订阅,使用如下:

SHSE.* : 上交所,所有数据
SHSE.600000.* : 上交所,600000,所有数据
SHSE.600000.tick : 上交所,600000, tick数据
SHSE.600000.bar.60: 上交所, 600000, 1分钟(60秒)Bar数据
SHSE.600000.*,SHSE.600004.* : 上交所,600000和600004所有数据(订阅多个代码)
init_with_config

使用配置文件初始化策略，配置文件已设置服务地址，账号密码，策略ID，行情模式以及需要订阅的symbol列表

函数原型：

__init__(self,
         username, 
         password, 
         strategy_id, 
         subscribe_symbols='', 
         mode=2, 
         td_addr='',
         config_file=None,
         config_file_encoding='utf-8')
参数：

参数名	类型	说明
config_file	string	策略配置文件路径
config_file_encoding	string	策略配置文件编码
  # 共用的配置或通讯层面的错诿 1000~1499

SUCCESS                                  = 0     # "成功"

ERR_CONFIG_FILE_NOT_EXIST                = 1001  # "策略配置文件不存圿"
ERR_CONFIG_PARSE                         = 1002  # "策略配置文件格式错误"
ERR_AUTH_CONNECT                         = 1003  # "无法连接掘金认证服务"
ERR_AUTH_LOGIN                           = 1004  # "无法登录掘金认证服务"
ERR_REQUEST_TIMEOUT                      = 1005  # "请求超时"
ERR_INVALID_PARAMETER                    = 1006  # "非法参数"
ERR_STRATEGY_INIT                        = 1007  # "策略未初始化"
ERR_INTERNAL_INIT_ERROR                  = 1008  # "SDK内部初始化错诿"
ERR_API_SERVER_CONNECT                   = 1009  # "无法连接掘金API服务"

# 业务层面错误共有部分＿ 1500~1999

ERR_INVALID_SYMBOL                       = 1501  # "非法证券代码"
ERR_INVALID_DATE                         = 1502  # "非法日期格式"
ERR_INVALID_STRATEGY_ID                  = 1503  # "非法策略ID"

# 交易部分 2000 ~ 2999

ERR_TD_CONNECT                           = 2000  # "交易服务连接失败"
ERR_TD_LOGIN                             = 2001  # "交易服务登录失败"
ERR_TD_TIMEOUT                           = 2002  # "交易命令请求超时"
ERR_TD_NO_RESULT                         = 2003  # "该条件没查到数据"
ERR_TD_INVALID_SESSION                   = 2004  # "交易请求没有登陆"
ERR_TD_INVALID_PARAMETER                 = 2005  # "交易请求参数非法"
ERR_TD_STRATEGY_LOCKED                   = 2006  # "策略被禁止交昿"
ERR_TD_SERVER_ERROR                      = 2007  # "交易服务内部错误"
ERR_TD_CORRUPT_DATA                      = 2008  # "返回数据包错诿"
ERR_TD_CONNECT_CLOSE                     = 2009  # "交易服务连接断开"


# 数据服务部分 3000~3999

ERR_MD_CONNECT                           = 3000  # "数据服务连接失败"
ERR_MD_LOGIN                             = 3001  # "数据服务登录失败"
ERR_MD_TIMEOUT                           = 3002  # "数据服务请求超时"
ERR_MD_NO_RESULT                         = 3003  # "该条件没查到数据"
ERR_MD_BUFFER_ALLOC                      = 3005  # "分配缓冲区错诿"
ERR_MD_INVALID_PARAMETER                 = 3006  # "数据请求参数非法"
ERR_MD_SERVER_ERROR                      = 3007  # "数据服务内部错误"
ERR_MD_CORRUPT_DATA                      = 3008  # "返回数据包错诿"
ERR_MD_CONNECT_CLOSE                     = 3009  # "数据服务连接断开"

#回测部分 4000~4999

ERR_BT_INVALID_TIMESPAN                  = 4000  # "回测时间区间错误"
ERR_BT_INVALID_INITIAL_CASH              = 4001  # "回测请求参数非法"
ERR_BT_INVALID_TRANSACTION_RATIO         = 4002  # "回测请求参数非法"
ERR_BT_INVALID_COMMISSION_RATIO          = 4003  # "回测请求参数非法"
ERR_BT_INVALID_SLIPPAGE_RATIO            = 4004  # "回测请求参数非法"
ERR_BT_READ_CACHE_ERROR                  = 4005  # "回测读取缓存数据错误"
ERR_BT_WRITE_CACHE_ERROR                 = 4006  # "回测写入缓存数据错误"
ERR_BT_CONNECT                           = 4007  # "终端未启动或无法连接到回测服务"

#网络错误 10000~19999
ERR_NET_ERROR                            = 10000 # "网络错误"
"""