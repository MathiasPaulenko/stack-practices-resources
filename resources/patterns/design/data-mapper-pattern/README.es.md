# Patrón Data Mapper — Archivos complementarios

Ejemplos ejecutables del recurso [Patrón Data Mapper](https://stackpractices.com/es/patterns/data-mapper-pattern/) en StackPractices.

## Contenido

| Archivo | Lenguaje | Qué muestra |
| ------- | -------- | ----------- |
| `src/user_mapper.py` | Python | Dataclass `User` + `UserMapper` sobre `sqlite3`, usando `conn.row_factory = sqlite3.Row` para acceder a columnas por nombre. Funciona tal cual. |
| `src/DataMapperDemo.java` | Java | Demo en un solo archivo: clase de dominio `User`, `UserMapper` sobre JDBC (`PreparedStatement`, claves generadas) y un `main` de entrada. |
| `src/user-mapper.js` | JavaScript | `UserMapper` sobre `node:sqlite` integrado en Node (`DatabaseSync`) — sin dependencias, API síncrona. |
| `schema.sql` | SQL | Tabla `users` mínima que usan los tres mappers. |

## Ejecutar

```bash
# Python
python src/user_mapper.py

# JavaScript (Node 22.5+; en Node 22 pasa --experimental-sqlite)
node src/user-mapper.js

# Java (necesita el driver JDBC de SQLite en el classpath)
javac src/DataMapperDemo.java && java -cp src DataMapperDemo
```

Cada demo crea la tabla `users` en memoria, inserta un `User` a través del mapper y lo lee de vuelta — el objeto de dominio nunca toca la conexión.
