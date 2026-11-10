-- SCD Type 2: keep full history with validity windows.
-- PostgreSQL dialect; for MySQL use CURDATE() and ON DUPLICATE KEY logic.

CREATE TABLE dim_customers (
    customer_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    segment VARCHAR(50),
    valid_date DATE NOT NULL,
    expiration_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    UNIQUE(customer_id, valid_date)
);

-- 1. Insert new versions for new or changed customers
INSERT INTO dim_customers (customer_id, name, email, segment, valid_date)
SELECT
    s.customer_id,
    s.name,
    s.email,
    s.segment,
    CURRENT_DATE
FROM staging_customers s
LEFT JOIN dim_customers d
    ON s.customer_id = d.customer_id AND d.is_current = TRUE
WHERE d.customer_sk IS NULL
   OR (d.name <> s.name OR d.email <> s.email OR d.segment <> s.segment);

-- 2. Expire the previous current rows
UPDATE dim_customers d
SET expiration_date = CURRENT_DATE - 1,
    is_current = FALSE
FROM staging_customers s
WHERE d.customer_id = s.customer_id
  AND d.is_current = TRUE
  AND (d.name <> s.name OR d.email <> s.email OR d.segment <> s.segment);
