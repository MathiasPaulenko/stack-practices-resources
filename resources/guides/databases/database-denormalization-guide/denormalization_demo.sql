-- Database Denormalization Demo (SQLite-compatible)
-- Mirrors the patterns in the guide: counter + trigger, computed column,
-- aggregate summary table, and the drift-check query.
-- The article uses PostgreSQL (SERIAL, GENERATED ALWAYS AS, materialized views);
-- this demo uses the SQLite equivalents so it runs anywhere Python does.

-- 1) Denormalized counter kept in sync by a trigger
CREATE TABLE posts (
    post_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    like_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE post_likes (
    post_id INTEGER NOT NULL REFERENCES posts(post_id),
    user_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, user_id)
);

CREATE TRIGGER trg_like_insert AFTER INSERT ON post_likes
FOR EACH ROW BEGIN
    UPDATE posts SET like_count = like_count + 1 WHERE post_id = NEW.post_id;
END;

CREATE TRIGGER trg_like_delete AFTER DELETE ON post_likes
FOR EACH ROW BEGIN
    UPDATE posts SET like_count = like_count - 1 WHERE post_id = OLD.post_id;
END;

-- 2) Stored computed column (SQLite supports GENERATED ALWAYS AS ... STORED)
CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    line_total NUMERIC(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- 3) Denormalized summary table (the materialized-view equivalent,
--    since SQLite has no materialized views)
CREATE TABLE daily_order_summary (
    day TEXT NOT NULL,
    order_count INTEGER NOT NULL DEFAULT 0,
    revenue NUMERIC(12,2) NOT NULL DEFAULT 0,
    PRIMARY KEY (day)
);

-- Seed data
INSERT INTO posts (title) VALUES ('Hello denormalization');
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (1, 10, 2, 19.99), (1, 20, 1, 49.50), (2, 10, 3, 19.99);
INSERT INTO daily_order_summary
    SELECT date('now'), COUNT(DISTINCT order_id), SUM(quantity * unit_price)
    FROM order_items;

-- Demo writes: the counter stays honest because the trigger owns the sync
INSERT INTO post_likes (post_id, user_id) VALUES (1, 101);
INSERT INTO post_likes (post_id, user_id) VALUES (1, 102);
INSERT INTO post_likes (post_id, user_id) VALUES (1, 103);
DELETE FROM post_likes WHERE post_id = 1 AND user_id = 102;

-- 4) Drift check: recompute from source and compare to the stored value
SELECT p.post_id,
       p.like_count AS stored,
       (SELECT COUNT(*) FROM post_likes l WHERE l.post_id = p.post_id) AS fresh,
       p.like_count - (SELECT COUNT(*) FROM post_likes l WHERE l.post_id = p.post_id) AS drift
FROM posts p;

-- Expected outputs when run:
--   posts.like_count = 2        (3 inserts - 1 delete, maintained by triggers)
--   order_items.line_total     = 39.98, 49.50, 59.97 (computed on write)
--   drift                      = 0 (stored counter matches fresh COUNT)
