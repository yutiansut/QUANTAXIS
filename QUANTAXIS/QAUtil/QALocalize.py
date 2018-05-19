# coding:utf-8
import os

path = os.path.expanduser('~')
qa_path = '{}{}{}'.format(path, os.sep, '.quantaxis')
setting_path = '{}{}{}'.format(qa_path, os.sep, 'setting')
cache_path = '{}{}{}'.format(qa_path, os.sep, 'cache')
download_path = '{}{}{}'.format(qa_path, os.sep, 'download')
