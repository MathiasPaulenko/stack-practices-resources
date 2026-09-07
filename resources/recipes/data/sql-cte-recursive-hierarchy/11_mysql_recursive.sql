-- MySQL 8.0+: recursive CTE syntax.
-- Run: mysql -u root -p testdb < setup_test_data.sql && mysql -u root -p testdb < 11_mysql_recursive.sql

WITH RECURSIVE org_tree AS (
    SELECT employee_id, manager_id, employee_name, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.employee_id, e.manager_id, e.employee_name, ot.level + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.employee_id
)
SELECT * FROM org_tree WHERE level <= 3 ORDER BY level;
