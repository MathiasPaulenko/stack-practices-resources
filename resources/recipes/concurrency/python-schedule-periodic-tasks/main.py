from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "jobs.sqlite")


def send_reminder(email: str = "reminder@stackpractices.com"):
    print(f"[{datetime.now().isoformat()}] Sending reminder to {email}")


def process_order(order_id: int, priority: str = "normal"):
    print(f"[{datetime.now().isoformat()}] Processing order {order_id} with priority {priority}")


def tick():
    print(f"[{datetime.now().isoformat()}] Tick every 2s")


def job_listener(event):
    if event.exception:
        print(f"Job {event.job_id} failed: {event.exception}")
    elif event.code == EVENT_JOB_MISSED:
        print(f"Job {event.job_id} missed its run time")
    else:
        print(f"Job {event.job_id} executed successfully")


def main():
    jobstores = {"default": SQLAlchemyJobStore(url=f"sqlite:///{DB_PATH}")}
    job_defaults = {
        "coalesce": True,
        "max_instances": 1,
        "misfire_grace_time": 5,
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, job_defaults=job_defaults)
    scheduler.add_listener(job_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED)

    scheduler.add_job(tick, "interval", seconds=2, id="tick")
    scheduler.add_job(process_order, "interval", seconds=5, args=[12345], id="process_order")

    run_time = datetime.now() + timedelta(seconds=3)
    scheduler.add_job(send_reminder, "date", run_date=run_time, args=["reminder@stackpractices.com"], id="reminder")

    print("Starting scheduler...")
    scheduler.start()

    try:
        time.sleep(12)
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down scheduler...")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
