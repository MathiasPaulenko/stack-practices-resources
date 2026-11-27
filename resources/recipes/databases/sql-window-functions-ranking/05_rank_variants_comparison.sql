-- ROW_NUMBER vs RANK vs DENSE_RANK side by side (ties at salary = 90)
SELECT
  employee,
  salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
  RANK()       OVER (ORDER BY salary DESC) AS rnk,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM employees
ORDER BY salary DESC;

-- Percentiles and bucketing
SELECT
  employee,
  salary,
  NTILE(4)       OVER (ORDER BY salary DESC) AS quartile,
  PERCENT_RANK() OVER (ORDER BY salary DESC) AS pct_rank,
  CUME_DIST()    OVER (ORDER BY salary DESC) AS cumulative_dist
FROM employees;
