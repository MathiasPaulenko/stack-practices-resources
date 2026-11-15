"""Batched SPSC ring buffer — publish a local batch with one head update.

Still lock-free: nothing shared is mutated by more than one thread.
Unbounded indices (wrap with % capacity) let you use every slot.
"""
import threading
import time


class SpscRingBufferBatched:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0  # unbounded — wrap with % capacity
        self.tail = 0

    def enqueue_batch(self, items):
        n = len(items)
        while self.head - self.tail + n > self.capacity:
            time.sleep(0)  # wait for room — yield the GIL
        for i, item in enumerate(items):
            self.buffer[(self.head + i) % self.capacity] = item
        self.head += n  # single publish for the whole batch

    def dequeue_batch(self, max_items):
        n = min(self.head - self.tail, max_items)
        items = [self.buffer[(self.tail + i) % self.capacity]
                 for i in range(n)]
        self.tail += n
        return items


def main():
    buf = SpscRingBufferBatched(256)
    TOTAL, BATCH = 10000, 32

    def producer():
        sent = 0
        while sent < TOTAL:
            batch = list(range(sent, min(sent + BATCH, TOTAL)))
            buf.enqueue_batch(batch)
            sent += len(batch)

    def consumer():
        got = 0
        while got < TOTAL:
            got += len(buf.dequeue_batch(BATCH))

    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    start = time.time()
    p.start(); c.start()
    p.join(); c.join()
    print(f"{TOTAL} items in batches of {BATCH}: {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()
