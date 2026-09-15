-- schema.sql
-- Schema and indexes for cursor-based (keyset) pagination in PostgreSQL.

CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  title TEXT NOT NULL,
  score INTEGER NOT NULL DEFAULT 0,
  deleted_at TIMESTAMPTZ
);

-- Composite index for cursor pagination by created_at DESC.
-- The (id DESC) tiebreaker guarantees deterministic ordering when
-- multiple rows share the same created_at timestamp.
CREATE INDEX idx_posts_created_at_id ON posts (created_at DESC, id DESC);

-- Composite index for cursor pagination by score DESC.
CREATE INDEX idx_posts_score_id ON posts (score DESC, id DESC);

-- Partial index for soft-deleted rows: keeps the index small and fast
-- when most rows are not deleted.
CREATE INDEX idx_posts_active_created_at_id
  ON posts (created_at DESC, id DESC)
  WHERE deleted_at IS NULL;

-- Generated column for sorting by a calculated value without
-- recomputing the expression on every query.
ALTER TABLE posts
  ADD COLUMN title_lower TEXT GENERATED ALWAYS AS (LOWER(title)) STORED;

CREATE INDEX idx_posts_title_lower_id ON posts (title_lower ASC, id ASC);
