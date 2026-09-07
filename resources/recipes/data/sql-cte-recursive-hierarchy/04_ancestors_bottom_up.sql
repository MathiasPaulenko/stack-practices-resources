-- Find all ancestors (bottom-up traversal).
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 04_ancestors_bottom_up.sql

WITH RECURSIVE ancestors AS (
    -- Anchor: starting node (e.g., iPhone category)
    SELECT
        id,
        parent_id,
        name,
        1 AS depth
    FROM categories
    WHERE id = 11

    UNION ALL

    -- Recursive: go up to parent
    SELECT
        c.id,
        c.parent_id,
        c.name,
        a.depth + 1
    FROM categories c
    INNER JOIN ancestors a ON c.id = a.parent_id
)
SELECT * FROM ancestors ORDER BY depth DESC;
