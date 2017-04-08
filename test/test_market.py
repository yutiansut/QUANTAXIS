import QUANTAXIS as QA
#QA.QA_Setting.client=QA.QAUtil.QA_util_sql_mongo_setting(QA.QA_Setting.QA_util_sql_mongo_ip,QA.QA_Setting.QA_util_sql_mongo_port)
market=QA.QAMarket_core.QA_Market()
bid=QA.QABid.QA_QAMarket_bid
market.market_make_deal(bid,QA.QA_Setting.client)
