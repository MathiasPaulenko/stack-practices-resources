"""Dead Letter Channel pattern — in-memory simulation.

A minimal broker with a main queue, a retry queue, and a dead letter
queue. The consumer processes orders; a poison message (missing
order_id) keeps failing, exhausts its retry budget, and lands in the
DLQ with failure metadata. Run: python src/dead_letter_channel.py
"""

import time
from collections import deque


class Broker:
    """In-memory broker with named queues."""

    def __init__(self):
        self.queues = {}

    def declare(self, name):
        self.queues.setdefault(name, deque())

    def send(self, name, body):
        self.queues[name].append({"body": body, "attempts": 0})

    def send_envelope(self, name, envelope):
        self.queues[name].append(envelope)

    def receive(self, name):
        return self.queues[name].popleft() if self.queues[name] else None

    def depth(self, name):
        return len(self.queues[name])


MAX_RETRIES = 3
RETRY_DELAY_S = 0.05


def handle_order(body):
    if body.get("order_id") is None:
        raise ValueError("Missing order_id")
    return {"status": "done", "order_id": body["order_id"]}


def main():
    broker = Broker()
    for queue in ("main", "retry", "dlq"):
        broker.declare(queue)

    broker.send("main", {"order_id": "A-1", "amount": 25})
    broker.send("main", {"order_id": None, "amount": 99})  # poison message
    broker.send("main", {"order_id": "A-3", "amount": 40})

    processed, retries = 0, 0

    while True:
        msg = broker.receive("main") or broker.receive("retry")
        if msg is None:
            break

        try:
            result = handle_order(msg["body"])
            processed += 1
            print(f"[main] processed order {result['order_id']}")
        except Exception as exc:
            msg["attempts"] += 1
            if msg["attempts"] >= MAX_RETRIES:
                msg["failure"] = {"error": str(exc), "attempts": msg["attempts"]}
                broker.send_envelope("dlq", msg)
                print(f"[dlq ] moved message after {msg['attempts']} attempts: {exc}")
            else:
                retries += 1
                print(f"[main] attempt {msg['attempts']} failed ({exc}); retrying")
                time.sleep(RETRY_DELAY_S)
                broker.send_envelope("retry", msg)

    print(f"\nmain={broker.depth('main')} retry={broker.depth('retry')} dlq={broker.depth('dlq')}")
    print(f"processed={processed} retried={retries}")

    # Replay: fix the poisoned payload, then move it back to the main queue
    msg = broker.receive("dlq")
    if msg:
        print(f"\n[replay] fixing message and re-queuing (was: {msg['failure']})")
        msg["body"]["order_id"] = "A-2-repaired"
        msg["attempts"] = 0
        broker.send_envelope("main", msg)
        fixed = broker.receive("main")
        print(f"[main] processed order {handle_order(fixed['body'])['order_id']}")


if __name__ == "__main__":
    main()
