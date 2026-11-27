# Estrategias de particionamiento de tablas SQL — Scripts de apoyo

Scripts ejecutables de PostgreSQL que acompañan la receta
[Particionar tablas SQL grandes por fecha, rango o lista](https://stackpractices.com/es/recipes/sql-partitioning-strategies/).

## Archivos

| Script | Qué hace |
|--------|----------|
| `range-partition-by-month.sql` | Particionamiento mensual por rango (default para series temporales) |
| `list-partition-by-region.sql` | Particionamiento por lista + partición por defecto |
| `hash-partition.sql` | Particionamiento hash para distribución pareja |
| `composite-subpartitioning.sql` | Sub-particionamiento rango + lista |
| `verify-partition-pruning.sql` | Chequeos de poda estática/dinámica con EXPLAIN |
| `detach-and-archive.sql` | Archivado instantáneo con DETACH PARTITION |
| `pg-partman-automation.sql` | Creación/rotación automática de particiones |
| `partition-indexes.sql` | Índices de la padre que se propagan a las hijas |
| `monitor-partition-sizes.sql` | Monitoreo de particiones calientes y tamaños |
| `foreign-keys-partitioned.sql` | FKs que referencian tablas particionadas (PG12+) |

## Uso

Requiere PostgreSQL 10+ (particionamiento declarativo); `pg_partman` y
`DETACH ... CONCURRENTLY` necesitan versiones/extensiones más nuevas.

```bash
psql -d tu_db -f range-partition-by-month.sql
```

Recuerda: la clave de partición tiene que ser parte de la clave primaria, y
los constraints `UNIQUE` también deben incluirla. Verifica siempre la poda
con `verify-partition-pruning.sql` después de configurar un layout nuevo.

## Más recursos

- Receta (EN): https://stackpractices.com/recipes/sql-partitioning-strategies/
- Biblioteca completa: https://mathiaspaulenko.github.io/stack-practices-resources/
