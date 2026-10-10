"""Message Queue Load Leveling with Celery + Redis.

Producer enqueues at any rate; the worker drains one task at a time.
Run Redis locally (`docker run -p 6379:6379 redis`), start a worker with
`celery -A celery_consumer worker --concurrency=1 --loglevel=info`, then run
`python celery_consumer.py` in another terminal to fire the burst.
"""
import time

from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379", backend="redis://localhost:6379")


# Consumer processes one task at a time at its own pace
@app.task(bind=True, max_retries=3)
def process_order(self, order_id):
    try:
        # Simulate slow processing (e.g., DB writes, API calls)
        time.sleep(2)
        print(f"Processed order {order_id}")
        return {"status": "done", "order_id": order_id}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


# Producer enqueues at any rate
def submit_orders(order_ids):
    for order_id in order_ids:
        process_order.delay(order_id)
    print(f"Enqueued {len(order_ids)} orders")


if __name__ == "__main__":
    # Burst: 1000 orders submitted instantly
    # Consumer processes them 1 at a time every 2 seconds
    submit_orders(range(1000))
