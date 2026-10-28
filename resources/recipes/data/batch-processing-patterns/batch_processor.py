"""Resilient batch processor with retry, checkpointing and dead-letter support.

Companion code for https://stackpractices.com/recipes/batch-processing-patterns/

Usage:
    python batch_processor.py
"""

import json
import logging
import os
import random
import tempfile
from typing import Callable, Iterator, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


class BatchProcessor:
    """Process an iterable of items in chunks with bounded retries.

    - Retries a whole batch up to ``max_retries`` times before moving the
      batch to the dead-letter list.
    - Persists a checkpoint file after every successful batch so an
      interrupted run can resume from the last completed batch.
    """

    def __init__(
        self,
        batch_size: int = 1000,
        max_retries: int = 3,
        checkpoint_path: str | None = None,
    ):
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.checkpoint_path = checkpoint_path
        self.processed = 0
        self.failed: List[dict] = []
        self._batch_number = self._load_checkpoint()

    def process(
        self,
        items: Iterator[dict],
        handler: Callable[[List[dict]], None],
    ) -> dict:
        batch = []
        for item in items:
            batch.append(item)
            if len(batch) >= self.batch_size:
                self._execute(batch, handler)
                batch = []
        if batch:
            self._execute(batch, handler)
        return {"processed": self.processed, "failed": len(self.failed)}

    def _execute(self, batch: List[dict], handler: Callable) -> None:
        self._batch_number += 1
        for attempt in range(self.max_retries):
            try:
                handler(batch)
                self.processed += len(batch)
                self._save_checkpoint()
                return
            except Exception as exc:  # noqa: BLE001 - batch boundary catch
                delay = min(2**attempt + random.uniform(0, 1), 30)
                logging.warning(
                    "Batch %s failed (attempt %s/%s): %s — retrying in %.1fs",
                    self._batch_number,
                    attempt + 1,
                    self.max_retries,
                    exc,
                    delay,
                )
                if attempt == self.max_retries - 1:
                    self.failed.extend(batch)

    def _save_checkpoint(self) -> None:
        if not self.checkpoint_path:
            return
        # Atomic write: temp file + replace so a crash can't corrupt the file.
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(self.checkpoint_path) or ".")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"last_completed_batch": self._batch_number}, f)
        os.replace(tmp, self.checkpoint_path)

    def _load_checkpoint(self) -> int:
        if self.checkpoint_path and os.path.exists(self.checkpoint_path):
            with open(self.checkpoint_path, encoding="utf-8") as f:
                return json.load(f).get("last_completed_batch", 0)
        return 0


def _demo() -> None:
    """Process 5,000 synthetic records in batches of 500."""
    processor = BatchProcessor(batch_size=500, max_retries=3)

    def handler(batch: List[dict]) -> None:
        # Simulate work: transform + load would happen here.
        _ = [r["value"] * 2 for r in batch]

    items = ({"id": i, "value": i} for i in range(5000))
    result = processor.process(items, handler)
    logging.info("Done: %s", result)


if __name__ == "__main__":
    _demo()
