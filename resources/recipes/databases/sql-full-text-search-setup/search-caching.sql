-- Cache and aggregate search results.

-- Materialized view for popular searches; refresh on a schedule
CREATE MATERIALIZED VIEW popular_search_results AS
SELECT a.id, a.title,
  ts_rank_cd(a.search_vector, query) AS rank
FROM articles a,
  plainto_tsquery('english', 'database') query
WHERE a.search_vector @@ query
ORDER BY rank DESC
LIMIT 100;

REFRESH MATERIALIZED VIEW CONCURRENTLY popular_search_results;

-- Faceted search: combine FTS with category/status filters
SELECT a.id, a.title, a.category,
  ts_rank_cd(a.search_vector, query) AS rank
FROM articles a,
  plainto_tsquery('english', 'database indexing') query
WHERE a.search_vector @@ query
  AND a.category IN ('engineering', 'data-science')
  AND a.status = 'published'
ORDER BY rank DESC
LIMIT 20;

-- Aggregate matches per category
SELECT a.category, COUNT(*) AS match_count
FROM articles a,
  plainto_tsquery('english', 'database') query
WHERE a.search_vector @@ query
GROUP BY a.category
ORDER BY match_count DESC;
