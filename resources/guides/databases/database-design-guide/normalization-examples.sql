-- 1NF / 2NF / 3NF violation-fix examples

-- Violation: multiple phone numbers in one column
CREATE TABLE bad_users (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  phones VARCHAR(500) -- '555-1234,555-5678'
);

-- Fix: separate table for phone numbers
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE user_phones (
  user_id INT REFERENCES users(id),
  phone VARCHAR(20),
  PRIMARY KEY (user_id, phone)
);


-- Violation: order_date depends only on order_id, not on (order_id, product_id)
CREATE TABLE bad_order_items (
  order_id INT,
  product_id INT,
  order_date DATE,  -- depends only on order_id
  quantity INT,
  PRIMARY KEY (order_id, product_id)
);

-- Fix: split into orders and order_items
CREATE TABLE orders (
  id INT PRIMARY KEY,
  order_date DATE
);

CREATE TABLE order_items (
  order_id INT REFERENCES orders(id),
  product_id INT,
  quantity INT,
  PRIMARY KEY (order_id, product_id)
);


-- Violation: city_name depends on zip_code, not on user_id
CREATE TABLE bad_users (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  zip_code VARCHAR(10),
  city_name VARCHAR(100)  -- depends on zip_code
);

-- Fix: separate table for zip → city mapping
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  zip_code VARCHAR(10)
);

CREATE TABLE zip_cities (
  zip_code VARCHAR(10) PRIMARY KEY,
  city_name VARCHAR(100)
);
