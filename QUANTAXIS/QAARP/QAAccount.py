# encoding: UTF-8
from QUANTAXIS.QAUtil import QA_util_log_info
from QUANTAXIS.QABacktest.QABacktest_standard import QA_backtest_standard_record_account,QA_backtest_standard_record_market
from QUANTAXIS.QABacktest import QAAnalysis as Ana
import random
import datetime
class QA_Account:
    
    assets=1000
    portfolio={'date':'', 'id':'N',' price':'', 'amount':''}
    
    history_trade=[['date', 'id',' price', 'amount',' towards']]
    
    total_profit=[0]
    total_cur_profit_present=[0]
    assets_market_hold_value=0
    assets_free=assets
    cur_profit_present=0
    #date, id, price, amount, towards
    account_cookie=str(random.random())
    portfit=0
    hold=0
    def init(self):
        self.total_assest=[self.assets]
        self.assets_free=self.total_assest[-1]

        self.message={
                'header':{
                    'source':'account',
                    'cookie':'',
                    'session':{
                        'user':'',
                        'strategy':''
                    }
                    
                    },
                'body':{
                    'account':{
                        'init_assest':self.assets,
                        'portfolio':self.portfolio,
                        'history':self.history_trade,
                        'assest_now':self.assets,
                        'assest_history':self.total_assest,
                        'assest_free':self.assets_free,
                        'assest_fix':self.assets_market_hold_value,
                        'profit':self.portfit,
                        'total_profit':self.total_profit,
                        'cur_profit_present':0,
                        'hold':self.hold
                    },
                    'bid':{},
                    'market':{},
                    'time':datetime.datetime.now(),
                    'date_stamp':str(datetime.datetime.now().timestamp())


                }
            }
        

    def QA_account_get_cash(self):
        return self.assets
    def QA_account_get_portfolio(self):
        return self.portfolio
    def QA_account_get_amount(self):
        pass
    def QA_account_get_history(self):
        return self.history_trade
    def QA_Account_get_cookie(self):
        return self.account_cookie


    def QA_account_update(self,update_message,client):
        #print(update_message)
        if update_message['update']==True:
            new_id=update_message['id']
            new_amount=update_message['amount']
            new_trade_date=update_message['date']
            new_towards=update_message['towards']
            new_price=update_message['price']
            

            appending_list=[new_trade_date, new_id, new_price, new_amount, new_towards]
            if int(new_towards)>0:
                
                self.portfolio['date']=new_trade_date
                self.portfolio['price']=new_price
                self.portfolio['id']=new_id
                self.portfolio['amount']=new_amount
                
            else:
                self.portfolio['date']=''
                self.portfolio['price']=0
                self.portfolio['id']='N'
                self.portfolio['amount']=0
            #print(self.total_assest)
            #print(int(new_amount))
            #print(float(new_price))
            #print(int(new_towards))
            self.assets_free=float(self.total_assest[-1])-int(new_amount)*float(new_price)*int(new_towards)

            self.history_trade.append(appending_list)
            self.QA_account_calc_profit(update_message)
            message={
                'header':{
                    'source':'account',
                    'cookie':self.account_cookie,
                    'session':{
                        'user':update_message['user'],
                        'strategy':update_message['strategy']
                    }
                    
                    },
                'body':{
                    'account':{
                        'init_assest':self.total_assest[0],
                        'portfolio':self.portfolio,
                        'history':self.history_trade,
                        'assest_now':self.assets,
                        'assest_history':self.total_assest,
                        'assest_free':self.assets_free,
                        'assest_fix':self.assets_market_hold_value,
                        'profit':self.portfit,
                        'total_profit':self.total_profit,
                        'cur_profit_present':self.cur_profit_present,
                        'hold':self.hold
                    },
                    'bid':update_message['bid'],
                    'market':update_message['market'],
                    'time':datetime.datetime.now(),
                    'date_stamp':str(datetime.datetime.now().timestamp())


                }
            }
            
        else:
            message={
                'header':{
                    'source':'account',
                    'cookie':self.account_cookie,
                    'session':{
                        'user':update_message['user'],
                        'strategy':update_message['strategy']
                    }
                    
                    },
                'body':{
                    'account':{
                        'init_assest':self.assets,
                        'portfolio':self.portfolio,
                        'history':self.history_trade,
                        'assest_now':self.assets,
                        'assest_history':self.total_assest,
                        'assest_free':self.assets_free,
                        'assest_fix':self.assets_market_hold_value,
                        'profit':self.portfit,
                        'total_profit':self.total_profit,
                        'cur_profit_present':self.cur_profit_present,
                        'hold':self.hold
                    },
                    'bid':update_message['bid'],
                    'market':update_message['market'],
                    'time':datetime.datetime.now(),
                    'date_stamp':str(datetime.datetime.now().timestamp())


                }
            }
            #属于不更新history和portfolio,但是要继续增加账户和日期的
        return message
        
    def QA_account_renew(self):
        #未来发送给R,P的
        pass
    def QA_account_calc_profit(self,update_message):
       # print(update_message)
        if update_message['update']==True and update_message['towards']==1:
            
            pass
           #success trade, buy
        elif update_message['update']==True and update_message['towards']==0:
            #success trade,sell
            pass
        elif update_message['update']==False :
            # hold
            pass
            
            
        
           
"""


        profit=0
        for item in range(1,len(self.history_trade),1):
        # history:
        # date, id, price, amount, towards
            profit=profit-float(self.history_trade[item][2])*float(self.history_trade[item][3])*float(self.history_trade[item][4])
            if str(self.portfolio['id'])[0]=='N' :
                self.hold=0
            else :self.hold=1
            # calc
            now_price=float(update_message['market']['close'])
            if (int(self.hold==1)):
                #QA_util_log_info('hold-=========================================')
                
                #（当前价-买入价）*量
                profit=profit+(now_price-float(self.portfolio['price']))*int(self.portfolio['amount'])+float(self.history_trade[-1][2])*float(self.history_trade[-1][3])*float(self.history_trade[-1][4])
                #print(now_price)
                #print(self.portfolio['price'])
                self.cur_profit_present=(now_price-float(self.portfolio['price']))/(float(self.portfolio['price']))
                self.assets_market_hold_value=float(now_price)*int(self.portfolio['amount'])
                self.assets=float(self.assets_free)+float(self.assets_market_hold_value)
            else: 
                #QA_util_log_info('No hold-=========================================')
                profit=profit
                self.cur_profit_present=0
        #print('---profit--')
        #print(profit)
        #print(now_price)
        #print(self.portfolio['amount'])
        self.total_profit.append(profit)
        self.assets_market_hold_value=float(now_price)*int(self.portfolio['amount'])
        self.assets=float(self.assets_free)+float(self.assets_market_hold_value)
        self.total_assest.append(str(self.assets))
        self.total_cur_profit_present.append(self.cur_profit_present)
        """
    def QA_account_analysis(self):
        pass
    def QA_Account_get_message(self):
        return self.message

    def QA_account_receive_deal(self,message,client):
        

        messages=self.QA_account_update({
            'update':message['header']['status'],
            'price':message['body']['bid']['price'],
            'id':message['body']['bid']['code'],
            'amount':message['body']['bid']['amount'],
            'towards':message['body']['bid']['towards'],
            'date':message['body']['bid']['time'],
            'user':message['header']['session']['user'],
            'strategy':message['header']['session']['strategy'],
            'time':datetime.datetime.now(),
            'date_stamp':str(datetime.datetime.now().timestamp()),
            'bid':message['body']['bid'],
            'market':message['body']['market']
            },client)
        return messages