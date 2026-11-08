# Seguimiento de Linaje de Datos — OpenLineage, Marquez y Extracción a Nivel de Columna

Código complementario del [patrón Data Lineage Tracking](https://stackpractices.com/es/patterns/data-lineage-tracking-pattern/) en StackPractices.

## Archivos

- `docker-compose.yml` — stack del backend Marquez (PostgreSQL + API + UI de grafo de linaje). Ejecuta con `docker compose up -d`; API en `:5000`, UI en `:3000`.
- `openlineage_event.json` — evento START completo con facets de esquema y `columnLineage`, como referencia o para probar `POST /api/v1/lineage` a mano.
- `src/lineage_tracker.py` — clase `LineageTracker` que emite eventos START/COMPLETE/FAIL de OpenLineage con facets de datasets desde cualquier pipeline en Python.
- `src/etl_with_lineage.py` — ejemplo de ETL que envuelve las llamadas de extract/transform/load en eventos de ejecución, incluyendo un facet `columnLineage` en la salida.
- `src/column_lineage.py` — parser con sqlglot que extrae linaje a nivel de columna (columna de salida → columnas de origen) de un SELECT.
- `src/table_lineage.py` — registrador mínimo de linaje a nivel de tabla en memoria con recorrido BFS aguas abajo.
- `src/impact_analysis.sql` — CTE recursiva que recorre una tabla `lineage_edges` para encontrar todas las tablas/columnas aguas abajo afectadas por un cambio en origen.
- `src/airflow_lineage.py` — DAG de Airflow con el provider de OpenLineage; empuja la metadata de datasets a XCom para el extractor.
- `src/LineageEmitter.java` — emisor en Java sin dependencias extra (solo Jackson) que publica eventos de ejecución en la API REST de Marquez.

## Requisitos

- Docker + docker compose para el stack de Marquez
- Python 3.9+ con `openlineage-python` y `sqlglot` para los scripts de emisión/extracción
- Airflow 2.7+ con `apache-airflow-providers-openlineage` para el DAG
