"""Size-based rotation with JSON-formatted records.

Rotated archives stay parseable by log pipelines that expect one JSON
object per line.
"""

import json
import logging
from logging.handlers import RotatingFileHandler


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


handler = RotatingFileHandler(
    "app.json.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
)
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if __name__ == "__main__":
    logger.info("structured event", extra={"user_id": 42})
