"""Quick throughput benchmark: batched SPSC vs item-by-item SPSC."""
import threading
import time

from spsc_ring_buffer import SpscRingBuffer
from spsc_ring_buffer_batched import SpscRingBufferBatched

TOTAL = 50_000


def bench_single():
    buf = SpscRingBuffer(1024)
    p = threading.Thread(target=lambda: [buf.enqueue(i) for i in range(TOTAL)])
    done = threading.Event()

    def consume():
        got = 0
        while got < TOTAL:
            buf.dequeue()
            got += 1
        done.set()

    c = threading.Thread(target=consume)
    t0 = time.time()
    p.start(); c.start()
    p.join(); done.wait()
    return time.time() - t0


def bench_batched(batch=32):
    buf = SpscRingBufferBatched(1024)

    def produce():
        sent = 0
        while sent < TOTAL:
            n = min(batch, TOTAL - sent)
            buf.enqueue_batch(range(sent, sent + n))
            sent += n

    done = threading.Event()

    def consume():
        got = 0
        while got < TOTAL:
            got += len(buf.dequeue_batch(batch))
        done.set()

    p = threading.Thread(target=produce)
    c = threading.Thread(target=consume)
    t0 = time.time()
    p.start(); c.start()
    p.join(); done.wait()
    return time.time() - t0


if __name__ == "__main__":
    t1 = bench_single()
    print(f"item-by-item : {t1:.2f}s  ({TOTAL/t1:,.0f} ops/s)")
    t2 = bench_batched()
    print(f"batch of 32  : {t2:.2f}s  ({TOTAL/t2:,.0f} ops/s)")
