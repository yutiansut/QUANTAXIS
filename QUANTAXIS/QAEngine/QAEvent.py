# encoding: UTF-8
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


from abc import abstractmethod
"""QUANTAXIS EVENT
EVENT 是会被推送进QUEUE的任务class
通过EVENT_QUEUE.get()拿到标准的event,然后执行"""


class QA_Worker(object):
    """JOB是worker 需要接受QA_EVENT 需要完善RUN方法"""

    def __init__(self):
        self.type = None

    def __repr__(self):
        return '< QA_Worker {} >'.format(self.type)

    @abstractmethod
    def run(self, event):
        raise NotImplementedError


class QA_Event(object):
    def __init__(self, event_type=None, func=None, message=None, callback=False, *args, **kwargs):
        self.event_type = event_type
        self.func = func
        self.message = message
        self.callback = callback

        for item in kwargs.keys():
            exec('self.{}=kwargs[item]'.format(item))
