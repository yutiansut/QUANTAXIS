import asyncio
from QUANTAXIS.Exp.asyncschedule import create_scheduler
import time


async def coro(timeout):
    print(timeout)
    # await asyncio.sleep(timeout)
    time.sleep(timeout)
    print('finish ', timeout)


async def main():
    scheduler = await create_scheduler()
    for i in range(100):
        # spawn jobs
        await scheduler.spawn(coro(i/10))

    await asyncio.sleep(6.0)
    # not all scheduled jobs are finished at the moment

    # gracefully close spawned jobs
    await scheduler.close()

asyncio.get_event_loop().run_until_complete(main())
