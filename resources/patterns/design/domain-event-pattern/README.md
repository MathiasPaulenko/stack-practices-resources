# Domain Event Pattern — Companion Files

Runnable examples for the pattern on
[stackpractices.com](https://stackpractices.com/patterns/domain-event-pattern/).

## Files

- `domain_events.py` — Python: frozen dataclass event + `Order` aggregate + class-level `EventPublisher` with two real subscribers
- `domain_events.js` — JavaScript: same model with `crypto.randomUUID()` (Node 19+)
- `DomainEvents.java` — Java: `record` event + `Consumer<DomainEvent>` publisher, `main` included

## Quick start

```bash
python domain_events.py   # stdlib only
node domain_events.js     # Node 19+
javac DomainEvents.java && java DomainEvents
```

Each script creates an order, submits it, drains `clearEvents()` and publishes — you'll see the email and analytics handlers react.
