# Migraciones de columnas sin downtime — Scripts de apoyo

Scripts ejecutables de PostgreSQL que acompañan la receta
[Migración de columnas sin downtime](https://stackpractices.com/es/recipes/sql-migration-zero-downtime/).

## Archivos

| Script | Qué hace |
|--------|----------|
| `rename-column-zero-downtime.sql` | Renombre expand-contract completo con trigger de sincronización |
| `change-type-zero-downtime.sql` | Cambio de tipo (ej: dólares a centavos) con trigger de conversión |
| `batch-backfill.sql` | Bucle de relleno por lotes con `pg_sleep` |
| `verify-parity.sql` | Chequeos de mismatch y NULL antes del cutover |
| `app-dual-write.sql` | Migración con dual-write a nivel aplicación |
| `view-migration.sql` | Renombre detrás de una vista de compatibilidad |
| `not-valid-constraint.sql` | Constraint `NOT VALID` + `VALIDATE` sin bloqueo largo |
| `foreign-key-migration.sql` | Migrar una columna FK de forma segura |
| `shadow-column-rollback.sql` | Columna shadow para rollback rápido |
| `lock-timeouts.sql` | Protección con `statement_timeout`/`lock_timeout` + monitoreo de locks |

## Uso

Requiere PostgreSQL 10+ (bloques `DO` con `DECLARE` y constraints `NOT VALID`).

```bash
psql -d tu_db -f rename-column-zero-downtime.sql
```

Ensaya siempre en una copia de staging, mantén el trigger de sincronización
hasta que todas las instancias corran el código nuevo, y nunca elimines
la columna vieja hasta que `verify-parity.sql` devuelva cero mismatches.

## Más recursos

- Receta (EN): https://stackpractices.com/recipes/sql-migration-zero-downtime/
- Biblioteca completa: https://mathiaspaulenko.github.io/stack-practices-resources/
