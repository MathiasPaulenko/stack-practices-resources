SELECT
    order_id::integer AS order_id,
    customer_id::integer AS customer_id,
    order_date::date AS order_date,
    amount::numeric(10,2) AS amount,
    status::varchar AS status
FROM {{ source('raw', 'orders') }}
