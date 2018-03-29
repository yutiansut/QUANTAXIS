#coding:utf-8

import asyncio
from collections.abc import Coroutine
import queue


class QA_Trade_Event_engine():
    def __init__(self, *args, **kwargs):
        self._queue = queue.Queue()
        self._event_loop = asyncio.get_event_loop()
        self._reg_func = {}
        self._engine_status = False



class _ContextManager(Coroutine):
    __slots__ = ('_coro', '_obj')

    def __init__(self, coro):
        self._coro = coro
        self._obj = None

    def send(self, value):
        return self._coro.send(value)

    def throw(self, typ, val=None, tb=None):
        if val is None:
            return self._coro.throw(typ)
        elif tb is None:
            return self._coro.throw(typ, val)
        else:
            return self._coro.throw(typ, val, tb)

    def close(self):
        return self._coro.close()

    @property
    def gi_frame(self):
        return self._coro.gi_frame

    @property
    def gi_running(self):
        return self._coro.gi_running

    @property
    def gi_code(self):
        return self._coro.gi_code

    def __next__(self):
        return self.send(None)

    @asyncio.coroutine
    def __iter__(self):
        resp = yield from self._coro
        return resp


    def __await__(self):
        resp = yield from self._coro
        return resp

    @asyncio.coroutine
    def __aenter__(self):
        self._obj = yield from self._coro
        return self._obj

    @asyncio.coroutine
    def __aexit__(self, exc_type, exc, tb):
        self._obj.close()
        self._obj = None


class QA_Trade_Status_Monitor():
    def __init__(self, *args, **kwargs):
        self._monitor = []
        self._0
