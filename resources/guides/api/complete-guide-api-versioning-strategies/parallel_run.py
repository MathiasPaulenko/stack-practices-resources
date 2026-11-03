import asyncio
import logging

logger = logging.getLogger("api_migration")

async def parallel_run(v1_handler, v2_handler, request):
    # Serve from v1 (source of truth)
    v1_response = await v1_handler(request)

    # Run v2 in background, compare results
    try:
        v2_response = await v2_handler(request)
        if v1_response != v2_response:
            logger.warning(f"Response mismatch: v1={v1_response}, v2={v2_response}")
    except Exception as e:
        logger.error(f"v2 handler failed: {e}")

    return v1_response
