# Guía Completa de Optimización de Consultas SQL - Ejemplos de Código

Ejemplos SQL y Python ejecutables de la guía:
<https://stackpractices.com/es/guides/complete-guide-sql-query-optimization/>

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `schema.sql` | Esquema PostgreSQL + datos semilla (users, orders, products, comments) — ejecútalo primero |
| `slow_queries.sql` | pg_stat_statements, pg_stat_activity, auditorías de índices/caché + slow log / Performance Schema de MySQL |
| `indexes.sql` | Índices de cobertura, parciales, compuestos, funcionales y de trigramas con EXPLAIN |
| `rewrites.sql` | Ocho pares de reescritura mal-vs-bien para comparar con EXPLAIN ANALYZE |
| `materialized_view.sql` | Creación de vistas materializadas, refresco CONCURRENTLY y el workaround con tabla resumen + evento en MySQL |
| `partitioning.sql` | Particiones por rango y por lista con poda de particiones visible |
| `n_plus_one.py` | Demo offline con sqlite3: N+1 vs JOIN, con contador de consultas |
| `pooling.py` | ThreadedConnectionPool de psycopg2 + esqueleto de pool con asyncpg |
| `redis_cache.py` | Caché de consultas en Redis con TTL |

## Comprobación offline

```bash
python n_plus_one.py 200
```

Imprime el número de consultas y el tiempo del bucle N+1 frente al JOIN único.

## Setup en vivo (PostgreSQL)

```bash
psql -d sandbox -f schema.sql
psql -d sandbox -f indexes.sql
psql -d sandbox -f materialized_view.sql
psql -d sandbox -f partitioning.sql
```

`slow_queries.sql` necesita `pg_stat_statements` en
`shared_preload_libraries`. `pooling.py` y `redis_cache.py` necesitan un
PostgreSQL corriendo (y Redis para el segundo) — ver `requirements.txt`.
