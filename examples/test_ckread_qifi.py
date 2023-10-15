# qifi sql

from typing import List
import clickhouse_driver


class test:
    def __init__(self, username, trading_day):
        self.client = clickhouse_driver.Client(database='qifi', host='localhost', port=9000, user='default',
                                               settings={
                                                   'insert_block_size': 100000000},
                                               compression=True)
        self.qifi_id = self.get_qifiid(username, trading_day)

    def execute(self, sql):
        return self.client.query_dataframe(sql).to_dict(orient='records')

    def get_qifiid(self, username, trading_day):
        return self.client.execute(
            "select qifi_id from qifi.qifi where account_cookie ='{}' and trading_day ='{}'".format(username, trading_day))[0][0]

    def get_orders(self) -> List:
        res = self.execute(
            "select * from qifi.orders where qifi_id='{}'".format(self.qifi_id))
        return res

    def get_trades(self) -> List:
        res = self.execute(
            "select * from qifi.trades where qifi_id='{}'".format(self.qifi_id))
        return res

    def get_positions(self) -> List:
        res = self.execute(
            "select * from qifi.positions where qifi_id='{}'".format(self.qifi_id))
        return res

    def get_accounts(self) -> List:
        res = self.execute(
            "select * from qifi.accounts where qifi_id='{}'".format(self.qifi_id))
        return res

    def get_qifi(self) -> List:
        res = self.execute(
            "select * from qifi.qifi where qifi_id='{}'".format(self.qifi_id))
        return res


if __name__ == "__main__":
    t = test('testx', '2021-09-30')

    print(t.qifi_id)

    print(t.get_accounts())
    print(t.get_orders())
    print(t.get_positions())
    print(t.get_trades())
