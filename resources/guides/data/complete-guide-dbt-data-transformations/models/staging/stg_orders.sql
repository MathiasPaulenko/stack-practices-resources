-- models/staging/stg_orders.sql — Clean raw data
SELECT
    order_id,
    customer_id,
    CAST(created_at AS TIMESTAMP) AS created_at,
    CAST(updated_at AS TIMESTAMP) AS updated_at,
    CAST(subtotal AS DECIMAL(10, 2)) AS subtotal,
    CAST(tax AS DECIMAL(10, 2)) AS tax,
    CAST(shipping AS DECIMAL(10, 2)) AS shipping,
    TRIM(status) AS status,
    TRIM(currency) AS currency
FROM {{ source('raw', 'orders') }}
WHERE order_id IS NOT NULL
