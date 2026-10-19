# database-transactions — Recursos complementarios

Código complementario para [Transacciones de Base de Datos en Python, JS y Java](https://stackpractices.com/es/recipes/database-transactions/).

## Archivos

| Archivo | Lenguaje | Propósito |
|---------|----------|-----------|
| `transfer_psycopg2.py` | Python | Transferencia con guard atómico de saldo, savepoints, `SELECT ... FOR UPDATE` |
| `deadlock_retry.py` | Python | Wrapper de reintento para deadlocks `40P01` con backoff exponencial |
| `transfer_node.js` | JavaScript | La misma transferencia con Pool de `pg` más helper de reintento |
| `TransferJDBC.java` | Java | Transacción JDBC plana con `setAutoCommit(false)` |
| `advisory_locks.sql` | SQL | Variantes `pg_advisory_lock`/`xact`/`try` y LISTEN/NOTIFY |
| `transaction_monitoring.sql` | SQL | Detección de idle-in-transaction, bloqueos, tasas por base |
| `README.md` / `README.es.md` | — | Esta documentación |

## Requisitos

- Python 3.10+ con `psycopg2-binary`
- Node.js 18+ con `pg`
- Java 17+ con el driver JDBC de PostgreSQL
- PostgreSQL 14+ corriendo localmente o `DATABASE_URL` definida

## Inicio rápido

### Python

```bash
pip install psycopg2-binary
export DATABASE_URL="postgresql://user:pass@localhost/db"
python transfer_psycopg2.py
python deadlock_retry.py
```

### Node.js

```bash
npm install pg
export DATABASE_URL="postgresql://user:pass@localhost/db"
node transfer_node.js
```

### Java

```bash
javac TransferJDBC.java
java -cp .:postgresql-<version>.jar TransferJDBC
```

### SQL

Ejecuta los snippets de monitoreo y advisory locks en `psql` o cualquier
cliente SQL contra tu base de datos.
