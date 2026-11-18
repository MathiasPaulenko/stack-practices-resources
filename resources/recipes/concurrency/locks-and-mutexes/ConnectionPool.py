from threading import Semaphore, Thread
import time


class ConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = Semaphore(max_connections)
        self.connections = [f"conn-{i}" for i in range(max_connections)]

    def acquire(self):
        self.semaphore.acquire()
        return self.connections.pop()

    def release(self, conn):
        self.connections.append(conn)
        self.semaphore.release()


pool = ConnectionPool(3)


def worker(worker_id):
    conn = pool.acquire()
    print(f"Worker {worker_id} using {conn}")
    time.sleep(1)
    pool.release(conn)
    print(f"Worker {worker_id} released {conn}")


threads = [Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
