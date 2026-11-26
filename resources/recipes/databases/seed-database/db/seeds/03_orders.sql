INSERT INTO orders (user_id, total, status, created_at)
SELECT id, 119.98, 'completed', NOW() - INTERVAL '2 days'
FROM users WHERE email = 'user1@example.com';
