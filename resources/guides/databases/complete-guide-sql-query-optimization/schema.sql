-- PostgreSQL schema + seed used by the other scripts in this folder.
-- Run first:  psql -d sandbox -f schema.sql

DROP TABLE IF EXISTS comments, order_items, orders, products, posts, authors, users CASCADE;

CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  age INT,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE authors (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  author_id BIGINT NOT NULL REFERENCES authors(id),
  title VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE comments (
  id BIGSERIAL PRIMARY KEY,
  post_id BIGINT NOT NULL REFERENCES posts(id),
  content TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(50) NOT NULL,
  price DECIMAL(10,2)
);

CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  order_number VARCHAR(20),
  total DECIMAL(10,2),
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
  id BIGSERIAL PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id),
  product_id BIGINT NOT NULL REFERENCES products(id),
  line_total DECIMAL(10,2)
);

-- Small seed for local EXPLAIN practice. For meaningful plans, scale up
-- with generate_series (see the commented block below).

INSERT INTO authors (name)
SELECT 'Author ' || i FROM generate_series(1, 20) AS i;

INSERT INTO users (name, email, status, age, created_at)
SELECT 'User ' || i,
       'user' || i || '@example.com',
       CASE WHEN i % 10 = 0 THEN 'archived' ELSE 'active' END,
       18 + (i % 60),
       now() - (i || ' days')::interval
FROM generate_series(1, 1000) AS i;

INSERT INTO posts (author_id, title, created_at)
SELECT 1 + (i % 20), 'Post ' || i, now() - (i || ' hours')::interval
FROM generate_series(1, 200) AS i;

INSERT INTO comments (post_id, content, created_at)
SELECT 1 + (i % 200), 'Comment ' || i, now() - (i || ' minutes')::interval
FROM generate_series(1, 2000) AS i;

INSERT INTO products (name, category, price)
SELECT 'Product ' || i,
       CASE WHEN i % 3 = 0 THEN 'electronics'
            WHEN i % 3 = 1 THEN 'books'
            ELSE 'other' END,
       (i % 500) + 0.99
FROM generate_series(1, 300) AS i;

INSERT INTO orders (user_id, order_number, total, status, created_at)
SELECT 1 + (i % 1000),
       'ORD-' || i,
       (i % 400) + 9.99,
       CASE WHEN i % 4 = 0 THEN 'completed'
            WHEN i % 4 = 1 THEN 'shipped'
            WHEN i % 4 = 2 THEN 'pending'
            ELSE 'cancelled' END,
       now() - (i || ' hours')::interval
FROM generate_series(1, 5000) AS i;

INSERT INTO order_items (order_id, product_id, line_total)
SELECT 1 + (i % 5000), 1 + (i % 300), (i % 200) + 0.99
FROM generate_series(1, 12000) AS i;

ANALYZE;

-- For realistic plans on a throwaway database, bump the row counts:
-- users 100k, orders 500k, order_items 1.5M — adjust the generate_series
-- bounds above and re-run ANALYZE.
