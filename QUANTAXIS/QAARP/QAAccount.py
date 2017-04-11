# encoding: UTF-8
from QUANTAXIS.QAUtil import QA_util_log_info
from QUANTAXIS.QASignal import QA_signal_send
import random
class QA_Account:
    def __init__(self):
        self.assets=1000
        self.portfolio={'date':'', 'id':'N',' price':'', 'amount':''}
        self.cash=self.assets
        self.history_trade=[['date', 'id',' price', 'amount',' towards']]
        self.total_assest=[].append(self.assets)
        self.total_profit=[].append('0')
        self.total_cur_profit=[].append('0')
        self.assets_market_hold_value=0
        self.assets_free=1000
        self.cur_profit
        #date, id, price, amount, towards
        self.account_cookie=str(random.random())
        self.portfit=0
        self.hold=0

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
    def QA_account_receive_deal(self,message,client):
        self.account.QA_account_update({
            'update':True,
            'price':message['bid']['price'],
            'id':message['bid']['code'],
            'amount':message['bid']['amount'],
            'towards':message['bid']['towards'],
            'date':message['bid']['time'],
            'user':message['header']['session']['user'],
            'strategy_name':message['header']['session']['strategy'],
            'time':datetime.datetime.now(),
            'date_stamp':str(datetime.datetime.now().timestamp()),
            'bid':message['body']['bid'],
            'market':message['body']['market']
            })
        

    def QA_account_update(self,update_message,client):
        if update_message['update']==True:
            new_id=update_message['id']
            new_amount=update_message['amount']
            new_trade_date=update_message['date']
            new_towards=update_message['towards']
            new_price=update_message['price']
            

            appending_list=[new_trade_date, new_id, new_price, new_amount, new_towards]
            if new_towards>0:
                
                self.portfolio['date']=new_trade_date
                self.portfolio['price']=new_price
                self.portfolio['id']=new_id
                self.portfolio['amount']=new_amount
                
            else:
                self.portfolio['date']=''
                self.portfolio['price']=''
                self.portfolio['id']='N'
                self.portfolio['amount']=''
            self.assets_free=float(self.total_assest[-1])-float(new_amount)*float(new_price)*int(new_towards)

            self.history_trade.append(appending_list)
            self.QA_account_calc_profit()
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
                        'cur_profit':self.cur_profit
                    },
                    'bid':update_message['bid'],
                    'market':update_message['market'],
                    'time':datetime.datetime.now(),
                    'date_stamp':str(datetime.datetime.now().timestamp())


                }
            }
            QA_signal_send(message,client)
    def QA_account_renew(self):
        #未来发送给R,P的
        pass
    def QA_account_calc_profit(self):
        profit=0
        for item in range(1,len(self.history),1):
        # history:
        # date, id, price, amount, towards
            profit=profit-self.account.history_trade[item][2]*self.account.history_trade[item][3]*self.account.history_trade[item][4]
        if str(self.portfolio['id'])[0]=='N' :
            self.hold=0
        else :self.hold=1
        # calc
        if (self.hold==1):
            QA_util_log_info('hold-=========================================')
            now_price=float(dataA[-1][3])
            #（当前价-买入价）*量
            profit=profit+(now_price-self.portfolio['price'])*self.portfolio['amount']+self.account.history_trade[-1][2]*self.account.history_trade[-1][3]*self.account.history_trade[-1][4]
            print(now_price)
            print(self.portfolio['price'])
            self.cur_profit=(now_price-self.portfolio['price'])/(self.portfolio['price'])
            self.assets_market_hold_value=now_price*self.portfolio['amount']
            self.assets=self.assets_free+self.assets_market_hold_value
        else: 
            QA_util_log_info('No hold-=========================================')
            profit=profit
            self.cur_profit=0
        self.assets_market_hold_value=float(now_price)*float(self.portfolio['amount'])
        self.assets=float(self.assets_free)+float(self.assets_market_hold_value)
        self.total_assest.append(str(self.assets))
        self.total_cur_profit.append(self.cur_profit)