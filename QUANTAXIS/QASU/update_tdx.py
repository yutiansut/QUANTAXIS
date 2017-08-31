from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info, trade_date_sse
from QUANTAXIS.QAFetch.QATushare import QA_fetch_get_stock_time_to_market
from QUANTAXIS.QASU.save_tdx import save_stock_day,QA_SU_save_stock_xdxr,save_stock_min
import datetime


def QA_update_stock_day_all(client=QA_Setting.client):

    coll_stock_day = client.quantaxis.stock_day
    for item in QA_fetch_get_stock_time_to_market().index:
        try:
            if coll_stock_day.find({'code': str(item)[0:6]}).count() > 0:
                # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现

                start_date = str(coll_stock_day.find({'code': str(item)[0:6]})[
                    coll_stock_day.find({'code': str(item)[0:6]}).count() - 1]['date'])
                end_date = str(datetime.date.today())
                start_date = trade_date_sse[trade_date_sse.index(
                    start_date) + 1]
                QA_util_log_info(' UPDATE_STOCK_DAY \n Trying updating %s from %s to %s' %
                                 (item, start_date, end_date))

                save_stock_day(item, start_date, end_date, coll_stock_day)

            else:
                save_stock_day(item, '1990-01-01',
                               datetime.date.today, coll_stock_day)

        except:
            QA_util_log_info('error in updating--- %s' % item)
    QA_util_log_info('Done == \n')


def QA_update_stock_xdxr_all(client=QA_Setting.client):
    client.quantaxis.drop_collection('stock_xdxr')
    QA_SU_save_stock_xdxr()


def QA_update_stock_min_all(client=QA_Setting.client):
    

    """
    stock_min 分三个库 type区分
    1. 1min_level 库
    2. 5min_level 库
    3. 15min_level 库
    """

    coll_stock_min = client.quantaxis.stock_min
    for item in QA_fetch_get_stock_time_to_market().index:
        try:
            if coll_stock_min.find({'code': str(item)[0:6]}).count() > 0:
                # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
                ref_=coll_stock_min.find({'code': str(item)[0:6],'type':'1min'})
                start_date = ref_[ref_.count()-1]['datetime']
                end_date = str(datetime.datetime.now())
                start_date = trade_date_sse[trade_date_sse.index(
                    start_date) + 1]
                QA_util_log_info(' UPDATE_STOCK_DAY \n Trying updating %s from %s to %s' %
                                 (item, start_date, end_date))

                save_stock_min(item, start_date, end_date,'1min', coll_stock_min)

            else:
                save_stock_min(item, '1990-01-01',
                               datetime.date.today,'1min', coll_stock_min)

        except:
            QA_util_log_info('error in updating--- %s' % item)
    QA_util_log_info('Done == \n')    

if __name__ == '__main__':
    QA_update_stock_day_all()
    QA_update_stock_xdxr_all()
