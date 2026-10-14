"""Production-style APScheduler setup with overlap and missed-run control.

Install: pip install apscheduler
Run:     python apscheduler_example.py
"""
import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def backup_job() -> None:
    logger.info("Starting database backup...")
    # Backup logic here
    logger.info("Backup completed.")


def health_check() -> None:
    logger.info("Health check OK")


scheduler = BackgroundScheduler(timezone="UTC")

# Every day at 3:00 AM UTC
scheduler.add_job(
    backup_job,
    CronTrigger(hour=3, minute=0),
    id="backup",
    max_instances=1,  # Prevent overlap — same role as flock in crontab
    coalesce=True,    # Merge missed runs into one after a restart
)

# Every 15 minutes with up to 60 s of random delay
scheduler.add_job(
    health_check,
    CronTrigger(minute="*/15"),
    id="health_check",
    max_instances=1,
    jitter=60,
)

scheduler.start()

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    scheduler.shutdown()
