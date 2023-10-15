### qifi sql

import clickhouse_driver
class test:
    def __init__(self):
        self.client = clickhouse_driver.Client(host='192.168.2.121', database='test',
                                                   settings={
                                                       'insert_block_size': 100000000},
                                                   compression=True)
    def execute(self, sql):
        return self.client.query_dataframe(sql)
    def get_orders(self,user_id):
        res=self.execute("select * from test.orders where `user_id`='{}'".format(user_id))
        return res