-- Limiting recursion depth.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 08_depth_limit.sql

WITH RECURSIVE limited_tree AS (
    SELECT id, parent_id, name, 1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.parent_id, c.name, lt.depth + 1
    FROM categories c
    INNER JOIN limited_tree lt ON c.parent_id = lt.id
    WHERE lt.depth < 3  -- Only 3 levels deep
)
SELECT * FROM limited_tree ORDER BY depth, name;
