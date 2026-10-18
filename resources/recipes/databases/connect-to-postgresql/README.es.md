# Conectar a PostgreSQL

Companion ejecutable de la receta [Conectar a PostgreSQL](https://stackpractices.com/es/recipes/connect-to-postgresql/): pool de conexiones, consultas parametrizadas, transacciones, reintentos con backoff e inserts masivos con `COPY` en Python, JavaScript y Java.

## Contenido

- `docker-compose.yml` + `init.sql` — PostgreSQL 16 local con datos de ejemplo
- `connect.py` — pool de `psycopg2` + context manager + retry con `tenacity` + `COPY`
- `connect.js` — `pg` Pool + transacción (`BEGIN`/`COMMIT`/`ROLLBACK`) + `pool.end()`
- `PostgresPool.java` — pool HikariCP + prepared statements + insert por lotes
- `requirements.txt`, `package.json`

## Ejecución

```bash
docker compose up -d          # levanta PostgreSQL en localhost:5432

# Python
pip install -r requirements.txt
python connect.py

# JavaScript
npm install
npm start

# Java — necesita los jars de postgresql y HikariCP en el classpath
javac -cp ".:postgresql.jar:HikariCP.jar" PostgresPool.java
java -cp ".:postgresql.jar:HikariCP.jar:slf4j-api.jar" PostgresPool
```

Todos los ejemplos leen `PGHOST`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` (y `PGSSLMODE` / `PGJDBC_URL` donde aplica) del entorno — sin credenciales en el código.

## Notas de seguridad

- `sslmode=prefer` / `ssl: false` es solo para desarrollo local. En producción usa `verify-full` con tu certificado CA y nunca `rejectUnauthorized: false`.
- Drena siempre los pools al apagar: `pool.end()` en Node, `pool.closeall()` en Python, `ds.close()` en Java.
