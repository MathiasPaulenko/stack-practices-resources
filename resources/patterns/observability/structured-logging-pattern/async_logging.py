"""Non-blocking structured logging with QueueHandler + QueueListener."""

import logging
import logging.handlers
import queue
import sys

from json_formatter import JsonFormatter


def build_async_logger(
    name: str = "myapp",
    stream=None,
) -> tuple[logging.Logger, logging.handlers.QueueListener]:
    log_queue: queue.Queue = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(log_queue)

    stream_handler = logging.StreamHandler(stream or sys.stdout)
    stream_handler.setFormatter(JsonFormatter())
    listener = logging.handlers.QueueListener(log_queue, stream_handler)

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(queue_handler)
    logger.setLevel(logging.INFO)
    listener.start()
    return logger, listener


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    logger, listener = build_async_logger()
    for i in range(3):
        logger.info("item_processed", extra={"index": i, "ok": True})
    listener.stop()
