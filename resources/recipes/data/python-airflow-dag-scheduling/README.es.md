# Programar y Monitorear DAGs con Apache Airflow

Proyecto complementario ejecutable para la receta de StackPractices.

## Contenido

- `dags/etl_daily_pipeline.py` — un DAG completo de Airflow usando la TaskFlow API.
- `dags/sensor_example.py` — un `PythonSensor` que espera un archivo con modo `reschedule`.
- `dags/branching_example.py` — un `BranchPythonOperator` que elige entre dos caminos.
- `dags/dynamic_mapping_example.py` — mapeo dinámico de tareas con `expand()`.
- `docker-compose.yml` — un setup local mínimo basado en `airflow standalone`.
- `requirements.txt` — dependencias de Python.

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
airflow standalone
```

`airflow standalone` inicializa la base de datos, arranca el web server y el scheduler, e
imprime las credenciales de admin. Luego abrí <http://localhost:8080>.

El DAG de ejemplo lee `/tmp/airflow_etl/raw/orders.csv`, filtra las filas con amount
faltante y escribe un archivo Parquet en `/tmp/airflow_etl/processed/`.

## Ejecutar con Docker

```bash
docker compose up
```

Luego abrí <http://localhost:8080>. Las credenciales por defecto se imprimen en los logs
del contenedor.

> Este es un setup local para aprender. Para producción, usá el Helm chart oficial de
> Airflow o el `docker-compose` multi-servicio de la documentación de Airflow.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `dags/etl_daily_pipeline.py` | DAG ETL de ejemplo con TaskFlow API |
| `dags/sensor_example.py` | Sensor que espera un archivo con modo `reschedule` |
| `dags/branching_example.py` | Branching condicional con `BranchPythonOperator` |
| `dags/dynamic_mapping_example.py` | Mapeo dinámico de tareas con `expand()` |
| `requirements.txt` | Dependencias de Python |
| `docker-compose.yml` | Contenedor mínimo de Airflow standalone |

## Links

- Receta: <https://stackpractices.com/es/recipes/python-airflow-dag-scheduling/>
- Documentación de Apache Airflow: <https://airflow.apache.org/docs/apache-airflow/stable/index.html>
