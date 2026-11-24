# celery_app.py — Celery application configured for a Redis broker/backend.
from celery import Celery
from celery.schedules import crontab

app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
)

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    result_expires=3600,
    task_track_started=True,
    # Soft limit raises SoftTimeLimitExceeded inside the task;
    # hard limit kills the worker if the task still refuses to stop.
    task_soft_time_limit=240,
    task_time_limit=300,
)

# Per-task retry defaults go here — there are no
# task_default_retry_delay / task_default_max_retries settings.
app.conf.task_annotations = {
    '*': {'max_retries': 3, 'default_retry_delay': 60},
}

app.conf.task_routes = {
    'tasks.send_email': {'queue': 'email'},
    'tasks.send_report_email': {'queue': 'email'},
    'tasks.generate_report': {'queue': 'reports'},
    'tasks.cleanup_*': {'queue': 'maintenance'},
}

app.conf.beat_schedule = {
    'daily-report': {
        'task': 'tasks.generate_report',
        'schedule': crontab(hour=6, minute=0),
        'args': ('daily', {'date': 'today'}),
    },
    'weekly-cleanup': {
        'task': 'tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    },
    'health-check': {
        'task': 'tasks.check_service_health',
        'schedule': 300.0,
    },
}

# Looks for tasks.py inside each listed package.
app.autodiscover_tasks(['myapp'])
