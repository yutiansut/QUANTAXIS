# coding:utf-8

# 输入一个stock_list/stock_block
# 生成相关因子

from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv, QA_fetch_stock_min_adv
#from QUANTAXIS.QAAnalysis.QAAnalysis_dataframe import QA_Analysis_stock
class QA_Analysis_block():
    def __init__(self, block, *args, **kwargs):
        try:
            self.block_code = block.code
        except:
            self.block_code = block

    def market_data(self, start, end, _type='day'):
        return QA_fetch_stock_day_adv(self.block_code, start, end)
    
    def calc_pcg(self,market_data):
        pass



#ana=QA_Analysis_block(QA_fetch_stock_block_adv().get_block('昨日涨停').code.tolist())
#print(ana.market_data('2017-10-01','2017-10-30'))