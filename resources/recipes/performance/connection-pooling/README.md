# Connection Pooling for Databases and HTTP Clients

Companion code for the StackPractices recipe:
https://stackpractices.com/recipes/connection-pooling/

## Files

| File | Language | Description |
| ---- | -------- | ----------- |
| `pg_pool.py` | Python | PostgreSQL pool with psycopg2, context manager, monitoring |
| `http_pool.js` | JavaScript | HTTP client pool with axios + keep-alive agents |
| `HikariPoolExample.java` | Java | HikariCP pool with query, monitoring, and cleanup |
| `test_pg_pool.py` | Python | Unit tests for pg_pool.py (7 tests, mocked) |

## Running the Python tests

```bash
pip install pytest psycopg2-binary
pytest test_pg_pool.py -v
```

## Running the Python example

```bash
pip install psycopg2-binary
python pg_pool.py
```

## Running the JavaScript example

```bash
npm install axios
node http_pool.js
```

## Running the Java example

```bash
javac -cp hikariCP.jar HikariPoolExample.java
java -cp .:hikariCP.jar HikariPoolExample
```

## Key takeaways

- Size the pool to actual concurrency, not CPU cores.
- Always release connections in a `finally` block or context manager.
- Keep `connectionTimeout` shorter than your request timeout.
- Monitor active, idle, and waiting connections.
- Enable keep-alive for HTTP clients to reuse TLS connections.