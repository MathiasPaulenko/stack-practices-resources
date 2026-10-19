"""Structured logging with Loguru: JSON output, rotation, async writes.

Run: pip install -r requirements.txt && python python_loguru.py
"""
import re
import sys

from loguru import logger

SENSITIVE = re.compile(r"(token|api_key|password)=\S+", re.IGNORECASE)


def mask(msg: str) -> str:
    """Redact secrets before they reach the logger."""
    return SENSITIVE.sub(r"\1=***", msg)


def main() -> None:
    logger.remove()
    # Human-readable output for local development
    logger.add(sys.stdout, format="{time:HH:mm:ss} | {level} | {message}", level="INFO")
    # JSON lines with rotation and async writes for production collectors
    logger.add(
        "app.log",
        serialize=True,
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        enqueue=True,
    )

    user_id = "u-42"
    api_key = "sk-live-abcdef123456"
    token = "secret-token-value"

    logger.debug("Processing user {}", user_id)
    logger.info("User {} logged in", user_id)
    logger.warning("Rate limit at 90% for API key {}", api_key[:4])
    logger.info(mask(f"fetched profile token={token}"))

    try:
        raise ConnectionError("database timeout")
    except ConnectionError:
        logger.exception("Database connection failed")

    # Attach context that travels with every subsequent log
    logger.bind(request_id="abc-123", duration_ms=45).info("Request completed")


if __name__ == "__main__":
    main()
