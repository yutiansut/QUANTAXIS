from curio import UniversalQueue, run, sleep, spawn
from threading import Thread


def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print('Got:', item)


async def producer(n, m, queue):
    for x in range(n):
        await queue.put(x)
        await sleep(m)
    await queue.put(None)


async def main():
    q = UniversalQueue()
    Thread(target=consumer, args=(q,)).start()
    t = await spawn(producer, 100, 1, q)
    t1 = await spawn(producer, 100, 0.2, q)
    t2 = await spawn(producer, 100, 0.5, q)
    await t.join()
    await t1.join()
    await t2.join()
run(main)
