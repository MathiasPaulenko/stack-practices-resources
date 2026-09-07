-- Test data for recursive CTE examples.
-- Works in PostgreSQL 16+, MySQL 8.0+, SQLite 3.8.4+, SQL Server 2019+.
-- Run this first before any other script.

-- Categories tree
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES categories(id),
    name VARCHAR(100) NOT NULL
);

INSERT INTO categories (id, parent_id, name) VALUES
    (1, NULL, 'Electronics'),
    (2, 1, 'Computers'),
    (3, 1, 'Phones'),
    (4, 2, 'Laptops'),
    (5, 2, 'Desktops'),
    (6, 3, 'Smartphones'),
    (7, 3, 'Accessories'),
    (8, 4, 'Gaming Laptops'),
    (9, 4, 'Ultrabooks'),
    (10, 6, 'Android'),
    (11, 6, 'iPhone')
ON CONFLICT (id) DO NOTHING;

-- Employees (org chart)
CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    manager_id INTEGER REFERENCES employees(employee_id),
    employee_name VARCHAR(100) NOT NULL
);

INSERT INTO employees (employee_id, manager_id, employee_name) VALUES
    (1, NULL, 'CEO'),
    (2, 1, 'VP Engineering'),
    (3, 1, 'VP Sales'),
    (4, 2, 'Engineering Manager'),
    (5, 2, 'DevOps Lead'),
    (6, 3, 'Sales Manager'),
    (7, 4, 'Senior Developer'),
    (8, 4, 'Junior Developer'),
    (9, 5, 'DevOps Engineer'),
    (10, 6, 'Sales Rep')
ON CONFLICT (employee_id) DO NOTHING;

-- Products (for aggregation example)
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO products (category_id, name, price) VALUES
    (8, 'Alienware m15', 1999.99),
    (9, 'MacBook Air M3', 1199.99),
    (10, 'Samsung Galaxy S24', 899.99),
    (11, 'iPhone 15 Pro', 1099.99),
    (7, 'USB-C Cable', 19.99),
    (5, 'Dell OptiPlex', 799.99)
ON CONFLICT DO NOTHING;

-- Nodes (for cycle detection and roll-up)
CREATE TABLE IF NOT EXISTS nodes (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES nodes(id),
    name VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) DEFAULT 0
);

INSERT INTO nodes (id, parent_id, name, amount) VALUES
    (1, NULL, 'Root', 100.00),
    (2, 1, 'Child A', 50.00),
    (3, 1, 'Child B', 75.00),
    (4, 2, 'Grandchild A1', 25.00),
    (5, 2, 'Grandchild A2', 30.00),
    (6, 3, 'Grandchild B1', 40.00)
ON CONFLICT (id) DO NOTHING;

-- Bill of materials
CREATE TABLE IF NOT EXISTS bill_of_materials (
    id SERIAL PRIMARY KEY,
    assembly_id VARCHAR(50) NOT NULL,
    component_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1
);

INSERT INTO bill_of_materials (assembly_id, component_id, quantity) VALUES
    ('PRODUCT-001', 'SUB-ASSY-A', 1),
    ('PRODUCT-001', 'SUB-ASSY-B', 2),
    ('SUB-ASSY-A', 'PART-X', 3),
    ('SUB-ASSY-A', 'PART-Y', 1),
    ('SUB-ASSY-B', 'PART-Z', 5),
    ('PART-X', 'RAW-MATERIAL-1', 2)
ON CONFLICT DO NOTHING;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_employees_manager ON employees(manager_id);
CREATE INDEX IF NOT EXISTS idx_nodes_parent ON nodes(parent_id);
