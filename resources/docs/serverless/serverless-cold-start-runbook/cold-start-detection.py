"""Cold start detection via a module-level flag (survives across invocations)."""
import json
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_init_start = time.time()
# heavy init would run here on cold start
_init_duration = time.time() - _init_start

_is_warm = False


def handler(event, context):
    global _is_warm

    if not _is_warm:
        logger.info(json.dumps({
            "COLD_START": True,
            "init_duration_ms": round(_init_duration * 1000, 2),
            "remaining_time_ms": context.get_remaining_time_in_millis(),
            "memory_limit_mb": context.memory_limit_in_mb,
        }))
        _is_warm = True

    logger.info(json.dumps({
        "INVOCATION": True,
        "request_id": context.aws_request_id,
    }))
    return process_request(event)
