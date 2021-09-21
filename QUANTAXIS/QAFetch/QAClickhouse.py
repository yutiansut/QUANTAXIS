import clickhouse_driver
import numpy as np
import pandas as pd
from qaenv import (clickhouse_ip, clickhouse_password, clickhouse_port,
                   clickhouse_user)
from QUANTAXIS.QAData import (QA_DataStruct_Day, QA_DataStruct_Future_day,
                              QA_DataStruct_Future_min,
                              QA_DataStruct_Index_day, QA_DataStruct_Index_min,
                              QA_DataStruct_Min, QA_DataStruct_Stock_day,
                              QA_DataStruct_Stock_min)
from QUANTAXIS.QAUtil import QA_util_get_real_date


def promise_list(x): return [x] if isinstance(x, str) else x


def stock_format(code):
    return code + '.XSHE' if code[0] != '6' else code+'.XSHG'


class QACKClient():
    def __init__(self, host=clickhouse_ip, port=clickhouse_port,  database='quantaxis', user=clickhouse_user, password=clickhouse_password):
        self.client = clickhouse_driver.Client(host=host, port=port,  database=database, user=user, password=password,
                                               settings={
                                                   'insert_block_size': 100000000},
                                               compression=True)

    def execute(self, sql):
        return self.client.query_dataframe(sql)

    def to_qfq(self, res):
        u = res.data.reset_index()
        u = u.assign(date=u.datetime.apply(lambda x: x.date()))
        u = u.set_index(['date', 'code'], drop=False)
        codelist = u.index.levels[1].unique().tolist()

        start = u.index.levels[0][0]
        end = u.index.levels[0][-1]
        adjx = self.get_stock_adj(codelist, start, end)
        if adjx is None:
            data = u.set_index(['datetime', 'code'])
        else:

            adjx = adjx.reset_index()
            adjx = adjx.assign(code=adjx.order_book_id).set_index(
                ['date', 'code']).adj
            data = u.join(adjx).set_index(['datetime', 'code']).fillna(1)

            for col in ['open', 'high', 'low', 'close']:
                data[col] = data[col] * data['adj']

                try:
                    data['high_limit'] = data['high_limit'] * data['adj']
                    data['low_limit'] = data['high_limit'] * data['adj']
                except:
                    pass

        return QA_DataStruct_Stock_min(data.sort_index(), if_fq='qfq')

    def make_ret5(self, data):
        """
        use open data make ret
        """
        r = data.groupby(level=1).open.apply(
            lambda x: x.pct_change(5).shift(-5))
        r.name = 'ret5'
        return r

    def make_ret_adjust(self, data):
        r = data.groupby(level=1).open.apply(lambda x: x.pct_change())
        return r

    def get_stock_industry(self, code, start, end):
        codex = []
        if isinstance(code, list):
            pass
        else:
            code = [code]
        start = QA_util_get_real_date(start)
        end = QA_util_get_real_date(end)
        for coder in code:
            if '.' in coder:
                codex.append(coder)
            else:
                codex.append(
                    coder+'.XSHG' if coder[0] == '6' else coder+'.XSHE')

        res = self.execute("SELECT * FROM quantaxis.citis_industry  WHERE ((`date` >= '{}')) AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(
            start, end, "'{}'".format("','".join(codex)))).drop_duplicates(['date', 'order_book_id'])
        return res

    def get_index_weight(self, code, start, end):
        codex = []
        if isinstance(code, list):
            pass
        else:
            code = [code]

        start = QA_util_get_real_date(start)
        end = QA_util_get_real_date(end)

        start = start[0:8]+'01'
        end = end[0:8]+'01'
        for coder in code:
            if '.' in coder:
                codex.append(coder)
            else:
                codex.append(
                    coder+'.XSHE' if coder[0] == '6' else coder+'.XSHG')

        res = self.execute("SELECT * FROM quantaxis.index_weight  WHERE ((`date` >= '{}')) AND (`date` <= '{}') AND (`index_code` IN ({}))".format(
            start, end, "'{}'".format("','".join(codex)))).drop_duplicates(['date', 'order_book_id'])
        return res

    def get_stock_adj(self, code, start, end):
        codex = []
        if isinstance(code, list):
            pass
        else:
            code = [code]

        start = QA_util_get_real_date(start)
        end = QA_util_get_real_date(end)

        for coder in code:
            if '.' in coder:
                codex.append(coder)
            else:
                codex.append(
                    coder+'.XSHG' if coder[0] == '6' else coder+'.XSHE')
        res = self.execute("SELECT * FROM quantaxis.stock_adj  WHERE ((`date` >= '{}')) AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(
            start, end, "'{}'".format("','".join(codex)))).drop_duplicates(['date', 'order_book_id'])
        #res = res.assign(code = res.code.apply(lambda x: x[0:6]))
        return res.set_index(['date', 'order_book_id']).sort_index()

    def get_stock_day_qfq(self, codelist, start, end):
        codelist = promise_list(codelist)
        adjx = self.get_stock_adj(codelist, start, end)

        columns_raw = ['date', 'order_book_id', 'num_trades', 'limit_up',
                       'limit_down', 'open', 'high', 'low', 'close', 'volume', 'total_turnover']
        u = self.execute("SELECT * FROM quantaxis.stock_cn_day  WHERE ((`date` >= '{}')) \
                         AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['date', 'order_book_id'])

        u = u.set_index(['date', 'order_book_id'], drop=False).sort_index()

        data = u.join(adjx).set_index(
            ['date', 'order_book_id']).sort_index().fillna(1)

        for col in ['open', 'high', 'low', 'close']:
            data[col] = data[col] * data['adj']

            try:
                data['limit_up'] = data['limit_up'] * data['adj']
                data['limit_down'] = data['limit_down'] * data['adj']
            except:
                pass

        return data.sort_index()

    def get_stock_day_qfq_adv(self, codelist, start, end):

        res = self.get_stock_day_qfq(codelist, start, end).reset_index()
        return QA_DataStruct_Stock_day(res.assign(amount=res.total_turnover, code=res.order_book_id).set_index(['date', 'code']), if_fq='qfq')

    def get_stock_min_qfq_adv(self, codelist, start, end):
        return self.to_qfq(self.get_stock_min(codelist, start, end))

    def get_stock_list(self):
        return self.client.query_dataframe('select * from stock_cn_codelist').query('status=="Active"')

    def get_fund_list(self):
        return self.client.query_dataframe('select * from fund_cn_codelist')

    def get_etf_components(self, etf, start, end):
        codelist = promise_list(etf)
        return self.client.query_dataframe("SELECT * FROM quantaxis.etf_components  WHERE ((`trading_date` >= '{}')) \
                                AND (`trading_date` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['trading_date', 'order_book_id'])

    def get_stock_day(self, codelist, start, end):
        codelist = promise_list(codelist)
        if 'XS' not in codelist[0]:
            codelist = pd.Series(codelist).apply(
                lambda x: x+'.XSHE' if x[0] != '6' else x+'.XSHG').tolist()
        columns_raw = ['date', 'order_book_id', 'num_trades', 'limit_up',
                       'limit_down', 'open', 'high', 'low', 'close', 'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.stock_cn_day  WHERE ((`date` >= '{}')) \
                         AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['date', 'order_book_id'])
        return QA_DataStruct_Stock_day(res.assign(date=pd.to_datetime(res.date), code=res.order_book_id, amount=res.total_turnover).set_index(['date', 'code']).sort_index())

    def get_stock_min(self, codelist, start, end):
        codelist = promise_list(codelist)
        if 'XS' not in codelist[0]:
            codelist = pd.Series(codelist).apply(
                lambda x: x+'.XSHE' if x[0] != '6' else x+'.XSHG').tolist()

        columns_raw = ['datetime', 'order_book_id',  'open',
                       'high', 'low', 'close', 'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.stock_cn_1min  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['datetime', 'order_book_id'])
        return QA_DataStruct_Stock_min(res.assign(datetime=pd.to_datetime(res.datetime), code=res.order_book_id, amount=res.total_turnover, type='1min',).set_index(['datetime', 'code']).sort_index())

    def get_stock_min_close(self, codelist, start, end):
        codelist = promise_list(codelist)
        if 'XS' not in codelist[0]:
            codelist = pd.Series(codelist).apply(
                lambda x: x+'.XSHE' if x[0] != '6' else x+'.XSHG').tolist()

        columns_raw = ['datetime', 'order_book_id', 'close']
        res = self.client.query_dataframe("SELECT datetime, order_book_id, close FROM quantaxis.stock_cn_1min  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['datetime', 'order_book_id'])
        return res.assign(datetime=pd.to_datetime(res.datetime)).set_index(['datetime', 'order_book_id']).sort_index()

    def get_future_day(self, codelist, start, end):
        codelist = promise_list(codelist)
        columns_raw = ['date', 'order_book_id', 'limit_up', 'limit_down', 'open_interest',
                       'prev_settlement', 'settlement', 'open', 'high', 'low', 'close',
                       'volume', 'total_turnover']

        res = self.client.query_dataframe("SELECT * FROM quantaxis.future_cn_day  WHERE ((`date` >= '{}')) \
                         AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['date', 'order_book_id'])

        return QA_DataStruct_Future_day(res.assign(date=pd.to_datetime(res.date),
                                                   code=res.order_book_id,
                                                   amount=res.total_turnover,
                                                   position=res.open_interest,
                                                   price=res.settlement).set_index(['date', 'code']))

    def get_future_min(self, codelist, start, end):
        codelist = promise_list(codelist)
        columns_raw = ['datetime', 'order_book_id', 'open_interest', 'trading_date',
                       'open', 'high', 'low', 'close',
                                   'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.future_cn_1min  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['datetime', 'order_book_id'])
        return QA_DataStruct_Future_min(res.assign(datetime=pd.to_datetime(res.datetime),
                                                   position=res.open_interest,
                                                   code=res.order_book_id,
                                                   tradetime=res.trading_date,
                                                   price=res.close,
                                                   type='1min',
                                                   amount=res.total_turnover).set_index(['datetime', 'code']).sort_index())

    def get_stock_tick(self, codelist, start, end):
        codelist = promise_list(codelist)
        if 'XS' not in codelist[0]:
            codelist = pd.Series(codelist).map(str).apply(
                lambda x: x+'.XSHE' if x[0] != '6' else x+'.XSHG').tolist()

        columns_raw = ['datetime', 'trading_date', 'order_book_id', 'open', 'last', 'high',
                       'low', 'prev_close', 'volume', 'total_turnover', 'limit_up',
                       'limit_down', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4',
                       'b5', 'a1_v', 'a2_v', 'a3_v', 'a4_v', 'a5_v', 'b1_v', 'b2_v', 'b3_v',
                       'b4_v', 'b5_v', 'change_rate']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.stock_cn_tick  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw]
        return res.assign(datetime=pd.to_datetime(res.datetime), code=res.order_book_id, amount=res.total_turnover).set_index(['datetime', 'code']).sort_index()

    def get_index_tick(self, codelist, start, end):
        codelist = promise_list(codelist)

        columns_raw = ['datetime', 'trading_date', 'order_book_id', 'open', 'last', 'high',
                       'low', 'prev_close', 'volume', 'total_turnover', 'limit_up',
                       'limit_down', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4',
                       'b5', 'a1_v', 'a2_v', 'a3_v', 'a4_v', 'a5_v', 'b1_v', 'b2_v', 'b3_v',
                       'b4_v', 'b5_v', 'change_rate']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.index_cn_tick  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['datetime', 'order_book_id'])
        return res.assign(datetime=pd.to_datetime(res.datetime), code=res.order_book_id, amount=res.total_turnover).set_index(['datetime', 'code']).sort_index()

    def get_future_tick(self, codelist, start, end):
        codelist = promise_list(codelist)
        columns_raw = ['datetime', 'trading_date', 'order_book_id', 'open', 'last', 'high',
                       'low', 'prev_settlement', 'prev_close', 'open_interest', 'volume',
                       'total_turnover', 'limit_up', 'limit_down', 'a1', 'a2', 'a3', 'a4',
                       'a5', 'b1', 'b2', 'b3', 'b4', 'b5', 'a1_v', 'a2_v', 'a3_v', 'a4_v',
                       'a5_v', 'b1_v', 'b2_v', 'b3_v', 'b4_v', 'b5_v', 'change_rate']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.future_cn_tick  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw]
        return res.assign(datetime=pd.to_datetime(res.datetime), code=res.order_book_id, amount=res.total_turnover).set_index(['datetime', 'code']).sort_index()

    def get_index_day(self, codelist, start, end):
        codelist = promise_list(codelist)
        # if 'XS' not in codelist[0]:
        #     codelist = pd.Series(codelist).apply(
        #         lambda x: x+'.XSHG' if x[0] != 6 else x+'.XSHE').tolist()

        columns_raw = ['date', 'order_book_id', 'num_trades', 'open', 'high', 'low', 'close',
                       'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.index_cn_day  WHERE ((`date` >= '{}')) \
                         AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['date', 'order_book_id'])
        return QA_DataStruct_Index_day(res.assign(date=pd.to_datetime(res.date), code=res.order_book_id, amount=res.total_turnover).set_index(['date', 'code']).sort_index())

    def get_index_min(self, codelist, start, end):
        codelist = promise_list(codelist)
        # if 'XS' not in codelist[0]:
        #     codelist = pd.Series(codelist).apply(
        #         lambda x: x+'.XSHG' if x[0] != 6 else x+'.XSHE').tolist()

        columns_raw = ['datetime', 'order_book_id',  'open',
                       'high', 'low', 'close', 'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.index_cn_1min  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['datetime', 'order_book_id'])
        return QA_DataStruct_Index_min(res.assign(datetime=pd.to_datetime(res.datetime), code=res.order_book_id, amount=res.total_turnover, type='1min',).set_index(['datetime', 'code']).sort_index())

    def get_etf_day(self, codelist, start, end):
        codelist = promise_list(codelist)
        # if 'XS' not in codelist[0]:
        #     codelist = pd.Series(codelist).apply(
        #         lambda x: x+'.XSHG' if x[0] != 6 else x+'.XSHE').tolist()

        columns_raw = ['date', 'order_book_id', 'num_trades', 'open', 'high', 'low', 'close',
                       'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.etf_cn_day  WHERE ((`date` >= '{}')) \
                         AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['date', 'order_book_id'])
        return QA_DataStruct_Index_day(res.assign(date=pd.to_datetime(res.date), code=res.order_book_id, amount=res.total_turnover).set_index(['date', 'code']).sort_index())

    def get_etf_min(self, codelist, start, end):
        codelist = promise_list(codelist)
        # if 'XS' not in codelist[0]:
        #     codelist = pd.Series(codelist).apply(
        #         lambda x: x+'.XSHG' if x[0] != 6 else x+'.XSHE').tolist()

        columns_raw = ['datetime', 'order_book_id',  'open',
                       'high', 'low', 'close', 'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.etf_cn_1min  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['datetime', 'order_book_id'])
        return QA_DataStruct_Index_min(res.assign(datetime=pd.to_datetime(res.datetime), code=res.order_book_id, amount=res.total_turnover, type='1min',).set_index(['datetime', 'code']).sort_index())

    def get_lof_day(self, codelist, start, end):
        codelist = promise_list(codelist)
        # if 'XS' not in codelist[0]:
        #     codelist = pd.Series(codelist).apply(
        #         lambda x: x+'.XSHG' if x[0] != 6 else x+'.XSHE').tolist()

        columns_raw = ['date', 'order_book_id', 'num_trades', 'open', 'high', 'low', 'close',
                       'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.lof_cn_day  WHERE ((`date` >= '{}')) \
                         AND (`date` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['date', 'order_book_id'])
        return QA_DataStruct_Index_day(res.assign(date=pd.to_datetime(res.date), code=res.order_book_id, amount=res.total_turnover).set_index(['date', 'code']).sort_index())

    def get_lof_min(self, codelist, start, end):
        codelist = promise_list(codelist)
        # if 'XS' not in codelist[0]:
        #     codelist = pd.Series(codelist).apply(
        #         lambda x: x+'.XSHG' if x[0] != 6 else x+'.XSHE').tolist()

        columns_raw = ['datetime', 'order_book_id',  'open',
                       'high', 'low', 'close', 'volume', 'total_turnover']
        res = self.client.query_dataframe("SELECT * FROM quantaxis.lof_cn_1min  WHERE ((`datetime` >= '{}')) \
                         AND (`datetime` <= '{}') AND (`order_book_id` IN ({}))".format(start, end, "'{}'".format("','".join(codelist)))).loc[:, columns_raw].drop_duplicates(['datetime', 'order_book_id'])
        return QA_DataStruct_Index_min(res.assign(datetime=pd.to_datetime(res.datetime), code=res.order_book_id, amount=res.total_turnover, type='1min',).set_index(['datetime', 'code']).sort_index())
