# coding:utf-8

import pymongo
import json
import datetime
import dateutil
import time

"""
connector 需要封装curl的内容,而且这些curl的内容需要是一致的
同时这个最好是被封装成@装饰器
"""


def save_data(database, data, *args, **kwargs):
    pass


def update_date(database, data, *args, **kwargs):
    pass


def database_config(configs, *args, **kwargs):
    pass


if __name__ == '__main__':
    @database_config
    def pymongo_connect():
        connector = {'ip': 'localhost', 'port': 7709, 'name': 'quantaxis'}
