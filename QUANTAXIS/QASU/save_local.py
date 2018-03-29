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
import os
import sys

#QUNATAXIS_DIR='{}{}{}'.format( os.path.expanduser('~'), os.sep, '.quantaxis')

path = os.path.expanduser('~')
qa_path = '{}{}{}'.format(path, os.sep, '.quantaxis')
setting_path = '{}{}{}'.format(qa_path, os.sep, '.setting')
cache_path = '{}{}{}'.format(qa_path, os.sep, '.cache')


def make_cache():
    pass


def make_dir():
    path = os.path.expanduser('~')
    qa_path = '{}{}{}'.format(path, os.sep, '.quantaxis')
    os.makedirs(qa_path, exist_ok=True)
    setting_path = '{}{}{}'.format(qa_path, os.sep, '.setting')
    cache_path = '{}{}{}'.format(qa_path, os.sep, '.cache')
    downloads_path = '{}{}{}'.format(qa_path, os.sep, 'downloads')
    os.makedirs(setting_path, exist_ok=True)
    os.makedirs(cache_path, exist_ok=True)
    os.makedirs(downloads_path, exist_ok=True)

