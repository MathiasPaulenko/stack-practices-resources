# Apache Airflow — Companion

Ejemplos DAG ejecutables de [Apache Airflow: DAGs, Operadores y Scheduling](https://stackpractices.com/es/guides/complete-guide-apache-airflow/).

## Archivos

- `core_dag.py` — DAG ETL clásico (operadores Bash + Python)
- `taskflow_dag.py` — ETL TaskFlow con upsert idempotente en Postgres
- `common_operators.py` — Bash, Python, Email, Snowflake, Spark, EmptyOperator
- `branching_dag.py` — BranchPythonOperator + reconvergencia con trigger_rule
- `sensors.py` — FileSensor, S3KeySensor, SqlSensor, ExternalTaskSensor
- `xcom_patterns.py` — XCom TaskFlow y patrón de storage externo para datos grandes
- `scheduled_dag.py` — presets de schedule, catchup, max_active_runs
- `connections_variables.py` — hooks, PostgresHook, patrones de Variable.get
- `pool_example.py` — pools y pool_slots con peso
- `test_dags.py` — tests DagBag para CI (errores de importación, catchup, presencia)

- `docker-compose.yaml` — stack local de Airflow 2.x (scheduler + webserver + Postgres)

## Uso

Copia los `.py` a `./dags` y levanta el stack:

```bash
docker compose up -d
# UI de Airflow en http://localhost:8080 (airflow/airflow)
```

Uso anterior: 

Copia los `dags/*.py` a tu carpeta `dags/` de Airflow. Requiere `apache-airflow>=2.5` (usa `EmptyOperator` y TaskFlow API); `SnowflakeOperator`/`S3KeySensor` necesitan los paquetes `apache-airflow-providers-*` correspondientes.
