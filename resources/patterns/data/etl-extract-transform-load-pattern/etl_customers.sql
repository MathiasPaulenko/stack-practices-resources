-- etl_customers.sql — SQL ETL with staging tables (PostgreSQL 15+, for MERGE)
-- Reference implementation for https://stackpractices.com/patterns/etl-extract-transform-load-pattern/

-- Stage 1: Extract — copy raw data to staging
CREATE TABLE stg_customers AS
SELECT
    id,
    email,
    first_name,
    last_name,
    status,
    created_at,
    updated_at,
    CURRENT_TIMESTAMP AS _extracted_at,
    'daily_batch' AS _source
FROM source_db.customers
WHERE updated_at >= CURRENT_DATE - INTERVAL '1 day';

-- Stage 2: Transform — clean and reshape into a second staging table
CREATE TABLE tmp_customers AS
SELECT
    id,
    LOWER(TRIM(email)) AS email,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    status,
    (status = 'active') AS is_active,
    CONCAT(TRIM(first_name), ' ', TRIM(last_name)) AS full_name,
    COALESCE(created_at, _extracted_at) AS created_at,
    updated_at
FROM stg_customers
WHERE id IS NOT NULL
  AND email IS NOT NULL;

-- Stage 3: Load — upsert to warehouse
MERGE INTO warehouse.customers AS target
USING tmp_customers AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET
        email = source.email,
        first_name = source.first_name,
        last_name = source.last_name,
        status = source.status,
        is_active = source.is_active,
        full_name = source.full_name,
        updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (id, email, first_name, last_name, status, is_active, full_name, created_at, updated_at)
    VALUES (source.id, source.email, source.first_name, source.last_name,
            source.status, source.is_active, source.full_name, source.created_at, source.updated_at);

-- Cleanup: staging tables are disposable once the load is validated
DROP TABLE stg_customers;
DROP TABLE tmp_customers;
