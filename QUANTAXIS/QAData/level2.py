

"""

字段 含义 数据类型 说明
SecurityID 证券代码 STRING
DateTime 日期时间 NUMBER 20151123091630
PreClosePx 昨收价 NUMBER(3)
OpenPx 开始价 NUMBER(3)
HighPx 最高价 NUMBER(3)
LowPx 最低价 NUMBER(3)
LastPx 最新价 NUMBER(3)
TotalVolumeTrade 成交总量 NUMBER 股票：股 基金：份 债券：手指数：手
TotalValueTrade 成交总金额 NUMBER(2) 元
InstrumentStatus 交易状态 STRING
BidPrice[10] 申买十价 NUMBER(3)
BidOrderQty[10] 申买十量 NUMBER
BidNumOrders[10] 申买十实际总委托笔数 NUMBER
BidOrders[50] 申买一前 50 笔订单 NUMBER
OfferPrice[10] 申卖十价 NUMBER(3)
OfferOrderQty[10] 申卖十量 NUMBER
OfferNumOrders[10] 申卖十实际总委托笔数 NUMBER
OfferOrders[50] 申卖一前 50 笔订单 NUMBER
NumTrades 成交笔数 NUMBER
IOPV ETF 净值估值 NUMBER (3)
TotalBidQty 委托买入总量 NUMBER 股票：股 基金：份 债券：手
TotalOfferQty 委托卖出总量 NUMBER 股票：股 基金：份 债券：手
WeightedAvgBidPx 加权平均委买价格 NUMBER (3)
WeightedAvgOfferPx 加权平均委卖价格 NUMBER (3)
TotalBidNumber 买入总笔数 NUMBER
TotalOfferNumber 卖出总笔数 NUMBER
BidTradeMaxDuration 买入成交最大等待时间 NUMBER
OfferTradeMaxDuration 卖出成交最大等待时间 NUMBER
NumBidOrders 买方委托价位数 NUMBER
NumOfferOrders 卖方委托价位数 NUMBER
WithdrawBuyNumber 买入撤单笔数 NUMBER
WithdrawBuyAmount 买入撤单数量 NUMBER
WithdrawBuyMoney 买入撤单金额 NUMBER (2)
WithdrawSellNumber 卖出撤单笔数 NUMBER
WithdrawSellAmount 卖出撤单数量 NUMBER
WithdrawSellMoney 卖出撤单金额 NUMBER (2)
ETFBuyNumber ETF 申购笔数 NUMBER
ETFBuyAmount ETF 申购数量 NUMBER
ETFBuyMoney ETF 申购金额 NUMBER (2)
ETFSellNumber ETF 赎回笔数 NUMBER
ETFSellAmount ETF 赎回数量 NUMBER
ETFSellMoney ETF 赎回金额 NUMBER (2)
"""

"""

SecurityID 证券代码 STRING
TradeTime 成交时间 NUMBER 2015112309163002
精确到百分之一秒
TradePrice 成交价格 NUMBER (3)
TradeQty 成交量 NUMBER
TradeAmount 成交金额 NUMBER (3)
BuyNo 买方订单号 NUMBER
SellNo 卖方订单号 NUMBER
TradeIndex 成交序号 NUMBER 自 2021 年 4 月 26 日启用
ChannelNo 频道代码 NUMBER 自 2021 年 4 月 26 日启用
TradeBSFlag 内外盘标志 STRING 内外盘标志：
B – 外盘，主动买
S – 内盘，主动卖
N – 未知
自 2021 年 4 月 26 日启用
BizIndex 业务序列号 NUMBER 业务序列号
与竞价逐笔委托消息合并后
的连续编号，从 1 开始，按
Channel 连续
自 2021 年 4 月 26 日启用
"""
shold_tick_columns = ['TradeTime', 'TradeChannel', 'SendingTime', 'SellNo', 'TradeAmount',
                      'TradeBSFlag', 'TradeIndex', 'TradePrice', 'TradeQty', 'BuyNo']
