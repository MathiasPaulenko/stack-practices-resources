# Idempotent API Endpoints — Companion Resources

Companion code for the StackPractices recipe [Idempotent API Endpoints](https://stackpractices.com/recipes/idempotent-api-endpoints/).

## Contents

- `python_fastapi.py` — Python FastAPI implementation with in-memory idempotency store.
- `javascript_express.js` — JavaScript Express implementation with Map-based store.
- `java_spring.java` — Java Spring Boot implementation with ConcurrentHashMap.
- `test_idempotency.py` — pytest tests covering duplicate, concurrent, and TTL expiry scenarios.
- `requirements.txt` — Python dependencies.
- `meta.json` — Resource metadata.

## Running the Python example

```bash
pip install -r requirements.txt
uvicorn python_fastapi:app --reload
```

## Running the tests

```bash
pip install -r requirements.txt
pytest test_idempotency.py -v
```

## Key concepts

- **Idempotency key**: client-generated UUID sent in the `Idempotency-Key` header.
- **Processing state**: prevents concurrent requests with the same key from executing twice.
- **TTL cleanup**: removes expired entries to prevent unbounded store growth.
- **Error recovery**: removes the processing marker on failure so clients can retry.
