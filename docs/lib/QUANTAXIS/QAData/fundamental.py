import tushare as ts
from logbook import Logger
from functools import wraps
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.sql import (
    func
)
from sqlalchemy.orm import (
    sessionmaker,
    Query,
)
from toolz import first
from schema import (
    full,
    fundamental,
    Base
)
import pandas as pd
import click

logger = Logger("fundamental")

engine = create_engine("sqlite:///fundamental.sqlite")

def retry(times=3):
    def wrapper(func):
        @wraps(func)
        def fun(*args, **kwargs):
            count = 0
            while count < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    count = count + 1

            logger.error("connection failed after retried 3 times. {} {}".format(args, kwargs))
            raise Exception("connection failed after retried 3 times. {} {}".format(args, kwargs))

        return fun

    return wrapper


@retry()
def call_func(name, i, j):
    return eval("ts.get_{}_data({}, {}).drop_duplicates('code').set_index(['code','name'])".format(name, i, j))


def query(*args):
    engine = create_engine("sqlite:///fundamental.sqlite")
    Session = sessionmaker(bind=engine)
    session = Session()
    args = [fundamental.code, fundamental.report_date, fundamental.roe,
            func.max(fundamental.report_date).label('report_date')]
    return Query(args).with_session(session).filter(
        fundamental.report_date < pd.to_datetime('2013-07-18')
    ).group_by(fundamental.code)


def query1(*args):
    engine = create_engine("sqlite:///fundamental.sqlite")
    Session = sessionmaker(bind=engine)
    session = Session()
    args = [full.code, full.report_date, full.roe]
    return Query(args).with_session(session).filter(
        full.trade_date == pd.to_datetime('2013-07-18')
    )


def sql_query():
    data = query(fundamental.code, fundamental.report_date, fundamental.roe,
                 fundamental.quarter).filter(
        fundamental.roe > 10
    ).all()

    df = pd.DataFrame(data)

    print(df)

    data = query1().filter(
        full.roe > 10
    ).all()

    df = pd.DataFrame(data)

    print(df)


class FundamentalReader(object):

    def __init__(self, engine):
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)()

    def query(self, dt, *args, **kwargs):
        args = list(args) + [fundamental.code, func.max(fundamental.report_date).label('report_date')]
        return Query(args).with_session(self.session).filter(
            fundamental.report_date < dt
        )

    def get_fundamental(self, query):
        return pd.DataFrame(query.group_by(fundamental.code).all())


class FundamentalWriter(object):
    table_names = ['fundamental', 'full']

    def __init__(self, engine):
        self.engine = engine

    def write(self, start, end):
        self.init_db(self.engine)

        end = min(int(pd.to_datetime('today', utc=True).strftime('%Y')), end) + 1

        pp = [(i, j) for i in range(start, end) for j in range(1, 5)]

        for i in pp:
            self.quarter_report(*i)
            print(i)

    def fill(self):
        self.init_db(self.engine)
        df = pd.read_sql("select * from fundamental", self.engine).sort_values(['report_date', 'quarter'])
        df['trade_date'] = df['report_date'] = pd.to_datetime(df['report_date'])

        with click.progressbar(df.groupby('code'),
                               label='writing data',
                               item_show_func=lambda x: x[0] if x else None) as bar:
            bar.is_hidden = False
            for stock, group in bar:
                group = group.drop_duplicates(subset='trade_date', keep="last").set_index('trade_date')
                sessions = pd.date_range(group.index[0], group.index[-1])
                d = group.reindex(sessions, copy=False).fillna(method='pad')
                d.to_sql('full', self.engine, if_exists='append', index_label='trade_date')

    def all_tables_presents(self, txn):
        conn = txn.connect()
        for table_name in self.table_names:
            if not txn.dialect.has_table(conn, table_name):
                return False

        return True

    def init_db(self, txn):
        if not self.all_tables_presents(txn):
            Base.metadata.create_all(txn.connect(), checkfirst=True)

    def quarter_report(self, year, quarter):
        func_names = ["report", "profit", "operation", "growth", "debtpaying", "cashflow"]
        dfs = [call_func(name, year, quarter) for name in func_names]

        df = pd.concat(dfs, axis=1).dropna(axis=0, subset=['report_date'])  # drop if no report_date
        df['report_date'] = pd.to_datetime(
            str(year) + '-' + df['report_date'].apply(lambda x: x if x != '02-29' else '02-28'))
        df['quarter'] = quarter
        df.to_sql('fundamental', self.engine, if_exists='append')


@click.command()
@click.option(
    '-s',
    '--start',
    default=2010,
    show_default=True,
    help='start year',
)
@click.option(
    '-e',
    '--end',
    default=2017,
    show_default=True,
    help='end year',
)
def main(start, end):
    writer = FundamentalWriter(engine)
    writer.write(start, end)


if __name__ == '__main__':
    main()
