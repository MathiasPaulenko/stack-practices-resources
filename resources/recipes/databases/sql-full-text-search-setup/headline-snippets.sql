-- Highlighted snippets of matching text.
-- Only run ts_headline on the page you return; it re-parses the document per row.

SELECT
  id,
  title,
  ts_headline('english', body, query, 'MaxWords=35, MinWords=15') AS snippet,
  ts_rank_cd(search_vector, query) AS rank
FROM articles, plainto_tsquery('english', 'database indexing') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
