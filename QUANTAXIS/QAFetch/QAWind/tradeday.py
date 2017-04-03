#Coding:utf-8
# based on [QAStandard-201-1]

from WindPy import w


def get_trade_date(endDate,exchange):
    
    supportExchanges=["SSE","SZSE","CFFEX","SHFE","DCE","CZCE"]
    if (exchange in supportExchanges):
    #"SSE","SZSE","CFFEX","SHFE","DCE","CZCE"
    #上海股票交易所,深圳股票交易所,中国金融期货交易所,上海期货交易所,大连商品交易所,郑州期货交易所
        exchanges="TradingCalendar="+exchange
        data=w.tdays("1990-01-01", endDate, exchanges)
        #print(data.Data)
        dates=data.Data
    else: 
        print("exchange name problem")
    return dates