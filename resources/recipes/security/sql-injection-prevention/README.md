# SQL Injection Prevention — Companion Code

Runnable examples for the recipe [Prevent SQL Injection Attacks](https://stackpractices.com/recipes/sql-injection-prevention/).

## Contents

| File | What it shows |
| --- | --- |
| `python/parameterized_queries.py` | Vulnerable vs parameterized sqlite3 queries, plus an ORDER BY allowlist. Runs standalone — no setup needed. |
| `node/parameterized_queries.js` | `pg` driver examples: `$1` placeholders, LIKE wildcard escaping, and dynamic sorting via allowlist. Needs a `DATABASE_URL`. |
| `java/PreparedStatementExample.java` | JDBC `PreparedStatement` with `?` placeholders and a validated dynamic `ORDER BY`. |
| `testing/sqlmap-cheatsheet.sh` | sqlmap commands for testing **your own** staging environments. |

## Quick start

```bash
# Python (zero dependencies, in-memory DB)
python python/parameterized_queries.py
# unsafe: returns every row — injection succeeded
# safe:   returns [] — same input became a literal value

# Node (requires `pg` and a reachable Postgres)
npm install pg
DATABASE_URL=postgres://user:pass@localhost/db node -e \
  "require('./node/parameterized_queries').getUsers().then(console.log)"
```

## Source

- https://stackpractices.com/recipes/sql-injection-prevention/
- https://stackpractices.com/es/recipes/sql-injection-prevention/
