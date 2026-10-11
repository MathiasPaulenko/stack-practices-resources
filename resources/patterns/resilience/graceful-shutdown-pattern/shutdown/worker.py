# shutdown/worker.py — Graceful shutdown for background workers
import signal
import threading
import time
import queue

class GracefulWorker:
    """Background worker that finishes current job before exiting."""

    def __init__(self, job_queue, max_workers=4):
        self._queue = job_queue
        self._max_workers = max_workers
        self._workers = []
        self._active_jobs = 0
        self._lock = threading.Lock()
        self._shutdown = threading.Event()
        self._jobs_done = threading.Event()

    def start(self):
        for i in range(self._max_workers):
            t = threading.Thread(target=self._worker_loop, args=(i,), daemon=True)
            t.start()
            self._workers.append(t)

    def _worker_loop(self, worker_id):
        while not self._shutdown.is_set():
            try:
                job = self._queue.get(timeout=1)
            except queue.Empty:
                continue

            with self._lock:
                self._active_jobs += 1

            try:
                self._process_job(job, worker_id)
            except Exception as e:
                print(f"Worker {worker_id} job failed: {e}")
            finally:
                with self._lock:
                    self._active_jobs -= 1
                    if self._shutdown.is_set() and self._active_jobs == 0:
                        self._jobs_done.set()
                self._queue.task_done()

    def _process_job(self, job, worker_id):
        print(f"Worker {worker_id} processing job {job['id']}")
        time.sleep(2)  # Simulate work
        print(f"Worker {worker_id} completed job {job['id']}")

    def shutdown(self, timeout=30):
        """Stop accepting new jobs, finish active ones."""
        print("Worker shutdown initiated...")
        self._shutdown.set()

        with self._lock:
            if self._active_jobs == 0:
                print("No active jobs, exiting immediately")
                return

        if self._jobs_done.wait(timeout=timeout):
            print("All jobs completed, exiting")
        else:
            print(f"Timeout: {self._active_jobs} jobs still active")

# Usage
job_queue = queue.Queue()
worker = GracefulWorker(job_queue, max_workers=4)
worker.start()

# Add jobs
for i in range(10):
    job_queue.put({"id": i, "data": f"job-{i}"})

# Handle shutdown
def handle_signal(signum, frame):
    worker.shutdown(timeout=30)

signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)
