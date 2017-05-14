import datetime


class QA_QAMarket_bid():
    bid={
        'price':float(10.846),
        'time':str('2015-01-05'),
        'amount':int(10),
        'towards':int(1),
        'code':str('000001.SZ'),
        'user':str('root'),
        'strategy':str('example01'),
        'status':'0x01'
        }
    bid_list=[]
    #报价队列  插入/取出/查询
    def QA_bid_insert(self):
        self.bid_list.append(self.bid)
        
    def QA_bid_pop(self):
        self.bid_list.pop()
    def QA_bid_status(self):
        lens=len(self.bid_list)
        return {'status':lens}