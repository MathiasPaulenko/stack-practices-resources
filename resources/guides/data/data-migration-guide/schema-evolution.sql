-- Expand-contract schema evolution (PostgreSQL)
-- From the data-migration guide: split users.email → users.email_normalized

-- Step 1: Add new column (nullable)
ALTER TABLE users ADD COLUMN email_normalized VARCHAR(255);

-- Step 2: Backfill new column
UPDATE users SET email_normalized = LOWER(email) WHERE email_normalized IS NULL;

-- Step 3: Deploy code that writes to both columns

-- Step 4: Make new column non-nullable
ALTER TABLE users ALTER COLUMN email_normalized SET NOT NULL;

-- Step 5: Deploy code that reads from the new column

-- Step 6: Drop the old column (after the rollback window)
ALTER TABLE users DROP COLUMN email;


-- Table split: users → users + user_profiles
CREATE TABLE user_profiles (
    user_id BIGINT PRIMARY KEY REFERENCES users(id),
    bio TEXT,
    preferences JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Dual-write trigger keeps both in sync during the window
CREATE OR REPLACE FUNCTION sync_user_profile() RETURNS trigger AS $$
BEGIN
    INSERT INTO user_profiles (user_id, bio, preferences, created_at)
    VALUES (NEW.id, NEW.bio, NEW.preferences, NEW.created_at)
    ON CONFLICT (user_id) DO UPDATE SET
        bio = EXCLUDED.bio,
        preferences = EXCLUDED.preferences;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_profile_sync
    AFTER INSERT OR UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION sync_user_profile();

-- Backfill
INSERT INTO user_profiles (user_id, bio, preferences, created_at)
SELECT id, bio, preferences, created_at FROM users
ON CONFLICT (user_id) DO NOTHING;
