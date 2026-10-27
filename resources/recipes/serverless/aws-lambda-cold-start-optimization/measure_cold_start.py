import json
import time

# Module-level: True only for the first invocation in this environment
cold_start = True

def lambda_handler(event, context):
    global cold_start
    start = time.time()
    is_cold_start = cold_start
    cold_start = False

    response = {
        "cold_start": is_cold_start,
        "init_time_ms": round((time.time() - start) * 1000, 2),
        "remaining_time_ms": context.get_remaining_time_in_millis(),
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
    }
