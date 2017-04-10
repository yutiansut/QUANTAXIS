#coding :utf-8
from QUANTAXIS.QAUtil import QA_util_log_info
import random
class QA_Account:
    def __init__(self):
        self.assets=0
        self.portfolio={'date':'', 'id':'',' price':'', 'amount':''}

        self.history_trade=[['date', 'id',' price', 'amount',' towards']]

        #date, id, price, amount, towards
        self.account_cookie=str(random.random())
        

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
    def QA_account_receive_deal(self,message):
        pass

    def QA_account_update(self,update_message):
        if update_message['update']==True:
            new_id=update_message['id']
            new_amount=update_message['amount']
            new_trade_date=update_message['date']
            new_towards=update_message['towards']
            new_price=update_message['price']
            

            appending_list=[new_trade_date,new_id,new_price,new_amount,new_towards]
            if new_towards>0:
                
                self.portfolio['date']=new_trade_date
                self.portfolio['price']=new_price
                self.portfolio['id']=new_id
                self.portfolio['amount']=new_amount
                
            else:
                self.portfolio['date']=''
                self.portfolio['price']=''
                self.portfolio['id']=''
                self.portfolio['amount']=''
                

            self.history_trade.append(appending_list)


    def QA_account_renew(self):
        #未来发送给R,P的
        pass