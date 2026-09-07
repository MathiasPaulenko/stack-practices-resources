-- Cycle detection in recursive traversal.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 07_cycle_detection.sql

WITH RECURSIVE traversal AS (
    SELECT
        id,
        parent_id,
        CAST(id AS VARCHAR(1000)) AS path,
        1 AS depth,
        false AS has_cycle
    FROM nodes
    WHERE id = 1

    UNION ALL

    SELECT
        n.id,
        n.parent_id,
        t.path || ' -> ' || CAST(n.id AS VARCHAR),
        t.depth + 1,
        POSITION(CAST(n.id AS VARCHAR) IN t.path) > 0 AS has_cycle
    FROM nodes n
    INNER JOIN traversal t ON n.parent_id = t.id
    WHERE t.has_cycle = false
    AND t.depth < 100  -- Safety limit
)
SELECT * FROM traversal WHERE has_cycle = true;

-- If no cycles exist in test data, this returns empty.
-- To test cycle detection, insert a cycle:
-- UPDATE nodes SET parent_id = 4 WHERE id = 1;  -- Creates cycle: 1→2→4→1
