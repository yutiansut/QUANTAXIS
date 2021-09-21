import datetime

import clickhouse_driver
import pandas as pd
from qaenv import (clickhouse_ip, clickhouse_password, clickhouse_port,
                   clickhouse_user)


class QASingleFactor_DailyBase():
    def __init__(self, factor_name="QAF_test", host=clickhouse_ip, port=clickhouse_port, user=clickhouse_user, password=clickhouse_password,):
        self.client = clickhouse_driver.Client(host=host, port=port, user=user, password=password,
                                               database='factor')

        self.client.execute("CREATE TABLE IF NOT EXISTS \
                `factor`.`factormetadata` (　\
                factorname String, \
                create_date Date, \
                update_date Date, \
                version Float32, \
                description String DEFAULT 'None')\
            ENGINE=ReplacingMergeTree()\
            ORDER BY (factorname)\
            SETTINGS index_granularity=8192 ")
        self.factor_name = factor_name

        self.description = 'None'
        self.finit()
        if not self.check_if_exist():
            print('start register')
            self.register()
            self.init_database()

    def finit(self):

        pass

    def __str__(self):
        return "QAFACTOR {}".format(self.factor_name)

    def __repr__(self):
        return self.__str__()

    @property
    def tablelist(self):
        return self.client.query_dataframe('show tables').name.tolist()

    def check_if_exist(self):
        print(self.tablelist)
        return self.factor_name in self.tablelist

    def init_database(self):
        self.client.execute('CREATE TABLE IF NOT EXISTS \
                            `factor`.`{}` (\
                            date Date,\
                            code String,\
                            factor Float32\
                            )\
                            ENGINE = ReplacingMergeTree() \
                            ORDER BY (date, code)\
                            SETTINGS index_granularity=8192'.format(self.factor_name))

    def register(self):
        self.client.execute("INSERT INTO factormetadata VALUES", [{
            'factorname': self.factor_name,
            'create_date': datetime.date.today(),
            'update_date': datetime.date.today(),
            'version': 1.0,
            'description': self.description
        }])
        self.client.execute('OPTIMIZE TABLE factormetadata FINAL')

    def insert_data(self, data: pd.DataFrame):

        # check the data
        data = data.assign(date=pd.to_datetime(data.date),
                           factor=data.factor.apply(float))
        columns = data.columns
        if 'date' not in columns or 'factor' not in columns:
            raise Exception('columns not exists')

        data = data.to_dict('records')


        self.client.execute('INSERT INTO {} VALUES'.format(
            self.factor_name), data)

        self.client.execute('OPTIMIZE TABLE {} FINAL'.format(self.factor_name))

    def update_to_database(self):
        self.insert_data(self.calc())
        self.update_metadb()

    def update_metadb(self):
        raw_reg_message = self.client.execute(
            "select create_date from factormetadata where factorname=='{}'".format(self.factor_name))[0][0]
        self.client.execute("INSERT INTO factormetadata VALUES", [{
            'factorname': self.factor_name,
            'create_date': raw_reg_message,
            'update_date': datetime.date.today(),
            'version': 1.0,
            'description': self.description
        }])

    def calc(self) -> pd.DataFrame:
        """

        the resulf of this function should be a dataframe with the folling columns


        ['date', 'code', 'factor']

        """
        raise NotImplementedError

    def fetch_data(self, start=None, end=None) -> pd.DataFrame:
        if start is None and end is None:
            res = self.client.query_dataframe(
                'SELECT * FROM {}'.format(self.factor_name))
            if res is not None:
                res.columns = ['date', 'code', self.factor_name]
                return res.set_index(['date', 'code']).sort_index()
            else:
                return pd.DataFrame([], columns=['date', 'code', self.factor_name])
