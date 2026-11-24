# Python Celery task queue — companion files

Files referenced by the recipe
[Distribute Background Tasks with Python Celery and Redis](https://stackpractices.com/recipes/python-celery-task-queue/).

| File | Purpose |
| --- | --- |
| `celery_app.py` | Celery app: Redis broker/backend, reliability flags, soft/hard time limits, `task_annotations` retry defaults, queue routing and a Beat schedule. |
| `tasks.py` | Task definitions: `send_email` with `autoretry_for` backoff, `send_report_email` as the chain target, and `summarize_reports` as the chord callback (registered task — a plain function has no `.s()`). |

## Run it

```bash
pip install 'celery[redis]' flower
celery -A celery_app worker --loglevel=info --concurrency=4
celery -A celery_app beat --loglevel=info      # exactly one instance
celery -A celery_app flower --port=5555
```

Replace `connect_smtp()` in `tasks.py` with your real SMTP client before
running `send_email`.
