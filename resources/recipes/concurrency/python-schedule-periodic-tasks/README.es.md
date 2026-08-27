# Proyecto de ejemplo de tareas periódicas con APScheduler

Proyecto companion para la receta de StackPractices
[Receta APScheduler](https://stackpractices.com/es/recipes/python-schedule-periodic-tasks/).

## Archivos

- `main.py` — ejemplo ejecutable con disparadores de intervalo, fecha y gestión dinámica de tareas.
- `flask_app.py` — app Flask mínima con planificador en segundo plano y endpoint `/health`.
- `requirements.txt` — dependencias.

## Inicio rápido

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate en Windows
pip install -r requirements.txt
python main.py
```

`main.py` inicia un `BackgroundScheduler`, programa un tick cada 2 segundos, una tarea de pedidos cada 5
segundos y un recordatorio puntual, corre durante 12 segundos y termina de forma limpia.

## Comandos útiles

```bash
python main.py
python flask_app.py
```