shold_snapshot_columns = ['NumTrades', 'OfferTradeMaxDuration', 'ImageStatus', 'TotalBidNumber',
                          'TotalWarrantExecQty', 'WithdrawSellMoney', 'IOPV', 'BidOrders',
                          'ETFSellAmount', 'TotalOfferQty', 'WithdrawBuyNumber',
                          'WeightedAvgOfferPx', 'ETFBuyNumber', 'WarLowerPx', 'MsgSeqNum',
                          'WithdrawSellAmount', 'ETFSellMoney', 'Volume', 'BidOrderQty', 'OpenPx',
                          'HighPx', 'PreClosePx', 'LowPx', 'WeightedAvgBidPx', 'ETFSellNumber',
                          'OfferNumOrders', 'WithdrawSellNumber', 'ETFBuyAmount',
                          'TotalOfferNumber', 'OfferPrice', 'NumOfferOrders', 'BidPrice',
                          'OfferOrderQty', 'TotalBidQty', 'SendingTime', 'ETFBuyMoney',
                          'InstrumentStatus', 'WithdrawBuyAmount', 'ClosePx',
                          'BidTradeMaxDuration', 'NumBidOrders', 'LastPx', 'Amount', 'AveragePx',
                          'WarUpperPx', 'YieldToMaturity', 'BidNumOrders', 'WithdrawBuyMoney',
                          'TradingPhaseCode', 'QuotTime', 'OfferOrders']
sz_snapshot_columns = ['NumTrades', 'OfferNumOrders', 'LowerLimitPx', 'ImageStatus',
                       'OfferPrice', 'BidPrice', 'BidOrders', 'OfferOrderQty', 'PeRatio2',
                       'TotalBidQty', 'SendingTime', 'PeRatio1', 'TotalOfferQty', 'ClosePx',
                       'WeightedAvgPxChg', 'Change2', 'Change1', 'LastPx',
                       'WeightedAvgOfferPx', 'Amount', 'UpperLimitPx', 'AveragePx',
                       'TotalLongPosition', 'MsgSeqNum', 'Volume', 'BidNumOrders',
                       'BidOrderQty', 'TradingPhaseCode', 'QuotTime', 'OpenPx', 'OfferOrders',
                       'PreWeightedAvgPx', 'HighPx', 'PreClosePx', 'LowPx',
                       'WeightedAvgBidPx']

sz_order = ['OrderQty', 'OrdType', 'TransactTime', 'ExpirationDays', 'Side',
            'ApplSeqNum', 'Contactor', 'SendingTime', 'Price', 'ChannelNo',
            'ExpirationType', 'ContactInfo', 'ConfirmID']

sz_tick_columns = ['ApplSeqNum', 'BidApplSeqNum', 'SendingTime', 'Price', 'ChannelNo',
                   'Qty', 'OfferApplSeqNum', 'Amt', 'ExecType', 'TransactTime']

sh_tick_columns = ['SecurityID', 'TradeTime', 'TradePrice', 'TradeQty', 'TradeAmount',
                   'BuyNo', 'SellNo', 'TradeIndex', 'ChannelNo', 'TradeBSFlag', 'BizIndex']


