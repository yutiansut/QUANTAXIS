# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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
import asyncio


def QA_util_sql_mongo_setting(uri='mongodb://localhost:27017/quantaxis'):
    """
    explanation:
        根据给定的uri返回一个MongoClient实例，采用@几何建议以使用加密

    params:
        * uri ->:
            meaning: mongodb连接uri
            type: str
            optional: [null]

    return:
        MongoClient

    demonstrate:
        Not described

    output:
        Not described
    """

    # 采用@几何的建议,使用uri代替ip,port的连接方式
    # 这样可以对mongodb进行加密:
    # uri=mongodb://user:passwor@ip:port
    client = pymongo.MongoClient(uri)
    return client

# async


def QA_util_sql_async_mongo_setting(uri='mongodb://localhost:27017/quantaxis'):
    """
    explanation:
        根据给定的uri返回一个异步AsyncIOMotorClient实例

    params:
        * uri ->:
            meaning: mongodb连接uri
            type: str
            optional: [null]

    return:
        AsyncIOMotorClient

    demonstrate:
        Not described

    output:
        Not described
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


ASCENDING = pymongo.ASCENDING
DESCENDING = pymongo.DESCENDING
QA_util_sql_mongo_sort_ASCENDING = pymongo.ASCENDING
QA_util_sql_mongo_sort_DESCENDING = pymongo.DESCENDING

if __name__ == '__main__':
    # test async_mongo
    client = QA_util_sql_async_mongo_setting().quantaxis.stock_day
    print(client)
