# Runbook de Job ETL — Recursos del repositorio companion

Companion ejecutable de [Plantilla de Runbook para Jobs ETL](https://stackpractices.com/es/docs/etl-job-runbook-template/) en StackPractices.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `runbook/etl-job-runbook-template.md` | Versión rellenable del runbook del artículo: cada campo es un `<placeholder>`. |
| `scripts/health-checks.sh` | Chequeo de salud pre-corrida ejecutable: pods del scheduler/workers, API de origen, bucket de staging, warehouse, compilación dbt y estado de la corrida anterior. Se configura con variables de entorno; lo que falte reporta SKIP, no FAIL. Sale con código distinto de cero si algo falla, así puede cortar un cron o un paso del pipeline. |
| `monitoring/airflow-commands.md` | Chuleta de la CLI de Airflow 2.x verificada contra la referencia oficial, incluidos los comandos que ya no existen (`tasks run`, `tasks logs`, `connections set`, `tasks duration`) y qué usar en su lugar. |
| `monitoring/dbt-tests-schema.yml` | `schema.yml` de dbt para `fct_orders`: los tests de columna que corre la tarea `quality_checks` en el escenario de fallo F4 (not_null, unique, accepted_values, soporte de frescura). |
| `checklists/game-day-drill.md` | Checklist de simulacro trimestral: cinco escenarios de fallo inyectables mapeados a las entradas F1–F6 del runbook, criterios de evaluación y reglas de actualización post-simulacro. |

## Inicio rápido

```bash
# Corre los chequeos contra tu entorno
DAG_ID=orders_etl_pipeline \
SOURCE_API_HEALTH_URL=https://api.example.com/health \
STAGING_BUCKET=example-staging/orders \
WAREHOUSE_HOST=analytics-cluster \
DBT_PROJECT_DIR=/opt/dbt \
bash scripts/health-checks.sh
```

Cada chequeo degrada a `SKIP` cuando falta su herramienta o variable, así que el script también funciona como checklist para leer a mano.

## Notas

- Todos los comandos de Airflow apuntan a **Airflow 2.x** (`tasks clear` para re-ejecutar, `dags backfill`, logs en la UI). Airflow 3 eliminó `dags backfill` y renombra varios subcomandos — mira `monitoring/airflow-commands.md`.
- Los snippets SQL asumen dialecto PostgreSQL/Redshift (tablas `stv_*`). Ajústalos a tu warehouse.
