# Makefile — daily Docker Compose commands
.PHONY: up down restart logs ps clean rebuild seed test shell db-shell

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f --tail=100

ps:
	docker compose ps

clean:
	docker compose down -v --remove-orphans

rebuild:
	docker compose up -d --build --force-recreate

seed:
	./seed-dev.sh

test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml up \
	  --abort-on-container-exit --exit-code-from backend

shell:
	docker compose exec backend /bin/sh

db-shell:
	docker compose exec db psql -U postgres -d myapp
