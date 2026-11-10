# Execute Raw SQL

Runnable demos of safe raw SQL execution. All examples use embedded SQLite so they run without a database server — the parameterized-query patterns are identical in psycopg2 (`%s`), pg (`$1`), and JDBC (`?`).

## Files

| File | Language | What it shows |
|------|----------|---------------|
| `raw_sql.py` | Python | Parameterized `?` placeholders, dynamic `IN` clauses, identifier whitelisting, `executemany` bulk insert |
| `raw_sql.js` | JavaScript | Same patterns with `node:sqlite` (`DatabaseSync`) — no dependencies needed |
| `RawSQL.java` | Java | `PreparedStatement` parameter binding, generated keys, dynamic `IN` placeholders |

## Run

```bash
python raw_sql.py      # Python 3.x, stdlib only
node raw_sql.js        # Node.js 22+ (built-in node:sqlite)
javac RawSQL.java      # Requires a JDBC driver to actually execute
```

## Key point

Values can always be parameterized; identifiers (table/column names) cannot. When a name must be dynamic, validate it against a whitelist — never interpolate unchecked input.

Source: https://stackpractices.com/recipes/execute-raw-sql/
