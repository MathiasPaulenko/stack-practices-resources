# SQL Deadlock Prevention — Lock Ordering Simulation

Runnable companions for the recipe [Prevent and Resolve Deadlocks in SQL Transactions](https://stackpractices.com/recipes/deadlock-prevention-sql/).

## What it shows

- **Unordered acquisition**: two transactions lock rows in opposite order and hit a deadlock (detected via lock timeout / wait-for cycle).
- **Ordered acquisition**: sorting the lock order removes the circular wait — both transactions complete.
- **Retry with jitter**: the standard pattern for surviving the deadlocks that still happen under load.

## Run

```bash
python src/deadlock_simulation.py
node src/deadlock-simulation.js
javac src/DeadlockSimulation.java && java -cp src DeadlockSimulation
```

No external dependencies — Python and JavaScript use only the stdlib; Java uses `java.util.concurrent`.

## Related

- Recipe: <https://stackpractices.com/recipes/deadlock-prevention-sql/>
