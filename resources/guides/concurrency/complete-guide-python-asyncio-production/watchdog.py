# watchdog.py — Detects when the event loop stops making progress.
import asyncio
import threading
import time
import logging

logger = logging.getLogger(__name__)


def start_watchdog(threshold: float = 0.5) -> threading.Thread:
    """Warn whenever the event loop is silent longer than `threshold` seconds."""
    last_tick = time.monotonic()

    def ticker() -> None:
        nonlocal last_tick
        last_tick = time.monotonic()

    loop = asyncio.get_running_loop()
    loop.call_soon(ticker)

    def checker() -> None:
        nonlocal last_tick
        while True:
            loop.call_soon_threadsafe(ticker)
            time.sleep(threshold)
            now = time.monotonic()
            if now - last_tick > threshold:
                logger.warning("Event loop blocked for %.2fs", now - last_tick)

    thread = threading.Thread(target=checker, daemon=True)
    thread.start()
    return thread
