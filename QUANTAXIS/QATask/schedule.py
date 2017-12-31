# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
import os
import sched
import time
from threading import Timer

from QUANTAXIS.QATask.QA_Queue_standard import QA_Queue
from QUANTAXIS.QAUtil import (QA_util_log_debug, QA_util_log_expection,
                              QA_util_log_info)

schedule = sched.scheduler(time.time, time.sleep)


# 被周期性调度触发的函数
def __execute_command(cmd, inc):
    '终端上显示当前计算机的连接情况 '
    os.system(cmd)
    schedule.enter(inc, 0, __execute_command, (cmd, inc))


def QA_schedule(cmd, inc=60):
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, __execute_command, (cmd, inc))
    schedule.run()


# 每60秒查看下网络连接情况
if __name__ == '__main__':
    QA_schedule("netstat -an", 60)
