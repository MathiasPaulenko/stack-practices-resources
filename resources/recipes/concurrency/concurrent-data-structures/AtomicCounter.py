import threading


class AtomicCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1
            return self._value

    def value(self):
        with self._lock:
            return self._value


def worker(counter):
    for _ in range(100_000):
        counter.increment()


if __name__ == "__main__":
    counter = AtomicCounter()
    threads = [threading.Thread(target=worker, args=(counter,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(counter.value())
