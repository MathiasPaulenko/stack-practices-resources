-- Top 3 highest-paid employees per department
WITH ranked AS (
  SELECT
    department,
    employee,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
)
SELECT department, employee, salary
FROM ranked
WHERE rn <= 3
ORDER BY department, salary DESC;
