# Debounce and Throttle — Event Burst Simulation

Runnable companions for the recipe [Debounce and Throttle](https://stackpractices.com/recipes/debounce-throttle/).

## What it shows

A burst of 12 events in 300ms plus a 3-event tail is fed through both limiters:

- **Raw**: every event fires (15 executions).
- **Debounce** (250ms wait): fires once per quiet gap — the burst collapses to a couple of calls.
- **Throttle** (300ms limit): fires at most once per window.

## Run

```bash
python src/debounce_throttle_simulation.py
node src/debounce-throttle-simulation.js
javac src/DebounceThrottleSimulation.java && java -cp src DebounceThrottleSimulation
```

No external dependencies.

## Related

- Recipe: <https://stackpractices.com/recipes/debounce-throttle/>
