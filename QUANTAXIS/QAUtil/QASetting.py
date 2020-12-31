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

import configparser
import json
import os
from multiprocessing import Lock
from QUANTAXIS.QASetting.QALocalize import qa_path, setting_path, strategy_path
from QUANTAXIS.QAUtil.QASql import (
    QA_util_sql_async_mongo_setting,
    QA_util_sql_mongo_setting
)

# quantaxis有一个配置目录存放在 ~/.quantaxis
# 如果配置目录不存在就创建，主要配置都保存在config.json里面
# 貌似yutian已经进行了，文件的创建步骤，他还会创建一个setting的dir
# 需要与yutian讨论具体配置文件的放置位置 author:Will 2018.5.19

DEFAULT_MONGO = os.getenv('MONGODB', 'localhost')
DEFAULT_DB_URI = 'mongodb://{}:27017'.format(DEFAULT_MONGO)
CONFIGFILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'config.ini')
INFO_IP_FILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'info_ip.json')
STOCK_IP_FILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'stock_ip.json')
FUTURE_IP_FILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'future_ip.json')


class QA_Setting():

    def __init__(self, uri=None):
        self.lock = Lock()

        self.mongo_uri = uri or self.get_mongo()
        self.username = None
        self.password = None

        # 加入配置文件地址

    def get_mongo(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIGFILE_PATH):
            config.read(CONFIGFILE_PATH)

            try:
                res = config.get('MONGODB', 'uri')
            except:
                res = DEFAULT_DB_URI

        else:
            config = configparser.ConfigParser()
            config.add_section('MONGODB')
            config.set('MONGODB', 'uri', DEFAULT_DB_URI)
            f = open('{}{}{}'.format(setting_path, os.sep, 'config.ini'), 'w')
            config.write(f)
            res = DEFAULT_DB_URI

        return res

    def get_config(
            self,
            section='MONGODB',
            option='uri',
            default_value=DEFAULT_DB_URI
    ):
        """[summary]

        Keyword Arguments:
            section {str} -- [description] (default: {'MONGODB'})
            option {str} -- [description] (default: {'uri'})
            default_value {[type]} -- [description] (default: {DEFAULT_DB_URI})

        Returns:
            [type] -- [description]
        """

        try:
            config = configparser.ConfigParser()
            config.read(CONFIGFILE_PATH)
            return config.get(section, option)
        except:
            res = self.client.quantaxis.usersetting.find_one(
                {'section': section})
            if res:
                return res.get(option, default_value)
            else:
                self.set_config(section, option, default_value)
                return default_value

    def set_config(
            self,
            section='MONGODB',
            option='uri',
            default_value=DEFAULT_DB_URI
    ):
        """[summary]

        Keyword Arguments:
            section {str} -- [description] (default: {'MONGODB'})
            option {str} -- [description] (default: {'uri'})
            default_value {[type]} -- [description] (default: {DEFAULT_DB_URI})

        Returns:
            [type] -- [description]
        """
        t = {'section': section, option: default_value}
        self.client.quantaxis.usersetting.update(
            {'section': section}, {'$set': t}, upsert=True)

        # if os.path.exists(CONFIGFILE_PATH):
        #     config.read(CONFIGFILE_PATH)
        #     self.lock.release()
        #     return self.get_or_set_section(
        #         config,
        #         section,
        #         option,
        #         default_value,
        #         'set'
        #     )

        #     # 排除某些IP
        #     # self.get_or_set_section(config, 'IPLIST', 'exclude', [{'ip': '1.1.1.1', 'port': 7709}])

        # else:
        #     f = open(CONFIGFILE_PATH, 'w')
        #     config.add_section(section)
        #     config.set(section, option, default_value)

        #     config.write(f)
        #     f.close()
        #     self.lock.release()
        #     return default_value

    def get_or_set_section(
            self,
            config,
            section,
            option,
            DEFAULT_VALUE,
            method='get'
    ):
        """[summary]

        Arguments:
            config {[type]} -- [description]
            section {[type]} -- [description]
            option {[type]} -- [description]
            DEFAULT_VALUE {[type]} -- [description]

        Keyword Arguments:
            method {str} -- [description] (default: {'get'})

        Returns:
            [type] -- [description]
        """

        try:
            if isinstance(DEFAULT_VALUE, str):
                val = DEFAULT_VALUE
            else:
                val = json.dumps(DEFAULT_VALUE)
            if method == 'get':
                return self.get_config(section, option)
            else:
                self.set_config(section, option, val)
                return val

        except:
            self.set_config(section, option, val)
            return val

    def env_config(self):
        return os.environ.get("MONGOURI", None)

    @property
    def client(self):
        return QA_util_sql_mongo_setting(self.mongo_uri)

    @property
    def client_async(self):
        return QA_util_sql_async_mongo_setting(self.mongo_uri)

    def change(self, ip, port):
        self.ip = ip
        self.port = port
        global DATABASE
        DATABASE = self.client
        return self


