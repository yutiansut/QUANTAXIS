#coding:utf-8
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_data
stock_list=['000001.SZ','600010.SZ']
variety='stock'
level='day'
start_date='2010-01-01'
end_date='2011-01-01'

# startegy


scribe_data=QA_fetch_data(variety,level,stock_list[0],start_date,end_date)
print(scribe_data)