# Plantilla de Reglas de Calidad de Datos — Archivos Companion

Archivos que acompañan a la [Plantilla de Reglas de Calidad de Datos](https://stackpractices.com/es/docs/data-quality-rules-template/) en StackPractices. Cópialos a tu proyecto y adapta el dataset, las columnas y los umbrales.

## Contenido

| Ruta | Qué es |
|------|--------|
| `template/data-quality-rules-template.md` | El documento de reglas completo de `fct_orders`: 28 reglas de completitud, consistencia, exactitud, actualidad, unicidad y validez, con severidad y acción por fallo en cada una. |
| `dbt/schema.yml` | Tests de modelo dbt: `not_null`, `unique`, `accepted_values`, `relationships` y checks con `dbt_utils.expression_is_true`, incluidas reglas condicionales a nivel de modelo. |
| `dbt/tests/assert_row_count_range.sql` | Test personalizado de dbt que falla cuando el recuento de filas sale del rango esperado. |
| `dbt/tests/assert_data_freshness.sql` | Test personalizado de dbt que falla cuando el `_ingested_at` más reciente tiene más de 24 horas. |
| `great-expectations/fct_orders_suite.py` | Suite de Great Expectations: nulos, unicidad, regex, conjuntos de valores, rangos, regla condicional entre columnas y recuento de filas de la tabla. |

## Cómo usar

1. Copia `template/data-quality-rules-template.md` a tu carpeta de documentación y reemplaza `fct_orders`, las columnas y los umbrales con los de tu dataset.
2. Adapta `dbt/schema.yml` a tu modelo dbt y colócalo junto al archivo del modelo. Los tests personalizados van en el directorio `tests/` de tu proyecto.
3. Adapta `great-expectations/fct_orders_suite.py` a tu checkpoint o flujo de validación. Requiere `great_expectations` instalado y un Data Context configurado.
4. Asigna las severidades con honestidad: crítico bloquea el pipeline, warning registra y continúa. Una suite donde todo es crítico entrena al equipo a ignorar las alertas.

Documento fuente: https://stackpractices.com/es/docs/data-quality-rules-template/
