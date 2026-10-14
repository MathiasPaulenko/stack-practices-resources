SELECT *
FROM {{ ref('fct_orders') }}
WHERE amount < 0
