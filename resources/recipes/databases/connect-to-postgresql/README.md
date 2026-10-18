# Connect to PostgreSQL

Runnable companion for the [Connect to PostgreSQL](https://stackpractices.com/recipes/connect-to-postgresql/) recipe: connection pool, parameterized queries, transactions, retry with backoff, and bulk `COPY` inserts in Python, JavaScript, and Java.

## Contents

- `docker-compose.yml` + `init.sql` — local PostgreSQL 16 with seed data
- `connect.py` — `psycopg2` pool + context manager + `tenacity` retry + `COPY`
- `connect.js` — `pg` Pool + transaction (`BEGIN`/`COMMIT`/`ROLLBACK`) + `pool.end()`
- `PostgresPool.java` — HikariCP pool + prepared statements + batch insert
- `requirements.txt`, `package.json`

## Run it

```bash
docker compose up -d          # starts PostgreSQL on localhost:5432

# Python
pip install -r requirements.txt
python connect.py

# JavaScript
npm install
npm start

# Java — needs postgresql + HikariCP jars on the classpath
javac -cp ".:postgresql.jar:HikariCP.jar" PostgresPool.java
java -cp ".:postgresql.jar:HikariCP.jar:slf4j-api.jar" PostgresPool
```

All examples read `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` (and `PGSSLMODE` / `PGJDBC_URL` where applicable) from the environment — no credentials in code.

## Security notes

- `sslmode=prefer` / `ssl: false` is for local development only. In production use `verify-full` with your CA certificate and never set `rejectUnauthorized: false`.
- Always drain pools on shutdown: `pool.end()` in Node, `pool.closeall()` in Python, `ds.close()` in Java.
