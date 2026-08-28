# Manejar deadlocks y reintentos en bases de datos — Recursos Companion

Ejemplos ejecutables para la receta [Manejar deadlocks y reintentos en bases de datos](https://stackpractices.com/es/recipes/database-deadlocks-retries/).

## Archivos

| Archivo | Lenguaje | Descripción |
| --------- | -------- | ----------- |
| `transfer_funds.py` | Python | Transferencia segura con SQLAlchemy y decorator de reintento |
| `transfer_funds.js` | JavaScript | Transferencia segura con Knex.js y wrapper de reintento |
| `TransferFunds.java` | Java | Transferencia con JDBC SQL Server y UPDLOCK + HOLDLOCK |
| `deadlock_test.py` | Python | Test de dos threads que reproduce un deadlock y verifica la víctima |
| `README.md` | — | Instrucciones en inglés |
| `README.es.md` | — | Instrucciones en español |

## Inicio Rápido

### Python

```bash
pip install sqlalchemy psycopg2-binary
python transfer_funds.py
python deadlock_test.py  # requiere PostgreSQL y tabla `accounts`
```

### JavaScript

```bash
npm install knex mysql2
node transfer_funds.js  # actualizar config de conexión
```

### Java

```bash
javac TransferFunds.java && java TransferFunds  # actualizar JDBC connection string
```

## Puntos Clave

- Siempre lockea filas en el mismo orden (e.g., clave primaria ascendente).
- Usá `SELECT ... FOR UPDATE` solo para filas que modificarás.
- Agregá backoff exponencial con jitter a la lógica de reintento.
- Mantené las transacciones cortas y evitá I/O dentro de ellas.
- Registrá y alertá sobre deadlocks repetidos.