QASETTING = QA_Setting()
DATABASE = QASETTING.client.quantaxis
DATABASE_ASYNC = QASETTING.client_async.quantaxis


def exclude_from_stock_ip_list(exclude_ip_list):
    """
    explanation:
        从stock_ip_list删除列表exclude_ip_list中的ip,从stock_ip_list删除列表future_ip_list中的ip

    params:
        * exclude_ip_list ->:
            meaning: 需要删除的ip_list
            type: list
            optional: [null]

    return:
        None

    demonstrate:
        Not described

    output:
        Not described
    """
    for exc in exclude_ip_list:
        if exc in stock_ip_list:
            stock_ip_list.remove(exc)

    # 扩展市场
    for exc in exclude_ip_list:
        if exc in future_ip_list:
            future_ip_list.remove(exc)


if os.path.exists(INFO_IP_FILE_PATH):
    with open(INFO_IP_FILE_PATH, "r") as f:
        info_ip_list = json.load(f)
else:
    info_ip_list = [
        {"ip": "101.227.73.20", "port": 7709},
        {"ip": "101.227.77.254", "port": 7709},
        {"ip": "114.80.63.12", "port": 7709},
        {"ip": "114.80.63.35", "port": 7709},
        {"ip": "115.238.56.198", "port": 7709},
        {"ip": "115.238.90.165", "port": 7709},
        {"ip": "124.160.88.183", "port": 7709},
        {"ip": "14.215.128.18", "port": 7709},
        {"ip": "180.153.18.170", "port": 7709},
        {"ip": "180.153.18.171", "port": 7709},
        {"ip": "180.153.39.51", "port": 7709},
        {"ip": "202.108.253.130", "port": 7709},
        {"ip": "202.108.253.131", "port": 7709},
        {"ip": "218.108.47.69", "port": 7709},
        {"ip": "218.108.98.244", "port": 7709},
        {"ip": "218.75.126.9", "port": 7709},
        {"ip": "221.231.141.60", "port": 7709},
        {"ip": "59.173.18.140", "port": 7709},
        {"ip": "60.12.136.250", "port": 7709},
        {"ip": "60.28.23.80", "port": 7709},
        # added 20190222 from tdx
        {"ip": "106.14.95.149", "port": 7711, "name": "上海双线资讯主站"},
        {"ip": "112.74.214.43", "port": 7711, "name": "深圳双线资讯主站1"},
        {"ip": "113.105.142.162", "port": 7711, "name": "东莞电信资讯主站"},
        {"ip": "119.97.185.10", "port": 7711, "name": "武汉电信资讯主站2"},
        {"ip": "119.97.185.6", "port": 7711, "name": "武汉电信资讯主站1"},
        {"ip": "120.24.0.77", "port": 7711, "name": "深圳双线资讯主站2"},
        {"ip": "120.79.212.229", "port": 7711, "name": "深圳双线资讯主站3"},
        {"ip": "47.107.75.159", "port": 7711, "name": "深圳双线资讯主站4"},
        {"ip": "47.92.127.181", "port": 7711, "name": "北京双线资讯主站"},

        {"ip": "113.105.142.162", "port": 7721},
        {"ip": "23.129.245.199", "port": 7721},

    ]
    with open(INFO_IP_FILE_PATH, "w") as f:
        json.dump(info_ip_list, f)

if os.path.exists(STOCK_IP_FILE_PATH):
    with open(STOCK_IP_FILE_PATH, "r") as f:
        stock_ip_list = json.load(f)
