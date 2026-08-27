from queue import Queue
from threading import Thread


class TaskQueue:
    def __init__(self, maxsize=100):
        self.queue = Queue(maxsize=maxsize)

    def submit(self, task):
        self.queue.put(task)  # blocks if full

    def process(self, task):
        print(f"Processing {task}")

    def producer(self):
        for i in range(1000):
            self.submit(i)
        for _ in range(4):
            self.queue.put(None)  # sentinel to stop each worker

    def worker(self):
        while True:
            task = self.queue.get()  # blocks if empty
            if task is None:
                self.queue.task_done()
                break
            self.process(task)
            self.queue.task_done()

    def start(self):
        workers = [Thread(target=self.worker) for _ in range(4)]
        for w in workers:
            w.start()
        producer = Thread(target=self.producer)
        producer.start()
        producer.join()
        self.queue.join()


if __name__ == "__main__":
    TaskQueue().start()
