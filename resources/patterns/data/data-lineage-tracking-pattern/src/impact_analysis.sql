-- impact_analysis.sql — find all downstream tables affected by a source change
-- Assumes a lineage_edges(upstream_table, upstream_column, downstream_table, downstream_column) table.
WITH RECURSIVE lineage_graph AS (
    -- Start from the changed table
    SELECT
        downstream_table,
        downstream_column,
        upstream_table,
        upstream_column,
        1 AS depth
    FROM lineage_edges
    WHERE upstream_table = 'source.customers'
      AND upstream_column = 'email'

    UNION ALL

    -- Recurse through downstream dependencies
    SELECT
        e.downstream_table,
        e.downstream_column,
        e.upstream_table,
        e.upstream_column,
        g.depth + 1
    FROM lineage_edges e
    JOIN lineage_graph g ON e.upstream_table = g.downstream_table
                        AND e.upstream_column = g.downstream_column
    WHERE g.depth < 10  -- prevent infinite loops
)
SELECT DISTINCT
    downstream_table,
    downstream_column,
    depth,
    STRING_AGG(upstream_table || '.' || upstream_column, ' -> ') AS path
FROM lineage_graph
GROUP BY downstream_table, downstream_column, depth
ORDER BY depth, downstream_table;
