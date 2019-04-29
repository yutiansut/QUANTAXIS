import asyncio
from QUANTAXIS.Exp.asyncschedule import create_scheduler
import time
import random


async def coro(timeout):
    z = timeout*random.randint(2, 10)
    await asyncio.sleep(z)
    print('wait X: {}'.format(z))

    time.sleep(timeout)
    print('do X: {}'.format(timeout))
    print('finish ', timeout)
    await coro(timeout)


async def main():
    scheduler = await create_scheduler()
    for i in range(2):
        # spawn jobs
        await scheduler.spawn(coro(i/100))
    await asyncio.sleep(100000000.0)
    await scheduler.close()


def x(): return asyncio.new_event_loop().run_until_complete(main())


import threading

threading.Thread(target=x).start()
