import QUANTAXIS as QA
#QA.QA_Setting.client=QA.QAUtil.QA_util_sql_mongo_setting(QA.QA_Setting.QA_util_sql_mongo_ip,QA.QA_Setting.QA_util_sql_mongo_port)
market=QA.QA_Market()
bid=QA.QA_QAMarket_bid.bid
market.market_make_deal(bid,QA.QA_Setting.client)
