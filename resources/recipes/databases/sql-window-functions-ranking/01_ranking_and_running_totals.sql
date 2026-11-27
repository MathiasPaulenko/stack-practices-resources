-- Ranking and running totals per partition
SELECT
  department,
  employee,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
  RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rank_num,
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_num,
  SUM(salary)  OVER (PARTITION BY department ORDER BY salary DESC) AS running_total,
  LAG(salary)  OVER (PARTITION BY department ORDER BY salary DESC) AS prev_salary
FROM employees
ORDER BY department, salary DESC;
