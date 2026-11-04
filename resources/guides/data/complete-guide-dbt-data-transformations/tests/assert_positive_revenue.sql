-- tests/assert_positive_revenue.sql — fails if any negative revenue rows exist
SELECT
    order_id,
    total_amount
FROM {{ ref('fct_orders') }}
WHERE total_amount < 0
