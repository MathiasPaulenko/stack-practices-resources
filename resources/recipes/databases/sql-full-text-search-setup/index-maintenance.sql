-- GIN index maintenance for FTS workloads.

-- fastupdate buffers pending index entries; good for frequently updated tables
CREATE INDEX idx_articles_search
ON articles USING GIN (search_vector) WITH (fastupdate = true);

-- Partial index: only the rows you actually search
CREATE INDEX idx_articles_published_search
ON articles USING GIN (search_vector)
WHERE status = 'published';

-- Monitor index size / bloat
SELECT schemaname, tablename, indexname,
       pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes
WHERE indexname LIKE '%search%';

-- Keep planner statistics fresh so it picks the GIN index
ANALYZE articles;

-- Always paginate ranked results
SELECT id, title, ts_rank_cd(search_vector, query) AS rank
FROM articles, plainto_tsquery('english', 'database indexing') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20 OFFSET 0;

-- Optional: RUM extension stores ranking data inside the index itself
-- CREATE EXTENSION rum;
-- CREATE INDEX idx_articles_rum ON articles USING rum (search_vector);
