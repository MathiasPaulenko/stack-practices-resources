-- tests/assert_row_count_range.sql
{{ config(severity='WARN') }}

SELECT
    CASE
        WHEN COUNT(*) < 100000 THEN 'FAIL: row count below minimum'
        WHEN COUNT(*) > 10000000 THEN 'FAIL: row count above maximum'
        ELSE 'OK'
    END AS result
FROM {{ ref('fct_orders') }}
HAVING result != 'OK'
