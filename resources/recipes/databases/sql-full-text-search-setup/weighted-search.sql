-- Weighted search: title matches rank higher than body matches.

ALTER TABLE articles
ADD COLUMN search_vector_weighted tsvector
GENERATED ALWAYS AS (
  setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
  setweight(to_tsvector('english', coalesce(body, '')), 'B')
) STORED;

CREATE INDEX idx_articles_search_weighted
ON articles USING GIN (search_vector_weighted);

SELECT id, title,
  ts_rank_cd(search_vector_weighted, query) AS rank
FROM articles, plainto_tsquery('english', 'database indexing') query
WHERE search_vector_weighted @@ query
ORDER BY rank DESC;
