from clickhouse_driver import client
from QUANTAXIS.QAFactor.feature import QASingleFactor_DailyBase
from QUANTAXIS.QAFetch.QAClickhouse import QACKClient
from QUANTAXIS.QAIndicator.indicators import QA_indicator_MA


class MA10(QASingleFactor_DailyBase):

    def finit(self):
        self.client = QACKClient()
        self.factor_name = 'MA10'

    def calc(self) -> pd.DataFrame:
        """

        the example is just a day datasource, u can use the min data to generate a day-frequence factor

        the factor should be in day frequence 
        """

        codellist = self.client.get_stock_list()
        start = '2020-01-01'
        end = '2021-05-22'
        data = self.client.get_stock_day_qfq(codellist, start, end)
        res = data.add_func(QA_indicator_MA, 10)
        res.columns = [self.factor_name]
        return res.reset_index().dropna()
