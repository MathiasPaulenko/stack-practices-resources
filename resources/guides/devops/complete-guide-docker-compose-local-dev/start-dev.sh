#!/bin/bash
# start-dev.sh — first-boot: build, wait for DB, migrate, seed

docker compose up --build -d

echo "Waiting for services..."
until docker compose exec -T db pg_isready -U postgres >/dev/null 2>&1; do
  sleep 1
done

echo "Running migrations..."
docker compose exec backend npx prisma migrate dev

echo "Seeding data..."
docker compose exec backend npm run seed

echo "Ready! API: http://localhost:3000"
