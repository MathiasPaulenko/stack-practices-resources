-- Find indexes covering the same columns on the same table
SELECT pg_size_pretty(pg_relation_size(indexrelid)) AS size,
       relname AS table_name,
       indexrelname AS index_name,
       string_agg(attname, ', ' ORDER BY array_position(ix.indkey, attnum)) AS columns
FROM pg_index ix
JOIN pg_class c ON c.oid = ix.indrelid
JOIN pg_class ci ON ci.oid = ix.indexrelid
JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(ix.indkey)
GROUP BY relname, indexrelname, ix.indkey
HAVING count(*) > 0
ORDER BY pg_relation_size(indexrelid) DESC;
