# Recursive CTEs for Hierarchical Data Queries — Companion Resources

Companion code for [Recursive CTEs for Hierarchical Data Queries](https://stackpractices.com/recipes/sql-cte-recursive-hierarchy/).

## Files

| File | Description |
| --- | --- |
| `setup_test_data.sql` | Test data for all examples (categories, employees, products, nodes, BOM) |
| `01_basic_recursive_cte.sql` | Basic recursive CTE structure |
| `02_org_chart.sql` | Org chart: all reports of a specific manager |
| `03_category_tree.sql` | Category tree with full path |
| `04_ancestors_bottom_up.sql` | Find all ancestors (bottom-up traversal) |
| `05_aggregation_hierarchy.sql` | Aggregating across hierarchy |
| `06_rollup.sql` | Roll-up: sum child values to ancestors using path containment |
| `07_cycle_detection.sql` | Cycle detection with path tracking |
| `08_depth_limit.sql` | Limiting recursion depth |
| `09_bill_of_materials.sql` | Bill of materials explosion |
| `10_postgresql_array_path.sql` | PostgreSQL: using ARRAY for path with cycle prevention |
| `11_mysql_recursive.sql` | MySQL 8.0+: recursive CTE syntax |
| `12_sql_server_no_recursive.sql` | SQL Server: no RECURSIVE keyword, OPTION (MAXRECURSION) |
| `13_snowflake_connect_by.sql` | Snowflake: using CONNECT BY (alternative) |

## Requirements

- PostgreSQL 16+ (recommended for testing, supports all examples)
- MySQL 8.0+ (for `11_mysql_recursive.sql`)
- SQL Server 2019+ (for `12_sql_server_no_recursive.sql`)
- Snowflake (for `13_snowflake_connect_by.sql`)
- SQLite 3.8.4+ (supports recursive CTEs, but no SERIAL type — modify schema)

## Running

### PostgreSQL

```bash
# Create database
createdb testdb

# Load test data
psql -d testdb -f setup_test_data.sql

# Run any example
psql -d testdb -f 01_basic_recursive_cte.sql
```

### MySQL 8.0+

```bash
mysql -u root -p -e "CREATE DATABASE testdb"
mysql -u root -p testdb < setup_test_data.sql
mysql -u root -p testdb < 11_mysql_recursive.sql
```

### SQL Server

```bash
sqlcmd -S localhost -d testdb -i setup_test_data.sql -E
sqlcmd -S localhost -d testdb -i 12_sql_server_no_recursive.sql -E
```

## License

MIT — see the main repository for details.
