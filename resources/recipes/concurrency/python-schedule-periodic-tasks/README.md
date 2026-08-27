# APScheduler periodic tasks sample

Companion project for the StackPractices recipe
[APScheduler recipe](https://stackpractices.com/recipes/python-schedule-periodic-tasks/).

## Files

- `main.py` — runnable example with interval, date, and dynamic job management.
- `flask_app.py` — minimal Flask app with a background scheduler and `/health` endpoint.
- `requirements.txt` — dependencies.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

`main.py` starts a `BackgroundScheduler`, schedules a 2-second tick, a 5-second order task, and a one-off
reminder, then runs for 12 seconds and shuts down cleanly.

## Useful commands

```bash
python main.py
python flask_app.py
```
