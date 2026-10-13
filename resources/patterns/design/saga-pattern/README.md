# Saga Pattern — Companion Files

Runnable orchestrated saga implementations in three languages. Each one runs
the same travel-booking flow from the article — reserve a flight, reserve a
hotel, charge the payment — where the payment step always fails so you can
watch the compensating transactions undo the completed steps in reverse order.

Source article: <https://stackpractices.com/patterns/saga-pattern/>

## Files

| File | Language | Notes |
|------|----------|-------|
| `saga_orchestrator.py` | Python 3.8+ | `SagaOrchestrator` keeps the completed steps and walks them backwards through `compensation` on failure |
| `sagaOrchestrator.mjs` | Node.js 18+ | async `execute`/`rollback`, supports async actions and compensations |
| `SagaOrchestrator.java` | Java 11+ | `Consumer`-based steps; `main` runs the booking demo |

## Run

```bash
python saga_orchestrator.py            # no dependencies
node sagaOrchestrator.mjs              # no dependencies
javac SagaOrchestrator.java && java SagaOrchestrator
```

Each demo prints the happy path for `reserve_flight` and `reserve_hotel`, then
the `charge_payment` failure and the compensations running in reverse
(`cancelHotel` → `cancelFlight`).

## For production

An in-memory step list loses everything if the process dies mid-saga. In
production you want a persisted saga log and timeouts per step — or a framework
that gives you both:

- **Temporal / Cadence**: durable workflows with compensation handlers
- **Axon Framework, Eventuate Tram** (Java): saga orchestration over messaging
- **MassTransit** (.NET): saga state machines with message correlation
- **AWS Step Functions**: `Catch` blocks act as compensations
