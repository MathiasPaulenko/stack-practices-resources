INSERT INTO users (email, name, role, created_at)
VALUES
  ('admin@example.com', 'Admin User', 'admin', NOW()),
  ('user1@example.com', 'Alice', 'user', NOW()),
  ('user2@example.com', 'Bob', 'user', NOW())
ON CONFLICT (email) DO NOTHING;
