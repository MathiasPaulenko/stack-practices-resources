# Connection Pooling para bases de datos y clientes HTTP

Código companion de la receta de StackPractices:
https://stackpractices.com/es/recipes/connection-pooling/

## Archivos

| Archivo | Lenguaje | Descripción |
| ------- | -------- | ----------- |
| `pg_pool.py` | Python | Pool de PostgreSQL con psycopg2, context manager, monitoreo |
| `http_pool.js` | JavaScript | Pool de cliente HTTP con axios + keep-alive agents |
| `HikariPoolExample.java` | Java | Pool HikariCP con query, monitoreo y limpieza |
| `test_pg_pool.py` | Python | Tests unitarios para pg_pool.py (7 tests, mockeados) |

## Ejecutar los tests de Python

```bash
pip install pytest psycopg2-binary
pytest test_pg_pool.py -v
```

## Ejecutar el ejemplo de Python

```bash
pip install psycopg2-binary
python pg_pool.py
```

## Ejecutar el ejemplo de JavaScript

```bash
npm install axios
node http_pool.js
```

## Ejecutar el ejemplo de Java

```bash
javac -cp hikariCP.jar HikariPoolExample.java
java -cp .:hikariCP.jar HikariPoolExample
```

## Puntos clave

- Dimensioná el pool según la concurrencia real, no los núcleos de CPU.
- Siempre liberá conexiones en un bloque `finally` o context manager.
- Mantené `connectionTimeout` menor que el timeout de tu petición.
- Monitoreá conexiones activas, inactivas y en espera.
- Activá keep-alive en clientes HTTP para reutilizar conexiones TLS.