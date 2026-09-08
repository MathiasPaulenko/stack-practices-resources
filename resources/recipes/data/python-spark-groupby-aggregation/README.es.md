# Agregaciones a Gran Escala con PySpark — Ejemplos Companion

Este companion provee ejemplos ejecutables de PySpark para la receta
[Agregaciones a Gran Escala con PySpark](https://stackpractices.com/es/recipes/python-spark-groupby-aggregation/)
en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---------|--------------|
| `basic_aggregation.py` | Group-by básico con sum, count, avg, max, min |
| `window_functions.py` | Row number, running total, lag, percentile |
| `broadcast_join.py` | Broadcast join vs regular join |
| `skew_handling.py` | Técnica de salting para keys skewed |
| `partition_tuning.py` | Shuffle partitions, repartition, coalesce |
| `test_spark_examples.py` | Tests con pytest para todos los ejemplos |

## Requisitos

- Python 3.8+
- PySpark 3.5+ (`pip install pyspark`)
- Java 8 u 11

## Ejecutar los ejemplos

```bash
python basic_aggregation.py
python window_functions.py
python broadcast_join.py
python skew_handling.py
python partition_tuning.py
```

## Ejecutar los tests

```bash
pip install pytest pyspark
pytest test_spark_examples.py -v
```

Los tests corren en modo local de Spark — no requieren cluster.
