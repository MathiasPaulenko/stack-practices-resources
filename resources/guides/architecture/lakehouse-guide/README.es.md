# Arquitectura Lakehouse — Scripts Companion del Pipeline

Scripts ejecutables del pipeline medallion descrito en la [guía de Arquitectura Lakehouse](https://stackpractices.com/es/guides/lakehouse-guide/) de StackPractices.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `bronze_to_silver_delta.py` | Limpia eventos JSON crudos y los fusiona con `MERGE` en la tabla Delta Silver (idempotente, claveado por `event_id`) |
| `silver_to_gold_delta.py` | Agregados diarios de negocio como tabla Delta Gold |
| `delta_maintenance.py` | Mantenimiento semanal: `OPTIMIZE`, `Z-ORDER`, `VACUUM` y `symlink_format_manifest` para Athena |
| `iceberg_setup.py` | Tabla Iceberg con particionado oculto + evolución de particiones (día → hora, sin reescritura) |
| `hudi_upsert.py` | Upserts a nivel de registro y lecturas incrementales con Apache Hudi |
| `spark_submit.sh` | El pipeline completo como comandos `spark-submit` en EMR/YARN |
| `requirements.txt` | Dependencias de Python |

## Uso

```bash
# Instalar localmente (o enviar a EMR/Databricks)
pip install -r requirements.txt

# Pipeline medallion de extremo a extremo (edita las rutas S3 primero)
./spark_submit.sh s3://lakehouse/bronze/events/dt=2026-07-11/ \
    s3://lakehouse/silver/events/ s3://lakehouse/gold/daily_metrics/
```

Cada script acepta las rutas de las tablas como argumentos posicionales; los valores por defecto coinciden con el escenario de la guía (`s3://lakehouse/...`).

## Notas

- El merge de Delta está claveado por `event_id`, así que reejecutar Bronze→Silver para el mismo día actualiza filas en lugar de duplicarlas.
- `VACUUM` es irreversible — 168h (7 días) es un default razonable; revisa primero tus requisitos de auditoría.
- `delta_maintenance.py` genera el `symlink_format_manifest` que Athena necesita para leer tablas Delta.
