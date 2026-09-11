"""Queue-Based Load Leveling Pattern - Consumer handler examples."""

import time
import random


def handle_email(task):
    """Simulate sending an email."""
    time.sleep(0.05)
    if random.random() < 0.05:
        raise RuntimeError("SMTP timeout")
    return {"status": "sent", "task_id": task.id}


def handle_report(task):
    """Simulate generating a report."""
    time.sleep(0.1)
    return {"status": "completed", "task_id": task.id, "report_url": f"/reports/{task.id}.pdf"}


def handle_payment(task):
    """Simulate processing a payment."""
    time.sleep(0.08)
    if random.random() < 0.1:
        raise RuntimeError("Payment gateway unavailable")
    return {"status": "processed", "task_id": task.id, "amount": task.payload.get("amount")}


HANDLERS = {
    "send-email": handle_email,
    "generate-report": handle_report,
    "process-payment": handle_payment,
}


def route_task(task):
    """Route a task to the correct handler based on task type."""
    handler = HANDLERS.get(task.type)
    if handler is None:
        raise ValueError(f"Unknown task type: {task.type}")
    return handler(task)
