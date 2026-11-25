-- Expand-contract column rename on PostgreSQL.
-- Goal: rename users.email -> users.email_normalized-equivalent without downtime.

-- PHASE 1: EXPAND - add the new column; existing code keeps working
ALTER TABLE users ADD COLUMN email_normalized VARCHAR(255);
CREATE INDEX CONCURRENTLY idx_users_email_normalized ON users(email_normalized);

-- Backfill in batches (repeat until done) to avoid long locks
UPDATE users
SET email_normalized = LOWER(email)
WHERE id BETWEEN 1 AND 10000;

-- PHASE 2: DUAL WRITE - deploy application code that writes both columns

-- PHASE 3: CONTRACT - drop the old column after parity verification
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_normalized TO email;
