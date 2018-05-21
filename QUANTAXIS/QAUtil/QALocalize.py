# coding:utf-8
import os

path = os.path.expanduser('~')
qa_path = '{}{}{}'.format(path, os.sep, '.quantaxis')
setting_path = '{}{}{}'.format(qa_path, os.sep, 'setting')
cache_path = '{}{}{}'.format(qa_path, os.sep, 'cache')
download_path = '{}{}{}'.format(qa_path, os.sep, 'download')

os.makedirs(qa_path, exist_ok=True)
os.makedirs(setting_path, exist_ok=True)
os.makedirs(cache_path, exist_ok=True)
os.makedirs(download_path, exist_ok=True)
