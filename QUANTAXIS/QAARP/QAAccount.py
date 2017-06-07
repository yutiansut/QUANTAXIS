# encoding: UTF-8
from QUANTAXIS.QAUtil import QA_util_log_info
import random
import datetime

"""
账户类:
记录回测的时候的账户情况(持仓列表,交易历史,利润,报单,可用资金)

"""
# 2017/6/4修改: 去除总资产的动态权益计算
class QA_Account:
    # 一个portfolio改成list模式
    portfolio = [['date', 'id', ' price', 'amount', 'status']]
    # 历史交易记录
    trade_history = [['date', 'id', ' price', 'amount', ' towards']]
    # 历史报单记录
    # 报单和真实情况去匹配:
    # 报单日期,报单股票,报单价格,报单数量,报单状态(限价/市价),info
    bid = [['date', 'id', ' price', 'amount', 'status']]
    # 可用资金记录表
    init_assest = 1000000
    cash=[]
    assets=[]


    def init(self):
        self.portfolio = [['date', 'id', ' price', 'amount', 'status']]
        self.history=[]
        self.profit = []
        self.account_cookie = str(random.random())
        self.cash = [self.init_assest]
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': '',
                    'strategy': ''
                }
            },
            'body': {
                'account': {
                    'portfolio': self.portfolio,
                    'cash': self.cash,
                    'assets':self.cash,
                    'history': self.history
                },
                #'time':datetime.datetime.now(),
                'date_stamp': str(datetime.datetime.now().timestamp())
            }
        }

    def QA_account_update(self, update_message):
        if str(update_message['status'])[0] == '2':
            # 这里就是买卖成功的情况
            # towards>1 买入成功
            # towards<1 卖出成功

            new_code = update_message['bid']['code']
            new_amount = update_message['bid']['amount']
            new_trade_date = update_message['bid']['date']
            new_towards = update_message['bid']['towards']
            new_price = update_message['bid']['price']
            self.history.append(update_message['bid'])
            # 先计算收益和利润
            
           
            # 修改持仓表
            if int(new_towards) > 0:

                self.portfolio.append([new_trade_date,new_price,new_code,new_amount])
                # 将交易记录插入历史交易记录


            else:
                #更新账户
                pop_list=[]
                while new_amount>0:
                    
                    if len(self.portfolio)>1:
                        for i in range(0,len(self.portfolio)):

                            
                            if new_code in self.portfolio[i]:
                                if new_amount>self.portfolio[i][3]:

                                    new_amount=new_amount-self.portfolio[i][3]
                                    print(new_amount)
                                    pop_list.append(i)

                                elif new_amount<self.portfolio[i][3]:
                                    self.portfolio[i][3]=self.portfolio[i][3]-new_amount
                                    new_amount=0
                                elif new_amount==self.portfolio[i][3]:
                                    
                                    new_amount=0
                                    pop_list.append(i)
                print(pop_list)
                pop_list.sort()
                pop_list.reverse()
                for id in pop_list:
                    self.portfolio.pop(id)

                
            # 将交易记录插入历史交易记录


        else:
            pass
        self.QA_account_calc_profit(update_message)
        self.message = {
                'header': {
                    'source': 'account',
                    'cookie': self.account_cookie,
                    'session': {
                        'user': update_message['user'],
                        'strategy': update_message['strategy'],
                        'code': update_message['bid']['code']
                    }

                },
                'body': {
                    'account': {
                        'portfolio': self.portfolio,
                        'history': self.history,
                        'cash': self.cash,
                        'assets': self.assets,
                    },
                    'time': datetime.datetime.now(),
                    'date_stamp': str(datetime.datetime.now().timestamp())
                }
            }

        return self.message

    def QA_account_calc_profit(self, update_message):
        if update_message['status'] == 200 and update_message['bid']['towards'] == 1:
            # 买入/
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值
           
            # 买入的部分在update_message
            
            # 可用资金=上一期可用资金-买入的资金
            self.cash.append(float(self.cash[-1]) - float(
                update_message['bid']['price']) * float(update_message['bid']['amount']) * update_message['bid']['towards'])

        elif update_message['status'] == 200 and update_message['bid']['towards'] == -1:
            # success trade,sell
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值
            # 买入的部分在update_message
            
            # 卖出的时候,towards=-1,所以是加上卖出的资产
            # 可用资金=上一期可用资金+卖出的资金
            self.cash.append(float(self.cash[-1]) - float(
                update_message['bid']['price']) * float(update_message['bid']['amount']) * update_message['bid']['towards'])
            
            # 更新可用资金历史
           
        
            # hold
        market_value=0
        for i in range(1,len(self.portfolio)):
            market_value=market_value+float(self.portfolio[i][1])*float(self.portfolio[i][3])
        self.assets.append(self.cash[-1]+market_value)

    def QA_account_receive_deal(self, message):
        # 主要是把从market拿到的数据进行解包,一个一个发送给账户进行更新,再把最后的结果反回
        
        
        data = self.QA_account_update({
            'code': message['header']['code'],
            'status': message['header']['status'],
            'user': message['header']['session']['user'],
            'strategy': message['header']['session']['strategy'],
            'date_stamp': str(datetime.datetime.now().timestamp()),
            'bid': message['body']['bid'],
            'market': message['body']['market']
        })
        return data
