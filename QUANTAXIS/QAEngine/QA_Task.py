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


import queue
import threading
import time

from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info

from QUANTAXIS.QAEngine.QAThread import QA_Thread


"""
标准的QUANTAXIS事件方法,具有QA_Thread,QA_Event等特性,以及一些日志和外部接口
"""


class QA_Task():
    def __init__(self, name='default'):
        self.Job = queue.Queue()
        self.Task = QA_Thread(self.Job)
        self.Task.setName(name)

    def query_state(self):
        self.Job.put({'func': 'QA_util_log_info(theading.enumerate())'})
        self.Job.put({'func': 'QA_util_log_info(theading.current_thread())'})

    def put(self, task):
        self.Job.put(vars(task))

    def start(self):
        self.Task.start()

    def pause(self):
        self.Task.pause()

    def resume(self):
        self.Task.resume()


if __name__ == '__main__':
    pass
