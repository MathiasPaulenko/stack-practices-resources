SELECT
    c.customer_id,
    c.customer_name,
    c.customer_tier,
    c.city,
    COUNT(o.order_id) AS completed_orders,
    COALESCE(SUM(o.amount), 0) AS lifetime_value
FROM {{ ref('stg_customers') }} c
LEFT JOIN {{ ref('stg_orders') }} o
    ON c.customer_id = o.customer_id
    AND o.status = 'completed'
GROUP BY c.customer_id, c.customer_name, c.customer_tier, c.city
