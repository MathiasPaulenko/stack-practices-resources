# Handle Database Deadlocks and Retries — Companion Resources

Runnable examples for the [Handle Database Deadlocks and Retries](https://stackpractices.com/recipes/database-deadlocks-retries/) recipe.

## Files

| File | Language | Description |
| ------ | -------- | ----------- |
| `transfer_funds.py` | Python | SQLAlchemy deadlock-safe transfer with retry decorator |
| `transfer_funds.js` | JavaScript | Knex.js deadlock-safe transfer with retry wrapper |
| `TransferFunds.java` | Java | JDBC SQL Server transfer with UPDLOCK + HOLDLOCK |
| `deadlock_test.py` | Python | Two-thread test that reproduces a deadlock and verifies the victim pattern |
| `README.md` | — | English instructions |
| `README.es.md` | — | Spanish instructions |

## Quick Start

### Python

```bash
pip install sqlalchemy psycopg2-binary
python transfer_funds.py
python deadlock_test.py  # requires a PostgreSQL database and `accounts` table
```

### JavaScript

```bash
npm install knex mysql2
node transfer_funds.js  # update connection config
```

### Java

```bash
javac TransferFunds.java && java TransferFunds  # update JDBC connection string
```

## Key Points

- Always lock rows in the same order (e.g., by primary key ascending).
- Use `SELECT ... FOR UPDATE` only for rows you will modify.
- Add exponential backoff with jitter to retry logic.
- Keep transactions short and avoid I/O inside them.
- Log and alert on repeated deadlocks.
