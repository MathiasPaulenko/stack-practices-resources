# Data Pipeline Design — `<pipeline-name>`

## Pipeline Overview

| Field | Value |
|-------|-------|
| Pipeline Name | |
| Pipeline ID | PL-XXX-000 |
| Version | 0.1.0 |
| Owner | |
| Last Updated | YYYY-MM-DD |
| Status | Draft / Development / Production |
| Schedule | |
| Average Runtime | |
| Data Volume | |
| Framework | |
| Orchestrator | |

## 1. Architecture Overview

```
Source ──▶ Staging ──▶ Transform ──▶ Sink
              │             │
              ▼             ▼
          Quality        Monitor
```

## 2. Data Sources

### Source 1: `<source-name>`

| Field | Value |
|-------|-------|
| Source Name | |
| Source Type | REST API / S3 / CDC / Database |
| API URL / Location | |
| Authentication | |
| Pagination | |
| Rate Limit | |
| Data Format | |
| Extraction Mode | Full / Incremental |
| Incremental Key | |
| Retry Policy | |
| Timeout | |

### Source Schema: `<source-name>`

| Field | Type | Nullable | Description | Example |
|-------|------|----------|-------------|---------|
| | | | | |

## 3. Staging Layer

### Staging Tables

| Table | Source | Storage | Retention | Purpose |
|-------|--------|---------|-----------|---------|
| | | | | |

## 4. Transformations

### Transform 1: `<transform-name>`

| Field | Value |
|-------|-------|
| Name | |
| Tool | |
| Model | input → output |
| Logic | |
| Type | Incremental / Full refresh |

```sql
-- model_name.sql
SELECT ... FROM {{ ref('stg_...') }}
```

## 5. Data Sinks

### Sink 1: `<sink-name>`

| Field | Value |
|-------|-------|
| Target Table / Path | |
| Database / Bucket | |
| Write Mode | Upsert / Append / Overwrite |
| Purpose | |

## 6. Scheduling and Orchestration

| Field | Value |
|-------|-------|
| DAG ID | |
| Schedule | cron or preset |
| Retries | |
| SLA | |
| Owner | |
| Notification on Failure | |

## 7. Error Handling

| Error Scenario | Detection | Action | Notification |
|---------------|-----------|--------|-------------|
| | | | |

### Dead Letter Queue

| Field | Value |
|-------|-------|
| DLQ Location | |
| Retention | |
| Trigger | |
| Review Process | |

## 8. Monitoring and Alerting

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| | | | |

## 9. Data Quality Checks

| Check | Type | Threshold | Action on Failure |
|-------|------|-----------|-------------------|
| | | | |

## 10. Operational Procedures

### Manual Re-run

```bash
# trigger + clear commands for your orchestrator
```

### Backfill Procedure

```bash
# backfill command for a date range
```
