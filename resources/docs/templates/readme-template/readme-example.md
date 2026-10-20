# Payment Service

Payment processing service for the platform.

## Quick Start

Requirements:
  - Node.js 20+
  - Docker 24+
  - PostgreSQL 16+

Installation:
  git clone https://github.com/company/payment-service.git
  cd payment-service
  npm install
  cp .env.example .env  # edit with your values
  docker compose up -d  # postgres and redis
  npm run db:migrate
  npm run dev

Tests:
  npm test           # unit tests
  npm run test:e2e   # end-to-end tests
  npm run test:cov   # coverage report

## Endpoints

  POST   /payments               Create a payment
  GET    /payments/:id           Get a payment
  POST   /payments/:id/refund    Refund a payment
  GET    /health                 Health check

## Configuration

  Variable          | Required | Default | Description
  ------------------|----------|---------|-------------------
  DATABASE_URL      | Yes      | -       | PostgreSQL URL
  REDIS_URL         | Yes      | -       | Redis URL
  CARRIER_API_KEY   | Yes      | -       | Carrier API key
  LOG_LEVEL         | No       | info    | Log level
  PORT              | No       | 3000    | Server port

## Monitoring

  - Dashboard: https://grafana.company.com/d/payment
  - Alerts: PagerDuty service PD-1234
  - SLO: 99.9% availability, p95 < 500ms

## Contributing

  See CONTRIBUTING.md for the contribution flow.
  Contact: #payments-team on Slack.
