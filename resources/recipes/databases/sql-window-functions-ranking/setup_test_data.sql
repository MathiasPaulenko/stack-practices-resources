-- Test data for window function examples (PostgreSQL-compatible)
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
  department TEXT,
  employee   TEXT,
  salary     NUMERIC(10,2)
);

INSERT INTO employees VALUES
  ('Engineering', 'Ana',    100),
  ('Engineering', 'Bruno',   90),
  ('Engineering', 'Carla',   90),
  ('Engineering', 'Diego',   80),
  ('Sales',       'Elena',   95),
  ('Sales',       'Fabio',   85),
  ('Sales',       'Gabi',    70);

DROP TABLE IF EXISTS monthly_revenue;
CREATE TABLE monthly_revenue (
  month   DATE,
  revenue NUMERIC(12,2)
);

INSERT INTO monthly_revenue
SELECT (DATE '2024-01-01' + (n || ' months')::interval)::date, 80000 + (n * 1370) % 25000
FROM generate_series(0, 23) AS n;

DROP TABLE IF EXISTS user_records;
CREATE TABLE user_records (
  user_id    INT,
  email      TEXT,
  updated_at TIMESTAMPTZ
);

INSERT INTO user_records VALUES
  (1, 'old@example.com',  '2025-01-10 08:00:00+00'),
  (1, 'new@example.com',  '2025-03-14 09:30:00+00'),
  (2, 'two@example.com',  '2025-02-01 12:00:00+00'),
  (2, 'two2@example.com', '2025-04-05 15:45:00+00');
