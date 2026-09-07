-- Org chart: all reports of a specific manager.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 02_org_chart.sql

WITH RECURSIVE reports AS (
    -- Anchor: direct reports of manager 2 (VP Engineering)
    SELECT
        employee_id,
        manager_id,
        employee_name,
        1 AS depth,
        CAST(manager_id AS VARCHAR(1000)) AS path
    FROM employees
    WHERE manager_id = 2

    UNION ALL

    -- Recursive: reports of reports
    SELECT
        e.employee_id,
        e.manager_id,
        e.employee_name,
        r.depth + 1,
        r.path || ' -> ' || CAST(e.manager_id AS VARCHAR)
    FROM employees e
    INNER JOIN reports r ON e.manager_id = r.employee_id
)
SELECT
    employee_id,
    employee_name,
    depth,
    path
FROM reports
ORDER BY depth, employee_name;
