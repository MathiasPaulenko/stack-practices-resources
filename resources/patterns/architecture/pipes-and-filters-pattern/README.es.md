# Patrón Pipes and Filters — Recursos Complementarios

Código complementario para el [Patrón Pipes and Filters](https://stackpractices.com/es/patterns/pipes-and-filters-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `pipe_python.py` | Python 3.12+ | Pipeline sincrónico con filtros de funciones puras |
| `pipe_javascript.js` | Node 20+ | Mismo pipeline usando composición con `reduce` |
| `PipesAndFilters.java` | Java 21+ | Pipeline type-safe con `Function<T, R>` |
| `async_pipe_python.py` | Python 3.12+ | Pipeline async con `asyncio` para filtros I/O-bound |
| `test_pipe_python.py` | Python 3.12+ | Tests unitarios para cada filtro y el pipeline completo |
| `test_pipe_javascript.js` | Node 20+ | Tests unitarios para cada filtro y la composibilidad del pipe |

## Inicio rápido

### Python

```bash
python pipe_python.py          # ejecutar el pipeline
python -m pytest test_pipe_python.py -v  # ejecutar tests
```

### JavaScript

```bash
node pipe_javascript.js        # ejecutar el pipeline
node test_pipe_javascript.js   # ejecutar tests
```

### Java

```bash
javac PipesAndFilters.java     # compilar
java PipesAndFilters           # ejecutar
```

## Qué hace cada filtro

1. **parse_csv** — divide texto CSV raw en una lista de registros (dicts/maps).
2. **filter_active** — keep solo los registros con `status == "active"`.
3. **normalize_emails** — pasa a minúsculas y trim el campo email.
4. **deduplicate** — elimina registros con emails duplicados.
5. **to_json** — serializa el resultado a JSON (solo Python/JS).

Cada filtro es una función pura: sin side effects ni estado compartido. Podés reordenarlos, agregar nuevos o testearlos en aislamiento.
