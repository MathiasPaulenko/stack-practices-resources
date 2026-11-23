# Paginación — Archivos complementarios

Archivos complementarios de [Paginación](https://stackpractices.com/es/recipes/pagination/) en StackPractices.

## Contenido

- `pagination.py` — implementaciones ejecutables por offset y por cursor sobre un dataset de 100 filas en memoria. Ejecútalo: `python pagination.py`.
- `test_pagination.py` — suite de pytest que cubre primera página, páginas profundas, última página, la sonda `page_size + 1`, resultados vacíos tras el final y un recorrido completo por cursor. Ejecútala: `pytest test_pagination.py`.

## Qué mirar

- `get_users_cursor` pide `page_size + 1` filas — la sonda responde `has_more` sin un `COUNT(*)`, y `next_cursor` se deriva del último ítem devuelto, nunca de la sonda.
- `walk_all_pages` es el patrón consumidor: devuelve `next_cursor` hasta que `has_more` sea falso. La página 1 y la 10.000 cuestan lo mismo — esa es la ventaja sobre offset.
