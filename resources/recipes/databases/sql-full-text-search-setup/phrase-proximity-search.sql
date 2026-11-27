-- Exact phrase match
SELECT id, title
FROM articles, phraseto_tsquery('english', 'database indexing') query
WHERE search_vector @@ query;

-- Proximity: words adjacent (<->)
SELECT id, title
FROM articles, to_tsquery('english', 'database <-> indexing') query
WHERE search_vector @@ query;

-- Words within N positions: <N> operator
SELECT id, title
FROM articles, to_tsquery('english', 'database <3> indexing') query
WHERE search_vector @@ query;

-- Boolean operators need to_tsquery, not plainto_tsquery
SELECT id, title
FROM articles, to_tsquery('english', 'database & (index | search) & !mysql') query
WHERE search_vector @@ query;
