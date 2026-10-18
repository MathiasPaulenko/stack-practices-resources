# Plantilla de Documentación de Esquema de Base de Datos

Plantilla Markdown lista para copiar y pegar para documentar esquemas de base de datos: definiciones de entidades, relaciones, razón de cada índice, referencia de enums, historial de migraciones y columnas obsoletas.

Artículo fuente: https://stackpractices.com/es/docs/database-schema-documentation-template/

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `template.md` | La plantilla de documentación, rellenada con un ejemplo realista de e-commerce (users, orders, order_items, user_preferences). Reemplaza el ejemplo con tus propias tablas. |
| `example-schema.dbml` | El mismo esquema de ejemplo en DBML. Pégalo en [dbdiagram.io](https://dbdiagram.io/d) para renderizar el diagrama ER. |

## Uso

1. Copia `template.md` en tu repositorio (por ejemplo, `docs/schema.md`).
2. Reemplaza el placeholder `[Database Name]` y los campos del resumen.
3. Documenta cada tabla: propósito, columnas, restricciones, índices y reglas de negocio.
4. Completa la sección de relaciones y la referencia de enums.
5. Mantén actualizado el historial de migraciones con cada cambio del esquema.
6. Opcionalmente, conserva `example-schema.dbml` junto al documento y actualízalo en el mismo PR.

Para generar la documentación automáticamente desde una base de datos en vivo, usa esta plantilla como capa narrativa sobre la salida de [tbls](https://github.com/k1LoW/tbls) o [dbdocs](https://dbdocs.io).
