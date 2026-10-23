#!/bin/bash
# seed-dev.sh — reset and repopulate the dev database

set -e

echo "Resetting database..."
docker compose exec -T db psql -U postgres -d myapp \
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

echo "Running migrations..."
docker compose exec -T backend npx prisma migrate dev --reset --force

echo "Seeding users..."
docker compose exec -T db psql -U postgres -d myapp <<'SQL'
INSERT INTO users (email, name, created_at) VALUES
  ('alice@example.com', 'Alice', NOW()),
  ('bob@example.com', 'Bob', NOW()),
  ('admin@example.com', 'Admin', NOW());
SQL

echo "Seed complete!"
