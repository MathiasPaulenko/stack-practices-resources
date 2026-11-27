-- Baseline full-text search setup: generated tsvector column + GIN index.
-- Requires PostgreSQL 12+ (generated columns).

ALTER TABLE articles
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || body)) STORED;

CREATE INDEX idx_articles_search
ON articles USING GIN (search_vector);

-- Search and rank results
SELECT id, title, ts_rank_cd(search_vector, query) AS rank
FROM articles, plainto_tsquery('english', 'database indexing') query
WHERE search_vector @@ query
ORDER BY rank DESC;
