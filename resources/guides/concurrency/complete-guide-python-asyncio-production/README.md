# Production Asyncio Patterns

Companion resources for [Complete Guide to Python Asyncio in Production](https://stackpractices.com/guides/complete-guide-python-asyncio-production/).

## Contents

| File | Purpose |
| --- | --- |
| `graceful_shutdown.py` | Signal-driven shutdown: cancel workers, bounded cleanup |
| `token_bucket.py` | Async token bucket rate limiter |
| `watchdog.py` | Event loop stall detector (thread-based) |
| `http_pool.py` | aiohttp connection pool with semaphore cap |
| `health_server.py` | /health + /live endpoints on a separate port |
| `test_asyncio_patterns.py` | pytest-asyncio tests: timeouts, cancellation, bucket |

## Usage

```bash
pip install aiohttp pytest pytest-asyncio
pytest test_asyncio_patterns.py -v
python graceful_shutdown.py   # Ctrl-C to see clean shutdown
```

See the guide for the full explanations and the troubleshooting table.
