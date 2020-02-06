# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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

import datetime
from subprocess import PIPE, Popen


def QA_util_web_ping(url):
    ms_list = []
    p = Popen(["ping", url],
              stdin=PIPE, stdout=PIPE, stderr=PIPE,
              shell=True)
    out = p.stdout.read()
    list_ = str(out).split('=')
    # print(list)
    for item in list_:
        if 'ms' in item:
            ms_list.append(int(item.split('ms')[0]))

    if len(ms_list) < 1:
        # Bad Request:
        ms_list.append(9999999)
    return ms_list[-1]


class QA_Util_web_pool():
    def __init__(self):
        pass

    def hot_update(self):
        pass

    def dynamic_optimics(self):
        pass

    def task_queue(self):
        pass


if __name__ == "__main__":
    print(datetime.datetime.now())
    print(QA_util_web_ping('www.baidu.com'))
    print(datetime.datetime.now())
