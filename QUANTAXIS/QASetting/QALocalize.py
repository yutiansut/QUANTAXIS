# coding:utf-8
import os

path = os.path.expanduser('~')
qa_path = '{}{}{}'.format(path, os.sep, '.quantaxis')
setting_path = '{}{}{}'.format(qa_path, os.sep, 'setting')
cache_path = '{}{}{}'.format(qa_path, os.sep, 'cache')
log_path = '{}{}{}'.format(qa_path, os.sep, 'log')
download_path = '{}{}{}'.format(qa_path, os.sep, 'downloads')

os.makedirs(qa_path, exist_ok=True)
os.makedirs(setting_path, exist_ok=True)
os.makedirs(cache_path, exist_ok=True)
os.makedirs(download_path, exist_ok=True)
os.makedirs(log_path, exist_ok=True)