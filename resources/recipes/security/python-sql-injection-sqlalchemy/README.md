# SQL Injection Prevention with SQLAlchemy — Companion Code

Runnable SQLAlchemy examples showing the vulnerable pattern and the safe alternatives side by side, against an in-memory SQLite database.

## Files

| File | What it shows |
|---|---|
| `safe_queries.py` | Vulnerable f-string query vs `text()` bound params, ORM `select`, dynamic filters, `ORDER BY` whitelists, and `LIKE` wildcard escaping. Includes a smoke test in `__main__`. |

## Quick start

```bash
pip install -r requirements.txt
python safe_queries.py
# vulnerable: 2 rows leaked
# safe text(): None
# safe ORM: None
# injection via ORDER BY falls back to a whitelisted column
```

## Source

- https://stackpractices.com/recipes/python-sql-injection-sqlalchemy/
- https://stackpractices.com/es/recipes/python-sql-injection-sqlalchemy/
