import asyncio
from QUANTAXIS.Exp.asyncschedule import create_scheduler
import time
import random
from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread


class X(QA_Thread):
    async def coro(self,timeout):
        z = timeout*random.randint(2, 10)
        await asyncio.sleep(z)
        print('wait X: {}'.format(z))

        self.do()
        print('do X: {}'.format(timeout))
        print('finish ', timeout)
        await self.coro(timeout)


    async def main(self):
        scheduler = await create_scheduler()
        for i in range(2):
            # spawn jobs
            await scheduler.spawn(self.coro(i/100))
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

x =X()
x.start()
for item in range(100):
    x.put_nowait(item)
    time.sleep(random.random())