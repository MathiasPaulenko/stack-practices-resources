# Event Sourcing en una Base de Datos Relacional

Código companion para la [receta de event sourcing](https://stackpractices.com/es/recipes/event-sourcing-relational/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `event_store.py` | Python | Clase EventStore con concurrencia optimista, replay y snapshots (PostgreSQL) |
| `event_store.js` | JavaScript | Clase EventStore con pool de conexiones (MySQL) |
| `EventStoreJava.java` | Java | EventStore con Spring y JPA (SQL Server) |
| `schema.sql` | SQL | DDL para tablas events y snapshots (PostgreSQL + variante MySQL) |
| `test_event_store.py` | Python | Tests unitarios para EventStore Python (mocked, sin DB) |

## Ejecutar los Tests

```bash
cd resources/recipes/databases/event-sourcing-relational
python -m pytest test_event_store.py -v
```

Los tests mockean `psycopg2` por lo que no requieren conexión a base de datos.

## Setup de Esquema

Para PostgreSQL:

```bash
psql -d tu_base -f schema.sql
```

Para MySQL, descomentá la variante MySQL al final de `schema.sql`.

## Uso (Python)

```python
import psycopg2
from event_store import EventStore, rebuild_account_balance

conn = psycopg2.connect("dbname=test user=postgres")
store = EventStore(conn)

# Agregar eventos
store.append("acc-1", "Deposit", {"amount": 50})
store.append("acc-1", "Withdrawal", {"amount": 20}, expected_version=1)

# Reconstruir estado
balance = rebuild_account_balance(conn, "acc-1")
print(f"Balance: {balance}")
```
