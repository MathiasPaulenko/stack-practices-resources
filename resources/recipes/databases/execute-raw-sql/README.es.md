# Ejecutar SQL Crudo

Demos ejecutables de SQL crudo seguro. Todos los ejemplos usan SQLite embebido para correr sin servidor de base de datos — los patrones de consultas parametrizadas son idénticos en psycopg2 (`%s`), pg (`$1`) y JDBC (`?`).

## Archivos

| Archivo | Lenguaje | Qué muestra |
|---------|----------|-------------|
| `raw_sql.py` | Python | Placeholders `?` parametrizados, cláusulas `IN` dinámicas, whitelist de identificadores, bulk insert con `executemany` |
| `raw_sql.js` | JavaScript | Los mismos patrones con `node:sqlite` (`DatabaseSync`) — sin dependencias |
| `RawSQL.java` | Java | Binding de parámetros con `PreparedStatement`, generated keys, placeholders `IN` dinámicos |

## Ejecutar

```bash
python raw_sql.py      # Python 3.x, solo stdlib
node raw_sql.js        # Node.js 22+ (node:sqlite integrado)
javac RawSQL.java      # Requiere un driver JDBC para ejecutar de verdad
```

## Punto clave

Los valores siempre se pueden parametrizar; los identificadores (nombres de tabla/columna) no. Cuando un nombre debe ser dinámico, valídalo contra una whitelist — nunca interpole input sin verificar.

Fuente: https://stackpractices.com/recipes/execute-raw-sql/
