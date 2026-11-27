# Shed Load Pattern — Code Examples

Companion examples for the [Shed Load Pattern](https://stackpractices.com/patterns/shed-load-pattern/) resource on StackPractices.

## Files

- `load_shedder.py` — Python implementation: threshold-based shedding on concurrency, CPU (via `psutil`), memory and queue depth, with shed/accept stats.
- `load_shedder.js` — Node.js implementation: same admission logic with `process.memoryUsage()` and async handlers.
- `LoadShedder.java` — Java implementation: `AtomicInteger` counters, JVM memory sampling, `ExecutorService` demo in `main`.

## Run

```bash
# Python (requires psutil)
pip install psutil
python load_shedder.py

# Node.js
node load_shedder.js

# Java
javac LoadShedder.java && java LoadShedder
```

Each demo fires 10 concurrent requests at a shedder capped at 3 concurrent; expect ~3 accepted and ~7 shed with HTTP 503.

## License

Code examples are provided for educational purposes as part of StackPractices.
