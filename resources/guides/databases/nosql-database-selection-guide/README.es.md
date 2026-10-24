# Guía de Selección de Bases de Datos NoSQL — Companion

Esquemas y ejemplos ejecutables de la [Guía de Selección de Bases de Datos NoSQL](https://stackpractices.com/es/guides/nosql-database-selection-guide/) en StackPractices.com.

## Archivos

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| `mongodb_example.js` | mongosh | Documento de producto embebido + consulta anidada |
| `dynamodb_example.py` | Python | Get y query por partition/sort key con boto3 |
| `redis_commands.sh` | Bash | TTL de caché, rate limiting atómico, sorted set de feed |
| `cassandra.cql` | CQL | Tablas query-first: lecturas de sensores y posts_by_user |

## Uso

Cada archivo corre contra su propio motor — son implementaciones de referencia por store de los ejemplos de la guía, no una sola app:

```bash
mongosh nosql_examples mongodb_example.js
python dynamodb_example.py          # necesita una tabla Users (ver docstring)
redis-cli < redis_commands.sh
cqlsh -f cassandra.cql
```

## Notas

- La matriz de decisión de la guía es el entregable real — estos archivos existen para que los ejemplos se puedan ejecutar, no solo leer.
- El esquema de Cassandra es query-first por diseño: `posts_by_user` existe para servir "posts recientes por usuario", no para modelar posts en abstracto.
