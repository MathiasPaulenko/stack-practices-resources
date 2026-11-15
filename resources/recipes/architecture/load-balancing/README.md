# Load Balancing — Companion Code

Runnable implementations for the [Distribute Traffic with Load Balancing Algorithms](https://stackpractices.com/recipes/load-balancing/) recipe on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `load_balancer.py` | Consistent-hash ring with virtual nodes: after removing one of three nodes only ~1/N of keys remap, versus ~all of them with naive `hash % N`. Plus a smooth weighted round-robin that interleaves picks instead of bursting. Runs with plain Python 3. |
| `load-balancer.js` | Least-response-time balancer in Node.js: scores backends on rolling average latency plus a per-connection penalty, drains the fastest server, and stops routing to an unhealthy one. |
| `SmoothWeightedBalancer.java` | The Nginx smooth weighted round-robin in Java 17+: exact proportional shares, interleaved sequence (compare with the bursty block order). `javac` + `java`, no dependencies. |

## Quick start

```bash
python load_balancer.py
node load-balancer.js
javac SmoothWeightedBalancer.java && java SmoothWeightedBalancer
```

Expected output: the ring remaps ~1/3 of keys when one node leaves while
`hash % N` remaps most of them; the least-response-time picker favors the
20ms backend ~90% of the time and gives a dead one zero traffic; the
weighted selector produces an interleaved 5:3:1 sequence.

## What to adapt for production

- The ring's routing key is whatever identifies "same destination": user
  ID, session token, cache key — pick one that survives reconnects, not
  the client IP (mobile users change networks mid-session).
- Real least-response-time needs out-of-band health checks; latency alone
  can't distinguish "slow" from "dead". Pair `markUnhealthy` with an
  active probe like `GET /health`.
- Weighted round-robin assumes weights reflect capacity. Re-measure after
  hardware changes, and use `slow_start` semantics when a server rejoins
  so cold caches don't fold under a full share.
- These are client-side pickers. For infrastructure balancing, the recipe
  covers the equivalent Nginx (`least_conn`, `weight`, `backup`,
  `keepalive`), HAProxy, and Route 53 DNS configurations.
