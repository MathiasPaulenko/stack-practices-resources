# Environment Setup: StackPractices Web (filled example)

## Prerequisites

| Tool | Version | Install Command |
|------|---------|-----------------|
| Node.js | 20.x | `nvm install 20` |
| Docker | 24.x | [Docker Desktop](https://docker.com) |
| Git | 2.40+ | `brew install git` |
| Astro CLI | 5.x | `npm install -g @astrojs/cli` |

## Quick Start

```bash
git clone git@github.com:org/stackpractices-web.git
cd stackpractices-web
npm install
cp .env.example .env
docker compose up -d
npm run db:migrate
npm run db:seed
npm run dev
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `REDIS_URL` | No | `redis://localhost:6379` | Cache connection |
| `GA_MEASUREMENT_ID` | No | — | Google Analytics 4 ID |
| `PUBLIC_SITE_URL` | Yes | `http://localhost:4321` | Base URL for SEO |

## Verification

```bash
curl http://localhost:4321/health
npm test
npm run build
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Port 4321 in use | Another process | `lsof -ti:4321 | xargs kill -9` |
| `npm install` fails | Node version mismatch | `nvm use 20` |
| Build fails | Missing env vars | Check `.env` against `.env.example` |
