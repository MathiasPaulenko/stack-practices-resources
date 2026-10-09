# Patrón Identity Map — Código complementario

Implementaciones ejecutables del patrón Identity Map. Fuente:
<https://stackpractices.com/es/patterns/identity-map-pattern/>

## Archivos

| Archivo | Lenguaje | Qué muestra |
| --- | --- | --- |
| `identity_map.py` | Python | Identity map sobre `sqlite3` — fíjate en la línea `row_factory`; sin ella las filas llegan como tuplas y `row["id"]` falla |
| `identity-map.js` | JavaScript | La misma estructura contra una db asíncrona mínima (compatible con `node:sqlite` / `sqlite`) |
| `IdentityMapDemo.java` | Java | La misma estructura; cambia JDBC por una tabla en memoria para ejecutarse con `javac` sin drivers |

## Ejecutar

```bash
python identity_map.py
node identity-map.js
javac IdentityMapDemo.java && java IdentityMapDemo
```

Cada uno carga `User(id=1)` dos veces e imprime `true`: la segunda llamada
viene del mapa, no de la base de datos. `find_all`/`findAll` también reutiliza
el mapa, que es la parte que la gente suele olvidar.

## Notas

- El mapa vive una unidad de trabajo. Si vive más, empieza a servir datos obsoletos.
- Al hacer rollback, vacía el mapa: los objetos no confirmados no deberían quedar en él.
- La versión JDBC del artículo necesita `sqlite-jdbc` en el classpath; el
  archivo Java de aquí usa una tabla falsa para no depender de nada.
