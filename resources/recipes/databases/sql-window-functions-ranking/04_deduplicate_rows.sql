-- Keep only the latest record per user
WITH deduped AS (
  SELECT
    user_id,
    email,
    updated_at,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM user_records
)
SELECT user_id, email, updated_at
FROM deduped
WHERE rn = 1
ORDER BY user_id;
