-- int_orders_enriched.sql — join orders with the customer dimension
SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.total_amount,
    o.currency,
    o.items,
    o.payment_method,
    o.discount_code,
    c.customer_segment,
    c.customer_country,
    c.customer_tier,
    c.is_enterprise
FROM {{ ref('int_orders_dedup') }} o
LEFT JOIN {{ ref('dim_customers') }} c
    ON o.customer_id = c.customer_id
