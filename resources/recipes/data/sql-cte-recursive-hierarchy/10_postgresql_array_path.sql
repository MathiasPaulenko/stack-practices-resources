-- PostgreSQL: using ARRAY for path with cycle prevention.
-- PostgreSQL 16+ only (uses ARRAY type and != ALL operator).
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 10_postgresql_array_path.sql

WITH RECURSIVE category_tree AS (
    SELECT
        id,
        parent_id,
        name,
        ARRAY[id] AS path,
        1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        c.id,
        c.parent_id,
        c.name,
        ct.path || c.id,
        ct.depth + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
    WHERE c.id != ALL(ct.path)  -- Cycle prevention
)
SELECT id, name, path, depth FROM category_tree ORDER BY path;
