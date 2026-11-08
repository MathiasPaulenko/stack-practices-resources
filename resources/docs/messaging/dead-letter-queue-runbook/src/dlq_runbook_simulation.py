"""In-memory simulation of the DLQ runbook workflow.

Mirrors the procedures in the runbook: a poison message exhausts its
retries, lands in the DLQ with failure metadata, gets inspected and
categorized, then replays back to the source queue once the fix deploys.

Run: python src/dlq_runbook_simulation.py
"""

from collections import Counter, deque
from datetime import datetime, timezone

MAX_RETRIES = 3
FIX_DEPLOYED = False


class Broker:
    """Minimal message broker with a main queue and a DLQ."""

    def __init__(self):
        self.main = deque()
        self.dlq = deque()

    def publish(self, msg):
        self.main.append(msg)


def process_message(msg):
    """Business handler — fails on poison payloads until the fix deploys."""
    if msg["value"].get("poison") and not FIX_DEPLOYED:
        raise ValueError("ValidationError: poison payload")
    return True


def consume(broker):
    """Consumer with retry-count headers and DLQ routing (runbook §1.3)."""
    while broker.main:
        msg = broker.main.popleft()
        try:
            process_message(msg)
        except Exception as e:
            retry_count = int(msg["headers"].get("retry-count", "0")) + 1
            msg["headers"]["retry-count"] = str(retry_count)
            if retry_count <= MAX_RETRIES:
                broker.publish(msg)  # requeue on the source queue
            else:
                msg["headers"].update({
                    "error": str(e),
                    "failed-at": datetime.now(timezone.utc).isoformat(),
                })
                broker.dlq.append(msg)


def inspect_dlq(broker):
    """Aggregate inspection — runbook §2.3."""
    categories = Counter()
    for msg in broker.dlq:
        error = msg["headers"].get("error", "unknown")
        if "ValidationError" in error:
            categories["schema_validation_error"] += 1
        else:
            categories["business_logic_error"] += 1
    return categories


def replay_dlq(broker):
    """Replay after the fix deploys — runbook §4."""
    replayed = 0
    while broker.dlq:
        msg = broker.dlq.popleft()
        for h in ("retry-count", "error", "failed-at"):  # strip DLQ metadata
            msg["headers"].pop(h, None)
        broker.publish(msg)
        replayed += 1
    return replayed


def main():
    global FIX_DEPLOYED

    broker = Broker()
    broker.publish({"headers": {}, "value": {"order_id": 1, "poison": True}})
    broker.publish({"headers": {}, "value": {"order_id": 2, "poison": False}})

    print("== Phase 1: consume (poison message retries then dead-letters) ==")
    consume(broker)
    print(f"  main queue: {len(broker.main)} | dlq: {len(broker.dlq)}")

    print("== Phase 2: inspect DLQ (error categorization) ==")
    for category, count in inspect_dlq(broker).most_common():
        print(f"  {category}: {count}")

    print("== Phase 3: fix deploys, replay DLQ ==")
    FIX_DEPLOYED = True  # the consumer now handles the poison payload
    print(f"  replayed: {replay_dlq(broker)}")
    consume(broker)

    print(f"== Phase 4: verified — dlq: {len(broker.dlq)}, "
          f"unprocessed: {len(broker.main)} ==")


if __name__ == "__main__":
    main()
