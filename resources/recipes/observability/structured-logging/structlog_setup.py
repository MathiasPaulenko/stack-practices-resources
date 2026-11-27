import structlog
import logging

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

def transfer_funds(from_account, to_account, amount):
    logger.info(
        "transfer_initiated",
        from_account=from_account,
        to_account=to_account,
        amount_cents=amount,
        request_id=get_current_request_id()
    )
