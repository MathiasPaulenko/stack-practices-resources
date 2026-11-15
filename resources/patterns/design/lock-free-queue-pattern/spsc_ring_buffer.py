"""SPSC lock-free ring buffer — corrected version (no shared counter).

Producer owns `head`, consumer owns `tail`. One slot stays empty so
'full' and 'empty' are distinguishable. In CPython the GIL makes
single-attribute reads/writes effectively atomic; in C++/Rust you
would publish the index with release ordering instead.
"""
import threading
import time
import random


class SpscRingBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0  # write index — producer only
        self.tail = 0  # read index — consumer only

    def enqueue(self, item):
        next_head = (self.head + 1) % self.capacity
        while next_head == self.tail:
            time.sleep(0)  # buffer full — yield the GIL (see backoff variant)
        self.buffer[self.head] = item
        self.head = next_head  # publish AFTER writing the data

    def dequeue(self):
        while self.tail == self.head:
            time.sleep(0)  # buffer empty — yield the GIL
        item = self.buffer[self.tail]
        self.buffer[self.tail] = None
        self.tail = (self.tail + 1) % self.capacity
        return item


def main():
    buffer = SpscRingBuffer(100)

    def producer(count):
        for i in range(count):
            buffer.enqueue(f"item-{i}")
            time.sleep(random.uniform(0, 0.001))

    def consumer(count):
        processed = 0
        for _ in range(count):
            buffer.dequeue()
            processed += 1
            if processed % 1000 == 0:
                print(f"Processed {processed} items")

    p = threading.Thread(target=producer, args=(10000,))
    c = threading.Thread(target=consumer, args=(10000,))
    start = time.time()
    p.start(); c.start()
    p.join(); c.join()
    print(f"All done in {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()
