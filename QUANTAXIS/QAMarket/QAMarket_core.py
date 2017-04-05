# coding :utf-8

from QUANTAXIS.QAUtil import QA_util_sql_mongo_setting,QA_util_log_info
from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QASignal import QA_signal_send
from .QABid import QA_QAMarket_bid
import datetime

class QA_market():

    client=QA_Setting.client
    # client=QA.QA_util_sql_mongo_setting()
    # db= client.market
    def market_make_deal(self,bid, client):
        db=client.quantaxis
        coll= db.stock_day
        item= coll.find_one({"code":str(bid.code)[0:6],"date": str(bid.time)})
        print(item["high"])
        print(item["low"])
        if ( bid.price<item["high"] and  bid.price>item["low"]):
            QA_util_log_info("deal success")
            QA_signal_message={'trade_status':'success','price':str(bid.price),
            'code':str( bid.code),'amount':str( bid.amount),'time':str( bid.time),
            'towards':str( bid.towards)}
            QA_signal_send('market','strategy',True,QA_signal_message)
            return True
        else:
            QA_util_log_info('not success')
            return False
