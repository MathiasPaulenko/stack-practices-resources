# Event Bus Pattern — Companion Files

Runnable in-memory event bus for the pattern on
[stackpractices.com](https://stackpractices.com/patterns/event-bus-pattern/).

## Files

- `event_bus.py` — Python: thread-safe bus (`threading.Lock`), `subscribe()` returns an `unsubscribe` closure, per-handler exception isolation
- `test_event_bus.py` — pytest: fan-out, unsubscribe, type filtering, failure isolation, unsubscribe-during-dispatch
- `event_bus.js` — JavaScript: `Map`-based bus with unsubscribe closures (Node 18+, ESM)
- `event_bus.test.js` — `node:test` suite mirroring the Python tests
- `EventBus.java` — Java: `record` event + `CopyOnWriteArrayList` for lock-free dispatch, `main` included

## Quick start

```bash
python event_bus.py          # stdlib only
pytest test_event_bus.py -q  # 5 tests
node event_bus.js            # Node 18+
node --test event_bus.test.js
javac EventBus.java && java EventBus
```

Each demo publishes `UserRegistered` twice — before and after one subscriber
unsubscribes — so you can see fan-out and cleanup in action.
