# Operaciones Paralelas de DataFrame con Dask

Código companion para la [receta de Dask parallel DataFrame](https://stackpractices.com/es/recipes/python-dask-parallel-dataframe/) en StackPractices.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `dask_dataframe.py` | Operaciones básicas de Dask DataFrame: read, lazy group-by, filter |
| `delayed_tasks.py` | Task graphs custom con `dask.delayed` |
| `distributed_setup.py` | Configuración del scheduler Dask Distributed con cluster local |
| `test_dask_examples.py` | Tests unitarios para todos los ejemplos (pytest) |

## Setup

```bash
pip install dask[dataframe] distributed pandas pytest
```

## Ejecutar los ejemplos

```bash
python dask_dataframe.py
python delayed_tasks.py
python distributed_setup.py
```

## Ejecutar los tests

```bash
python -m pytest test_dask_examples.py -v
```

## Uso

```python
import pandas as pd
import dask.dataframe as dd

from dask_dataframe import create_sample_dataframe, to_dask, lazy_groupby

pdf = create_sample_dataframe()
ddf = to_dask(pdf, npartitions=4)
result = lazy_groupby(ddf).compute()
print(result.head())
```
