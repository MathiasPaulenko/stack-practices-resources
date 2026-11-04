# Data Quality Guide — Companion Resources

Runnable data-quality assets for the [Data Quality Guide](https://stackpractices.com/guides/complete-guide-data-quality/).

| File | What |
|------|------|
| profile_dataset.py | ydata-profiling report + manual pandas profile |
| orders_suite.py | GX 1.x suite + validation definition flow |
| pandera_schemas.py | Pandera DataFrameSchema with lazy validation |
| orders_checks.yml | Soda Core checks (warn/fail, freshness, anomaly) |
| anomaly_detection.py | z-score anomaly detection functions |
| pipeline_with_quality.py | Airflow DAG with quality gates + PostgresHook |
