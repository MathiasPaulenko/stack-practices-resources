# Plantilla de Documento de Diseño de Data Pipeline — Companion

Archivos companion del documento [Plantilla de Documento de Diseño de Data Pipeline](https://stackpractices.com/es/docs/data-pipeline-design-document-template/).

## Contenido

| Ruta | Propósito |
|------|-----------|
| `template/pipeline-design-document-template.md` | Versión en blanco y rellenable del documento de diseño — cópiala junto al código de tu pipeline |
| `dbt/models/int_orders_dedup.sql` | Modelo incremental de deduplicación (ROW_NUMBER por `order_id`) |
| `dbt/models/int_orders_enriched.sql` | Join de pedidos con la dimensión de clientes |
| `dbt/models/fct_order_metrics.sql` | Mart de métricas diarias con la referencia `is_enterprise` corregida |
| `airflow/orders_etl_dag.py` | Esqueleto de DAG Airflow 2.x según el grafo de tareas del documento |

## Notas

- `fct_order_metrics.sql` lee `is_enterprise` directamente de
  `int_orders_enriched` — la columna la agrega el join de enriquecimiento, así
  que en ese paso no hay alias de `dim_customers` en scope.
- `orders_etl_dag.py` es un esqueleto: `extract_orders_from_api` lanza
  `NotImplementedError` hasta que implementes la lógica de extracción según la
  tabla de fuentes (paginación, OAuth2, política de reintentos).
- La plantilla en blanco mantiene la estructura de 10 secciones: fuentes,
  staging, transformaciones, destinos, orquestación, manejo de errores,
  monitoreo, chequeos de calidad y procedimientos operativos.
