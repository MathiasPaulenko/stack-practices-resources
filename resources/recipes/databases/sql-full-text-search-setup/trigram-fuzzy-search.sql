-- Fuzzy matching with pg_trgm (contrib extension; needs elevated privilege).
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_articles_title_trgm
ON articles USING GIN (title gin_trgm_ops);

-- Finds titles similar to the misspelled 'databse indexing'
SELECT id, title, similarity(title, 'databse indexing') AS sim
FROM articles
WHERE title % 'databse indexing'
ORDER BY sim DESC
LIMIT 10;

-- Combined FTS + trigram: meaning + typo tolerance
SELECT a.id, a.title,
  ts_rank_cd(a.search_vector, ftq) AS text_rank,
  similarity(a.title, 'databse indexing') AS trigram_rank
FROM articles a,
  plainto_tsquery('english', 'database indexing') ftq
WHERE a.search_vector @@ ftq
   OR a.title % 'databse indexing'
ORDER BY (text_rank + trigram_rank) DESC
LIMIT 20;

-- Autocomplete / prefix search
SELECT title
FROM articles
WHERE title LIKE 'data%'
ORDER BY similarity(title, 'data') DESC
LIMIT 10;
