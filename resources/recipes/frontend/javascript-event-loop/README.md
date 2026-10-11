# JavaScript Event Loop — Companion Resources

Companion files for [JavaScript Event Loop](https://stackpractices.com/recipes/javascript-event-loop/) on StackPractices.

## Files

| File | What it demonstrates |
|------|----------------------|
| `event_loop_order.js` | Execution order of sync code, `process.nextTick`, microtasks (Promise, queueMicrotask), and macrotasks (setTimeout) — with expected output in comments |
| `chunked_processing.js` | Breaking a heavy array pass into `setTimeout` chunks so the loop stays responsive |
| `event_loop_lag.js` | Measuring event loop lag via timer drift while periodic blocking bursts run |

## How to use

```bash
node event_loop_order.js      # prints the scheduling order
node chunked_processing.js    # watch chunks yield to the loop
node event_loop_lag.js        # ctrl+C to stop; lag spikes after each burst
```

No dependencies — plain Node.js ≥ 18 works for all three scripts.
