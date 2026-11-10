"""Demo app: Python JsonFormatter emitting structured logs for Fluentd."""
import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "level": record.levelname.lower(),
            "message": record.getMessage(),
            "timestamp": self.formatTime(record),
            "service": "api",
        }
        return json.dumps(log_data)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
log = logging.getLogger("api")

if __name__ == "__main__":
    import time
    log.info("Worker started")
    for i in range(5):
        log.info("Processed item", extra={})
        time.sleep(1)
    log.error("Simulated failure for the demo")
