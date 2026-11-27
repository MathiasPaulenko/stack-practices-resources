# Rank Rows and Calculate Running Totals with Window Functions

Runnable SQL examples for the StackPractices recipe
[Rank Rows and Calculate Running Totals with Window Functions](https://stackpractices.com/recipes/sql-window-functions-ranking/).

## Contents

| File | What it shows |
| --- | --- |
| `setup_test_data.sql` | Employees, monthly revenue, and user-record fixtures |
| `01_ranking_and_running_totals.sql` | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, running totals, `LAG` |
| `02_top_n_per_group.sql` | Top-N rows per partition via `ROW_NUMBER` |
| `03_moving_average_and_growth.sql` | Window frames (`ROWS BETWEEN`) and YoY growth |
| `04_deduplicate_rows.sql` | Keep the latest row per group |
| `05_rank_variants_comparison.sql` | Ranking variants, `NTILE`, `PERCENT_RANK`, `CUME_DIST` |

## Usage

Run `setup_test_data.sql` first, then any numbered script.
Tested on PostgreSQL 14+; most queries also work on MySQL 8.0+, SQLite 3.25+, and SQL Server.
