# Patrón Null Object — Código Companion

Ejemplos ejecutables de [Patrón Null Object](https://stackpractices.com/es/patterns/null-object-pattern/) en StackPractices.

Un objeto nulo implementa la misma interfaz que el real pero devuelve valores seguros — `"Guest"`, `false`, listas vacías, no-ops — para que los llamadores nunca ramifiquen sobre `null`.

## Archivos

- `null_user.py` — ABC `User` + `RealUser` + `NullUser` con una búsqueda `find_user()` que nunca devuelve `None`. Ejecutar: `python null_user.py`
- `null_logger.js` — `OrderService` con colaboradores `Logger`/`AppConfig` inyectados por el constructor; `NullLogger`/`NullConfig` dan tests silenciosos sin framework de mocks. Ejecutar: `node null_logger.js`
- `NullUser.java` — la misma interfaz `User` en Java con un `Demo` main. Ejecutar: `javac NullUser.java && java NullUser\$Demo`

## Idea clave

`findUser(999)` devuelve un `NullUser`, no `null`: `user.getName()` funciona sin cláusula de guarda. La rama "usuario no encontrado" vive dentro del grafo de objetos en lugar de en cada punto de llamada.
