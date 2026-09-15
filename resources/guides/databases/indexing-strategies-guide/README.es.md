# Estrategias de Indexación de Bases de Datos — Recursos Companion

Repositorio companion para la [Guía de Estrategias de Indexación](https://stackpractices.com/es/guides/indexing-strategies-guide/).

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `unused-indexes-audit.sql` | Script de auditoría trimestral para encontrar y dropear índices no usados (PostgreSQL + MySQL) |
| `create-index-concurrently-examples.sql` | Ejemplos de `CREATE INDEX CONCURRENTLY` seguros para producción (PostgreSQL + MySQL 8+) |
| `index-monitoring-queries.sql` | Queries para trackear uso de índices, cache hit ratio y bloat |

## Uso

1. **Auditar índices no usados trimestralmente:**
   ```bash
   psql -d tu_db -f unused-indexes-audit.sql
   ```

2. **Construir índices seguro en producción:**
   ```bash
   psql -d tu_db -f create-index-concurrently-examples.sql
   ```

3. **Monitorear salud de índices:**
   ```bash
   psql -d tu_db -f index-monitoring-queries.sql
   ```

## Requisitos

- PostgreSQL 12+ (para `CONCURRENTLY`, `pgstattuple`)
- MySQL 8+ (para `ALGORITHM=INPLACE`)
- Extensión `pgstattuple` para análisis de bloat: `CREATE EXTENSION pgstattuple;`

## Guía relacionada

- [Estrategias de Indexación — Desde B-Trees hasta BRIN](https://stackpractices.com/es/guides/indexing-strategies-guide/)
- [Versión en inglés](https://stackpractices.com/guides/indexing-strategies-guide/)
