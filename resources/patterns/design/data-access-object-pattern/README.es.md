# Patrón Data Access Object (DAO) — Archivos complementarios

Ejemplos ejecutables del patrón:
<https://stackpractices.com/es/patterns/data-access-object-pattern/>

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `dao-python.py` | Demo ejecutable completa: crear tabla, `save()` (insert → lastrowid), `find_by_id`, `find_all`, `find_paginated`, `delete` sobre sqlite3 — más un `FakeUserDao` para tests |
| `SqlUserDao.java` | Versión Java con JDBC: interfaz + implementación, manejo de claves generadas, envoltorio `DataAccessException`, demo `main()` sobre SQLite en memoria |
| `dao-javascript.js` | DAO asíncrono con handle `sqlite`/`sqlite3` inyectado (`db.get`/`all`/`run`) — más un `FakeUserDao` para tests |

## El patrón en una línea

**El código de negocio habla con una interfaz CRUD; el DAO es dueño del SQL, la conexión y el mapeo de filas.**

## Puntos clave

- Inyecta la conexión — todos los ejemplos reciben un handle listo en el constructor, así los tests pueden pasar SQLite en memoria y producción una conexión del pool.
- Envuelve las excepciones del driver una vez (`DataAccessException`) para que los callers manejen "falló el guardado", no "JDBC falló con SQLState 23505".
- Una conexión por consulta es el antipatrón clásico — deja que un pool controle el ciclo de vida.
- Cuando los métodos empiezan a verse como `findOverdueInvoices` en lugar de `insert`/`update`, superaste el DAO — eso ya es territorio de Repository.
