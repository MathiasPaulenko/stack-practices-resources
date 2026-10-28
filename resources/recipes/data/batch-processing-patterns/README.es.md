# Patrones de Procesamiento por Lotes — Ejemplos ejecutables

Código complementario de [Patrones de Procesamiento por Lotes](https://stackpractices.com/es/recipes/batch-processing-patterns/).

- `batch_processor.py` — clase `BatchProcessor`: procesamiento en chunks, reintentos acotados con backoff, archivo de checkpoint atómico y lista de dead letters. Incluye una demo con 5.000 registros.
- `schema.sql` — DDL de PostgreSQL para `job_runs`, `job_checkpoints`, `job_watermarks`, `dead_letters` y `reconciliation_results`.
- `test_batch_processor.py` — suite de pytest que cubre el procesamiento completo, la recuperación ante fallos transitorios, el enrutado a dead letters y la reanudación desde checkpoint.

Ejecutar:

```bash
python batch_processor.py          # demo
pytest test_batch_processor.py     # tests (requiere pytest)
```
