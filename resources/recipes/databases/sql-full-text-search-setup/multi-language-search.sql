-- Per-row language: each row is stemmed with its own dictionary.
-- The language column must hold valid text search config names
-- ('english', 'spanish', 'german', ...).

ALTER TABLE articles
ADD COLUMN search_vector_multi tsvector
GENERATED ALWAYS AS (
  to_tsvector(coalesce(language, 'english'), title || ' ' || body)
) STORED;

CREATE INDEX idx_articles_search_multi
ON articles USING GIN (search_vector_multi);

-- Search in the appropriate language
SELECT id, title
FROM articles, plainto_tsquery('spanish', 'base de datos') query
WHERE search_vector_multi @@ query
ORDER BY ts_rank_cd(search_vector_multi, query) DESC;
