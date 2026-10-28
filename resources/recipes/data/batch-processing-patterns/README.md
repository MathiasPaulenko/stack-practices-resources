# Batch Processing Patterns — Runnable Examples

Companion code for [Batch Processing Patterns](https://stackpractices.com/recipes/batch-processing-patterns/).

- `batch_processor.py` — `BatchProcessor` class: chunked processing, bounded retries with backoff, atomic checkpoint file, dead-letter list. Includes a 5,000-record demo.
- `schema.sql` — PostgreSQL DDL for `job_runs`, `job_checkpoints`, `job_watermarks`, `dead_letters`, and `reconciliation_results`.
- `test_batch_processor.py` — pytest suite covering full processing, transient-retry recovery, dead-letter routing, and checkpoint resume.

Run:

```bash
python batch_processor.py          # demo run
pytest test_batch_processor.py     # tests (requires pytest)
```
