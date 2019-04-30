import asyncio
import threading
from functools import wraps

from janus import Queue as QAAsyncQueue

from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread


class QA_AsyncThread(threading.Thread):
    _loop = asyncio.new_event_loop()
    _queue: QAAsyncQueue = QAAsyncQueue(loop=_loop)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._stopped = False
        self._main_loop = self.get_event_loop

    def __repr__(self):
        return '<QA_AsyncThread: {}  id={} ident {}>'.format(
            self.name,
            id(self),
            self.ident
        )

    @property
    def queue(self):
        return self._queue.async_q

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.main())

    async def event_hadler(self, event):
        self.do(event)

    def do(self, event):
        raise NotImplementedError('QA ASYNCTHREAD 需要重载do方法')

    def put(self, event):

        event = event if isinstance(event, QA_Event) else QA_Event(
            data=event, event_type=None)
        self.queue.put_nowait(event)

    def put_nowait(self, event):
        self.put(event)

    def stop(self):
        self._stopped = True

    def set_main_event_loop(self, loop):
        self._main_loop = loop

    def get_event_loop(self):
        return self._loop

    async def main(self):
        print('start')
        async_q = self._queue.async_q
        main_loop = asyncio.get_event_loop()
        while not (self._stopped and async_q.empty()):

            try:
                event = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            else:
                asyncio.run_coroutine_threadsafe(
                    self.event_hadler(event),
                    main_loop
                )
                async_q.task_done()
            await asyncio.sleep(0.0001)
