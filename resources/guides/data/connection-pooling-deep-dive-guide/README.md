# Connection Pooling — Companion Resources

Runnable configs referenced by
[Connection Pooling: Optimize Database Connections for Scale](https://stackpractices.com/guides/connection-pooling-deep-dive-guide/).

| File | Purpose |
| --- | --- |
| `pgbouncer.ini` | Transaction-mode PgBouncer config with reserve pool and admin console notes |
| `HikariPoolConfig.java` | Reference HikariCP setup: sizing, timeouts, leak detection, prepared-statement cache |
| `pool_sqlalchemy.py` | SQLAlchemy engine with `pool_size`, `pre_ping`, and a leak anti-pattern example |
| `pool_monitor.py` | Prometheus exporter sketch for pool metrics (active/idle/waiters/timeouts) |
| `lambda-pool.js` | Warm-reuse pool for AWS Lambda pointed at a proxy |

Sizing rule of thumb used throughout: `pool_size × instances < max_connections − headroom`,
or put PgBouncer in front and treat the app pool as a concurrency limiter.
