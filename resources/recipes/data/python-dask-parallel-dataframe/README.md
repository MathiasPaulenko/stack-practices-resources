# Parallel DataFrame Operations with Dask

Companion code for the [Dask parallel DataFrame recipe](https://stackpractices.com/recipes/python-dask-parallel-dataframe/) on StackPractices.

## Files

| File | Description |
| --- | --- |
| `dask_dataframe.py` | Basic Dask DataFrame operations: read, lazy group-by, filter |
| `delayed_tasks.py` | Custom task graphs with `dask.delayed` |
| `distributed_setup.py` | Dask Distributed scheduler setup with local cluster |
| `test_dask_examples.py` | Unit tests for all examples (pytest) |

## Setup

```bash
pip install dask[dataframe] distributed pandas pytest
```

## Running the Examples

```bash
python dask_dataframe.py
python delayed_tasks.py
python distributed_setup.py
```

## Running the Tests

```bash
python -m pytest test_dask_examples.py -v
```

## Usage

```python
import pandas as pd
import dask.dataframe as dd

from dask_dataframe import create_sample_dataframe, to_dask, lazy_groupby

pdf = create_sample_dataframe()
ddf = to_dask(pdf, npartitions=4)
result = lazy_groupby(ddf).compute()
print(result.head())
```
