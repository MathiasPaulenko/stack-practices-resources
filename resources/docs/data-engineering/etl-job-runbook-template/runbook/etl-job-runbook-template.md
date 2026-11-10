# ETL Job Runbook — `<Job Name>`

## Runbook Overview

| Field | Value |
|-------|-------|
| Job Name | `<job name>` |
| Job ID | `<id>` |
| Owner | `<team>` |
| On-Call Rotation | `<rotation>` |
| Escalation | `<lead>` |
| Last Updated | `<YYYY-MM-DD>` |
| Schedule | `<cron or description>` |
| Expected Duration | `<minutes>` |
| SLA | `<minutes>` |
| Framework | `<Airflow + dbt / other>` |
| Orchestrator | `<Kubernetes / other>` |

## 1. Quick Reference

| Action | Command |
|--------|---------|
| Check job status | `airflow dags state <dag_id> <logical_date>` |
| View task logs | Airflow UI → Grid → task instance → Log; on k8s: `kubectl logs -n <namespace> <worker-pod> -c base` |
| Manual trigger | `airflow dags trigger <dag_id>` |
| Re-run failed task | `airflow tasks clear <dag_id> -t <task_id> -s <date> -e <date>` |
| Clear task + downstream | `airflow tasks clear <dag_id> -t <task_id> --downstream -s <date> -e <date>` |
| Backfill range | `airflow dags backfill <dag_id> -s <start> -e <end>` |
| Pause DAG | `airflow dags pause <dag_id>` |
| Unpause DAG | `airflow dags unpause <dag_id>` |

## 2. Architecture

```
<diagram: source -> staging -> transform -> load>
```

### Task Flow

| Task | Description | Typical Duration | Dependencies |
|------|-------------|-----------------|--------------|
| `<task>` | `<what it does>` | `<min>` | `<upstream task or —>` |

## 3. Health Checks

### Pre-run

| Check | Command | Expected Result | Action if Failed |
|-------|---------|-----------------|------------------|
| `<check>` | `<command>` | `<expected>` | `<action>` |

### Post-run

| Check | Command | Expected Result | Action if Failed |
|-------|---------|-----------------|------------------|
| `<check>` | `<command>` | `<expected>` | `<action>` |

## 4. Common Failures and Diagnostics

### F1: `<failure name>`

| Field | Value |
|-------|-------|
| Severity | `<High/Medium/Low>` |
| Error Message | `<exact message>` |
| Task Affected | `<task_id>` |
| Frequency | `<how often>` |

**Symptoms:**
- `<observable symptom>`

**Diagnostic Steps:**
1. `<step>`

**Resolution:**
1. `<step>`

**Prevention:**
- `<measure>`

## 5. Recovery Procedures

### Full pipeline re-run

```bash
## 1. Clear every task for the run date (scheduler re-runs them)
airflow tasks clear <dag_id> -s <date> -e <date>

## 2. Trigger the DAG manually
airflow dags trigger <dag_id> --conf '{"date": "<date>"}'

## 3. Monitor
airflow dags state <dag_id> <date>
```

### Partial re-run (from a specific task)

```bash
## 1. Clear the task and its downstream tasks
airflow tasks clear <dag_id> -t <task_id> --downstream -s <date> -e <date>

## 2. Cleared tasks are rescheduled automatically
##    (Airflow 2.x has no "tasks run" — clearing IS the re-run)

## 3. Monitor
airflow tasks list <dag_id> --state running
```

### Backfill

```bash
## 1. Pause the DAG
airflow dags pause <dag_id>

## 2. Backfill the range
airflow dags backfill <dag_id> -s <start> -e <end> --reset-dagruns --run-backwards

## 3. Monitor
airflow dags list-runs -d <dag_id> --limit 10

## 4. Unpause
airflow dags unpause <dag_id>
```

## 6. Contacts and Escalation

| Role | Name | Primary | Secondary | Escalation |
|------|------|---------|-----------|------------|
| On-Call (Tier 1) | `<name>` | `<pagerduty>` | `<slack>` | After `<min>` → Tier 2 |
| Lead (Tier 2) | `<name>` | `<slack>` | `<phone>` | After `<min>` → Tier 3 |
| Manager (Tier 3) | `<name>` | `<slack>` | `<phone>` | — |
| Source Team | `<name>` | `<slack>` | `<email>` | — |
