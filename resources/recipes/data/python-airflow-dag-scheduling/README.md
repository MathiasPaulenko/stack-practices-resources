# Schedule and Monitor DAGs with Apache Airflow

Runnable companion project for the StackPractices recipe.

## What it contains

- `dags/etl_daily_pipeline.py` — a complete Airflow DAG using the TaskFlow API.
- `dags/sensor_example.py` — a `PythonSensor` that waits for a file using `reschedule` mode.
- `dags/branching_example.py` — a `BranchPythonOperator` that chooses between two paths.
- `dags/dynamic_mapping_example.py` — dynamic task mapping with `expand()`.
- `docker-compose.yml` — a minimal local Airflow setup based on `airflow standalone`.
- `requirements.txt` — Python dependencies.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
airflow standalone
```

`airflow standalone` initializes the database, starts the web server and scheduler, and
prints the admin credentials. Then open <http://localhost:8080>.

The sample DAG reads `/tmp/airflow_etl/raw/orders.csv`, filters rows with missing amounts,
and writes a Parquet file to `/tmp/airflow_etl/processed/`.

## Run with Docker

```bash
docker compose up
```

Then open <http://localhost:8080>. The default credentials are printed in the container
logs.

> This is a local learning setup. For production, use the official Airflow Helm chart or
> the multi-service `docker-compose` from the Airflow docs.

## Files

| File | Purpose |
| --- | --- |
| `dags/etl_daily_pipeline.py` | Sample ETL DAG with TaskFlow API |
| `dags/sensor_example.py` | File-waiting sensor with reschedule mode |
| `dags/branching_example.py` | Conditional branching with `BranchPythonOperator` |
| `dags/dynamic_mapping_example.py` | Dynamic task mapping with `expand()` |
| `requirements.txt` | Python dependencies |
| `docker-compose.yml` | Minimal Airflow standalone container |

## Links

- Recipe: <https://stackpractices.com/recipes/python-airflow-dag-scheduling/>
- Apache Airflow docs: <https://airflow.apache.org/docs/apache-airflow/stable/index.html>
