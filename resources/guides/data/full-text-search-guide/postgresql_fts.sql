-- PostgreSQL full-text search: setup, queries, and maintenance
-- Requires: PostgreSQL 11+ (triggers, generated columns), pg_trgm for autocomplete section
-- Run with: psql -d yourdb -f postgresql_fts.sql

-- ============================================================================
-- 1. SETUP: stored tsvector column + GIN index
-- ============================================================================

-- Example products table (skip if yours exists)
CREATE TABLE IF NOT EXISTS products (
    id          SERIAL PRIMARY KEY,
    sku         TEXT,
    name        TEXT NOT NULL,
    description TEXT,
    category    TEXT,
    price       NUMERIC(10,2),
    tags        TEXT[],
    in_stock    BOOLEAN DEFAULT TRUE
);

ALTER TABLE products ADD COLUMN IF NOT EXISTS search_vector tsvector;

-- GIN is the right index type for inverted structures; B-tree can't index
-- "contains this token" efficiently.
CREATE INDEX IF NOT EXISTS idx_products_search
    ON products USING GIN(search_vector);

-- Weighted backfill: A = name/SKU, B = description, C = tags/category.
-- coalesce() matters: to_tsvector on NULL yields NULL and silently drops the
-- document from the index.
UPDATE products SET search_vector =
    setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(sku, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(category, '')), 'C') ||
    setweight(to_tsvector('english', coalesce(array_to_string(tags, ' '), '')), 'C');

-- ============================================================================
-- 2. KEEP IT FRESH: BEFORE INSERT OR UPDATE trigger
--    Alternative for hot tables: a GENERATED ALWAYS AS ... STORED column.
-- ============================================================================

CREATE OR REPLACE FUNCTION products_search_update() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.sku, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.description, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(NEW.category, '')), 'C') ||
        setweight(to_tsvector('english', coalesce(array_to_string(NEW.tags, ' '), '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS products_search_trigger ON products;
CREATE TRIGGER products_search_trigger
    BEFORE INSERT OR UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION products_search_update();

-- ============================================================================
-- 3. QUERIES
-- ============================================================================

-- Basic ranked search (plainto_tsquery: safe for raw user input)
SELECT id, name, description,
       ts_rank(search_vector, query) AS rank
FROM products,
     plainto_tsquery('english', 'wireless headphones') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;

-- Highlighting: the snippet UI that makes results feel like a search engine
SELECT id, name,
       ts_headline('english', description, query) AS highlighted
FROM products,
     plainto_tsquery('english', 'noise canceling') query
WHERE search_vector @@ query;

-- Faceting: the vector is just a column, so you can aggregate over it
SELECT category,
       count(*) AS product_count,
       avg(ts_rank(search_vector, query)) AS avg_relevance
FROM products,
     plainto_tsquery('english', 'gaming keyboard') query
WHERE search_vector @@ query
GROUP BY category
ORDER BY product_count DESC;

-- Custom field weights with ts_rank_cd (D,C,B,A order)
SELECT id, name,
       ts_rank_cd('{0.1, 0.2, 0.4, 1.0}', search_vector, query, 32) AS rank
FROM products,
     plainto_tsquery('english', 'laptop stand') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- ============================================================================
-- 4. AUTOCOMPLETE with pg_trgm (typo-tolerant prefix matching)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Index for similarity + prefix lookups on names
CREATE INDEX IF NOT EXISTS idx_products_name_trgm
    ON products USING GIN(name gin_trgm_ops);

SELECT name
FROM products
WHERE name % 'wirless'                 -- tolerates the typo
ORDER BY similarity(name, 'wirless') DESC
LIMIT 5;
