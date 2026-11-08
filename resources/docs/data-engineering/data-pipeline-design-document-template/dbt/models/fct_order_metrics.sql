-- fct_order_metrics.sql — daily order metrics for the analytics mart
{{ config(materialized='incremental', unique_key='order_date') }}

SELECT
    DATE(order_date) AS order_date,
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(total_amount) AS gross_revenue,
    SUM(CASE WHEN status = 'refunded' THEN total_amount ELSE 0 END) AS refund_amount,
    SUM(CASE WHEN discount_code IS NOT NULL THEN 1 ELSE 0 END) AS discounted_orders,
    AVG(total_amount) AS avg_order_value,
    SUM(CASE WHEN is_enterprise THEN 1 ELSE 0 END) AS enterprise_orders,
    SUM(CASE WHEN is_enterprise THEN total_amount ELSE 0 END) AS enterprise_revenue
FROM {{ ref('int_orders_enriched') }}
{% if is_incremental() %}
WHERE DATE(order_date) > (SELECT MAX(order_date) FROM {{ this }})
{% endif %}
GROUP BY DATE(order_date)
