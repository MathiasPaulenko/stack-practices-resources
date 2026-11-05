# Configuraciones de Pytest para Producción

Recursos complementarios de la [Guía de Pytest en Producción](https://stackpractices.com/es/guides/complete-guide-pytest-production/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `conftest.py` | Fixtures por scope, fixture de BD consciente de xdist, factoría, hooks |
| `pytest.ini` | Markers, addopts, cobertura y filterwarnings para producción |
| `coveragerc` | Config de source/omit/exclude con fail_under = 80 |
| `factories.py` | Factorías factory_boy (User, Product, Order) |
| `tests.yml` | Workflow de GitHub Actions con servicios postgres/redis + matrix |

## Uso

1. Copia `conftest.py` a `tests/`, `pytest.ini` y `coveragerc` a la raíz (renombra a `.coveragerc`).
2. `pip install pytest pytest-xdist pytest-cov factory_boy`
3. `pytest -n auto` — los workers obtienen bases de datos aisladas vía `PYTEST_XDIST_WORKER`.

Consulta la guía para la tabla de decisión de scopes y la resolución de problemas.
