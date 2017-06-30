# encoding: UTF-8
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

import sys
from datetime import datetime
from threading import *

from QUANTAXIS.QAUtil import QA_util_log_info

# this is a standard module of writing signal


#coding:utf-8

class Event(object):
    '''
      事件初始化的一个方式
    '''
    def __init__(self,event_type,data=None):
        self._type = event_type
        self._data = data

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

class EventDispatcher(object):
     """
    event分发类 监听和分发event事件
    """
     def __init__(self):
         #初始化事件
         self._events = dict()

     def __del__(self):
         self._events = None

     def has_listener(self,event_type,listener):
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        else:
            return False

     def dispatch_event(self,event):
          """
        Dispatch an instance of Event class
        """
        # 分发event到所有关联的listener
          if event.type in self._events.keys():
              listeners = self._events[event.type]

              for listener in listeners:
                  listener(event)

     def add_event_listener(self,event_type,listener):
         #给某种事件类型添加listner
         if not self.has_listener(event_type,listener):
             listeners = self._events.get(event_type,[])
             listeners.append(listener)
             self._events[event_type] = listeners

     def remove_event_listener(self,event_type,listener):
         if self.has_listener(event_type,listener):
             listeners = self._events[event_type]
             if len(listeners) == 1:
                 del self._events[event_type]
             else:
                 listeners.remove(listener)
                 self._events[event_type] = listeners

class MyEvent(Event):
    ASK = "askMyEvent"
    RESPOND = "respondMyEvent"

class WhoAsk(object):
    def __init__(self,event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event_listener(
            MyEvent.RESPOND,self.on_answer_event
        )
    def ask(self):
        print("who are listener to me?")
        self.event_dispatcher.dispatch_event(MyEvent(MyEvent.ASK,self))

    def on_answer_event(self,event):
        print("receive event %s",event.data)

class WhoRespond(object):
   def __init__(self,event_dispatcher):
       self.event_dispatcher = event_dispatcher
       self.event_dispatcher.add_event_listener(MyEvent.ASK,self.on_ask_event)

   def on_ask_event(self,event):
       self.event_dispatcher.dispatch_event(MyEvent(MyEvent.RESPOND,self))


dispatcher = EventDispatcher()
who_ask = WhoAsk( dispatcher )
who_responde1 = WhoRespond(dispatcher )
who_responde2 = WhoRespond(dispatcher )

# WhoAsk ask
who_ask.ask()