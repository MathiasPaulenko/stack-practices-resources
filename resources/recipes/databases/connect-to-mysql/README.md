# Connect to MySQL

Runnable companion for the [Connect to MySQL](https://stackpractices.com/recipes/connect-to-mysql/) recipe: connection pool, parameterized queries, transactions, retry with backoff, and batch inserts in Python, JavaScript, and Java.

## Contents

- `docker-compose.yml` + `init.sql` — local MySQL 8.4 with seed data
- `connect.py` — `mysql-connector-python` pool + context manager + `tenacity` retry
- `connect.js` — `mysql2` Pool + transaction (`beginTransaction`/`commit`/`rollback`) + keepalive + `pool.end()`
- `MySQLPool.java` — HikariCP pool + prepared statements + batch insert
- `requirements.txt`, `package.json`

## Run it

```bash
docker compose up -d          # starts MySQL on localhost:3306

# Python
pip install -r requirements.txt
python connect.py

# JavaScript
npm install
npm start

# Java — needs mysql-connector-j + HikariCP jars on the classpath
javac -cp ".:mysql-connector-j.jar:HikariCP.jar" MySQLPool.java
java -cp ".:mysql-connector-j.jar:HikariCP.jar:slf4j-api.jar" MySQLPool
```

## Notes

- Credentials come from env vars (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) with local-dev defaults. Never hardcode production credentials.
- Local dev runs without SSL. In production enable `ssl_ca` / `sslMode=VERIFY_CA` and point the driver at a current CA bundle — on AWS RDS, IAM database authentication replaces stored passwords.
- The pool's idle timeout should stay below the server's `wait_timeout` (28800s by default) or idle connections come back dead.
- Use `utf8mb4` charset — MySQL's `utf8` is 3-byte only and silently mangles 4-byte characters.
