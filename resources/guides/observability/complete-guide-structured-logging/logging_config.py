# logging_config.py — structlog configuration
import logging
import sys

import structlog


def configure_logging(service_name: str = "order-service", env: str = "production"):
    """Configure structured logging. Call once at app startup."""
    structlog.contextvars.bind_contextvars(service=service_name, env=env)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ]
            ),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
        )
    )
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO)


if __name__ == "__main__":
    configure_logging()
    log = structlog.get_logger()
    log.info("service_started", version="1.4.2")
    structlog.contextvars.bind_contextvars(request_id="demo-123", user_id=456)
    log.info("order_created", order_id=1001, total=99.99)
