# Large-Scale Aggregation with PySpark — Companion Examples

This companion provides runnable PySpark examples for the
[Large-Scale Aggregation with PySpark](https://stackpractices.com/recipes/python-spark-groupby-aggregation/)
recipe on StackPractices.

## Files

| File | What it shows |
|------|---------------|
| `basic_aggregation.py` | Basic group-by with sum, count, avg, max, min |
| `window_functions.py` | Row number, running total, lag, percentile |
| `broadcast_join.py` | Broadcast join vs regular join |
| `skew_handling.py` | Salting technique for skewed keys |
| `partition_tuning.py` | Shuffle partitions, repartition, coalesce |
| `test_spark_examples.py` | Pytest tests for all examples |

## Requirements

- Python 3.8+
- PySpark 3.5+ (`pip install pyspark`)
- Java 8 or 11

## Running the examples

```bash
python basic_aggregation.py
python window_functions.py
python broadcast_join.py
python skew_handling.py
python partition_tuning.py
```

## Running the tests

```bash
pip install pytest pyspark
pytest test_spark_examples.py -v
```

The tests run in Spark local mode — no cluster required.
