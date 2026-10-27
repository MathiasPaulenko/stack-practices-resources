"""Async task cancellation demo for Python (asyncio).

Shows cooperative cancellation with asyncio.CancelledError, a timeout via
asyncio.wait_for, and graceful shutdown of worker tasks on SIGINT/SIGTERM.

Run: python python_cancel.py
Stop: press Ctrl+C before the 2-second auto-cancel to see the signal path.
"""

import asyncio
import signal


async def long_running_task(task_id: str) -> None:
    try:
        for i in range(1000):
            # Cancellation is delivered at the next await point
            await asyncio.sleep(0.1)
            print(f"Task {task_id}: processing item {i}")
    except asyncio.CancelledError:
        print(f"Task {task_id}: cancelled, cleaning up...")
        await cleanup_resources(task_id)
        raise  # re-raise so the caller sees the cancellation


async def cleanup_resources(task_id: str) -> None:
    print(f"Task {task_id}: closing connections...")
    await asyncio.sleep(0.05)
    print(f"Task {task_id}: cleanup complete")


async def fetch_data(url: str) -> bytes:
    from urllib.parse import urlparse

    host = urlparse(url).hostname or url
    reader, writer = await asyncio.open_connection(host, 80)
    try:
        writer.write(f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
        await writer.drain()
        return await reader.read(4096)
    finally:
        writer.close()
        await writer.wait_closed()


async def fetch_with_timeout(url: str, timeout: float = 5.0):
    try:
        return await asyncio.wait_for(fetch_data(url), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"Request to {url} timed out after {timeout}s")
        return None


class GracefulShutdown:
    def __init__(self) -> None:
        self.shutdown_event = asyncio.Event()
        self.tasks: set[asyncio.Task] = set()

    def setup_signal_handlers(self) -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self._signal_handler)

    def _signal_handler(self) -> None:
        print("\nShutdown signal received, cancelling tasks...")
        self.shutdown_event.set()

    async def run_with_shutdown(self, worker_func, num_workers: int = 4) -> None:
        self.setup_signal_handlers()
        for i in range(num_workers):
            task = asyncio.create_task(worker_func(i, self.shutdown_event))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

        await self.shutdown_event.wait()

        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        print("All tasks shut down gracefully")


async def worker(worker_id: int, shutdown: asyncio.Event) -> None:
    try:
        while not shutdown.is_set():
            print(f"Worker {worker_id}: processing...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f"Worker {worker_id}: cleaning up...")
        await asyncio.sleep(0.1)
        print(f"Worker {worker_id}: done")
        raise


async def main() -> None:
    task = asyncio.create_task(long_running_task("worker-1"))
    await asyncio.sleep(2)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled successfully")


if __name__ == "__main__":
    asyncio.run(main())
