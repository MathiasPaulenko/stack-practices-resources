# Serverless DB Connection Pooling — Companion Examples

Runnable examples for the [Serverless DB Connection Pooling Pattern](https://stackpractices.com/patterns/serverless-db-connection-pooling-pattern/).

## Files

- `lambda_pgbouncer.py` — Python Lambda reusing one warm psycopg2 connection through PgBouncer (transaction pooling).
- `lambda_rds_proxy.js` — Node.js `pg` Pool with `max: 1` behind RDS Proxy.
- `HikariLambda.java` — Java Lambda with HikariCP `maximumPoolSize=1` and `prepareThreshold=0`.
- `pgbouncer.ini` — Reference PgBouncer config (`pool_mode = transaction`).

## Key rule

One connection per Lambda container. The external pooler does the multiplexing — setting `max > 1` reintroduces the connection-exhaustion problem the pattern solves.

## Env vars

`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — no defaults for credentials.
