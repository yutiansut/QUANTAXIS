import pandas as pd
from qaenv import (clickhouse_ip, clickhouse_password, clickhouse_port,
                   clickhouse_user)
from QUANTAXIS.QAFactor.feature import QASingleFactor_DailyBase
from QUANTAXIS.QAFetch.QAClickhouse import QACKClient
from QUANTAXIS.QAIndicator.indicators import QA_indicator_MA


class MA10(QASingleFactor_DailyBase):

    def finit(self):
        
        self.clientr = QACKClient(clickhouse_ip, clickhouse_port, user=clickhouse_user, password=clickhouse_password)
        self.factor_name = 'MA10'

    def calc(self) -> pd.DataFrame:
        """

        the example is just a day datasource, u can use the min data to generate a day-frequence factor

        the factor should be in day frequence 
        """

        codellist = self.clientr.get_stock_list().order_book_id.tolist()
        start = '2020-01-01'
        end = '2021-09-22'
        data = self.clientr.get_stock_day_qfq_adv(codellist, start, end)
        res = data.add_func(QA_indicator_MA, 10)
        res.columns = ['factor']
        return res.reset_index().dropna()
