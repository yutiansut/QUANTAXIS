# coding :utf-8
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


"""
需要一个可以被修改和继承的基类

2017/8/12

"""
from abc import ABC, abstractmethod

from QUANTAXIS.QAEngine.QAEvent import QA_Event, QA_Job
from QUANTAXIS.QAUtil.QAParameter import BROKER_EVENT, EVENT_TYPE


class QA_Broker(QA_Job):
    """MARKET ENGINGE ABSTRACT

    receive_order => warp => get_data => engine
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.type = EVENT_TYPE.BROKER_EVENT
        self.name = None

    def __repr__(self):
        return '< QA_MARKET >'

    @abstractmethod
    def receive_order(self, event):
        raise NotImplementedError

    def get_data(self, order):
        pass

    def warp(self, order):
        pass

    


class QA_BROKER_EVENT(QA_Event):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.event_type = None
