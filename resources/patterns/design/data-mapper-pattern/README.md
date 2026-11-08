# Data Mapper Pattern — Companion Files

Runnable examples for the [Data Mapper Pattern](https://stackpractices.com/patterns/data-mapper-pattern/) resource on StackPractices.

## Contents

| File | Language | What it shows |
| ---- | -------- | ------------- |
| `src/user_mapper.py` | Python | `User` dataclass + `UserMapper` over `sqlite3`, using `conn.row_factory = sqlite3.Row` for named-column access. Runs out of the box. |
| `src/DataMapperDemo.java` | Java | Single-file demo: `User` domain class, `UserMapper` over JDBC (`PreparedStatement`, generated keys), and a `main` entry point. |
| `src/user-mapper.js` | JavaScript | `UserMapper` over Node's built-in `node:sqlite` (`DatabaseSync`) — no dependencies, synchronous API. |
| `schema.sql` | SQL | Minimal `users` table used by all three mappers. |

## Run

```bash
# Python
python src/user_mapper.py

# JavaScript (Node 22.5+; on Node 22 pass --experimental-sqlite)
node src/user-mapper.js

# Java (needs the SQLite JDBC driver on the classpath)
javac src/DataMapperDemo.java && java -cp src DataMapperDemo
```

Each demo creates an in-memory `users` table, inserts a `User` through the mapper, and reads it back — the domain object never touches the connection.
