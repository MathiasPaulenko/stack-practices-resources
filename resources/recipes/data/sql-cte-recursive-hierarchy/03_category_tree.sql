-- Category tree with full path.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 03_category_tree.sql

WITH RECURSIVE category_tree AS (
    SELECT
        id,
        parent_id,
        name,
        CAST(name AS VARCHAR(1000)) AS full_path,
        1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        c.id,
        c.parent_id,
        c.name,
        ct.full_path || ' / ' || c.name,
        ct.depth + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT
    id,
    name,
    full_path,
    depth
FROM category_tree
ORDER BY full_path;
