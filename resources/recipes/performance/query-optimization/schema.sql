-- Demo schema for the query-optimization recipe (PostgreSQL).
-- Run against an empty database: psql -d demo -f schema.sql

DROP TABLE IF EXISTS order_items, orders, customers, products CASCADE;

CREATE TABLE customers (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE products (
    id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name  TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

CREATE TABLE orders (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id),
    status      TEXT NOT NULL,
    total       NUMERIC(12,2) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id   BIGINT NOT NULL REFERENCES orders(id),
    product_id BIGINT NOT NULL REFERENCES products(id),
    quantity   INT NOT NULL,
    price      NUMERIC(10,2) NOT NULL
);

-- Seed data sized to make Seq Scan vs Index Scan differences visible.
INSERT INTO customers (name, email, created_at)
SELECT 'customer_' || i, 'customer' || i || '@example.com',
       now() - (random() * interval '365 days')
FROM generate_series(1, 5000) i;

INSERT INTO products (name, price)
SELECT 'product_' || i, (random() * 500 + 5)::numeric(10,2)
FROM generate_series(1, 500) i;

INSERT INTO orders (customer_id, status, total, created_at)
SELECT (random() * 4999 + 1)::bigint,
       (ARRAY['pending','paid','shipped','cancelled'])[floor(random()*4+1)],
       (random() * 1000 + 10)::numeric(12,2),
       now() - (random() * interval '365 days')
FROM generate_series(1, 200000) i;

INSERT INTO order_items (order_id, product_id, quantity, price)
SELECT (random() * 199999 + 1)::bigint,
       (random() * 499 + 1)::bigint,
       floor(random() * 5 + 1),
       (random() * 500 + 5)::numeric(10,2)
FROM generate_series(1, 500000) i;

ANALYZE;
