-- Moving average over an explicit window frame + year-over-year growth
SELECT
  month,
  revenue,
  AVG(revenue) OVER (
    ORDER BY month
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS moving_avg_3m,
  SUM(revenue) OVER (
    ORDER BY month
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS cumulative_revenue,
  ROUND(
    (revenue - LAG(revenue, 12) OVER (ORDER BY month)) /
     NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0) * 100, 2
  ) AS yoy_pct_change
FROM monthly_revenue
ORDER BY month;
