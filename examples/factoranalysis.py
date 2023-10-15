import QUANTAXIS as QA
import pandas as pd
clickhouse_port = 9001
clickhouse_ip = 'localhost'
clickhouse_user = 'admin'
clickhouse_password = 'admin'


class MA(QA.QASingleFactor_DailyBase):

    def finit(self):

        self.clientr = QA.QACKClient(
            clickhouse_ip, clickhouse_port, user=clickhouse_user, password=clickhouse_password)
        self.factor_name = 'MA5'

    def calc(self) -> pd.DataFrame:
        """

        the example is just a day datasource, u can use the min data to generate a day-frequence factor

        the factor should be in day frequence 
        """

        codellist = self.clientr.get_stock_list().order_book_id.tolist()
        start = '2020-01-01'
        end = '2021-09-22'
        data = self.clientr.get_stock_day_qfq_adv(codellist, start, end)
        res = data.add_func(QA.QA_indicator_MA, 5)
        res.columns = ['factor']
        return res.reset_index().dropna()


feature = MA(host=clickhouse_ip, port=clickhouse_port,
             user=clickhouse_user, password=clickhouse_password)
feature.update_to_database()

"""
create feature view
"""
fv = QA.QAFeatureView(host=clickhouse_ip, port=clickhouse_port,
                      user=clickhouse_user, password=clickhouse_password)
ma5factor = fv.get_single_factor('MA5').sort_index()


"""
create analysis

"""
fa = QA.QAFeatureAnalysis(ma5factor, host=clickhouse_ip, port=clickhouse_port,
                          user=clickhouse_user, password=clickhouse_password)

fa.create_tear_sheet()
