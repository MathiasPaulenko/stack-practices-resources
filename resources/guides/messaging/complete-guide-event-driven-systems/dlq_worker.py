"""Consumer loop with retry counter + dead letter queue routing."""
import json
from datetime import datetime

MAX_RETRIES = 3


def consume_with_dlq(consumer, processor, dlq_producer, logger):
    for message in consumer:
        event = json.loads(message.value)
        retry_count = event.get("metadata", {}).get("retry_count", 0)

        try:
            processor.process(event)
            consumer.commit()
        except Exception as exc:
            meta = event.setdefault("metadata", {})
            meta["last_error"] = str(exc)
            meta["last_retry_at"] = datetime.utcnow().isoformat()

            if retry_count < MAX_RETRIES:
                meta["retry_count"] = retry_count + 1
                dlq_producer.send("retry-topic", value=json.dumps(event))
            else:
                meta["final_error"] = str(exc)
                meta["failed_at"] = datetime.utcnow().isoformat()
                dlq_producer.send("dead-letter-topic", value=json.dumps(event))
                logger.error("Event %s sent to DLQ", event["event_id"])

            consumer.commit()
