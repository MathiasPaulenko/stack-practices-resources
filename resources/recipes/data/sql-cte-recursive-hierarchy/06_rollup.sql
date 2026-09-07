-- Roll-up: sum child values to all ancestors using path containment.
-- This version uses a recursive path array for accurate roll-up.
-- Run: psql -d testdb -f setup_test_data.sql && psql -d testdb -f 06_rollup.sql

WITH RECURSIVE descendants AS (
    SELECT
        id,
        parent_id,
        name,
        amount,
        1 AS depth,
        ARRAY[id] AS path
    FROM nodes
    WHERE id = 1  -- Root node

    UNION ALL

    SELECT
        n.id,
        n.parent_id,
        n.name,
        n.amount,
        d.depth + 1,
        d.path || n.id
    FROM nodes n
    INNER JOIN descendants d ON n.parent_id = d.id
)
SELECT
    d.id,
    d.name,
    d.depth,
    d.amount AS own_amount,
    (
        SELECT SUM(child.amount)
        FROM descendants child
        WHERE child.id != d.id
          AND child.path[1:d.depth] = d.path[1:d.depth]
    ) AS descendant_total
FROM descendants d
ORDER BY d.depth, d.name;
