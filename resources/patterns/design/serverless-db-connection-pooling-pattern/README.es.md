# Patrón Serverless DB Connection Pooling — Ejemplos Companion

Ejemplos ejecutables del [Patrón Serverless DB Connection Pooling](https://stackpractices.com/es/patterns/serverless-db-connection-pooling-pattern/).

## Archivos

- `lambda_pgbouncer.py` — Lambda Python que reutiliza una conexión psycopg2 caliente a través de PgBouncer (transaction pooling).
- `lambda_rds_proxy.js` — Pool de `pg` en Node.js con `max: 1` detrás de RDS Proxy.
- `HikariLambda.java` — Lambda Java con HikariCP `maximumPoolSize=1` y `prepareThreshold=0`.
- `pgbouncer.ini` — Configuración de referencia de PgBouncer (`pool_mode = transaction`).

## Regla clave

Una conexión por contenedor Lambda. El pooler externo hace la multiplexación — poner `max > 1` reintroduce el problema de agotamiento que el patrón resuelve.

## Variables de entorno

`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — sin defaults para credenciales.
