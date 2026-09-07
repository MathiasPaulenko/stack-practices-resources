# Pipes and Filters Pattern — Companion Resources

Companion code for the [Pipes and Filters Pattern](https://stackpractices.com/patterns/pipes-and-filters-pattern/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `pipe_python.py` | Python 3.12+ | Synchronous pipeline with pure-function filters |
| `pipe_javascript.js` | Node 20+ | Same pipeline using `reduce` composition |
| `PipesAndFilters.java` | Java 21+ | Type-safe pipeline with `Function<T, R>` |
| `async_pipe_python.py` | Python 3.12+ | Async pipeline with `asyncio` for I/O-bound filters |
| `test_pipe_python.py` | Python 3.12+ | Unit tests for each filter and the full pipeline |
| `test_pipe_javascript.js` | Node 20+ | Unit tests for each filter and pipe composability |

## Quick start

### Python

```bash
python pipe_python.py          # run the pipeline
python -m pytest test_pipe_python.py -v  # run tests
```

### JavaScript

```bash
node pipe_javascript.js        # run the pipeline
node test_pipe_javascript.js   # run tests
```

### Java

```bash
javac PipesAndFilters.java     # compile
java PipesAndFilters           # run
```

## What each filter does

1. **parse_csv** — splits raw CSV text into a list of records (dicts/maps).
2. **filter_active** — keeps only records with `status == "active"`.
3. **normalize_emails** — lowercases and trims the email field.
4. **deduplicate** — removes records with duplicate emails.
5. **to_json** — serializes the result to JSON (Python/JS only).

Each filter is a pure function: no side effects, no shared state. You can reorder them, add new ones, or test them in isolation.
