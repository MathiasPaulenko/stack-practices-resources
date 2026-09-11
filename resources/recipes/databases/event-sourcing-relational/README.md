# Event Sourcing in a Relational Database

Companion code for the [Event Sourcing recipe](https://stackpractices.com/recipes/event-sourcing-relational/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `event_store.py` | Python | EventStore class with optimistic concurrency, replay, and snapshots (PostgreSQL) |
| `event_store.js` | JavaScript | EventStore class with pool-based connections (MySQL) |
| `EventStoreJava.java` | Java | Spring-based EventStore with JPA (SQL Server) |
| `schema.sql` | SQL | DDL for events and snapshots tables (PostgreSQL + MySQL variant) |
| `test_event_store.py` | Python | Unit tests for the Python EventStore (mocked, no DB required) |

## Running the Tests

```bash
cd resources/recipes/databases/event-sourcing-relational
python -m pytest test_event_store.py -v
```

The tests mock `psycopg2` so no database connection is required.

## Schema Setup

For PostgreSQL:

```bash
psql -d your_database -f schema.sql
```

For MySQL, uncomment the MySQL variant at the bottom of `schema.sql`.

## Usage (Python)

```python
import psycopg2
from event_store import EventStore, rebuild_account_balance

conn = psycopg2.connect("dbname=test user=postgres")
store = EventStore(conn)

# Append events
store.append("acc-1", "Deposit", {"amount": 50})
store.append("acc-1", "Withdrawal", {"amount": 20}, expected_version=1)

# Rebuild state
balance = rebuild_account_balance(conn, "acc-1")
print(f"Balance: {balance}")
```
