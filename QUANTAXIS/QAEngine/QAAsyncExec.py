import asyncio
import random
import time
import sys
import threading
from QUANTAXIS.QAEngine.QAAsyncSchedule import create_QAAsyncScheduler
from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread
from QUANTAXIS.QAEngine.QAEvent import QA_Event
import asyncio
import janus


class QA_AsyncExec(QA_Thread):
    sys.setrecursionlimit(10000)
    async def coro(self, timeout=0.01):
        z = timeout*random.randint(2, 10)
        await asyncio.sleep(z)
        self.do()
        await self.coro(timeout)

    async def main(self):
        scheduler = await create_QAAsyncScheduler()
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