sh_snapshot_columns = ['SecurityID', 'DateTime', 'PreClosePx', 'OpenPx', 'HighPx', 'LowPx', 'LastPx',
                       'TotalVolumeTrade', 'TotalValueTrade', 'InstrumentStatus',
                       'BidPrice0', 'BidPrice1', 'BidPrice2', 'BidPrice3', 'BidPrice4', 'BidPrice5', 'BidPrice6', 'BidPrice7', 'BidPrice8', 'BidPrice9',
                       'BidOrderQty0', 'BidOrderQty1', 'BidOrderQty2', 'BidOrderQty3', 'BidOrderQty4', 'BidOrderQty5', 'BidOrderQty6', 'BidOrderQty7', 'BidOrderQty8', 'BidOrderQty9',
                       'BidNumOrders0', 'BidNumOrders1', 'BidNumOrders2', 'BidNumOrders3', 'BidNumOrders4', 'BidNumOrders5', 'BidNumOrders6', 'BidNumOrders7', 'BidNumOrders8', 'BidNumOrders9',
                       'BidOrders0', 'BidOrders1', 'BidOrders2', 'BidOrders3', 'BidOrders4', 'BidOrders5', 'BidOrders6', 'BidOrders7', 'BidOrders8', 'BidOrders9',
                       'BidOrders10', 'BidOrders11', 'BidOrders12', 'BidOrders13', 'BidOrders14', 'BidOrders15', 'BidOrders16', 'BidOrders17', 'BidOrders18', 'BidOrders19',
                       'BidOrders20', 'BidOrders21', 'BidOrders22', 'BidOrders23', 'BidOrders24', 'BidOrders25', 'BidOrders26', 'BidOrders27', 'BidOrders28', 'BidOrders29',
                       'BidOrders30', 'BidOrders31', 'BidOrders32', 'BidOrders33', 'BidOrders34', 'BidOrders35', 'BidOrders36', 'BidOrders37', 'BidOrders38', 'BidOrders39',
                       'BidOrders40', 'BidOrders41', 'BidOrders42', 'BidOrders43', 'BidOrders44', 'BidOrders45', 'BidOrders46', 'BidOrders47', 'BidOrders48', 'BidOrders49',
                       'OfferPrice0', 'OfferPrice1', 'OfferPrice2', 'OfferPrice3', 'OfferPrice4', 'OfferPrice5', 'OfferPrice6', 'OfferPrice7', 'OfferPrice8', 'OfferPrice9',
                       'OfferOrderQty0', 'OfferOrderQty1', 'OfferOrderQty2', 'OfferOrderQty3', 'OfferOrderQty4', 'OfferOrderQty5', 'OfferOrderQty6', 'OfferOrderQty7', 'OfferOrderQty8', 'OfferOrderQty9',
                       'OfferNumOrders0', 'OfferNumOrders1', 'OfferNumOrders2', 'OfferNumOrders3', 'OfferNumOrders4', 'OfferNumOrders5', 'OfferNumOrders6', 'OfferNumOrders7', 'OfferNumOrders8', 'OfferNumOrders9',
                       'OfferOrders0', 'OfferOrders1', 'OfferOrders2', 'OfferOrders3', 'OfferOrders4', 'OfferOrders5', 'OfferOrders6', 'OfferOrders7', 'OfferOrders8', 'OfferOrders9',
                       'OfferOrders10', 'OfferOrders11', 'OfferOrders12', 'OfferOrders13', 'OfferOrders14', 'OfferOrders15', 'OfferOrders16', 'OfferOrders17', 'OfferOrders18', 'OfferOrders19',
                       'OfferOrders20', 'OfferOrders21', 'OfferOrders22', 'OfferOrders23', 'OfferOrders24', 'OfferOrders25', 'OfferOrders26', 'OfferOrders27', 'OfferOrders28', 'OfferOrders29',
                       'OfferOrders30', 'OfferOrders31', 'OfferOrders32', 'OfferOrders33', 'OfferOrders34', 'OfferOrders35', 'OfferOrders36', 'OfferOrders37', 'OfferOrders38', 'OfferOrders39',
                       'OfferOrders40', 'OfferOrders41', 'OfferOrders42', 'OfferOrders43', 'OfferOrders44', 'OfferOrders45', 'OfferOrders46', 'OfferOrders47', 'OfferOrders48', 'OfferOrders49',
                       'NumTrades', 'IOPV', 'TotalBidQty', 'TotalOfferQty', 'WeightedAvgBidPx', 'WeightedAvgOfferPx', 'TotalBidNumber',
                       'TotalOfferNumber', 'BidTradeMaxDuration', 'OfferTradeMaxDuration', 'NumBidOrders', 'NumOfferOrders',
                       'WithdrawBuyNumber', 'WithdrawBuyAmount', 'WithdrawBuyMoney', 'WithdrawSellNumber', 'WithdrawSellAmount', 'WithdrawSellMoney',
                       'ETFBuyNumber', 'ETFBuyAmount', 'ETFBuyMoney', 'ETFSellNumber', 'ETFSellAmount', 'ETFSellMoney']


def maketime(time):
    time = str(time)
    return time[0:4]+'-'+time[4:6]+'-' + time[6:8] + ' '+time[8:10]+':'+time[10:12]+':'+time[12:14]


def maketime_tick(time):
    time = str(time)
    return time[0:4]+'-'+time[4:6]+'-' + time[6:8] + ' '+time[8:10]+':'+time[10:12]+':'+time[12:14]+'.' + time[14:]
