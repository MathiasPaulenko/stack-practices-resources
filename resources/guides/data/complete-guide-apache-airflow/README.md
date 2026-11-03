# Apache Airflow — Companion

Runnable DAG examples from [Apache Airflow: DAGs, Operators, Scheduling](https://stackpractices.com/guides/complete-guide-apache-airflow/).

## Files

- `core_dag.py` — classic ETL DAG (Bash + Python operators)
- `taskflow_dag.py` — TaskFlow API ETL with idempotent Postgres upsert
- `common_operators.py` — Bash, Python, Email, Snowflake, Spark, EmptyOperator
- `branching_dag.py` — BranchPythonOperator + trigger_rule reconvergence
- `sensors.py` — FileSensor, S3KeySensor, SqlSensor, ExternalTaskSensor
- `xcom_patterns.py` — TaskFlow XCom and external-storage pattern for large data
- `scheduled_dag.py` — schedule presets, catchup, max_active_runs
- `connections_variables.py` — hooks, PostgresHook, Variable.get patterns
- `pool_example.py` — pools and weighted pool_slots
- `test_dags.py` — DagBag CI tests (import errors, catchup, presence)

- `docker-compose.yaml` — local Airflow 2.x stack (scheduler + webserver + Postgres)

## Usage

Copy the `.py` files into `./dags` and start the stack:

```bash
docker compose up -d
# Airflow UI at http://localhost:8080 (airflow/airflow)
```

Old usage: 

Drop the `dags/*.py` files into your Airflow `dags/` folder. Requires `apache-airflow>=2.5` (uses `EmptyOperator` and TaskFlow API); `SnowflakeOperator`/`S3KeySensor` need the matching `apache-airflow-providers-*` packages.