else:
    stock_ip_list = [
        # added 20190222 from tdx
        {"ip": "106.120.74.86", "port": 7711, "name": "北京行情主站1"},
        {"ip": "113.105.73.88", "port": 7709, "name": "深圳行情主站"},
        {"ip": "113.105.73.88", "port": 7711, "name": "深圳行情主站"},
        {"ip": "114.80.80.222", "port": 7711, "name": "上海行情主站"},
        {"ip": "117.184.140.156", "port": 7711, "name": "移动行情主站"},
        {"ip": "119.147.171.206", "port": 443, "name": "广州行情主站"},
        {"ip": "119.147.171.206", "port": 80, "name": "广州行情主站"},
        {"ip": "218.108.50.178", "port": 7711, "name": "杭州行情主站"},
        {"ip": "221.194.181.176", "port": 7711, "name": "北京行情主站2"},
        # origin
        {"ip": "106.120.74.86", "port": 7709},  # 北京
        {"ip": "112.95.140.74", "port": 7709},
        {"ip": "112.95.140.92", "port": 7709},
        {"ip": "112.95.140.93", "port": 7709},
        {"ip": "113.05.73.88", "port": 7709},  # 深圳
        {"ip": "114.67.61.70", "port": 7709},
        {"ip": "114.80.149.19", "port": 7709},
        {"ip": "114.80.149.22", "port": 7709},
        {"ip": "114.80.149.84", "port": 7709},
        {"ip": "114.80.80.222", "port": 7709},  # 上海
        {"ip": "115.238.56.198", "port": 7709},
        {"ip": "115.238.90.165", "port": 7709},
        {"ip": "117.184.140.156", "port": 7709},  # 移动
        {"ip": "119.147.164.60", "port": 7709},  # 广州
        {"ip": "119.147.171.206", "port": 7709},  # 广州
        {"ip": "119.29.51.30", "port": 7709},
        {"ip": "121.14.104.70", "port": 7709},
        {"ip": "121.14.104.72", "port": 7709},
        {"ip": "121.14.110.194", "port": 7709},  # 深圳
        {"ip": "121.14.2.7", "port": 7709},
        {"ip": "123.125.108.23", "port": 7709},
        {"ip": "123.125.108.24", "port": 7709},
        {"ip": "124.160.88.183", "port": 7709},
        {"ip": "180.153.18.17", "port": 7709},
        {"ip": "180.153.18.170", "port": 7709},
        {"ip": "180.153.18.171", "port": 7709},
        {"ip": "180.153.39.51", "port": 7709},
        {"ip": "218.108.47.69", "port": 7709},
        {"ip": "218.108.50.178", "port": 7709},  # 杭州
        {"ip": "218.108.98.244", "port": 7709},
        {"ip": "218.75.126.9", "port": 7709},
        {"ip": "218.9.148.108", "port": 7709},
        {"ip": "221.194.181.176", "port": 7709},  # 北京
        {"ip": "59.173.18.69", "port": 7709},
        {"ip": "60.12.136.250", "port": 7709},
        {"ip": "60.191.117.167", "port": 7709},
        {"ip": "60.28.29.69", "port": 7709},
        {"ip": "61.135.142.73", "port": 7709},
        {"ip": "61.135.142.88", "port": 7709},  # 北京
        {"ip": "61.152.107.168", "port": 7721},
        {"ip": "61.152.249.56", "port": 7709},  # 上海
        {"ip": "61.153.144.179", "port": 7709},
        {"ip": "61.153.209.138", "port": 7709},
        {"ip": "61.153.209.139", "port": 7709},
        {"ip": "hq.cjis.cn", "port": 7709},
        {"ip": "hq1.daton.com.cn", "port": 7709},
        {"ip": "jstdx.gtjas.com", "port": 7709},
        {"ip": "shtdx.gtjas.com", "port": 7709},
        {"ip": "sztdx.gtjas.com", "port": 7709},

        {"ip": "113.105.142.162", "port": 7721},
        {"ip": "23.129.245.199", "port": 7721},
    ]
    with open(STOCK_IP_FILE_PATH, "w") as f:
        json.dump(stock_ip_list, f)

if os.path.exists(FUTURE_IP_FILE_PATH):
    with open(FUTURE_IP_FILE_PATH, "r") as f:
        future_ip_list = json.load(f)
else:
    future_ip_list = [
        # origin
        {"ip": "106.14.95.149", "port": 7727, "name": "扩展市场上海双线"},
        {"ip": "112.74.214.43", "port": 7727, "name": "扩展市场深圳双线1"},
        #{"ip": "113.105.142.136", "port": 443, "name": "扩展市场东莞主站"},
        {"ip": "119.147.86.171", "port": 7727, "name": "扩展市场深圳主站"},
        {"ip": "119.97.185.5", "port": 7727, "name": "扩展市场武汉主站1"},
        {"ip": "120.24.0.77", "port": 7727, "name": "扩展市场深圳双线2"},
        {"ip": "124.74.236.94", "port": 7721},
        {"ip": "14.215.128.18", "port": 7721, "name": "华泰证券深圳电信"},
        {"ip": "139.219.103.190", "port": 7721, "name": "华泰证券云行情"},
        {"ip": "202.103.36.71", "port": 443, "name": "扩展市场武汉主站2"},
        {"ip": "47.92.127.181", "port": 7727, "name": "扩展市场北京主站"},
        {"ip": "59.175.238.38", "port": 7727, "name": "扩展市场武汉主站3"},
        {"ip": "61.152.107.141", "port": 7727, "name": "扩展市场上海主站1"},
        {"ip": "61.152.107.171", "port": 7727, "name": "扩展市场上海主站2"},
        # {"ip": "124.74.236.94","port": 7721},
        # {"ip": "218.80.248.229", "port": 7721},
        # {"ip": "58.246.109.27", "port": 7721},
        # added 20190222 from tdx
        {"ip": "119.147.86.171", "port": 7721, "name": "扩展市场深圳主站"},
        {"ip": "47.107.75.159", "port": 7727, "name": "扩展市场深圳双线3"},


    ]
    with open(FUTURE_IP_FILE_PATH, "w") as f:
        json.dump(future_ip_list, f)

"""
["121.14.110.210", "119.147.212.76", "113.105.73.86", "119.147.171.211", "119.147.164.57", "119.147.164.58", "61.49.50.180", "61.49.50.181",
"61.135.142.85", "61.135.149.181", "114.80.80.210", "222.73.49.15", "221.194.181.176"]
"""
