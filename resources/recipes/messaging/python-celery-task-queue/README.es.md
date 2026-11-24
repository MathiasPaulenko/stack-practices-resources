# Cola de tareas Celery en Python — archivos companion

Archivos referenciados por la receta
[Distribuir tareas en background con Python Celery y Redis](https://stackpractices.com/es/recipes/python-celery-task-queue/).

| Archivo | Propósito |
| --- | --- |
| `celery_app.py` | App Celery: broker/backend Redis, flags de fiabilidad, límites soft/hard, defaults de retry en `task_annotations`, routing por colas y un schedule de Beat. |
| `tasks.py` | Definiciones de tareas: `send_email` con backoff `autoretry_for`, `send_report_email` como destino del chain y `summarize_reports` como callback del chord (tarea registrada — una función plana no tiene `.s()`). |

## Ejecución

```bash
pip install 'celery[redis]' flower
celery -A celery_app worker --loglevel=info --concurrency=4
celery -A celery_app beat --loglevel=info      # exactamente una instancia
celery -A celery_app flower --port=5555
```

Sustituye `connect_smtp()` en `tasks.py` por tu cliente SMTP real antes de
ejecutar `send_email`.
