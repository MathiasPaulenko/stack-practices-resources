# Environment Configuration — Payment API (filled example)

## 1. Environment Identification

| Field | Value |
|-------|-------|
| Application / Service | Payment API |
| Environment | production |
| Region / Zone | us-east-1 |
| Cluster / Instance | prod-k8s-cluster-01 |
| Version deployed | v2.4.1 |
| Owner | Payments team |
| Last reviewed | 2026-11-10 |

## 2. Core Environment Variables

| Variable | Purpose | dev Value | staging Value | production Value | Secret |
|----------|---------|-----------|---------------|------------------|--------|
| `APP_ENV` | Runtime environment | `development` | `staging` | `production` | No |
| `LOG_LEVEL` | Logging verbosity | `debug` | `info` | `warn` | No |
| `DATABASE_URL` | Primary DB connection | `postgres://dev-db` | `postgres://staging-db` | `postgres://prod-db` | Yes |
| `JWT_SECRET` | Token signing | `dev-secret` | `staging-secret` | `prod-secret` | Yes |

## 3. Service Endpoints

| Service | Environment | URL / Host | Port | Protocol | Notes |
|---------|-------------|------------|------|----------|-------|
| Application | production | `api.payments.example.com` | `443` | HTTPS | Behind load balancer |
| Database | production | `prod-db.internal.example.com` | `5432` | PostgreSQL | Private subnet |

## 5. Secrets and Credentials

| Secret Name | Used By | Storage Location | Rotation Schedule | Last Rotated |
|-------------|---------|------------------|-------------------|--------------|
| `DATABASE_PASSWORD` | Application | AWS Secrets Manager | Quarterly | `2026-06-01` |

## 6. Configuration Change Log

| Date | Change | Author | Reason | Approved By |
|------|--------|--------|--------|-------------|
| 2026-06-10 | Increased production cache cluster size | `alice@example.com` | Flash sale prep | `bob@example.com` |
