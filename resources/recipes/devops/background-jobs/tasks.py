"""Celery task module for the background-jobs recipe.

Run a worker:    celery -A tasks worker --loglevel=info --concurrency=4
Run the beat:    celery -A tasks beat --loglevel=info
Enqueue a job:   python -c "import tasks; tasks.send_email.delay('a@b.co','Hi','Body')"
"""
from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

# Deliver at-least-once: only remove the job after the task finishes.
app.conf.task_acks_late = True


@app.task(bind=True, max_retries=3)
def send_email(self, to, subject, body):
    try:
        # Real implementation goes through SMTP or an API like SendGrid
        print(f"Sending email to {to}: {subject}")
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task
def generate_report(user_id):
    print(f"Generating report for user {user_id}")
    return f"/reports/{user_id}.pdf"


@app.task
def cleanup_old_logs():
    print("Deleting log files older than 30 days")


@app.task(bind=True)
def long_running_task(self, items):
    total = len(items)
    for i, item in enumerate(items):
        print(f"Processing {item}")
        self.update_state(
            state="PROGRESS",
            meta={"current": i + 1, "total": total, "percent": (i + 1) / total * 100},
        )
    return {"status": "complete", "processed": total}


# Periodic tasks run through celery beat.
app.conf.beat_schedule = {
    "daily-cleanup": {
        "task": "tasks.cleanup_old_logs",
        "schedule": crontab(hour=2, minute=0),
    },
}
