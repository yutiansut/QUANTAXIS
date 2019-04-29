import asyncio
import random
import time

from QUANTAXIS.QAEngine.asyncschedule import create_scheduler
from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread


class QA_AsyncExec(QA_Thread):
    async def coro(self,timeout=0.01):
        z = timeout*random.randint(2, 10)
        await asyncio.sleep(z)

        self.do()

        await self.coro(timeout)


    async def main(self):
        scheduler = await create_scheduler()
        # for i in range(2):
        #     # spawn jobs
        await scheduler.spawn(self.coro(1/100))
        await asyncio.sleep(100000000.0)
        await scheduler.close()
    
    
    def do(self):
        try:
            event = self.queue.get()
            print(event)
        except:
            pass

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.main())

