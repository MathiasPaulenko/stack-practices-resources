# CTEs Recursivas para Consultas de Datos Jerárquicos — Recursos Complementarios

Código complementario para [CTEs Recursivas para Consultas de Datos Jerárquicos](https://stackpractices.com/es/recipes/sql-cte-recursive-hierarchy/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `setup_test_data.sql` | Datos de prueba para todos los ejemplos (categorías, empleados, productos, nodos, BOM) |
| `01_basic_recursive_cte.sql` | Estructura básica de CTE recursiva |
| `02_org_chart.sql` | Org chart: todos los reports de un manager específico |
| `03_category_tree.sql` | Árbol de categorías con path completo |
| `04_ancestors_bottom_up.sql` | Encontrar todos los ancestors (traversal bottom-up) |
| `05_aggregation_hierarchy.sql` | Agregar a través de la jerarquía |
| `06_rollup.sql` | Roll-up: sumar valores de hijos a ancestors usando path containment |
| `07_cycle_detection.sql` | Detección de ciclos con tracking de path |
| `08_depth_limit.sql` | Limitar profundidad de recursión |
| `09_bill_of_materials.sql` | Explosión de bill of materials |
| `10_postgresql_array_path.sql` | PostgreSQL: usar ARRAY para path con prevención de ciclos |
| `11_mysql_recursive.sql` | MySQL 8.0+: sintaxis de CTE recursiva |
| `12_sql_server_no_recursive.sql` | SQL Server: sin keyword RECURSIVE, OPTION (MAXRECURSION) |
| `13_snowflake_connect_by.sql` | Snowflake: usar CONNECT BY (alternativa) |

## Requisitos

- PostgreSQL 16+ (recomendado para testing, soporta todos los ejemplos)
- MySQL 8.0+ (para `11_mysql_recursive.sql`)
- SQL Server 2019+ (para `12_sql_server_no_recursive.sql`)
- Snowflake (para `13_snowflake_connect_by.sql`)
- SQLite 3.8.4+ (soporta CTEs recursivas, pero sin tipo SERIAL — modificar schema)

## Ejecución

### PostgreSQL

```bash
# Crear base de datos
createdb testdb

# Cargar datos de prueba
psql -d testdb -f setup_test_data.sql

# Correr cualquier ejemplo
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

## Licencia

MIT — ver el repositorio principal para detalles.
