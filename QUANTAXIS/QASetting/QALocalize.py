# coding:utf-8
import os

"""创建本地文件夹


1. setting_path ==> 用于存放配置文件 setting.cfg
2. cache_path ==> 用于存放临时文件
3. log_path ==> 用于存放储存的log
4. download_path ==> 下载的数据/财务文件
5. strategy_path ==> 存放策略模板
6. bin_path ==> 存放一些交易的sdk/bin文件等
"""


path = os.path.expanduser('~')
qa_path = '{}{}{}'.format(path, os.sep, '.quantaxis')


def generate_path(name):
    return '{}{}{}'.format(qa_path, os.sep, name)


def make_dir(path, exist_ok=True):
    os.makedirs(path, exist_ok=exist_ok)


setting_path = generate_path('setting')
cache_path = generate_path('cache')
log_path = generate_path('log')
download_path = generate_path('downloads')
strategy_path = generate_path('strategy')
bin_path = generate_path('bin')  #给一些dll文件存储用


make_dir(qa_path, exist_ok=True)
make_dir(setting_path, exist_ok=True)
make_dir(cache_path, exist_ok=True)
make_dir(download_path, exist_ok=True)
make_dir(log_path, exist_ok=True)
make_dir(strategy_path, exist_ok=True)
make_dir(bin_path, exist_ok=True)
