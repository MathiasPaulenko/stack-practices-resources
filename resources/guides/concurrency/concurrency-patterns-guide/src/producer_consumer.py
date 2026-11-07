"""Producer-consumer with a bounded asyncio.Queue.

Producers enqueue work; consumers drain at their own pace. The bounded
queue provides backpressure: when it is full, producers wait instead of
buffering unbounded work in memory. Shutdown uses one sentinel per
consumer, pushed only after every producer has finished.

Run: python producer_consumer.py
"""

import asyncio


async def producer(queue: asyncio.Queue, items: list[int], name: str) -> None:
    for item in items:
        await queue.put(item)  # blocks when the queue is full — backpressure
        print(f"[{name}] queued {item} (queue size: {queue.qsize()})")


async def consumer(queue: asyncio.Queue, worker_id: int) -> None:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"  worker {worker_id} processing {item}")
        await asyncio.sleep(0.05)  # simulate work
        queue.task_done()


async def main() -> None:
    queue: asyncio.Queue = asyncio.Queue(maxsize=5)

    producers = [
        asyncio.create_task(producer(queue, range(10), "producer-A")),
        asyncio.create_task(producer(queue, range(100, 110), "producer-B")),
    ]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(3)]

    await asyncio.gather(*producers)
    for _ in consumers:
        await queue.put(None)  # one sentinel per consumer
    await asyncio.gather(*consumers)
    print("all work drained")


if __name__ == "__main__":
    asyncio.run(main())
