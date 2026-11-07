# Data Access Object (DAO) Pattern — Companion Files

Runnable examples for the pattern:
<https://stackpractices.com/patterns/data-access-object-pattern/>

## Files

| File | What it shows |
|------|---------------|
| `dao-python.py` | Complete runnable demo: create table, `save()` (insert → lastrowid), `find_by_id`, `find_all`, `find_paginated`, `delete` over sqlite3 — plus a `FakeUserDao` for tests |
| `SqlUserDao.java` | Java JDBC version: interface + implementation, generated-key handling, `DataAccessException` wrapper, `main()` demo over in-memory SQLite |
| `dao-javascript.js` | Async DAO with an injected `sqlite`/`sqlite3` handle (`db.get`/`all`/`run`) — plus a `FakeUserDao` for tests |

## The pattern in one line

**Business code talks to a CRUD interface; the DAO owns the SQL, the connection, and the row mapping.**

## Key takeaways

- Inject the connection — every example takes a ready handle in the constructor, so tests can pass in-memory SQLite and production can pass a pooled connection.
- Wrap driver exceptions once (`DataAccessException`) so callers handle "the save failed", not "JDBC failed with SQLState 23505".
- A connection per query is the classic anti-pattern — let a pool own the lifecycle.
- When methods start looking like `findOverdueInvoices` instead of `insert`/`update`, you've outgrown DAO — that's Repository territory.
