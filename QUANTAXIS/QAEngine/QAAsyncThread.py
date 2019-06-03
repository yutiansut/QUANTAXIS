import asyncio
import threading
from functools import wraps

from janus import Queue as QA_AsyncQueue

from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAUtil import QA_util_log_info, QA_util_random_with_topic, RUNNING_STATUS


class QA_AsyncThread(threading.Thread):
    _loop = asyncio.new_event_loop()
    _queue: QA_AsyncQueue = QA_AsyncQueue(loop=_loop)

    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._stopped = False
        self._main_loop = self.get_event_loop
        self.name = QA_util_random_with_topic(
            topic='QA_AsyncThread',
            lens=3
        ) if name is None else name
        self._status = RUNNING_STATUS.PENDING

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
        try:
            asyncio.new_event_loop().run_until_complete(self.main())
            self._status = RUNNING_STATUS.RUNNING
        except Exception as e:
            print('QAASYNCTHREAD ERROR: {}'.format(e))
            self._status = RUNNING_STATUS.STOPED
            raise Exception

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
