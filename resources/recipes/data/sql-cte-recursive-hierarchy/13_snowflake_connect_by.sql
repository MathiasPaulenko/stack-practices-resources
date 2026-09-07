-- Snowflake: using CONNECT BY (alternative to recursive CTE).
-- Snowflake supports both CONNECT BY and recursive CTEs.
-- Run in Snowflake worksheet after loading test data.

SELECT
    employee_id,
    manager_id,
    employee_name,
    LEVEL AS depth,
    SYS_CONNECT_BY_PATH(employee_name, ' -> ') AS path
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR employee_id = manager_id
ORDER SIBLINGS BY employee_name;
