-- int_orders_dedup.sql — keep the latest record per order_id
{{ config(materialized='incremental', unique_key='order_id') }}

SELECT
    order_id,
    customer_id,
    order_date,
    status,
    total_amount,
    currency,
    items,
    shipping_address,
    payment_method,
    discount_code,
    created_at,
    updated_at
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY updated_at DESC
        ) AS rn
    FROM {{ ref('stg_orders') }}
    {% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
)
WHERE rn = 1
