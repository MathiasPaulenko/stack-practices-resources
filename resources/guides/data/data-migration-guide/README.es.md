# Guía de migración de datos — Código complementario

Complemento ejecutable para la [guía de migración de datos](https://stackpractices.com/es/guides/data-migration-guide/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `backfill_demo.py` | Demo completa en sqlite en memoria: doble escritura, backfill reanudable con checkpoints, re-ejecución idempotente, validación por conteos y campos |
| `schema-evolution.sql` | Expand-contract para columnas y división de tabla con trigger de doble escritura (PostgreSQL) |
| `migration-plan-template.md` | Plan de migración rellenable: fases, checklist de validación, plan de rollback |

## Ejecutar

```bash
python backfill_demo.py
# → dual-write created user 21 in both tables
# → backfill migrated 20 rows
# → backfill migrated 0 rows   (segunda ejecución: no-op — idempotencia)
# → validation passed: 21 rows, 0 mismatches
# → data-migration-guide demo OK
```

`schema-evolution.sql` está pensado para PostgreSQL — ejecútalo en una base de prueba para ver cómo el trigger mantiene `users` y `user_profiles` en sync.
