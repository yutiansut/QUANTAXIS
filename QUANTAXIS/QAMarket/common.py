
# shipane

# "申报时间", "证券代码", "证券名称", "操作", "委托状态", "委托数量", "成交数量", "撤消数量", , "委托价格", "成交均价", "合同编号", "委托子业务", "约定号", "对方账户", "参考汇率", "结算币种", "交易币种", "证券中文名", "出错信息
from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION, TRADE_STATUS, ORDER_STATUS
cn_en_compare = {'明细': 'id',
                 '证券代码': 'code',
                 '市场代码': 'market_code',
                 '证券名称': 'name',
                 '股票余额': 'amount',
                 '可用余额': 'sell_available',
                 '冻结数量': 'frozen',
                 '买卖标志': 'towards',
                 '撤消数量': 'cancel_amount',
                 '撤单数量': 'cancel_amount',
                 '订单类型': 'order_type',
                 '操作': 'towards',  # 这个是模拟交易的买卖标志
                 '委托价格': 'order_price',
                 '委托数量': 'order_amount',
                 '成交价格': 'trade_price',
                 '成交数量': 'trade_amount',
                 '状态说明': 'status',
                 '备注': 'status',  # 这个是模拟交易的status
                 '场外撤单': 'cancel_outside',
                 '场内撤单': 'cancel_inside',
                 '未成交': 'pending',
                 '全部撤单': 'cancel_all',
                 '委托时间': 'order_time',
                 '合同编号': 'realorder_id',  # 模拟交易的委托编号
                 '撤销数量': 'cancel_amount',
                 '委托编号': 'realorder_id',
                 '批次号': 'pc_id',
                 '盈亏': 'pnl',
                 "": 'None',
                 '成本金额': 'cost',
                 '盈亏估算': 'pnl_prob',
                 '成本价': 'hold_price',
                 '实现盈亏': 'pnl_money_already',
                 '盈亏比例(%)': 'pnl_ratio',
                 '市价': 'price',
                 '市值': 'market_value',
                 '交易市场': 'SSE',
                 '股东帐户': 'shareholders',
                 '实际数量': 'total_amount',
                 '可申赎数量': 'redemption_number',
                 '资讯': 'message',
                 '汇率': 'exchange_rate',
                 '沪港深港市场': 'hkmarket',
                 '成本价港币': 'hold_price_hk',
                 '买入成本价港币': 'buy_price_hk',
                 '买入在途数量': 'buy_onway',
                 '卖出在途数量': 'sell_onway',
                 '场内废单': 'failled',
                 '场外撤单': 'cancel_outside',
                 '场内撤单': 'cancel_inside',
                 '未成交': 'pending',
                 '已成交': 'finished',
                 '全部撤单': 'cancel_all',
                 '成交均价': 'trade_price',  # 成交价
                 '成交金额': 'trade_money',
                 '成交编号': 'trade_id',
                 '委托状态': 'status',
                 '申报时间': 'order_time',
                 '委托日期': 'order_date',
                 '委托子业务': 'order_subjob',
                 '约定号': 'yd_id',
                 '对方账户': 'other_account',
                 '参考汇率': 'refer_exchange',
                 '结算币种': 'settlement_currency',
                 '交易币种': 'trade_currency',
                 '证券中文名': 'CNname',
                 '出错信息': 'error',
                 '成交时间': 'trade_time'}


trade_towards_cn_en = {
    '买入': ORDER_DIRECTION.BUY,
    '买': ORDER_DIRECTION.BUY,
    '卖出': ORDER_DIRECTION.SELL,
    '卖': ORDER_DIRECTION.SELL,
    '申购': ORDER_DIRECTION.ASK,
    '申': ORDER_DIRECTION.ASK,
    '证券买入': ORDER_DIRECTION.BUY,
    '证券卖出': ORDER_DIRECTION.SELL,
    '派息': ORDER_DIRECTION.XDXR,
    '': ORDER_DIRECTION.OTHER
}

order_status_cn_en = {
    '已报': ORDER_STATUS.QUEUED,  # 　委托已经被交易端接受了
    '未成交': ORDER_STATUS.QUEUED,
    '已确认': ORDER_STATUS.QUEUED,  # 新股申购已经被交易端接受
    '场内废单': ORDER_STATUS.FAILED,
    '废单': ORDER_STATUS.FAILED,  # 委托不符合交易规则，被交易端拒绝了
    '未报': ORDER_STATUS.FAILED,  # 委托还没有被交易端接受
    '场外废单': ORDER_STATUS.FAILED,
    '已成交': ORDER_STATUS.SUCCESS_ALL,
    '已成': ORDER_STATUS.SUCCESS_ALL,
    '全部成交': ORDER_STATUS.SUCCESS_ALL,
    '部成': ORDER_STATUS.SUCCESS_PART,  # 委托已经成交了一部份
    '已撤单': ORDER_STATUS.CANCEL_ALL,
    '全部撤单': ORDER_STATUS.CANCEL_ALL,
    '已撤': ORDER_STATUS.CANCEL_ALL,
    '已报待撤': ORDER_STATUS.QUEUED,  # 已经申报了撤单，交易端也已接受，但目前可能因为还没在交易时间段，所以还在等待撤消
    '场内撤单': ORDER_STATUS.CANCEL_ALL,
}
