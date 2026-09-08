# Distributed Rate Limiting with FastAPI and Redis — Companion Resources

Companion code for the [FastAPI + Redis Rate Limiting recipe](https://stackpractices.com/recipes/python-rate-limiting-fastapi-redis/) on StackPractices.

## Contents

|File|Description|
|------|-------------|
|`sliding_window.py`|Sliding window rate limiter using Redis ZSET|
|`token_bucket.py`|Token bucket rate limiter using Redis Lua script|
|`fixed_window.py`|Fixed window rate limiter using Redis INCR|
|`middleware.py`|FastAPI middleware + per-endpoint decorator|
|`test_rate_limiting.py`|Unit tests for all three limiters (uses fakeredis)|
|`README.md`|English README|
|`README.es.md`|Spanish README|

## Running the Examples

### Install dependencies

```bash
pip install fastapi redis uvicorn
pip install fakeredis pytest  # for tests
```

### Run the FastAPI app

```bash
uvicorn middleware:app --reload
```

### Run unit tests

```bash
pytest test_rate_limiting.py -v
```

## Algorithms

|Algorithm|Burst handling|Accuracy|Redis ops|
|-----------|----------------|----------|-----------|
|Sliding window|No bursts|High|ZSET pipeline|
|Token bucket|Bursts up to capacity|Medium|Lua script|
|Fixed window|Double bursts at boundary|Low|INCR + EXPIRE|
