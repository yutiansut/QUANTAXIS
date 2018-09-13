# coding:utf-8
import os

"""创建本地文件夹
"""


path = os.path.expanduser('~')
qa_path = '{}{}{}'.format(path, os.sep, '.quantaxis')


def generate_path(name):
    return '{}{}{}'.format(qa_path, os.sep, name)


def make_dir(path,exist_ok=True):
    os.makedirs(path, exist_ok=exist_ok)


setting_path = generate_path('setting')
cache_path = generate_path('cache')
log_path = generate_path('log')
download_path = generate_path('downloads')
strategy_path = generate_path('strategy')

make_dir(qa_path, exist_ok=True)
make_dir(setting_path, exist_ok=True)
make_dir(cache_path, exist_ok=True)
make_dir(download_path, exist_ok=True)
make_dir(log_path, exist_ok=True)
make_dir(strategy_path, exist_ok=True)
