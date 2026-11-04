-- models/marts/core/fct_orders.sql — Fact table (incremental)
{{ config(materialized='incremental', unique_key='order_id') }}

SELECT
    o.order_id,
    o.customer_id,
    o.created_at,
    o.status,
    o.total_amount,
    o.discount_rate,
    ROUND(o.total_amount * (1 - o.discount_rate), 2) AS net_amount,
    d.country,
    d.customer_tier
FROM {{ ref('int_orders_enriched') }} o
LEFT JOIN {{ ref('dim_customers') }} d
    ON o.customer_id = d.customer_id
{% if is_incremental() %}
WHERE o.created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
