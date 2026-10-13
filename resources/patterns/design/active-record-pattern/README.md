# Active Record Pattern — Companion Files

Runnable examples for the pattern:
<https://stackpractices.com/patterns/active-record-pattern/>

## Files

| File | What it shows |
|------|---------------|
| `active-record-python.py` | Complete runnable demo: create table, `save()` (insert → lastrowid), `find_by_id`, `find_all`, `delete` over sqlite3 |
| `ActiveRecordUser.java` | Java JDBC version with generated-key handling and `toString()` |
| `active-record-javascript.js` | Async Active Record with an injected connection (`db.run`/`get`/`all`, e.g. the `sqlite` package) |

## The pattern in one line

**An object is a row; `user.save()` writes it to the database with no separate data-access layer.**

## Key takeaways

- Minimal boilerplate — the framework conventions (Rails, Django, Eloquent, Sequelize) do the mapping for you.
- The domain model knows SQL exists: that coupling is the price of the simplicity.
- Testing without a database is hard — use in-memory SQLite or extract logic into plain service objects.
- When you need multi-entity transactions or rich domain logic, look at Data Mapper / Repository / Unit of Work.
