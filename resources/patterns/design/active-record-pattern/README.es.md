# Patrón Active Record — Archivos complementarios

Ejemplos ejecutables del patrón:
<https://stackpractices.com/es/patterns/active-record-pattern/>

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `active-record-python.py` | Demo completa ejecutable: crear tabla, `save()` (insert → lastrowid), `find_by_id`, `find_all`, `delete` sobre sqlite3 |
| `ActiveRecordUser.java` | Versión Java con JDBC, manejo de claves generadas y `toString()` |
| `active-record-javascript.js` | Active Record asíncrono con conexión inyectada (`db.run`/`get`/`all`, p. ej. el paquete `sqlite`) |

## El patrón en una línea

**Un objeto es una fila; `user.save()` lo escribe en la base de datos sin capa de acceso a datos separada.**

## Puntos clave

- Boilerplate mínimo — las convenciones del framework (Rails, Django, Eloquent, Sequelize) hacen el mapeo por ti.
- El modelo de dominio sabe que existe SQL: ese acoplamiento es el precio de la simplicidad.
- Testear sin base de datos es difícil — usa SQLite in-memory o extrae la lógica a service objects planos.
- Cuando necesites transacciones multi-entidad o lógica de dominio rica, mira Data Mapper / Repository / Unit of Work.
