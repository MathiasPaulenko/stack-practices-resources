# Desnormalización de bases de datos — Demo complementaria

Demo ejecutable en SQLite de los patrones de desnormalización de la guía
[Desnormalización: espacio por velocidad de lectura](https://stackpractices.com/es/guides/database-denormalization-guide/)
([English version](https://stackpractices.com/guides/database-denormalization-guide/)).

La guía usa sintaxis de PostgreSQL (`SERIAL`, `GENERATED ALWAYS AS`, vistas
materializadas). Esta demo adapta los mismos patrones a SQLite para ejecutarse
en cualquier máquina con Python — sin servidor de base de datos.

## Contenido

| Archivo | Qué muestra |
|---------|-------------|
| `denormalization_demo.sql` | Columna contador + triggers, columna computada materializada, tabla resumen (el equivalente en SQLite a una vista materializada) y la consulta de divergencias |
| `run_demo.py` | Ejecuta el SQL contra una base SQLite en memoria e imprime los resultados |

## Ejecución

```bash
python run_demo.py
```

Salida esperada: `posts.like_count = 2` tras tres likes y un unlike — los
triggers son dueños de la sincronización, así que el contador almacenado siempre
coincide con un `COUNT(*)` fresco (divergencia = 0).

## Notas de producción

- En PostgreSQL, usa `GENERATED ALWAYS AS ... STORED` para derivaciones por fila
  y vistas materializadas reales para agregados — ver el escenario de la guía.
- El control de divergencias es la pieza a copiar a producción: recalcula una
  muestra de valores desnormalizados desde la fuente y alerta sobre diferencias.
