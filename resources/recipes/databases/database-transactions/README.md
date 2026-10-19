# database-transactions — Companion Resources

Companion code for [Database Transactions: Python, JavaScript & Java Examples](https://stackpractices.com/recipes/database-transactions/).

## Files

| File | Language | Purpose |
|------|----------|---------|
| `transfer_psycopg2.py` | Python | Transfer with atomic balance guard, savepoints, `SELECT ... FOR UPDATE` |
| `deadlock_retry.py` | Python | Retry wrapper for `40P01` deadlocks with exponential backoff |
| `transfer_node.js` | JavaScript | Same transfer with `pg` Pool plus deadlock retry helper |
| `TransferJDBC.java` | Java | Plain JDBC transaction with `setAutoCommit(false)` |
| `advisory_locks.sql` | SQL | `pg_advisory_lock`/`xact`/`try` variants and LISTEN/NOTIFY |
| `transaction_monitoring.sql` | SQL | Idle-in-transaction detection, lock blockers, per-DB rates |
| `README.md` / `README.es.md` | — | This doc |

## Requirements

- Python 3.10+ with `psycopg2-binary`
- Node.js 18+ with `pg`
- Java 17+ with the PostgreSQL JDBC driver
- PostgreSQL 14+ running locally or `DATABASE_URL` set

## Quick start

### Python

```bash
pip install psycopg2-binary
export DATABASE_URL="postgresql://user:pass@localhost/db"
python transfer_psycopg2.py
python deadlock_retry.py
```

### Node.js

```bash
npm install pg
export DATABASE_URL="postgresql://user:pass@localhost/db"
node transfer_node.js
```

### Java

```bash
javac TransferJDBC.java
java -cp .:postgresql-<version>.jar TransferJDBC
```

### SQL

Run the monitoring and advisory lock snippets in `psql` or any SQL client
against your database.
