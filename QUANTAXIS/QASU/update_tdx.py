from QUANTAXIS.QAUtil import QA_Setting,QA_util_log_info
from QUANTAXIS.QAFetch.QATushare import QA_fetch_get_stock_time_to_market


def update_stock_day(client=QA_Setting.client):
    
    coll_stocklist = client.quantaxis.stock_list
    # 使用find_one
    stock_list = coll_stocklist.find_one()['stock']['code']
    for item in stock_list:
        QA_util_log_info('updating stock data -- %s' % item)
        # coll.find({'code':str(item)[0:6]}).count()
        # 先拿到最后一个记录的交易日期
        try:
            if coll_stock_day.find({'code': str(item)[0:6]}).count() > 0:
                # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
                start_date = str(coll_stock_day.find({'code': str(item)[0:6]})[
                                 coll_stock_day.find({'code': str(item)[0:6]}).count() - 1]['date'])
                end_date = str(datetime.date.today())

                QA_util_log_info('trying updating from %s to %s' %
                                 (start_date, end_date))
                data = QATushare.QA_fetch_get_stock_day(
                    str(item)[0:6], start_date, end_date,'02')[1::]
            else:
                # 这时候直接更新拿到所有的数据就好了
                data = QATushare.QA_fetch_get_stock_day(
                    item, startDate='1990-01-01',if_fq='02')

            coll_stock_day.insert_many(data)