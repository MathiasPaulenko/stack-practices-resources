# Funciones de ventana en SQL: ranking y totales acumulados

Ejemplos SQL ejecutables de la receta de StackPractices
[Funciones de ventana en SQL: ranking y totales acumulados](https://stackpractices.com/es/recipes/sql-window-functions-ranking/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `setup_test_data.sql` | Datos de empleados, ingresos mensuales y registros de usuario |
| `01_ranking_and_running_totals.sql` | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, totales acumulados, `LAG` |
| `02_top_n_per_group.sql` | Top-N filas por partición con `ROW_NUMBER` |
| `03_moving_average_and_growth.sql` | Marcos de ventana (`ROWS BETWEEN`) y crecimiento interanual |
| `04_deduplicate_rows.sql` | Mantener la fila más reciente por grupo |
| `05_rank_variants_comparison.sql` | Variantes de ranking, `NTILE`, `PERCENT_RANK`, `CUME_DIST` |

## Uso

Ejecuta primero `setup_test_data.sql` y luego cualquier script numerado.
Probado en PostgreSQL 14+; la mayoría de las consultas funcionan en MySQL 8.0+, SQLite 3.25+ y SQL Server.
