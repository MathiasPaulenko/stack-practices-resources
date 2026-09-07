-- SQL Server: no RECURSIVE keyword needed.
-- Uses OPTION (MAXRECURSION) to override default 100-level limit.
-- Run: sqlcmd -S localhost -d testdb -i setup_test_data.sql -E && sqlcmd -S localhost -d testdb -i 12_sql_server_no_recursive.sql -E

WITH org_tree AS (
    SELECT employee_id, manager_id, employee_name, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.employee_id, e.manager_id, e.employee_name, ot.level + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.employee_id
)
SELECT * FROM org_tree OPTION (MAXRECURSION 100);
