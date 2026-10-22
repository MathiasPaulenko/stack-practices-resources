# Background Jobs — Runnable Examples

Companion code for the StackPractices recipe
[Background Jobs: Task Queues, Cron & Workers](https://stackpractices.com/recipes/background-jobs/).

## Files

| File | What it shows |
| --- | --- |
| `tasks.py` | Celery task module: `send_email` with retry backoff, `generate_report`, `cleanup_old_logs`, `long_running_task` with progress state, and a `beat_schedule` for daily cron. |
| `worker.js` | BullMQ worker and producer: retries with exponential backoff, dead-letter queue moved only after the last attempt, and a repeatable cron job. |
| `JobService.java` | Spring `@Scheduled` service: daily cron, fixed-rate sync, and an executor-backed async method. Requires `@EnableScheduling`. |
| `docker-compose.yml` | Redis + Celery worker + Celery beat + API wired together for local development. |
| `requirements.txt` / `package.json` | Dependencies for the Python and Node examples. |

## Quick start

### Python (Celery + Redis)

```bash
pip install -r requirements.txt
docker run -d -p 6379:6379 redis:7-alpine
celery -A tasks worker --loglevel=info --concurrency=4   # terminal 1
celery -A tasks beat --loglevel=info                     # terminal 2
python -c "import tasks; tasks.send_email.delay('a@b.co', 'Hi', 'Body')"
```

### JavaScript (BullMQ + Redis)

```bash
npm install
docker run -d -p 6379:6379 redis:7-alpine
node worker.js
```

### Docker Compose (full stack)

```bash
docker compose up --build
```
