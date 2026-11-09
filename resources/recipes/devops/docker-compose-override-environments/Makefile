# Makefile — stable commands per environment instead of long -f chains
.PHONY: dev staging prod test down logs config

dev:        # docker-compose.override.yml loads automatically
	docker compose up

staging:
	docker compose --env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml up -d

prod:
	docker compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d

test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit

down:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down
	docker compose down

logs:
	docker compose logs -f

config:     # inspect the merged result before running anything
	docker compose -f docker-compose.yml -f docker-compose.prod.yml config
