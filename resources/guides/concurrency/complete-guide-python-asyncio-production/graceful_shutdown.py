# graceful_shutdown.py — Production shutdown pattern: signal-driven cancellation.
import asyncio
import signal
import logging

logger = logging.getLogger(__name__)


class Application:
    """Survives SIGTERM: cancel workers, bound cleanup, exit cleanly."""

    def __init__(self, worker_count: int = 4, shutdown_timeout: float = 10.0):
        self.shutdown_event = asyncio.Event()
        self.shutdown_timeout = shutdown_timeout
        self.worker_count = worker_count
        self.tasks: list[asyncio.Task] = []

    async def start(self) -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self.shutdown_event.set)

        self.tasks = [
            asyncio.create_task(self.worker(i)) for i in range(self.worker_count)
        ]

        await self.shutdown_event.wait()

        for task in self.tasks:
            task.cancel()

        await asyncio.wait_for(
            asyncio.gather(*self.tasks, return_exceptions=True),
            timeout=self.shutdown_timeout,
        )
        logger.info("Shutdown complete")

    async def worker(self, worker_id: int) -> None:
        try:
            while not self.shutdown_event.is_set():
                job = await self.fetch_job()
                await self.process_job(job)
        except asyncio.CancelledError:
            logger.info("Worker %s shutting down", worker_id)
            await self.flush_state()
            raise

    async def fetch_job(self):
        await asyncio.sleep(0.5)
        return {"id": worker_id}

    async def process_job(self, job) -> None:
        await asyncio.sleep(0.1)

    async def flush_state(self) -> None:
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(Application().start())
