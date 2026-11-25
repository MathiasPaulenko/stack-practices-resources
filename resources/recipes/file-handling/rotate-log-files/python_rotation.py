"""Log rotation strategies with Python's logging.handlers.

- RotatingFileHandler: size-based rotation (10 MB, 5 backups).
- TimedRotatingFileHandler: daily rotation at midnight, 30 days kept.
- WatchedFileHandler: external rotation compatible with logrotate —
  reopens the file automatically when it is renamed.
"""

import logging
import logging.handlers

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

# Size-based rotation: 10MB max, keep 5 backups
handler = logging.handlers.RotatingFileHandler(
    "app.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
    encoding="utf-8",
)
handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
)
logger.addHandler(handler)

# Time-based rotation: daily at midnight, keep 30 days
timed_handler = logging.handlers.TimedRotatingFileHandler(
    "app_daily.log",
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8",
    utc=True,
)
timed_handler.suffix = "%Y-%m-%d"
timed_handler.extMatch = r"^\d{4}-\d{2}-\d{2}$"
logger.addHandler(timed_handler)

# WatchedFileHandler for external rotation (logrotate compatibility)
watched = logging.handlers.WatchedFileHandler("app.log")
logger.addHandler(watched)

if __name__ == "__main__":
    for i in range(10):
        logger.info("test message %d", i)
