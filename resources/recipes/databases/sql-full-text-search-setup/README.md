# Set Up Full-Text Search Indexes

Runnable PostgreSQL scripts for full-text search: generated `tsvector` columns, GIN indexes, ranking, highlighting, weighted columns, phrase/proximity queries, trigram fuzzy matching, multi-language vectors, trigger updates, custom configurations and search caching. Source recipe: [Set Up Full-Text Search Indexes](https://stackpractices.com/recipes/sql-full-text-search-setup/).

## Files

| File | What it shows |
|------|---------------|
| `setup-gin-index.sql` | Generated `tsvector` column + GIN index + ranked search — the baseline setup |
| `headline-snippets.sql` | `ts_headline` snippets with `MaxWords`/`MinWords` tuning |
| `weighted-search.sql` | `setweight` A/B weighting so title hits outrank body hits |
| `phrase-proximity-search.sql` | `phraseto_tsquery`, the `<->` operator and `<N>` proximity |
| `trigram-fuzzy-search.sql` | `pg_trgm` setup, similarity search, combined FTS+trigram and autocomplete |
| `multi-language-search.sql` | Per-row language column feeding `to_tsvector` |
| `index-maintenance.sql` | `fastupdate`, partial indexes, bloat monitoring and `ANALYZE` |
| `trigger-updates.sql` | Trigger function to keep a manual `search_vector` column in sync |
| `custom-text-search-config.sql` | Custom configuration + dictionary for domain terminology |
| `search-caching.sql` | Materialized view caching plus faceted/aggregated search |

## Usage

The examples assume an `articles(id, title, body, category, status, language)` table. Adapt column names and the text search configuration (`'english'` vs `'spanish'` etc.) to your schema — wrong-language stemming is the most common reason queries return nothing.

Requires PostgreSQL 12+ (generated columns). `pg_trgm` and `rum` are contrib extensions: `CREATE EXTENSION pg_trgm;` needs superuser or the appropriate cloud privilege.

## Key point

Index the `tsvector`, not the raw text. Generated columns stay in sync for free; manual columns need the trigger in `trigger-updates.sql`. Use `pg_trgm` alongside FTS when you need typo tolerance — `to_tsvector` alone can't match partial words.
