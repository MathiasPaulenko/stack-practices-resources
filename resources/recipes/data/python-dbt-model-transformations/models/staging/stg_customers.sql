SELECT
    customer_id::integer AS customer_id,
    customer_name::varchar AS customer_name,
    customer_tier::varchar AS customer_tier,
    city::varchar AS city
FROM {{ source('raw', 'customers') }}
