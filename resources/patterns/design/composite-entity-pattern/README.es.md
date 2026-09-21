# Patrón Composite Entity — Ejemplos de Acompañamiento

Ejemplos ejecutables del [patrón Composite Entity](https://stackpractices.com/es/patterns/composite-entity-pattern/): un aggregate root (`Order`) que posee objetos dependientes (`LineItem`, `ShippingAddress`) persistidos en tres tablas como una sola unidad.

## Contenido

| Archivo | Lenguaje | Propósito |
| --- | --- | --- |
| `order_mapper.py` | Python | `OrderMapper` completo sobre `sqlite3` — `save()` escribe las tres tablas en una transacción; `find_by_id()` rehidrata el agregado entero. Ejecutable: `python order_mapper.py` imprime `Order total: $109.97`. |
| `OrderMapper.java` | Java | El mismo mapper con JDBC, con `save()` usando `setAutoCommit(false)` + rollback y una demo `main()`. |
| `order-mapper.js` | JavaScript | Mapper asíncrono para un handle de sqlite, con transacción `BEGIN`/`COMMIT`/`ROLLBACK` en `save()`. |
| `schema.sql` | SQL | Esquema que codifica la propiedad: `ON DELETE CASCADE`, clave compuesta `(order_id, line_no)`, restricciones `CHECK`. |
| `order_projection.py` | Python | Proyección para vistas de lista — una query agregada en lugar de cargar compuestos enteros para una tabla. |
| `order_mapper_json.py` | Python | Variante con columna JSON — el mismo agregado como una sola fila con dependientes JSON. Ejecutable: imprime `Order total: $109.97`. |

## Conceptos cubiertos

- **Identidad local en los dependientes** — `line_items` usa `(order_id, line_no)`, sin UUID global por línea.
- **Una transacción por guardado** — escrituras parciales dejarían el agregado inconsistente.
- **Borrar y re-insertar** las colecciones hijas — gestiona las filas huérfanas gratis.
- **Limpieza de huérfanos a nivel de base de datos** — `ON DELETE CASCADE` hace de "borrar el agregado" una sola sentencia.

## Pruébalo

```bash
python order_mapper.py    # -> Order total: $109.97
sqlite3 orders.db < schema.sql
```
