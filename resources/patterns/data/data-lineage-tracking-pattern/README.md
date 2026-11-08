# Data Lineage Tracking — OpenLineage, Marquez and Column-Level Extraction

Companion code for the [Data Lineage Tracking pattern](https://stackpractices.com/patterns/data-lineage-tracking-pattern/) on StackPractices.

## Files

- `docker-compose.yml` — Marquez backend stack (PostgreSQL + API + lineage graph UI). Run with `docker compose up -d`; API on `:5000`, UI on `:3000`.
- `openlineage_event.json` — a complete START run event with schema and `columnLineage` facets, for reference or manual `POST /api/v1/lineage` testing.
- `src/lineage_tracker.py` — `LineageTracker` class that emits START/COMPLETE/FAIL OpenLineage events with dataset facets from any Python pipeline.
- `src/etl_with_lineage.py` — ETL example wrapping extract/transform/load calls in run events, including a `columnLineage` output facet.
- `src/column_lineage.py` — sqlglot-based parser that extracts column-level lineage (output column → source columns) from a SELECT statement.
- `src/table_lineage.py` — minimal in-memory table-level lineage recorder with BFS downstream traversal.
- `src/impact_analysis.sql` — recursive CTE that walks a `lineage_edges` table to find every downstream table/column affected by a source change.
- `src/airflow_lineage.py` — Airflow DAG using the OpenLineage provider; pushes dataset metadata to XCom for the extractor.
- `src/LineageEmitter.java` — dependency-free (Jackson only) Java emitter that posts run events to the Marquez REST API.

## Requirements

- Docker + docker compose for the Marquez stack
- Python 3.9+ with `openlineage-python` and `sqlglot` for the emitter/extractor scripts
- Airflow 2.7+ with `apache-airflow-providers-openlineage` for the DAG
