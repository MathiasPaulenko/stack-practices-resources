# Pipeline Medallion de Data Lake

Companion ejecutable de la [Data Lake vs Data Warehouse — Guía de Arquitectura](https://stackpractices.com/es/guides/data-lake-guide/) en StackPractices.

Dos formas de correr el mismo flujo Bronze → Silver → Gold: un pipeline con pandas/pyarrow que funciona en una laptop, y los jobs de Spark + Delta Lake del escenario e-commerce de la guía.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `medallion_pipeline.py` | Pipeline autocontenido: genera eventos de clickstream sintéticos, los aterriza en Bronze (JSON), los limpia/deduplica/particiona a Silver (Parquet estilo hive `event_date=YYYY-MM-DD/`) y agrega métricas diarias en Gold. |
| `bronze_to_silver.py` | El job de Spark de la guía: limpia JSON crudo → tabla Delta particionada por `event_date`, luego `OPTIMIZE` + `VACUUM`. |
| `delta_example.py` | Lo esencial de Delta Lake: escritura ACID, time travel (`versionAsOf`), evolución de schema (`mergeSchema`). |
| `requirements.txt` | pandas + pyarrow para el pipeline ejecutable; pyspark + delta-spark opcionales para los ejemplos Spark. |

## Ejecutarlo (sin Spark)

```bash
pip install -r requirements.txt
python medallion_pipeline.py
```

Obtendrás un directorio `lake/` con:

```text
lake/
├── bronze/events/dt=2026-10-18/events.json
├── silver/events/event_date=2026-10-18/*.parquet
└── gold/daily_events.parquet
```

La salida de Silver muestra las dos cosas que la guía enfatiza: nulls y duplicados eliminados (Silver está validada), y datos particionados por la columna por la que las consultas filtran.

## Ejecutar la versión Spark

```bash
pip install pyspark delta-spark
spark-submit bronze_to_silver.py   # apunta a rutas s3:// — ajusta para local
python delta_example.py            # escribe ./lake/silver/orders
```

## Idea clave

Bronze es solo-append (tu fuente de replay), Silver es tipada y deduplicada (adonde van la mayoría de las consultas), Gold existe por consumidor. Si una tabla Gold no tiene consumidor, bórrala.
