# Patrón Eager Loading — Código complementario

Demos ejecutables del patrón Eager Loading. Fuente:
<https://stackpractices.com/es/patterns/eager-loading-pattern/>

## Archivos

| Archivo | Lenguaje | Qué muestra |
| --- | --- | --- |
| `eager_loading.py` | Python | Bucle N+1 ingenuo vs JOIN vs carga por lotes sobre `sqlite3`, con un `CountingConnection` que imprime el número de consultas de cada estrategia |
| `eager-loading.js` | JavaScript | Las mismas tres estrategias sobre `node:sqlite` (Node ≥ 22.13), contando consultas por estrategia |
| `EagerLoadingDemo.java` | Java | La misma estructura; cambia JDBC por una tabla en memoria que cuenta "consultas" para ejecutarse con `javac` sin drivers |

## Ejecutar

```bash
python eager_loading.py
node eager-loading.js
javac EagerLoadingDemo.java && java EagerLoadingDemo
```

Cada demo crea 100 libros y 2 autores, y ejecuta el mismo método del
repositorio de tres formas. La salida esperada es parecida a:

```text
     naive: 101 queries for 100 books
eager JOIN: 1 queries for 100 books
     batch: 2 queries for 100 books
Book 1 by Alice
```

## Notas

- La versión ingenua es lo importante: mira el número de consultas, no la
  latencia. El N+1 aparece como cientos de consultas pequeñas, no como una
  sentencia lenta.
- El JOIN es el valor por defecto correcto para relaciones a-uno; la carga
  por lotes (`WHERE id IN`) evita el producto cartesiano que produce unir
  colecciones a-muchos.
- La versión JDBC del artículo necesita `sqlite-jdbc` en el classpath; el
  archivo Java de aquí usa una tabla falsa para no depender de nada.
