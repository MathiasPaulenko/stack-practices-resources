# Prevención de inyección SQL — Código complementario

Ejemplos ejecutables de la receta [Prevenir Ataques de Inyección SQL](https://stackpractices.com/es/recipes/sql-injection-prevention/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `python/parameterized_queries.py` | Consultas sqlite3 vulnerables vs parametrizadas, más una lista permitida para `ORDER BY`. Se ejecuta sin configuración. |
| `node/parameterized_queries.js` | Ejemplos del driver `pg`: placeholders `$1`, escape de comodines en `LIKE` y orden dinámico con lista permitida. Requiere `DATABASE_URL`. |
| `java/PreparedStatementExample.java` | `PreparedStatement` de JDBC con placeholders `?` y un `ORDER BY` dinámico validado. |
| `testing/sqlmap-cheatsheet.sh` | Comandos de sqlmap para probar **tus propios** entornos de staging. |

## Inicio rápido

```bash
# Python (sin dependencias, BD en memoria)
python python/parameterized_queries.py
# unsafe: devuelve todas las filas — la inyección funcionó
# safe:   devuelve [] — el mismo texto se vuelve un valor literal

# Node (requiere `pg` y un Postgres accesible)
npm install pg
DATABASE_URL=postgres://user:pass@localhost/db node -e \
  "require('./node/parameterized_queries').getUsers().then(console.log)"
```

## Fuente

- https://stackpractices.com/recipes/sql-injection-prevention/
- https://stackpractices.com/es/recipes/sql-injection-prevention/
