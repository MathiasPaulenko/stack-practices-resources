# Tareas en Segundo Plano — Ejemplos Ejecutables

Código companion de la receta de StackPractices
[Tareas en Segundo Plano (Background Jobs)](https://stackpractices.com/es/recipes/background-jobs/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `tasks.py` | Módulo de tareas Celery: `send_email` con backoff de reintentos, `generate_report`, `cleanup_old_logs`, `long_running_task` con estado de progreso y `beat_schedule` para cron diario. |
| `worker.js` | Worker y productor BullMQ: reintentos con backoff exponencial, dead-letter queue que solo mueve el trabajo tras el último intento y un trabajo cron repetible. |
| `JobService.java` | Servicio Spring `@Scheduled`: cron diario, sincronización a tasa fija y método async con executor. Requiere `@EnableScheduling`. |
| `docker-compose.yml` | Redis + worker Celery + beat Celery + API conectados para desarrollo local. |
| `requirements.txt` / `package.json` | Dependencias de los ejemplos en Python y Node. |

## Inicio rápido

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

### Docker Compose (stack completo)

```bash
docker compose up --build
```
