import asyncio
import random
import time
import sys
import threading
from QUANTAXIS.QAEngine.asyncschedule import create_scheduler
from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAEngine.QAAsyncThread import QA_AsyncThread, QAAsyncEMS

import asyncio
import janus



class QA_AsyncExec1(QA_Thread):
    # sys.setrecursionlimit(10000)
    async def coro(self, timeout=0.01):
        z = timeout*random.randint(2, 10)
        await asyncio.sleep(z)
        self.do()
        await self.coro(timeout)

    async def main(self):
        scheduler = await create_scheduler()
        await scheduler.spawn(self.coro(0.001))

        await asyncio.sleep(60*60*24)
        await scheduler.close()

    def do(self):
        try:
            event = self.queue.get()
            print(event)
        except:
            pass

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.main())


class QA_AsyncExec(threading.Thread):
    asyncEMS= QAAsyncEMS()
    asyncThread = QA_AsyncThread(asyncEMS)
    

    @asyncEMS.register(QA_Event)
    async def event_hadler(self, event):
        self.do(event)

    def put(self, event):

        event = event if isinstance(event, QA_Event) else QA_Event(data=event, event_type=None)

        future = asyncio.run_coroutine_threadsafe(
            self.asyncThread.queue.put(event),
            asyncio.get_event_loop()
        )
        future.result()  # wait for the event to be saved in the queue

    def put_nowait(self, event):

        event = event if isinstance(event, QA_Event) else QA_Event(data=event, event_type=None)

        future = asyncio.run_coroutine_threadsafe(
            self.asyncThread.queue.put_nowait(event),
            worker.get_event_loop()
        )
        future.result()  # wait for the event to be saved in the queue

    async def main(self):
        self.asyncThread.set_main_event_loop(asyncio.get_event_loop())
        #threading.Thread(target=self.asyncThread.start).start()
        self.asyncThread.start()
        await asyncio.sleep(60*60*24)

        self.asyncThread.stop()
        self.asyncThread.join()

    def do(self, event):
        try:
            print(event)
        except:
            pass

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.main())
