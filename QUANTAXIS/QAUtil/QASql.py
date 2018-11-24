# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from motor import MotorClient
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from sqlalchemy import create_engine
import asyncio


def QA_util_sql_mongo_setting(uri='mongodb://localhost:27017/quantaxis'):
    # 采用@几何的建议,使用uri代替ip,port的连接方式
    # 这样可以对mongodb进行加密:
    # uri=mongodb://user:passwor@ip:port
    client = pymongo.MongoClient(uri)
    return client

# async


def QA_util_sql_async_mongo_setting(uri='mongodb://localhost:27017/quantaxis'):
    """异步mongo示例

    Keyword Arguments:
        uri {str} -- [description] (default: {'mongodb://localhost:27017/quantaxis'})

    Returns:
        [type] -- [description]
    """
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # async def client():
    return AsyncIOMotorClient(uri, io_loop=loop)
    # yield  client()


try:
    import pymssql
    from influxdb import InfluxDBClient
except:
    pass


def get_connect():
    conn = create_engine(
        'mysql+mysqlconnector://root:123456@localhost:3306/quantaxis', echo=False)
    # engine 是 from sqlalchemy import create_engine
    connection = conn.raw_connection()
    cursor = connection.cursor()
    # null value become ''
    return cursor


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def QA_util_sql_store_mysql(data, table_name, host="localhost", user="root", passwd="123456", db="quantaxis", if_exists="fail"):
    engine = create_engine(
        'mssql+pyodbc://sa:123456@localhost:1433/quantaxis?driver=SQL+Server')

    columns = list(data.columns)
    for i in range(len(columns)):
        if columns[i].isdigit():
            columns[i] = "column_%s" % (columns[i]).strip(" ")
        else:
            columns[i] = columns[i].strip(" ")
    columns = ",".join(columns).replace(
        '-', '_').replace('/', '_').replace(';', '')
    data.columns = columns.split(",")
    columns = "["+"],[".join(data.columns)+"]"
    try:
        data[:0].to_sql(table_name, engine,
                        if_exists=if_exists, index_label=False)
    except Exception as e:
        print("Table '%s' already exists." % (table_name))

    #sql_start = "insert into {} ({}) values(%s,%s,%s)".format(table_name, columns)
    sql_end = '%s,'*(data.shape[1]-1)+"%s"
    sql = "insert into {} ({}) values({})".format(table_name, columns, sql_end)

    conn = pymssql.connect(user="sa", password="123456",
                           host="localhost", database="quantaxis", charset="utf8")
    cursor = conn.cursor()

    if data.shape[1] > 30:
        break_num = 100000
    else:
        break_num = 1000000
    try:
        for i in chunks([tuple(x) for x in data.values], break_num):
            cursor.executemany(sql, i)
    except Exception as e:
        conn.rollback()
        print("执行MySQL: %s 时出错：%s" % (sql, e))
    finally:
        cursor.close()
        conn.commit()
        conn.close()
    print("{} has been stored into Table {} Mysql DataBase ".format(
        table_name, table_name))


ASCENDING = pymongo.ASCENDING
DESCENDING = pymongo.DESCENDING
QA_util_sql_mongo_sort_ASCENDING = pymongo.ASCENDING
QA_util_sql_mongo_sort_DESCENDING = pymongo.DESCENDING

if __name__ == '__main__':
    # test async_mongo
    client = QA_util_sql_async_mongo_setting().quantaxis.stock_day
    print(client)
