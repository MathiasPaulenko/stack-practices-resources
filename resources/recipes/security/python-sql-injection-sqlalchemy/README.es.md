# Prevencion de inyeccion SQL con SQLAlchemy — Codigo complementario

Ejemplos ejecutables de SQLAlchemy que muestran el patron vulnerable y las alternativas seguras lado a lado, contra una base de datos SQLite en memoria.

## Archivos

| Archivo | Que muestra |
|---|---|
| `safe_queries.py` | Query vulnerable con f-strings vs `text()` con parametros vinculados, `select` ORM, filtros dinamicos, whitelists de `ORDER BY` y escape de wildcards en `LIKE`. Incluye un smoke test en `__main__`. |

## Inicio rapido

```bash
pip install -r requirements.txt
python safe_queries.py
# vulnerable: se filtran 2 filas
# safe text(): None
# safe ORM: None
# la inyeccion via ORDER BY cae en una columna de la whitelist
```

## Fuente

- https://stackpractices.com/recipes/python-sql-injection-sqlalchemy/
- https://stackpractices.com/es/recipes/python-sql-injection-sqlalchemy/
