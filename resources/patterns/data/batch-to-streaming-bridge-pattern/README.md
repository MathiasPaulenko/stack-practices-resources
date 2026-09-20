# Batch-to-Streaming Bridge — Companion Examples

Runnable examples for the [Batch-to-Streaming Bridge pattern](https://stackpractices.com/patterns/batch-to-streaming-bridge-pattern/): how batch ETL and real-time streaming write into one partitioned data lake, and how the serving layer merges them.

No external services needed — the examples simulate the architecture in memory so the semantics (partition layout, schema alignment, dedup) are easy to see and test.

## What's inside

| File | Purpose |
| --- | --- |
| `bridge.py` / `bridge.js` | The pattern: shared-schema producers, partitioned lake, speed layer, serving-layer dedup, unified consumer |
| `test_bridge.py` | pytest suite (7 tests) |
| `bridge.test.js` | `node:test` suite (7 tests) |

## Concepts covered

- **Shared schema** — `BatchProducer` and `StreamingProducer` normalize both sources into the same record (lowercase email, derived `is_active`, tagged `source`).
- **Partition layout** — every record lands under `year=/month=/day=/hour=`; the hour segment is what trips up real implementations.
- **Serving-layer dedup** — `ROW_NUMBER()` semantics: prefer streaming (fresher), fall back to batch.
- **Speed layer** — keyed lookup for the freshest state instead of re-consuming the stream.
- **Selective merge** — streaming fields override batch only when present, so partial updates can't wipe fields.

## Run

```bash
node bridge.js        # JS demo
python bridge.py      # Python demo

node --test bridge.test.js   # JS tests
python -m pytest test_bridge.py -v   # Python tests
```

Zero dependencies beyond pytest for the test suite.
