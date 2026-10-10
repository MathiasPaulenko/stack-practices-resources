# Concurrent HTTP Requests with asyncio.gather and aiohttp

Companion resource for [Concurrent HTTP Requests with asyncio.gather and aiohttp](https://stackpractices.com/recipes/python-async-gather-concurrent-requests/).

## Files

- `fetch_all.py` — fetches several endpoints concurrently with a semaphore, per-request timeouts and `return_exceptions` error capture.
- `requirements.txt` — the only dependency is `aiohttp`.

## Usage

```bash
pip install -r requirements.txt
python fetch_all.py
```

Expected output: five fetches finish in roughly the time of the slowest request (~2s) instead of the ~5s a sequential loop would take.

## What it demonstrates

- `asyncio.gather` with `return_exceptions=True` so one failure doesn't cancel the rest.
- `asyncio.Semaphore` to cap in-flight requests.
- `aiohttp.ClientTimeout` for total/connect deadlines.
- A shared `ClientSession` so TCP connections get reused.
