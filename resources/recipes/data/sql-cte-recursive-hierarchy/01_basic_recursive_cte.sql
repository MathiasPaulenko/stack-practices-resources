-- Basic recursive CTE structure.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 01_basic_recursive_cte.sql

WITH RECURSIVE hierarchy AS (
    -- Anchor member: starting point
    SELECT
        id,
        parent_id,
        name,
        1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive member: join back to the CTE
    SELECT
        c.id,
        c.parent_id,
        c.name,
        h.depth + 1 AS depth
    FROM categories c
    INNER JOIN hierarchy h ON c.parent_id = h.id
)
SELECT * FROM hierarchy ORDER BY depth, name;
