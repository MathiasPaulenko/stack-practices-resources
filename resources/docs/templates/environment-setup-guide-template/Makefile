.PHONY: setup dev test clean

setup:
	nvm install
	npm ci
	cp .env.example .env
	npm run db:migrate
	npm run db:seed

dev:
	npm run dev

test:
	npm run test:unit
	npm run test:integration

clean:
	rm -rf node_modules dist .astro
