-- Aggregating across hierarchy.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 05_aggregation_hierarchy.sql

WITH RECURSIVE category_tree AS (
    SELECT id, parent_id, name, 1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.parent_id, c.name, ct.depth + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT
    ct.id,
    ct.name,
    ct.depth,
    COUNT(p.id) AS product_count,
    COALESCE(SUM(p.price), 0) AS total_value
FROM category_tree ct
LEFT JOIN products p ON p.category_id = ct.id
GROUP BY ct.id, ct.name, ct.depth
ORDER BY ct.depth, ct.name;
