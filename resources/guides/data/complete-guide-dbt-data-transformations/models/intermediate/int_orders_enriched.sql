-- models/intermediate/int_orders_enriched.sql — Join staging models
SELECT
    o.order_id,
    o.customer_id,
    o.created_at,
    o.status,
    o.subtotal + o.tax + o.shipping AS total_amount,
    c.country,
    c.customer_tier,
    CASE
        WHEN c.customer_tier = 'premium' THEN 0.10
        WHEN c.customer_tier = 'gold' THEN 0.05
        ELSE 0.00
    END AS discount_rate
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_customers') }} c
    ON o.customer_id = c.customer_id
