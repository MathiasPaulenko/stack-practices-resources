-- tests/assert_data_freshness.sql
SELECT
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(_ingested_at))) / 3600 AS hours_since_last_ingest
FROM {{ ref('fct_orders') }}
HAVING hours_since_last_ingest > 24
