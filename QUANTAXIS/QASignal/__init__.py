#Encoding:utf-8
from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting, QA_util_sql_mongo_setting
from QUANTAXIS.QABacktest.QABacktest_standard import QA_backtest_standard_record_account,QA_backtest_standard_record_market
from QUANTAXIS.QAARP.QAAccount import QA_Account
from .EventManager import QA_Signal_events, QA_Signal_eventManager
from .usualevnet import QA_Signal_Sender, QA_Signal_Listener, QA_signal_usual_model
from threading import *
import time,datetime,re

def QA_signal_send(message,client):
    # dispackage the message
    QA_util_log_info(message)
    if message['header']['source'] in ['market','Market']:
        # market message
        """
        something like this

        QA_signal_message={
            'header':{
                'source':'market',
                'status':200
            },
            'body':{
                'bid':{
                    'price':str(bid.price),
                    'code':str( bid.code),
                    'amount':str( bid.amount),
                    'time':str( bid.time),
                    'towards':str( bid.towards)
                    },
                'market':{
                    'open':item['open'],
                    'high':item['high'],
                    'low':item['low'],
                    'close':item['close'],
                    'amount':item['amount'],
                    'code':item['code']
                    }
                }
            }

            
        """
        
        account=QA_Account()
        account.QA_account_receive_deal(message,client)
        #QA_backtest_standard_record_market(message,client)
    elif message['header'] in ['account','Account','acc','ACC','ACCOUNT']:
        # account message
        """
        something like this
        message={
            'header':{
                'source':'account',
                'cookie':self.account_cookie
                },
            'body':{
                'init_assest':self.assets,
                'portfolio':self.portfolio,
                'history':self.history_trade
            }
            
        }
        """
        QA_backtest_standard_record_account(message, client)

    elif message['header'] in ['risk','RISK','QA_RISK']:
        pass
    

def QA_signal_resend(listener):
    pass





